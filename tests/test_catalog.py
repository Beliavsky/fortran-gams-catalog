import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import tempfile
import unittest
import shutil
import subprocess
from urllib.parse import unquote, urlsplit

from catalog import ROOT, assemble, belongs, matching_drivers, read, validate_local
from vendor.catalog_export import merge_catalog, snapshot_id
from xbuild import build
from xrefresh import refresh


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.urls = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('href', 'src'):
            if key in attrs:
                self.urls.append(attrs[key])


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree, cls.projects, cls.merged = assemble()
        cls.feed = read(ROOT/'data/imports/fortran-playground.json')
        cls.local = read(ROOT/'data/local.json')

    def test_independent_reviews_and_imports_are_retained(self):
        ids = [p['id'] for p in self.projects]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(set(p['id'] for p in self.feed['projects']) <= set(ids))
        self.assertTrue(set(p['id'] for p in self.local['projects']) <= set(ids))
        expokit = next(p for p in self.projects if p['id'] == 'github:rasmusgo/expokit')
        self.assertFalse(expokit.get('playground'))
        self.assertEqual(expokit['drivers'], [])
        self.assertEqual(expokit['local']['classifications'][0]['level'], 'documentation-reviewed')

    def test_merge_is_idempotent_and_local_override_survives(self):
        local = copy.deepcopy(self.local)
        first = self.feed['projects'][0]
        local['projects'].append({'id': first['id'], 'local': {'description': 'Catalog-owned wording'}, 'imports': {}})
        merged = merge_catalog(local, self.feed)
        self.assertEqual(merge_catalog(merged, self.feed), merged)
        p = next(p for p in merged['projects'] if p['id'] == first['id'])
        self.assertEqual(p['local']['description'], 'Catalog-owned wording')
        self.assertEqual(p['imports']['fortran-playground'], first)
        self.assertEqual(local['projects'][-1]['imports'], {})

    def test_refresh_preserves_destination_on_invalid_feed(self):
        with tempfile.TemporaryDirectory() as folder:
            source, destination = Path(folder)/'bad.json', Path(folder)/'saved.json'
            corrupted = copy.deepcopy(self.feed)
            corrupted['projects'][0]['description'] = 'Changed without recomputing snapshot'
            source.write_text(json.dumps(corrupted), encoding='utf-8')
            destination.write_text('original snapshot', encoding='utf-8')
            with self.assertRaises(ValueError):
                refresh(str(source), destination)
            self.assertEqual(destination.read_text(encoding='utf-8'), 'original snapshot')
            self.assertFalse(destination.with_name('saved.json.tmp').exists())

    def test_refresh_local_snapshot_is_reproducible(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder)/'saved.json'
            refresh(str(ROOT/'data/imports/fortran-playground.json'), destination)
            self.assertEqual(read(destination), self.feed)
            self.assertEqual(read(destination)['snapshot_id'], snapshot_id(read(destination)))
        with self.assertRaises(ValueError):
            refresh('http://example.com/feed.json', 'unused.json')

    def test_taxonomy_and_driver_scope_use_explicit_parents(self):
        self.assertFalse(belongs(self.tree, 'C10', 'C1'))
        self.assertTrue(belongs(self.tree, 'D2a1', 'D'))
        stdlib = next(p for p in self.projects if p['id'] == 'github:fortran-lang/stdlib')
        sorting = matching_drivers(self.tree, stdlib, 'N6')
        self.assertTrue(sorting)
        self.assertTrue(all(belongs(self.tree, d['gams_code'], 'N6') for d in sorting))
        self.assertNotIn('gams-stdlib-cholesky-reference', [d['name'] for d in sorting])

    def test_reviews_require_real_class_pin_and_evidence_hash(self):
        for field, value in [('code', 'NONEXISTENT'), ('revision', 'main'), ('level', 'verified')]:
            local = copy.deepcopy(self.local)
            local['projects'][0]['local']['classifications'][0][field] = value
            with self.assertRaises(ValueError):
                validate_local(local, self.tree)
        local = copy.deepcopy(self.local)
        local['projects'][0]['local']['classifications'][0]['evidence'][0]['sha256'] = 'missing'
        with self.assertRaises(ValueError):
            validate_local(local, self.tree)

    def test_generated_pages_have_resolving_relative_links_and_scoped_drivers(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder)
            build(destination)
            index = (destination/'index.html').read_text(encoding='utf-8')
            self.assertIn('<h1>Fortran software by GAMS classification</h1>', index)
            self.assertTrue((destination/'catalog.json').is_file())
            for page in destination.rglob('index.html'):
                for url in Links(page.read_text(encoding='utf-8')).urls:
                    parsed = urlsplit(url)
                    if parsed.scheme or not parsed.path:
                        continue
                    target = (page.parent/unquote(parsed.path)).resolve()
                    self.assertTrue(target.is_relative_to(destination.resolve()), (page, url))
                    if parsed.path.endswith('/'):
                        target = target/'index.html'
                    self.assertTrue(target.is_file(), (page, url))
            sorting = (destination/'classes/N6/index.html').read_text(encoding='utf-8')
            self.assertNotIn('example=gams-stdlib-cholesky-reference', sorting)
            self.assertIn('checked hosted driver', sorting)
            expokit = (destination/'projects/rasmusgo/expokit/index.html').read_text(encoding='utf-8')
            self.assertIn('documentation reviewed', expokit)
            self.assertIn('Not built or run', expokit)
            self.assertNotIn('<h2>Checked hosted drivers</h2>', expokit)

    def test_seed_review_document_matches_catalog_owned_records(self):
        document = (ROOT/'docs/local-reviews.md').read_text(encoding='utf-8')
        for p in self.local['projects']:
            self.assertIn(p['local']['repository']['url'], document)
            self.assertIn(p['local']['classifications'][0]['revision'], document)

    @unittest.skipUnless(shutil.which('node'), 'Optional JavaScript check needs Node.js')
    def test_browser_search_restores_and_combines_filters(self):
        subprocess.run(['node', 'tests/search.cjs'], cwd=ROOT, check=True, timeout=15,
                       capture_output=True, text=True)


if __name__ == '__main__':
    unittest.main()
