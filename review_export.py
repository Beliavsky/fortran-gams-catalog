"""Export independently authored reviews, excluding playground imports and checks."""
import copy
import hashlib
import json
from pathlib import Path

PUBLISHER = 'fortran-gams-catalog-independent-reviews'
FEED_NAME = 'reviewed-metadata.json'
SOURCE_REPOSITORY = 'https://github.com/Beliavsky/fortran-gams-catalog'


def snapshot_id(data):
    content = {k: v for k, v in data.items() if k != 'snapshot_id'}
    return 'sha256:' + hashlib.sha256(json.dumps(
        content, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def build_review_feed(projects):
    """Accept assembled, validated projects; read only their local review layer."""
    records = []
    for project in sorted(projects, key=lambda p: p['id']):
        local = project.get('local', {})
        claims = []
        for claim in local.get('classifications', []):
            if claim['level'] != 'source-reviewed':
                continue
            exported = copy.deepcopy({k: claim[k] for k in (
                'code', 'level', 'revision', 'reviewed_on', 'notes', 'evidence')})
            exported['procedures'] = []
            for procedure in claim.get('procedures', []):
                if procedure.get('role') != 'public-entry-point':
                    continue
                fields = ('procedure', 'role', 'module', 'derived_type', 'summary',
                          'signature', 'path', 'line_start', 'line_end', 'declarations')
                item = copy.deepcopy({k: procedure[k] for k in fields if k in procedure})
                # A successful local check must never become a hosted playground check.
                if procedure.get('usage') and not procedure.get('local_driver'):
                    item.update(usage=procedure['usage'],
                                usage_notes=procedure.get('usage_notes', ''),
                                usage_kind='calling-sketch')
                exported['procedures'].append(item)
            claims.append(exported)
        license_data = local.get('license')
        if not claims and not license_data:
            continue
        records.append({'id': project['id'], 'repository': copy.deepcopy(project['repository']),
                        'license': copy.deepcopy(license_data), 'classifications': claims})
    result = {'schema_version': 1, 'publisher': PUBLISHER,
              'source_repository': SOURCE_REPOSITORY, 'projects': records}
    result['snapshot_id'] = snapshot_id(result)
    return result


def publish_review_feed(destination, projects):
    target = Path(destination) / FEED_NAME
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(build_review_feed(projects), indent=2,
                                    ensure_ascii=False) + '\n', encoding='utf-8')
    temporary.replace(target)
