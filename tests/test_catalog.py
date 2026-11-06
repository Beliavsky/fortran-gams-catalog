import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import tempfile
import unittest
import shutil
import subprocess
from urllib.parse import unquote, urlsplit

from catalog import ROOT, assemble, belongs, extend_taxonomy, matching_drivers, read, validate_local, procedure_label
from vendor.catalog_export import merge_catalog, snapshot_id
from xbuild import build, supports_fpm, source_codes, license_html
from xrefresh import refresh
from xreviews import render


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

    def test_source_reviews_require_matching_files_and_valid_line_ranges(self):
        original = next(p for p in self.local['projects'] if p['id'] == 'github:derivativefreelibrary/acrs')
        claim = next(c for c in original['local']['classifications'] if c['level'] == 'source-reviewed')
        for change in ('missing', 'wrong-file', 'backwards', 'zero', 'noninteger'):
            record = copy.deepcopy(original)
            review = next(c for c in record['local']['classifications'] if c['level'] == 'source-reviewed')
            if change == 'missing':
                review.pop('procedures')
            elif change == 'wrong-file':
                review['procedures'][0]['path'] = 'unreviewed.f90'
            elif change == 'backwards':
                review['procedures'][0]['line_end'] = 1
            elif change == 'zero':
                review['procedures'][0]['line_start'] = 0
            else:
                review['procedures'][0]['line_start'] = True
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_local({'schema_version': 1, 'projects': [record]}, self.tree)
        self.assertEqual(claim['code'], 'G2i')

    def test_entry_point_usage_requires_pinned_argument_declarations(self):
        original = next(p for p in self.local['projects'] if p['id'] == 'github:derivativefreelibrary/acrs')
        for change in ('unknown-role', 'bad-module', 'bad-type', 'no-summary', 'no-declarations', 'unhashed-file', 'reversed-range', 'sketch-without-notes'):
            record = copy.deepcopy(original)
            claim = next(c for c in record['local']['classifications'] if c['level'] == 'source-reviewed')
            procedure = claim['procedures'][0]
            if change == 'unknown-role': procedure['role'] = 'callable-maybe'
            elif change == 'bad-module': procedure['module'] = 'module::routine'
            elif change == 'bad-type': procedure['derived_type'] = 'object%binding'
            elif change == 'no-summary': procedure.pop('summary')
            elif change == 'no-declarations': procedure.pop('declarations')
            elif change == 'unhashed-file': procedure['declarations'][0]['path'] = 'other.f90'
            elif change == 'reversed-range': procedure['declarations'][0]['line_end'] = 1
            else: procedure['usage'] = 'call acrs(...)'
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_local({'schema_version': 1, 'projects': [record]}, self.tree)
        self.assertEqual(procedure_label({'module': 'mod_introsort', 'procedure': 'sort'}), 'mod_introsort::sort')
        self.assertEqual(procedure_label({'module': 'mod_splines', 'derived_type': 'spline', 'procedure': 'value'}),
                         'mod_splines::spline%value')

    def test_local_checks_bind_sources_results_and_safe_artifacts(self):
        original = next(p for p in self.local['projects'] if p['id'] == 'github:clawpack/riemann')
        validate_local({'schema_version': 1, 'projects': [original]}, self.tree)
        for change in ('unsafe-path', 'changed-driver', 'changed-runner', 'changed-report', 'missing-case', 'changed-source', 'changed-main'):
            record = copy.deepcopy(original)
            claim = next(c for c in record['local']['classifications'] if c['level'] == 'source-reviewed')
            procedure = claim['procedures'][0]
            driver = procedure['local_driver']
            if change == 'unsafe-path': driver['path'] = 'drivers/../../README.md'
            elif change == 'changed-driver': driver['sha256'] = '0'*64
            elif change == 'changed-runner': driver['runner_sha256'] = '0'*64
            elif change == 'changed-report': driver['report_sha256'] = '0'*64
            elif change == 'missing-case': driver['check_name'] = 'not-run'
            elif change == 'changed-source': claim['evidence'][0]['sha256'] = '0'*64
            else: procedure['usage'] += '\nerror stop "unverified edit"'
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_local({'schema_version': 1, 'projects': [record]}, self.tree)
        # Even a freshly rehashed report cannot turn a failing run into a checked driver.
        with tempfile.TemporaryDirectory() as folder:
            temporary = Path(folder)
            shutil.copytree(ROOT/'drivers', temporary/'drivers')
            record = copy.deepcopy(original)
            claim = next(c for c in record['local']['classifications'] if c['level'] == 'source-reviewed')
            report_path = temporary/'drivers/riemann/results.json'
            report = read(report_path)
            report['checks'][0]['run_returncode'] = 1
            report_path.write_text(json.dumps(report), encoding='utf-8')
            import hashlib
            digest = hashlib.sha256(report_path.read_text(encoding='utf-8').encode()).hexdigest()
            for procedure in claim['procedures']:
                procedure['local_driver']['report_sha256'] = digest
            with self.assertRaises(ValueError):
                validate_local({'schema_version': 1, 'projects': [record]}, self.tree, temporary)

    def test_licenses_distinguish_reviewed_imported_and_unknown_terms(self):
        acrs = next(p for p in self.projects if p['id'] == 'github:derivativefreelibrary/acrs')
        self.assertEqual(acrs['license']['spdx_expression'], 'GPL-3.0-or-later')
        self.assertIn('/blob/'+acrs['license']['revision']+'/LICENSE', license_html(acrs))
        self.assertNotIn('imported metadata', license_html(acrs))
        self.assertIn('License not yet reviewed', license_html({'local': {}}))
        self.assertIn('No license identified', license_html({'local': {}, 'license': {'label': 'NOASSERTION'}}))
        imported = license_html({'local': {}, 'license': {'label': 'MIT', 'spdx_expression': None}}, detailed=True)
        self.assertIn('MIT', imported)
        self.assertIn('imported metadata', imported)
        self.assertNotIn('<a ', imported)
        custom = copy.deepcopy(acrs)
        custom['license']['label'] = 'Custom license'
        custom['license']['spdx_expression'] = None
        self.assertIn('Custom license', license_html(custom))
        original = next(p for p in self.local['projects'] if p['id'] == acrs['id'])
        for change in ('missing-evidence', 'unpinned-url', 'bad-hash'):
            record = copy.deepcopy(original)
            license_data = record['local']['license']
            if change == 'missing-evidence': license_data['evidence'] = []
            elif change == 'unpinned-url': license_data['evidence'][0]['url'] = 'https://github.com/DerivativeFreeLibrary/ACRS/blob/main/LICENSE'
            else: license_data['evidence'][0]['sha256'] = 'unknown'
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_local({'schema_version': 1, 'projects': [record]}, self.tree)

    def test_local_taxonomy_extensions_and_procedures_are_searchable(self):
        extension = read(ROOT/'data/gams-extensions.json')
        self.assertTrue(belongs(self.tree, 'G2h3b2', 'G2h3b'))
        self.assertEqual(extend_taxonomy(self.tree, extension), self.tree)
        for parent in ('MISSING', 'G2h3b2'):
            broken = copy.deepcopy(extension)
            broken['classes']['G2h3b2']['parent'] = parent
            with self.assertRaises(ValueError):
                extend_taxonomy(self.tree, broken)
        acrs = next(p for p in self.projects if p['id'] == 'github:derivativefreelibrary/acrs')
        self.assertIn('PRICE_BASE_ITERATION', [p['procedure'] for p in acrs['procedures']])
        self.assertEqual(acrs['drivers'], [])
        self.assertIn('G2i', acrs['codes'])

    def test_generated_pages_have_resolving_relative_links_and_scoped_drivers(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder)
            build(destination)
            index = (destination/'index.html').read_text(encoding='utf-8')
            self.assertIn('<h1>Fortran software by GAMS classification</h1>', index)
            self.assertIn('id="exclude-fpm"', index)
            self.assertIn('id="source-reviewed"', index)
            self.assertIn('data-source-count=', index)
            self.assertIn('data-without-fpm=', index)
            listing = (destination/'projects/index.html').read_text(encoding='utf-8')
            self.assertEqual(listing.count('data-fpm="true"'), sum(supports_fpm(p) for p in self.projects))
            self.assertEqual(listing.count('data-source-match="true"'), sum(bool(source_codes(p)) for p in self.projects))
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
            riemann = (destination/'projects/clawpack/riemann/index.html').read_text(encoding='utf-8')
            self.assertEqual(riemann.count('Locally checked main program:'), 2)
            self.assertNotIn('Calling sketch (not a checked driver)', riemann)
            for name in ('advection.f90', 'burgers.f90', 'run.py', 'results.json', 'README.md'):
                self.assertEqual((destination/'drivers/riemann'/name).read_bytes(), (ROOT/'drivers/riemann'/name).read_bytes())
            self.assertIn('Saved numerical results', riemann)
            ndsm = (destination/'projects/sag2021/ndsm/index.html').read_text(encoding='utf-8')
            self.assertIn('Locally checked main program:', ndsm)
            self.assertNotIn('Calling sketch (not a checked driver)', ndsm)
            box = (destination/'projects/mrachh/boxcode2d-legacy/index.html').read_text(encoding='utf-8')
            self.assertIn('Locally checked main program:', box)
            self.assertIn('Calling sketch (not a checked driver)', box)
            self.assertTrue((destination/'drivers/ndsm/results.json').is_file())
            self.assertTrue((destination/'drivers/boxcode-quadrature/moments.f90').is_file())
            acrs = (destination/'projects/derivativefreelibrary/acrs/index.html').read_text(encoding='utf-8')
            self.assertIn('PRICE_BASE_ITERATION', acrs)
            self.assertIn('#L424-L660', acrs)
            self.assertIn('source reviewed', acrs)
            self.assertNotIn('<h2>Checked hosted drivers</h2>', acrs)
            self.assertIn('price_base_iteration', listing)
            self.assertIn('Reviewed entry points:', listing)
            self.assertIn('Usage (click for argument declarations)', acrs)
            self.assertIn('#L28-L84', acrs)
            self.assertIn('Implementation helper', acrs)
            self.assertIn('Author example: F90_src/main.f90:1', acrs)
            self.assertIn('License: <a ', acrs)
            self.assertIn('GPL-3.0-or-later', acrs)
            intro = (destination/'projects/suzuyuyuyu/fortran-introsort/index.html').read_text(encoding='utf-8')
            self.assertIn('mod_introsort::sort', intro)
            self.assertIn('/blob/0907093a66f05f1c59bee70fb82ed9e40924416d/LICENSE', intro)
            self.assertIn('Calling sketch (not a checked driver)', intro)
            geometry = (destination/'projects/johngardenghi/bglcovering/index.html').read_text(encoding='utf-8')
            self.assertIn('VorCells_Polygons::interCellBall', geometry)
            self.assertIn('#L845-L858', geometry)
            spline = (destination/'projects/ja72/fortranconsolespline/index.html').read_text(encoding='utf-8')
            self.assertIn('mod_splines::spline%value', spline)
            self.assertIn('y = sp%value(x)', spline)
            self.assertIn('#L105-L109', spline)
            sorting_cards = (destination/'classes/N6a2a/index.html').read_text(encoding='utf-8')
            # Only entry points for the current problem belong on a class card.
            import re
            intro_card = next(c for c in re.findall(r'<article .*?</article>', sorting_cards, re.S)
                              if 'suzuyuyuyu/Fortran-introsort' in c)
            entries = intro_card.split('class="entry-points"', 1)[1]
            self.assertIn('mod_introsort::sort', entries)
            self.assertNotIn('apply_permutation', entries)
            self.assertNotIn('introsort_recurs', entries)
            # A reviewed BLAS mapping must not qualify an unreviewed
            # linear-system classification in the same repository.
            linear_systems = (destination/'classes/D2/index.html').read_text(encoding='utf-8')
            from html import unescape
            import re
            card = next(c for c in re.findall(r'<article .*?</article>', linear_systems, re.S)
                        if 'awvwgk/blas-interface' in unescape(c))
            self.assertIn('data-source-match="false"', card)
            self.assertTrue((destination/'classes/G2h3b2/index.html').is_file())

    def test_seed_review_document_matches_catalog_owned_records(self):
        document = (ROOT/'docs/local-reviews.md').read_text(encoding='utf-8')
        self.assertEqual(document, render(self.local))
        for p in self.local['projects']:
            self.assertIn(p['local']['repository']['url'], document)
            self.assertIn(p['local']['classifications'][0]['revision'], document)

    def test_fpm_status_uses_build_metadata_not_import_origin(self):
        self.assertTrue(supports_fpm({'build_systems': ['cmake', 'FPM']}))
        self.assertFalse(supports_fpm({'build_systems': ['cmake']}))
        self.assertFalse(supports_fpm({}))
        independent_fpm = [p for p in self.projects if not p.get('playground') and supports_fpm(p)]
        self.assertTrue(independent_fpm)

    def test_source_filter_requires_explicit_review_level(self):
        project = {'local': {'classifications': [
            {'code': 'H', 'level': 'documentation-reviewed'},
            {'code': 'H1', 'level': 'source-reviewed'}]}, 'procedures': [
                {'gams_codes': ['D'], 'review_level': 'documentation-reviewed'},
                {'gams_codes': ['D2a2'], 'review_level': 'source-reviewed'}]}
        self.assertEqual(source_codes(project), ['D2a2', 'H1'])

    def test_classification_scope_does_not_turn_support_tools_into_solvers(self):
        records = {p['id']: p['local'] for p in self.local['projects']}
        # These distinctions matter to somebody looking for a runnable algorithm.
        # Source review also identifies numerical problem-evaluation services;
        # these evaluate a supplied problem and do not perform optimization.
        self.assertEqual({c['code'] for c in records['github:ralna/cutest']['classifications']}, {'S', 'R'})
        # Documentation and source reviews may independently support the same
        # class; neither should turn a derivative primitive into a factorizer.
        chol = records['github:imurray/chol-rev']['classifications']
        self.assertEqual({c['code'] for c in chol}, {'H1'})
        gamma = records['github:ckormanyos/gamma_f77']
        self.assertIn('real Gamma', gamma['classifications'][0]['notes'])
        self.assertIn('complex-argument', gamma['classifications'][0]['notes'])

    @unittest.skipUnless(shutil.which('node'), 'Optional JavaScript check needs Node.js')
    def test_browser_search_restores_and_combines_filters(self):
        subprocess.run(['node', 'tests/search.cjs'], cwd=ROOT, check=True, timeout=15,
                       capture_output=True, text=True)


if __name__ == '__main__':
    unittest.main()
