"""Offline catalog assembly. Imported and catalog-owned metadata stay separate."""
import copy
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from vendor.catalog_export import merge_catalog, owner_display_name

ROOT = Path(__file__).resolve().parent
LEVELS = {'documentation-reviewed', 'source-reviewed'}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def https(url):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Evidence and repository links must be public HTTPS URLs.')
    return url


def validate_local(local, tree):
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
    return local


def assemble(root=ROOT):
    root = Path(root)
    feed = read(root/'data/imports/fortran-playground.json')
    tree = feed['taxonomies']['gams']['classes']
    local = validate_local(read(root/'data/local.json'), tree)
    merged = merge_catalog(local, feed)
    projects = []
    owners = feed.get('owners', {})
    names = feed.get('attributions', {}).get('owner_names', {})
    for layered in merged['projects']:
        imported = layered['imports'].get('fortran-playground', {})
        data = layered['local']
        effective = copy.deepcopy(imported)
        for key in ('name', 'description', 'repository', 'languages', 'build_systems'):
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
        effective['procedures'] = curation.get('procedures', [])
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
