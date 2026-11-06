"""Refresh a small source-available GAMS/Netlib pilot; normal builds stay offline."""
import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.request import urlopen

from catalog import ROOT, assemble
from legacy_gams import validate

INDEX = 'https://netlib.org/quadpack/'
PROCEDURES = ('dqag', 'dqags', 'dqagi', 'dqagp', 'dqawo', 'dqaws', 'dqawc', 'dqawf', 'dqng')
RELATED = ['github:jacobwilliams/quadpack', 'github:nshaffer/modern_quadpack']


class IndexText(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.parts = []
        self.feed(html)

    def handle_data(self, text):
        self.parts.append(text)


def parse_index(html):
    records = {}
    for block in re.split(r'(?m)^file\s+', ''.join(IndexText(html).parts))[1:]:
        lines = block.splitlines()
        filename = lines[0].split()[0]
        fields = dict(re.findall(r'(?m)^(gams|for|prec)\s+([^\n]+)', block))
        if all(key in fields for key in ('gams', 'for', 'prec')):
            records[filename] = fields
    return records


def download(url):
    with urlopen(url, timeout=30) as response:
        if response.status != 200 or not response.url.startswith(INDEX):
            raise ValueError('Unexpected Netlib response: '+url)
        raw = response.read(2_000_001)
    if len(raw) > 2_000_000:
        raise ValueError('Netlib response exceeds pilot size limit')
    return raw.decode('utf-8').replace('\r\n', '\n')


def snapshot(fetch=download):
    index = fetch(INDEX)
    records = parse_index(index)
    timestamp = datetime.now(timezone.utc).isoformat()
    entries = []
    digest = lambda text: hashlib.sha256(text.encode('utf-8')).hexdigest()
    for name in PROCEDURES:
        fields = records[name+'.f']
        url = INDEX+name+'.f'
        text = fetch(url)
        if not re.search(r'(?im)^\s*subroutine\s+'+name+r'\s*\(', text):
            raise ValueError('Expected Fortran subroutine missing: '+url)
        entries.append(dict(id='netlib:quadpack/'+name, library='QUADPACK',
            procedure=name.upper(), description=fields['for'].strip(),
            language='Fortran', precision=fields['prec'].strip(),
            gams_codes=fields['gams'].strip().split(','),
            availability='source-available', source_url=url, source_sha256=digest(text),
            index_url=INDEX, index_sha256=digest(index), retrieved_at=timestamp,
            related_projects=RELATED))
    return dict(schema_version=1, provenance={
        'classification_source': 'GAMS codes recorded by the Netlib QUADPACK index',
        'nist_import_status': 'NIST dynamic pages returned HTTP 403 during pilot setup; no NIST module records were retrieved.',
        'review_status': 'Imported classification; not independently reviewed or compiled',
        'license_status': 'Not reviewed; source availability does not establish reuse permission',
        'scope': 'Nine double-precision QUADPACK entry points; no proprietary references'}, entries=entries)


def refresh(output, tree, project_ids, fetch=download):
    output = Path(output)
    data = validate(snapshot(fetch), tree, project_ids)
    temporary = output.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    temporary.replace(output)
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'data/imports/gams-netlib.json')
    args = parser.parse_args()
    tree, projects, _ = assemble()
    data = refresh(args.output, tree, {p['id'] for p in projects})
    print('Saved '+str(len(data['entries']))+' GAMS/Netlib entries to '+str(args.output))


if __name__ == '__main__':
    main()
