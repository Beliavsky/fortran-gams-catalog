import unittest
import json
from html.parser import HTMLParser
from argument_intents import signature_markup, argument_details_markup, validate_arguments, individual_declaration
from intent_sources import scopes, inspect


class ArgumentDeclarationTests(unittest.TestCase):
    def capture(self, source, signature='call solve(x, y)', path='src.f90'):
        procedure={'procedure':'solve','role':'public-entry-point','path':path,'line_start':1,'line_end':100,
                   'signature':signature,'declarations':[{'path':path,'line_start':1,'line_end':100}]}
        details=[]
        annotations,review=inspect(procedure,{path:scopes(source,path)},details)
        procedure.update(argument_details=details,arguments=annotations)
        if not annotations:procedure.pop('arguments')
        validate_arguments(procedure,{path})
        return procedure

    def test_full_declarations_comments_and_separate_attributes(self):
        p=self.capture('''subroutine solve(x,y)
!> Solution matrix. <script>alert('bad')</script>
real(kind=8), allocatable, intent(out) :: x(:,:) ! Allocated by this routine.
real :: y
!! Input shift.
optional :: y
intent(in) :: y
end subroutine
''')
        x,y=p['argument_details']
        self.assertIn('allocatable',x['declarations'][0]['text'])
        comments=x['declarations'][0]['comments']
        self.assertEqual({c['kind'] for c in comments},{'preceding','trailing'})
        self.assertEqual([d['text'] for d in y['declarations']],['real :: y','optional :: y','intent(in) :: y'])
        self.assertEqual(y['declarations'][0]['comments'][0]['text'],'Input shift.')
        markup=signature_markup(p)
        self.assertIn('real(kind=8), allocatable, intent(out)',markup)
        self.assertNotIn('<script>',markup)
        self.assertIn('&lt;script&gt;',markup)
        expanded=argument_details_markup(p,'https://github.com/a/b/blob/'+'a'*40+'/')
        self.assertIn('<details',expanded);self.assertEqual(expanded.count('<pre>'),1)
        self.assertIn('</span> ! Solution matrix.',expanded)
        self.assertNotIn('Shared declaration',expanded)
        self.assertNotIn('<dt>',expanded)
        self.assertIn('Input shift.',expanded)

    def test_unspecified_intent_shared_declaration_and_unrelated_comments(self):
        p=self.capture('''subroutine solve(x,y)
! A section heading is not an argument description.
real x,y ! Both use the same unit.
!> Explanation of a local variable, not y.
integer :: local
end subroutine
''')
        self.assertFalse(p.get('arguments'))
        x,y=p['argument_details']
        self.assertTrue(x['declarations'][0]['shared'])
        self.assertEqual(len(x['declarations'][0]['comments']),1)
        self.assertEqual(x['declarations'],y['declarations'])
        markup=signature_markup(p)
        self.assertIn('data-argument-intent="unspecified"',markup)
        self.assertNotIn('Explanation of a local',markup)
        self.assertNotIn('Shared declaration',markup)
        self.assertIn('Shared comment: Both use the same unit.',markup)
        self.assertIn('x: real x',markup)
        self.assertNotIn('real x,y',markup)
        self.assertIn('real x,y',argument_details_markup(p,'https://example.test/'))

    def test_continuations_quoted_bang_fixed_form_and_raw_templates(self):
        p=self.capture('''subroutine solve(x,y)
character(len=*), intent(in) :: x ! literal ! remains comment
real, &
 & intent(out) :: y
end subroutine
''')
        self.assertEqual(p['argument_details'][1]['declarations'][0]['line_end'],4)
        p=self.capture('''      subroutine solve(x,y)
c     Unrelated fixed comment.
      real*8 x,y
      intent(in) x
      end
''',path='src.f')
        self.assertEqual(p['argument_details'][0]['declarations'][0]['text'],'real*8 x,y')
        p=self.capture('''subroutine solve(x,y)
${TYPE}$, intent(in) :: x
BIGREAL, intent(out) :: y
end subroutine
''')
        self.assertEqual(p['argument_details'][0]['declarations'][0]['text'],'${TYPE}$, intent(in) :: x')
        self.assertNotIn('zztemplate',signature_markup(p))

    def test_individual_projection_preserves_shapes_attributes_and_literals(self):
        cases=[
            ('real(wp), intent(in) :: x(n), y(n)', 'x', 'real(wp), intent(in) :: x(n)'),
            ('real, dimension(n,m), allocatable :: x, y(:,:)', 'y', 'real, dimension(n,m), allocatable :: y(:,:)'),
            ('integer :: x=1, y=f(2,3)', 'y', 'integer :: y=f(2,3)'),
            ("character(*) :: x='a,b', y='::'", 'y', "character(*) :: y='::'"),
            ('double precision x(n,m),y(*)', 'y', 'double precision y(*)'),
            ('real*8 X,Y', 'x', 'real*8 X'),
            ('TYPE ( FM ) MA,MB,FMBETA_FM', 'ma', 'TYPE ( FM ) MA'),
            ('intent(in) x,y', 'y', 'intent(in) y'),
            ('character(len=max(1,n)) :: x,y', 'x', 'character(len=max(1,n)) :: x'),
            ('${TYPE}$, intent(in) :: x,y', 'x', '${TYPE}$, intent(in) :: x')]
        for text,name,expected in cases:
            with self.subTest(text=text):self.assertEqual(individual_declaration(text,name),expected)
        self.assertIsNone(individual_declaration('unfamiliar x,y','x'))
        self.assertIsNone(individual_declaration('real :: x,y','z'))
        p=self.capture('subroutine solve(left,right)\nreal :: left(2,2),right(2,2)\nend subroutine')
        markup=signature_markup(p)
        self.assertIn('real :: left(2,2)',markup)
        self.assertIn('real :: right(2,2)',markup)
        self.assertNotIn('left(2,2),right',markup)
        self.assertNotIn('Shared comment',markup)

    def test_intent_is_not_repeated_when_the_displayed_declaration_has_it(self):
        def tooltip(procedure):
            class P(HTMLParser):
                def __init__(self):super().__init__();self.values=[]
                def handle_starttag(self,tag,attrs):
                    attrs=dict(attrs)
                    if tag=='span':self.values.append(attrs['title'])
            parser=P();parser.feed(signature_markup(procedure));return parser.values[0]
        p=self.capture('subroutine solve(x,y)\nreal,intent(out)::x\nreal::y\nend subroutine')
        self.assertEqual(tooltip(p).count('intent(out)'),1)
        p['argument_details'][0]['declarations'][0]['text']='real :: x'
        self.assertIn('\n\nintent(out)',tooltip(p))
        p['argument_details'][0]['declarations'][0]['text']='real :: x'
        p['argument_details'][0]['declarations'][0]['comments']=[{'text':'Example: intent(out)'}]
        self.assertTrue(tooltip(p).endswith('\n\nintent(out)'))
        p['argument_details'][0]['declarations'][0]['text']="character(*) :: x='intent(out)'"
        self.assertTrue(tooltip(p).endswith('\n\nintent(out)'))
        p['arguments'][0].update(intent='conditional',variants=[
            {'intent':'out','condition':'FEATURE is off'}, {'intent':'inout','condition':'FEATURE is on'}])
        p['argument_details'][0]['declarations'][0]['text']='real,intent(out)::x'
        self.assertIn('intent(inout) when FEATURE is on',tooltip(p))
        p.pop('argument_details')
        self.assertIn('intent(out) when FEATURE is off',tooltip(p))

    def test_tooltip_format_ranges_cover_code_without_comments(self):
        p=self.capture('subroutine solve(x,y)\nREAL :: x\n!! Keep UPPER, COMMENT ??\nOPTIONAL :: x\nREAL :: y\nend subroutine')
        p['argument_details'][0]['dummy']='X'
        class Spans(HTMLParser):
            def __init__(self):super().__init__();self.spans=[]
            def handle_starttag(self,tag,attrs):
                if tag=='span':self.spans.append(dict(attrs))
        parser=Spans();parser.feed(signature_markup(p))
        span=parser.spans[0];description=span['data-intent-description']
        fragments=[description[first:last] for first,last in json.loads(span['data-code-ranges'])]
        self.assertEqual(fragments,['REAL :: x','OPTIONAL :: x'])
        self.assertIn('Keep UPPER, COMMENT ??',description)
        self.assertEqual(span['data-argument-label'],'x')
        self.assertIn('class="declaration-code"',argument_details_markup(p,'https://example.test/'))

    def test_declaration_without_intent_and_disclosure(self):
        p=self.capture('subroutine solve(x,y)\nREAL X,Y\nend subroutine')
        markup=signature_markup(p)
        self.assertNotIn('No explicit INTENT',markup)
        self.assertNotIn('Declaration unavailable',markup)
        details=argument_details_markup(p,'https://example.test/')
        self.assertIn('Show declarations',details)
        self.assertIn('Hide declarations',details)
        self.assertIn('data-normalized-code="REAL X"',details)
        self.assertIn('REAL X,Y',details)
        self.assertNotIn(' open',details)

    def test_alias_and_multicall_ranges_validation(self):
        p=self.capture('''subroutine solve(left,right)
real,intent(in)::left
real,intent(out)::right
end subroutine
''')
        self.assertEqual(p['argument_details'][0]['dummy'],'left')
        p['argument_details'][0]['declarations'][0]['comments']=[{'text':'bad','path':'elsewhere','line_start':1,'line_end':1}]
        with self.assertRaises(ValueError):validate_arguments(p,{'src.f90'})


    def test_declarations_share_one_box_with_trailing_comments_in_call_order(self):
        procedure={'signature':'call solve(n, x, l)', 'argument_details':[
            {'name':'l','declarations':[{'text':'REAL(8) :: X(N), L(N)','shared':True}]},
            {'name':'n','declarations':[{'text':'INTEGER :: N','comments':[
                {'text':'!> Number of entries.\n!! Must be positive.'}]}]},
            {'name':'x','declarations':[{'text':'REAL(8) :: X(N), L(N)','shared':True,
                'comments':[{'text':'Input <values>.'}]}]}]}
        rendered=argument_details_markup(procedure,'https://example.test/')
        self.assertEqual(rendered.count('<pre>'),1)
        self.assertEqual(rendered.count('<code>'),1)
        self.assertNotIn('<dl>',rendered)
        self.assertNotIn('Shared declaration',rendered)
        self.assertNotIn('<a ',rendered)
        self.assertIn('</span> ! Number of entries. Must be positive.',rendered)
        self.assertIn('</span> ! Input &lt;values&gt;.',rendered)
        self.assertLess(rendered.index('INTEGER :: N'),rendered.index('data-normalized-code="REAL(8) :: X(N)"'))
        self.assertLess(rendered.index('data-normalized-code="REAL(8) :: X(N)"'),rendered.index('data-normalized-code="REAL(8) :: L(N)"'))

if __name__=='__main__':unittest.main()
