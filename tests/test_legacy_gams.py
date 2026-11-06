import copy
import json
from pathlib import Path
import tempfile
import unittest

from catalog import ROOT, assemble
from legacy_gams import listing_records, load, validate
from licenses import license_group, license_reviewed
from xbuild import source_codes, supports_fpm
from ximport_gams import INDEX, PROCEDURES, parse_index, refresh


class LegacyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree, cls.projects, _ = assemble()
        cls.ids = {p['id'] for p in cls.projects}
        cls.data = load(ROOT, cls.tree, cls.ids)

    def test_separate_snapshot_has_available_sources_but_no_review_claims(self):
        self.assertEqual(len(self.data['entries']), 9)
        for item in listing_records(self.data):
            self.assertNotIn(item['id'], self.ids)
            self.assertEqual(source_codes(item), [])
            self.assertFalse(license_reviewed(item))
            self.assertFalse(supports_fpm(item))
            self.assertEqual(license_group(item), 'unclear')
            self.assertEqual(item['availability'], 'source-available')
        self.assertIn('HTTP 403', self.data['provenance']['nist_import_status'])

    def test_invalid_imports_fail_without_becoming_reviewed_projects(self):
        for field, value in [('source_url', 'javascript:alert(1)'),
                             ('source_sha256', 'missing'), ('library', 'IMSL'),
                             ('gams_codes', ['MISSING']), ('related_projects', ['github:missing/repo']),
                             ('retrieved_at', '2026-11-06'), ('availability', 'proprietary')]:
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data['entries'][0][field] = value
                with self.assertRaises(ValueError):
                    validate(data, self.tree, self.ids)
        data = copy.deepcopy(self.data)
        data['entries'].append(data['entries'][0])
        with self.assertRaises(ValueError):
            validate(data, self.tree, self.ids)

    def test_index_extraction_and_atomic_refresh_are_offline(self):
        index = '<pre>\n'+''.join(
            'file\t<a href="'+name+'.f">'+name+'.f</a> <a href="extra">plus dependencies</a>\n'
            'gams\tH2a1a1\nfor\tA fixture &amp; description\nprec\tdouble\n\n'
            for name in PROCEDURES)+'</pre>'
        self.assertEqual(parse_index(index)['dqags.f']['for'], 'A fixture & description')

        def fetch(url):
            return index if url == INDEX else '      subroutine '+Path(url).stem+'(x)\n      end\n'

        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)/'snapshot.json'
            data = refresh(output, self.tree, self.ids, fetch)
            self.assertEqual(json.loads(output.read_text(encoding='utf-8')), data)
            original = output.read_bytes()
            with self.assertRaises(ValueError):
                refresh(output, self.tree, self.ids, lambda url: index if url == INDEX else 'not Fortran')
            self.assertEqual(output.read_bytes(), original)
            self.assertFalse(output.with_suffix('.tmp').exists())
