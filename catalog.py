"""Offline catalog assembly. Imported and catalog-owned metadata stay separate."""
import copy
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from vendor.catalog_export import merge_catalog, owner_display_name

ROOT = Path(__file__).resolve().parent
LEVELS = {'documentation-reviewed', 'source-reviewed'}
PROCEDURE_ROLES = {
    'public-entry-point': 'Public entry point',
    'public-data': 'Public data (not a callable procedure)',
    'public-template': 'Public template instantiation',
    'public-adapter': 'Playground adapter (not an upstream public procedure)',
    'implementation-helper': 'Implementation helper',
    'program-entry-point': 'Program entry point',
    'callback': 'Callback',
    'implementation-evidence': 'Implementation evidence',
    'module-interface': 'Module interface',
}


def procedure_label(procedure):
    module = procedure.get('module')
    derived_type = procedure.get('derived_type')
    return ((module + '::' if module else '') +
            (derived_type + '%' if derived_type else '') + procedure['procedure'])


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def https(url):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Evidence and repository links must be public HTTPS URLs.')
    return url


def extend_taxonomy(tree, extension):
    """Add independently reviewed NIST classes without editing the imported feed."""
    result = copy.deepcopy(tree)
    if extension.get('schema_version') != 1:
        raise ValueError('Expected a version 1 taxonomy extension.')
    for code, info in extension['classes'].items():
        definition = {'label': info['label'], 'parent': info['parent']}
        https(info['source'])
        if code in result and result[code] != definition:
            raise ValueError('Conflicting taxonomy definition: ' + code)
        result[code] = definition
    for code in result:
        if result[code]['parent'] is not None and result[code]['parent'] not in result:
            raise ValueError('Missing taxonomy parent: ' + code)
        lineage(result, code)
    return result


def validate_local_driver(driver, procedure, claim, root):
    """Bind a local verification claim to shipped files and a successful report."""
    if not isinstance(driver, dict):
        raise ValueError('Local driver metadata must be an object.')
    paths = {}
    for field in ('path', 'runner', 'report', 'readme'):
        value = driver.get(field, '')
        if not isinstance(value, str):
            raise ValueError('Invalid local driver path.')
        relative = Path(value)
        if (not value.startswith('drivers/') or '\\' in value
                or relative.is_absolute() or '..' in relative.parts):
            raise ValueError('Local driver files must stay under drivers/.')
        target = (Path(root)/relative).resolve()
        if not target.is_relative_to((Path(root)/'drivers').resolve()) or not target.is_file():
            raise ValueError('Missing or unsafe local driver artifact.')
        paths[field] = target
        if field != 'readme':
            key = 'sha256' if field == 'path' else field+'_sha256'
            digest = hashlib.sha256(target.read_text(encoding='utf-8').encode()).hexdigest()
            if driver.get(key) != digest:
                raise ValueError('Local driver artifact hash mismatch: '+field)
    report = read(paths['report'])
    if not all(isinstance(report.get(k), str) and report[k].strip()
               for k in ('compiler', 'platform', 'checked_at')):
        raise ValueError('Local checks need compiler, platform and date.')
    checks = [c for c in report.get('checks', []) if c.get('name') == driver.get('check_name')]
    if len(checks) != 1:
        raise ValueError('Local driver needs one named result.')
    check = checks[0]
    evidence = next(e for e in claim['evidence'] if e['path'] == procedure['path'])
    if (check.get('gams_code') != claim['code']
            or type(check.get('build_returncode')) is not int or check['build_returncode'] != 0
            or type(check.get('run_returncode')) is not int or check['run_returncode'] != 0
            or not check.get('flags') or 'PASS' not in check.get('stdout', '')
            or check.get('driver') != paths['path'].name
            or check.get('driver_sha256') != driver['sha256']
            or check.get('source') != {'path': procedure['path'], 'revision': claim['revision'], 'sha256': evidence['sha256']}
            or procedure.get('usage', '').rstrip() != paths['path'].read_text(encoding='utf-8').rstrip()):
        raise ValueError('Local check must match its source, main program and successful result.')


def validate_local(local, tree, root=ROOT):
    if local.get('schema_version') != 1 or not isinstance(local.get('projects'), list):
        raise ValueError('Expected a version 1 local catalog.')
    seen = set()
    for project in local['projects']:
        identity = project.get('id', '')
        if not re.fullmatch(r'github:[a-z0-9_.-]+/[a-z0-9_.-]+', identity) or identity in seen:
            raise ValueError('Invalid or duplicate repository identity: ' + identity)
        seen.add(identity)
        data = project['local']
        if project.get('imports'):
            raise ValueError('Keep imports in the saved feed, not data/local.json.')
        repo = data.get('repository')
        if repo:
            if ('github:' + repo['owner'].lower() + '/' + repo['name'].lower() != identity
                    or repo['url'] != 'https://github.com/' + repo['owner'] + '/' + repo['name']):
                raise ValueError('Repository and canonical identity disagree: ' + identity)
        license_data = data.get('license')
        if license_data is not None:
            if (not isinstance(license_data, dict) or not isinstance(license_data.get('label'), str) or not license_data['label'].strip()
                    or not re.fullmatch(r'[0-9a-f]{40}', license_data.get('revision', ''))
                    or not license_data.get('reviewed_on') or not license_data.get('notes')
                    or not license_data.get('evidence')):
                raise ValueError('License reviews need a label, pin, date, notes and evidence: ' + identity)
            expression = license_data.get('spdx_expression')
            if expression is not None and (not isinstance(expression, str) or not expression.strip()):
                raise ValueError('Invalid SPDX expression: ' + identity)
            for evidence in license_data['evidence']:
                https(evidence['url'])
                if (not evidence.get('path') or '/blob/'+license_data['revision']+'/' not in evidence['url']
                        or not re.fullmatch(r'[0-9a-f]{64}', evidence.get('sha256', ''))):
                    raise ValueError('License evidence needs a pinned file and hash: ' + identity)
        for claim in data.get('classifications', []):
            if claim['code'] not in tree or claim['level'] not in LEVELS:
                raise ValueError('Unknown class or review level: ' + identity)
            if not re.fullmatch(r'[0-9a-f]{40}', claim.get('revision', '')):
                raise ValueError('Pin classification evidence to a full commit: ' + identity)
            if not claim.get('notes') or not claim.get('evidence'):
                raise ValueError('Each classification needs evidence and scope notes.')
            for evidence in claim['evidence']:
                https(evidence['url'])
                if ('/blob/' + claim['revision'] + '/') not in evidence['url']:
                    raise ValueError('Evidence URL must identify the reviewed commit.')
                if not re.fullmatch(r'[0-9a-f]{64}', evidence.get('sha256', '')):
                    raise ValueError('Each evidence document needs a SHA-256 digest.')
            if claim['level'] == 'source-reviewed':
                if not claim.get('procedures'):
                    raise ValueError('Source reviews need named procedures and line ranges.')
                paths = {v['path'] for v in claim['evidence']}
                for procedure in claim['procedures']:
                    start, end = procedure.get('line_start'), procedure.get('line_end')
                    if (not procedure.get('procedure') or procedure.get('path') not in paths
                            or type(start) is not int or type(end) is not int
                            or start < 1 or end < start):
                        raise ValueError('Invalid source procedure evidence: ' + identity)
                    if 'role' in procedure and procedure['role'] not in PROCEDURE_ROLES:
                        raise ValueError('Unknown procedure role: ' + identity)
                    if 'module' in procedure and not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', procedure['module']):
                        raise ValueError('Invalid module name: ' + identity)
                    if 'derived_type' in procedure and not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', procedure['derived_type']):
                        raise ValueError('Invalid derived type name: ' + identity)
                    if procedure.get('role') in {'public-entry-point', 'public-data', 'public-template', 'public-adapter'} and not procedure.get('summary'):
                        raise ValueError('Public entry points need a usage summary: ' + identity)
                    for field in ('summary', 'signature', 'usage', 'usage_notes'):
                        if field in procedure and (not isinstance(procedure[field], str) or not procedure[field].strip()):
                            raise ValueError('Invalid procedure '+field+': ' + identity)
                    if 'usage' in procedure and not procedure.get('usage_notes'):
                        raise ValueError('Calling sketches need usage notes: ' + identity)
                    for example in procedure.get('examples', []) + procedure.get('declarations', []):
                        first, last = example.get('line_start'), example.get('line_end')
                        if (example.get('path') not in paths or type(first) is not int
                                or type(last) is not int or first < 1 or last < first):
                            raise ValueError('Procedure links need pinned evidence and valid ranges: ' + identity)
                    if 'signature' in procedure and not procedure.get('declarations'):
                        raise ValueError('Usage signatures need pinned argument declarations: ' + identity)
                    if 'local_driver' in procedure:
                        validate_local_driver(procedure['local_driver'], procedure, claim, root)
    return local


def assemble(root=ROOT):
    root = Path(root)
    feed = read(root/'data/imports/fortran-playground.json')
    tree = feed['taxonomies']['gams']['classes']
    extensions = root/'data/gams-extensions.json'
    if extensions.exists():
        tree = extend_taxonomy(tree, read(extensions))
    local = validate_local(read(root/'data/local.json'), tree, root)
    merged = merge_catalog(local, feed)
    projects = []
    owners = feed.get('owners', {})
    names = feed.get('attributions', {}).get('owner_names', {})
    for layered in merged['projects']:
        imported = layered['imports'].get('fortran-playground', {})
        data = layered['local']
        effective = copy.deepcopy(imported)
        for key in ('name', 'description', 'repository', 'languages', 'build_systems', 'license'):
            if key in data:
                effective[key] = copy.deepcopy(data[key])
        if not all(effective.get(k) for k in ('name', 'description', 'repository')):
            raise ValueError('Local-only projects need name, description and repository.')
        effective['id'] = layered['id']
        effective['local'] = data
        curation = imported.get('curation', {})
        effective['topics'] = sorted(set(data.get('topics', []) + curation.get('topics', [])
                                        + imported.get('github', {}).get('topics', [])))
        effective['codes'] = sorted(set(curation.get('gams_codes', [])
                                       + [c['code'] for c in data.get('classifications', [])]))
        effective['procedures'] = copy.deepcopy(curation.get('procedures', []))
        for claim in data.get('classifications', []):
            for procedure in claim.get('procedures', []):
                effective['procedures'].append({**procedure, 'gams_codes': [claim['code']],
                                                'origin': 'local'})
        package_id = imported.get('playground', {}).get('package_id')
        effective['drivers'] = [d for d in feed.get('demonstrations', [])
                                if package_id and d['package_id'] == package_id]
        owner = effective['repository']['owner'].lower()
        effective['owner_label'] = owner_display_name(owner, owners.get(owner, {}), names.get(owner, {}))
        effective['origin'] = 'Imported playground package' if imported else 'Independent repository review'
        projects.append(effective)
    return tree, sorted(projects, key=lambda p: p['name'].casefold()), merged


def lineage(tree, code):
    """Explicit taxonomy parents: C1 must never include sibling C10."""
    result = []
    while code is not None:
        if code in result:
            raise ValueError('Cycle in taxonomy')
        result.append(code)
        code = tree[code]['parent']
    return result


def belongs(tree, child, parent):
    return parent is None or parent in lineage(tree, child)


def matching_drivers(tree, project, code=None):
    return [d for d in project['drivers'] if belongs(tree, d['gams_code'], code)]
