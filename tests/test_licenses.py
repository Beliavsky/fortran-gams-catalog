import unittest

from licenses import license_group, license_reviewed
from xbuild import license_counts


class LicenseTests(unittest.TestCase):
    def test_groups_preserve_scoped_uncertain_and_dual_terms(self):
        cases = {
            'MIT': 'permissive', 'BSD-3': 'permissive', 'Apache-2.0': 'permissive',
            'GPL-3.0-only': 'strong-copyleft', 'AGPL-3.0-or-later': 'strong-copyleft',
            'LGPL-2.1-or-later': 'weak-copyleft', 'MPL-2.0': 'weak-copyleft',
            'MIT OR GPL-3.0-only': 'permissive',
            'MIT AND GPL-3.0-only': 'strong-copyleft',
            '(MIT OR GPL-3.0-only) AND LGPL-3.0-only': 'weak-copyleft',
            'MIT OR BSD-3-Clause AND GPL-3.0-only': 'permissive',
            'MIT AND (BSD-3-Clause OR Apache-2.0)': 'permissive',
            'MIT AND LicenseRef-Extra': 'custom-mixed',
            'GPL-3.0-or-later WITH GCC-exception-3.1': 'custom-mixed',
            'MIT wrapper; core terms unresolved': 'custom-mixed',
            'MIT root; bundled QRUPDATE GPL-3.0-or-later': 'custom-mixed',
            'Public Domain': 'custom-mixed', 'BSD': 'custom-mixed',
            'GPL version 3 text; version scope unresolved': 'custom-mixed',
            'MIT AND': 'custom-mixed', '(MIT': 'custom-mixed',
            'AND OR MIT': 'custom-mixed', 'MIT OR': 'custom-mixed',
            '': 'unclear', 'NOASSERTION': 'unclear',
            'No explicit project reuse grant identified': 'unclear',
            'Not specified upstream': 'unclear',
        }
        for label, expected in cases.items():
            with self.subTest(label=label):
                self.assertEqual(license_group({'license': {'label': label}}), expected)
        self.assertEqual(license_group({'license': {'label': 'standard terms', 'spdx_expression': 'MIT'}}), 'permissive')
        self.assertFalse(license_reviewed({'license': {'label': 'MIT'}}))
        # A reviewed absence of a grant still has reviewed evidence.
        self.assertTrue(license_reviewed({'local': {'license': {'evidence': [{'path': 'README'}]}}}))

    def test_category_counts_combine_license_review_source_and_build_filters(self):
        members = [
            {'id': 'a', 'license': {'label': 'MIT'}, 'local': {}, 'build_systems': ['fpm']},
            {'id': 'b', 'license': {'label': 'MIT'}, 'local': {'license': {'evidence': [{}]}}},
            {'id': 'c', 'license': {'label': 'GPL-3.0-only'}, 'local': {}},
        ]
        counts = license_counts(members, {'a', 'b'})
        self.assertEqual(counts['|0|0|0'], 3)
        self.assertEqual(counts['permissive|0|0|0'], 2)
        self.assertEqual(counts['permissive|1|1|1'], 1)
        self.assertEqual(counts['|0|1|1'], 1)
        self.assertNotIn('strong-copyleft|1|0|0', counts)
