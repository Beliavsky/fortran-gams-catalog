import copy
from html.parser import HTMLParser
import unittest

from argument_intents import signature_markup, validate_arguments
from catalog import assemble, validate_local
from review_export import build_review_feed
from intent_coverage import records, write_reports


class ArgumentIntentTests(unittest.TestCase):
    def setUp(self):
        self.procedure = {'procedure':'solve','role':'public-entry-point',
            'signature':"X = p%solve(X, [XX], INFO, 'X')", 'path':'src.f90',
            'declarations':[{'path':'src.f90','line_start':10,'line_end':20}],
            'arguments':[{'name':'x','intent':'inout','path':'src.f90','line_start':11,'line_end':11},
                         {'name':'INFO','intent':'out','path':'src.f90','line_start':12,'line_end':12}]}

    def test_markup_preserves_text_and_annotates_only_argument_tokens(self):
        class Signature(HTMLParser):
            def __init__(self):
                super().__init__();self.text=[];self.spans=[]
            def handle_data(self,data):self.text.append(data)
            def handle_starttag(self,tag,attrs):
                if tag=='span':self.spans.append(dict(attrs))
        markup=signature_markup(self.procedure)
        parsed=Signature();parsed.feed(markup)
        self.assertEqual(''.join(parsed.text),self.procedure['signature'])
        self.assertEqual([p['data-argument-intent'] for p in parsed.spans],['inout','out'])
        self.assertTrue(all(p['tabindex']=='0' and 'intent(' in p['aria-label'] for p in parsed.spans))
        # The result X, XX and quoted 'X' must not acquire an inferred intent.
        self.assertTrue(markup.startswith('X = p%solve('))
        self.assertIn('[XX]',markup)
        self.assertIn('&#x27;X&#x27;',markup)
        plain={'signature':'USE constants, ONLY: x < y & z'}
        self.assertEqual(signature_markup(plain),'USE constants, ONLY: x &lt; y &amp; z')

    def test_validation_requires_explicit_intent_and_declaration_provenance(self):
        validate_arguments(self.procedure,{'src.f90'})
        changes=[lambda p:p['arguments'][0].update(intent='unknown'),
                 lambda p:p['arguments'][0].update(name='missing'),
                 lambda p:p['arguments'][0].update(path='other.f90'),
                 lambda p:p['arguments'][0].update(line_start=1,line_end=1),
                 lambda p:p['arguments'].append(copy.deepcopy(p['arguments'][0])),
                 lambda p:p.update(role='public-data'),
                 lambda p:p.update(arguments={}),
                 lambda p:p.update(signature='X = p%solve()')]
        for change in changes:
            bad=copy.deepcopy(self.procedure);change(bad)
            with self.assertRaises(ValueError):validate_arguments(bad,{'src.f90'})

    def test_seed_annotations_preserve_overloads_and_unspecified_intents(self):
        tree,projects,_=assemble()
        by_id={p['id']:p for p in projects}
        def find(identity,name):
            return next(p for p in by_id['github:'+identity]['procedures']
                        if p.get('origin')=='local' and p['procedure']==name)
        p=find('jacobwilliams/minpack','hybrd1')
        values={a['name'].casefold():a['intent'] for a in p['arguments']}
        self.assertEqual(values['x'],'inout');self.assertEqual(values['info'],'out')
        self.assertNotIn('fcn',values)  # Callback has no explicit INTENT.
        self.assertFalse(find('certik/minpack','hybrd1').get('arguments'))
        feq=find('fluidnumerics/feq-parse','Evaluate')
        self.assertFalse(feq.get('arguments'))  # Same name, separate unannotated overloads.
        fparse=find('jacobwilliams/fparse','get')
        self.assertEqual(next(a['intent'] for a in fparse['arguments'] if a['name']=='VALUE'),'out')
        record={'id':'github:example/test','local':{'classifications':[{
            'code':'N3','level':'source-reviewed','revision':'a'*40,'reviewed_on':'2026-11-12',
            'notes':'Scoped review.','evidence':[{'path':'src.f90',
                'url':'https://github.com/example/test/blob/'+'a'*40+'/src.f90','sha256':'b'*64}],
            'procedures':[{**self.procedure,'line_start':1,'line_end':30,'summary':'Public interface.'}]}]}}
        validate_local({'schema_version':1,'projects':[record]},tree)
        record['local']['classifications'][0]['procedures'][0]['arguments'][0]['intent']='bogus'
        with self.assertRaises(ValueError):validate_local({'schema_version':1,'projects':[record]},tree)

    def test_review_export_keeps_structured_intents_without_promoting_checks(self):
        _,projects,_=assemble()
        project=next(p for p in projects if p['id']=='github:jacobwilliams/fparse')
        exported=build_review_feed([project])['projects'][0]
        proc=next(p for p in exported['classifications'][0]['procedures'] if p['procedure']=='get')
        self.assertTrue(proc['arguments'])
        self.assertNotIn('local_driver',proc)
        proc['arguments'][0]['intent']='out'
        original=next(p for p in project['local']['classifications'][0]['procedures'] if p['procedure']=='get')
        self.assertEqual(original['arguments'][0]['intent'],'in')

    def test_conditional_intents_show_alternatives_without_a_fixed_intent(self):
        p=copy.deepcopy(self.procedure)
        p['arguments']=[{'name':'X','intent':'conditional','path':'src.f90','line_start':10,'line_end':15,
            'variants':[{'intent':'out','condition':'FEATURE is not defined','path':'src.f90','line_start':11,'line_end':11},
                        {'intent':'inout','condition':'FEATURE is defined','path':'src.f90','line_start':14,'line_end':14}]}]
        validate_arguments(p,{'src.f90'})
        markup=signature_markup(p)
        self.assertIn('data-argument-intent="conditional"',markup)
        self.assertIn('intent(inout) when FEATURE is defined',markup)
        p['arguments'][0]['variants'][0]['line_start']=1
        with self.assertRaises(ValueError):validate_arguments(p,{'src.f90'})

    def test_every_current_usage_has_a_review_or_an_explicit_exemption(self):
        _,projects,_=assemble()
        rows=records(projects)
        self.assertFalse([r for r in rows if r['status'] in {'partial','unreviewed'}])
        self.assertGreater(sum(bool(r['argument_count']) for r in rows),1000)
        c=next(r for r in rows if r['project']=='github:trex-coe/sherman-morrison' and r['procedure']=='SM1_f')
        self.assertEqual(c['status'],'not-applicable')
        self.assertIn('six',c['notes'])
        gateway=next(r for r in rows if r['project']=='github:slicot/slicot-systemidentification')
        self.assertEqual(gateway['status'],'not-applicable')
        self.assertIn('MATLAB',gateway['notes'])
        # New records are exposed as unreviewed without a manually maintained snapshot.
        new={'id':'github:example/new','local':{'classifications':[{'code':'N3','revision':'a'*40,
             'procedures':[{**self.procedure,'line_start':1,'line_end':30}]}]}}
        self.assertEqual(records([new])[0]['status'],'unreviewed')
