import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from catalog import assemble
from topics import (DIFFERENTIATION_TOPICS, EXPRESSION_TOPICS, DISCOVERY_TOPICS,
                    differentiation_topics, expression_topics, discovery_topics)
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
        self.assertEqual(len(ad), 20)
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

    def test_expression_membership_capabilities_and_review_scope(self):
        parsers = {p['id']: p for p in self.projects if expression_topics(p)}
        self.assertEqual(len(parsers), 15)
        self.assertEqual(expression_topics({'topics': ['expression-parser']}), [])
        self.assertEqual(expression_topics({'local': {'topics': ['complex-evaluation']}}), [])
        for p in parsers.values():
            self.assertIn('N3', p['codes'])
            self.assertNotIn('O', p['codes'])
        fparse = parsers['github:jacobwilliams/fparse']
        self.assertIn('parser-derivatives', expression_topics(fparse))
        self.assertIn('expression-code-generation', expression_topics(fparse))
        self.assertIn('automatic-differentiation', discovery_topics(fparse))
        self.assertEqual(next(c for c in fparse['local']['classifications'] if c['code']=='H1')['level'],
                         'documentation-reviewed')
        names = {p['procedure'] for p in fparse['local']['classifications'][0]['procedures']}
        self.assertTrue({'parse', 'set_variable', 'evaluate', 'get', 'get_derivative',
                         'add_function', 'generate_fortran'} <= names)
        self.assertNotIn('array-evaluation', expression_topics(parsers['github:jacobwilliams/fortran_function_parser']))
        self.assertNotIn('complex-evaluation', expression_topics(parsers['github:muhammad-fiaz/fortran-calc']))
        self.assertNotIn('reusable-parser', expression_topics(parsers['github:sgeard/hp']))

    def test_expression_page_links_counts_and_combined_capabilities(self):
        ids = {'github:jacobwilliams/fparse', 'github:fluidnumerics/feq-parse',
               'github:sgeard/hp', 'github:jacobwilliams/numdiff'}
        selected = [p for p in self.projects if p['id'] in ids]
        with tempfile.TemporaryDirectory() as tmp, \
                patch('xbuild.assemble', return_value=(self.tree, selected, self.merged)), \
                patch('xbuild.load_legacy', return_value={'entries': []}):
            destination = Path(tmp)
            build(destination)
            page = (destination/'topics/expression-parsers/index.html').read_text(encoding='utf-8')
            self.assertEqual(page.count('<article data-search='), 3)
            self.assertIn('Parser capabilities:', page)
            self.assertIn('Usage (argument declarations)', page)
            self.assertIn('Fortran code generation', page)
            self.assertIn('not evidence of symbolic algebra',
                          (destination/'classes/O/index.html').read_text(encoding='utf-8'))
            for code in ('N3','O'):
                self.assertIn('../../topics/expression-parsers/',
                              (destination/f'classes/{code}/index.html').read_text(encoding='utf-8'))
            home = (destination/'index.html').read_text(encoding='utf-8')
            self.assertIn('topics/expression-parsers/', home)
            self.assertIn('&quot;expression-parser&quot;', home)
            self.assertIn('calling-sequences/', home)
            report = json.loads((destination/'calling-sequence-audit.json').read_text(encoding='utf-8'))
            self.assertEqual(report['project_count'], 4)
            self.assertEqual(report['status_counts']['program-entry-points'], 0)
            self.assertEqual(report['status_counts']['no-public-interface-reviewed'], 1)  # hp: docs only
            audit_page = (destination/'calling-sequences/index.html').read_text(encoding='utf-8')
            self.assertIn('../projects/sgeard/hp/', audit_page)
            self.assertIn('../calling-sequence-audit.md', audit_page)
            self.assertTrue((destination/'calling-sequence-audit.md').is_file())
            from html.parser import HTMLParser
            class Topics(HTMLParser):
                def __init__(self):
                    super().__init__(); self.cards=[]; self.options=[]; self.counts=[]
                def handle_starttag(self, tag, attrs):
                    attrs = dict(attrs)
                    if tag=='article': self.cards.append(attrs.get('data-topics','').split())
                    if tag=='option': self.options.append(attrs.get('value'))
                    if 'data-topic-counts' in attrs:
                        self.counts.append(json.loads(attrs['data-topic-counts']))
            parsed=Topics(); parsed.feed(page)
            self.assertTrue(set(DISCOVERY_TOPICS) <= set(parsed.options))
            self.assertTrue(any({'automatic-differentiation','expression-parser','parser-derivatives'} <= set(c)
                                for c in parsed.cards))
            counts=Topics(); counts.feed(home)
            self.assertTrue(any(c['expression-parser'].get('|0|0|0')==3 for c in counts.counts))
            self.assertTrue(any(c['expression-parser'].get('|0|1|0')==2 for c in counts.counts))

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
            self.assertIn('>Fortran software catalog</a>', home)
            self.assertEqual(home.count('<h1>Fortran software by GAMS classification</h1>'), 1)
            self.assertNotIn('>Fortran software by GAMS classification</a>', home)
            self.assertIn('<details id="filters" class="filters-panel">', home)
            self.assertNotIn('<details id="filters" class="filters-panel" open', home)
            self.assertIn('action="projects/" data-destination="projects/"', home)
            self.assertEqual(home.count('id="collection"'), 1)
            self.assertLess(home.index('id="collection"'), home.index('</details>'))
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
