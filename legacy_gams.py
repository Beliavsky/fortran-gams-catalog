"""Separate, unreviewed discovery records from historical GAMS/Netlib indexes."""
from datetime import datetime
import json
from pathlib import Path
import re


def validate(data, tree, project_ids):
    if data.get('schema_version') != 1 or not isinstance(data.get('entries'), list):
        raise ValueError('Invalid legacy GAMS snapshot')
    seen = set()
    for item in data['entries']:
        name = item.get('procedure', '')
        if (not re.fullmatch(r'DQ[A-Z]+', name)
                or item.get('id') != 'netlib:quadpack/'+name.lower()
                or item['id'] in seen or item.get('library') != 'QUADPACK'
                or item.get('language') != 'Fortran' or item.get('precision') != 'double'
                or not item.get('description') or not item.get('gams_codes')
                or any(c not in tree for c in item['gams_codes'])
                or item.get('source_url') != 'https://netlib.org/quadpack/'+name.lower()+'.f'
                or item.get('index_url') != 'https://netlib.org/quadpack/'
                or item.get('availability') != 'source-available'
                or not re.fullmatch(r'[0-9a-f]{64}', item.get('source_sha256', ''))
                or not re.fullmatch(r'[0-9a-f]{64}', item.get('index_sha256', ''))
                or any(p not in project_ids for p in item.get('related_projects', []))):
            raise ValueError('Invalid legacy GAMS entry: '+str(item.get('id')))
        try:
            if datetime.fromisoformat(item['retrieved_at']).tzinfo is None:
                raise ValueError()
        except (KeyError, ValueError, TypeError):
            raise ValueError('Legacy entry needs a retrieval timestamp') from None
        seen.add(item['id'])
    return data


def load(root, tree, project_ids):
    path = Path(root)/'data/imports/gams-netlib.json'
    return validate(json.loads(path.read_text(encoding='utf-8')), tree, project_ids)


def listing_records(data):
    """Adapters for shared counts/filters; never merged into GitHub project records."""
    return [{**item, 'legacy_gams': True, 'name': item['procedure'],
             'codes': item['gams_codes'], 'local': {}, 'procedures': [],
             'drivers': [], 'build_systems': [], 'topics': [],
             'license': {}} for item in data['entries']]
