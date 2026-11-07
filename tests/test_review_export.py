import unittest

from review_export import build_review_feed, snapshot_id


class ReviewExportTests(unittest.TestCase):
    def test_only_local_source_reviews_are_exported_and_checks_are_not_promoted(self):
        imported = {'id': 'github:example/imported', 'local': {}, 'procedures': [{'procedure': 'imported'}]}
        claim = {'code': 'D2a1', 'level': 'source-reviewed', 'revision': 'a'*40,
                 'reviewed_on': '2026-11-07', 'notes': 'Scoped review', 'evidence': [],
                 'procedures': [{'procedure': 'solve', 'role': 'public-entry-point',
                                 'path': 'src.f90', 'line_start': 1, 'line_end': 2,
                                 'usage': 'checked main', 'local_driver': {'report': 'results.json'}},
                                {'procedure': 'helper', 'role': 'implementation-helper'}]}
        local = {'id': 'github:example/local', 'repository': {'url': 'https://github.com/example/local'},
                 'local': {'classifications': [claim, {**claim, 'level': 'documentation-reviewed'}]}}
        feed = build_review_feed([imported, local])
        self.assertEqual(len(feed['projects']), 1)
        procedures = feed['projects'][0]['classifications'][0]['procedures']
        self.assertEqual(len(procedures), 1)
        self.assertNotIn('usage', procedures[0])
        self.assertNotIn('local_driver', procedures[0])
        self.assertEqual(feed['snapshot_id'], snapshot_id(feed))
        self.assertEqual(feed, build_review_feed([local, imported]))

    def test_unchecked_sketch_retains_its_explicit_status(self):
        claim = {'code': 'D2a1', 'level': 'source-reviewed', 'revision': 'a'*40,
                 'reviewed_on': '2026-11-07', 'notes': 'Scoped review', 'evidence': [],
                 'procedures': [{'procedure': 'solve', 'role': 'public-entry-point',
                                 'path': 'src.f90', 'line_start': 1, 'line_end': 2,
                                 'usage': 'call solve(a,b)', 'usage_notes': 'Not compiled.'}]}
        project = {'id': 'github:example/local', 'repository': {}, 'local': {'classifications': [claim]}}
        result = build_review_feed([project])['projects'][0]['classifications'][0]['procedures'][0]
        self.assertEqual(result['usage_kind'], 'calling-sketch')


if __name__ == '__main__':
    unittest.main()
