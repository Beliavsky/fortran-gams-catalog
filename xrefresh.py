"""Refresh the saved playground feed; building the site itself is offline."""
import argparse
import json
from pathlib import Path
import urllib.request

from catalog import ROOT
from vendor.catalog_export import validate_export, write_json

FEED = 'https://beliavsky.github.io/fortran-playground/catalog/catalog-v1.json'
MAX_BYTES = 16 * 1024 * 1024


class HTTPSOnly(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, newurl):
        if not newurl.startswith('https://'):
            raise ValueError('Feed redirects must use HTTPS.')
        return super().redirect_request(request, fp, code, message, headers, newurl)


def refresh(source, destination):
    if source.startswith('https://'):
        request = urllib.request.Request(source, headers={'User-Agent': 'fortran-gams-catalog/1'})
        with urllib.request.build_opener(HTTPSOnly()).open(request, timeout=30) as response:
            raw = response.read(MAX_BYTES + 1)
    elif '://' in source:
        raise ValueError('Use a local file or an HTTPS feed.')
    else:
        with Path(source).open('rb') as stream:
            raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError('Feed exceeds the 16 MiB limit.')
    data = json.loads(raw)
    validate_export(data)
    # Validate completely before the atomic replacement. Local reviews are untouched.
    write_json(destination, data)
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--feed', default=FEED)
    parser.add_argument('--output', type=Path, default=ROOT/'data/imports/fortran-playground.json')
    args = parser.parse_args()
    try:
        data = refresh(args.feed, args.output)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Refresh failed: {error}\n')
    print(f'Saved {len(data["projects"])} projects; {data["snapshot_id"]}')


if __name__ == '__main__':
    main()
