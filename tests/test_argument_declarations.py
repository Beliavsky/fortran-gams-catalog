import unittest
from html.parser import HTMLParser
from argument_intents import signature_markup, argument_details_markup, validate_arguments
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
        self.assertIn('<details',expanded);self.assertIn('#L2-L2',expanded)
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
        self.assertIn('Shared declaration',markup)

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

    def test_alias_and_multicall_ranges_validation(self):
        p=self.capture('''subroutine solve(left,right)
real,intent(in)::left
real,intent(out)::right
end subroutine
''')
        self.assertEqual(p['argument_details'][0]['dummy'],'left')
        p['argument_details'][0]['declarations'][0]['comments']=[{'text':'bad','path':'elsewhere','line_start':1,'line_end':1}]
        with self.assertRaises(ValueError):validate_arguments(p,{'src.f90'})


if __name__=='__main__':unittest.main()
