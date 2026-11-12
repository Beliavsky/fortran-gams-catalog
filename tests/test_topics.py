import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from catalog import assemble
from topics import DIFFERENTIATION_TOPICS, differentiation_topics
from xbuild import build


class DifferentiationTopicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree, cls.projects, cls.merged = assemble()

    def test_facets_require_explicit_curator_membership(self):
        self.assertEqual(differentiation_topics({'topics': ['automatic-differentiation', 'forward-mode']}), [])
        self.assertEqual(differentiation_topics({'local': {'topics': ['forward-mode']}}), [])
        self.assertEqual(differentiation_topics({'local': {'topics': [
            'automatic-differentiation', 'reverse-mode', 'unrelated-topic']}}),
            ['automatic-differentiation', 'reverse-mode'])

    def test_existing_ad_entries_are_discoverable_without_symbolic_remapping(self):
        ad = {p['id']: p for p in self.projects if differentiation_topics(p)}
        self.assertEqual(len(ad), 19)
        expected = {
            'github:lauvergn/ad_dnsvm': {'forward-mode', 'higher-derivatives'},
            'github:pv/adjac': {'reverse-mode', 'sparse-jacobians'},
            'github:nedtaylor/diffstruc': {'forward-mode', 'reverse-mode'},
            'github:imurray/chol-rev': {'reverse-mode', 'matrix-derivatives'},
            'github:atmmod/hyperdualize-fortran': {'source-transformation'},
        }
        for identity, facets in expected.items():
            with self.subTest(identity=identity):
                self.assertTrue(facets.issubset(differentiation_topics(ad[identity])))
                self.assertNotIn('O', ad[identity]['codes'])
        numdiff = next(p for p in self.projects if p['id'] == 'github:jacobwilliams/numdiff')
        self.assertEqual(differentiation_topics(numdiff), [])
        self.assertNotIn('github:octoflar/m_ad', ad)

    def test_topic_page_related_links_and_filter_counts_are_generated(self):
        selected = [p for p in self.projects if p['id'] in {
            'github:pv/adjac', 'github:atmmod/hyperdualize-fortran', 'github:jacobwilliams/numdiff'}]
        with tempfile.TemporaryDirectory() as tmp, \
                patch('xbuild.assemble', return_value=(self.tree, selected, self.merged)), \
                patch('xbuild.load_legacy', return_value={'entries': []}):
            destination = Path(tmp)
            build(destination)
            topic = (destination/'topics/automatic-differentiation/index.html').read_text(encoding='utf-8')
            self.assertEqual(topic.count('<article data-search='), 2)
            self.assertIn('AD capabilities:', topic)
            self.assertIn('id="topic"', topic)
            self.assertIn('m_ad repository link returned 404', topic)
            self.assertIn('not proof that every method', topic)
            for code in ('O', 'H1'):
                page = (destination/'classes'/code/'index.html').read_text(encoding='utf-8')
                self.assertIn('../../topics/automatic-differentiation/', page)
                self.assertIn('Related:', page)
            home = (destination/'index.html').read_text(encoding='utf-8')
            # Extract the H hierarchy counts without depending on attribute ordering.
            from html.parser import HTMLParser
            class Counts(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.values = []
                def handle_starttag(self, tag, attrs):
                    values = dict(attrs)
                    if 'data-topic-counts' in values:
                        self.values.append(json.loads(values['data-topic-counts']))
            parser = Counts(); parser.feed(home)
            self.assertTrue(any(c['automatic-differentiation'].get('|0|0|0') == 1
                                for c in parser.values))
            self.assertTrue(any(c['source-transformation'].get('|0|0|0') == 1
                                for c in parser.values))
            for path in [destination/'index.html', destination/'topics/automatic-differentiation/index.html']:
                self.assertIn('topic-filter-help', path.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
