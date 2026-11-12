import unittest

from argument_intents import signature_markup, validate_arguments
from intent_sources import inspect, scopes, statements


class IntentSourceTests(unittest.TestCase):
    def procedure(self, signature='CALL solve(X,Y)', name='solve', **fields):
        return {'procedure':name,'role':'public-entry-point','path':'src.f90',
                'line_start':1,'line_end':100,'signature':signature,
                'declarations':[{'path':'src.f90','line_start':1,'line_end':100}],**fields}

    def test_free_continuation_separate_intent_strings_and_inner_scope(self):
        text='''subroutine solve(x,y)
real :: x,y
intent(in out) :: x
real, intent( &
 & out) :: y
print *, "! intent(in)::x"
contains
subroutine callback(x)
real,intent(out)::x
end subroutine callback
end subroutine solve
'''
        annotations,result=inspect(self.procedure(),{'src.f90':scopes(text,'src.f90')})
        self.assertEqual(result['status'],'checked')
        self.assertEqual({a['name']:a['intent'] for a in annotations},{'X':'inout','Y':'out'})
        self.assertEqual(annotations[1]['line_start'],4)
        self.assertEqual(annotations[1]['line_end'],5)

    def test_fixed_form_and_no_intent_are_distinct(self):
        text='''      subroutine solve(x,y)
c     intent(out)::x is a comment
      real x,y
      intent(in)
     & x
      end
'''
        p=self.procedure(path='src.f',declarations=[{'path':'src.f','line_start':1,'line_end':6}])
        annotations,result=inspect(p,{'src.f':scopes(text,'src.f')})
        self.assertEqual(result['status'],'checked')
        self.assertEqual([(a['name'],a['intent']) for a in annotations],[('X','in')])
        self.assertNotIn('Y',[a['name'] for a in annotations])

    def test_multicall_distinguishes_same_name_with_different_intents(self):
        text='''subroutine init(x)
real,intent(in)::x
end subroutine
subroutine solve(x)
real,intent(out)::x
end subroutine
'''
        p=self.procedure('CALL init(X)\nCALL solve(X)')
        annotations,result=inspect(p,{'src.f90':scopes(text,'src.f90')})
        self.assertEqual(result['status'],'checked')
        self.assertEqual([(a['call_index'],a['intent']) for a in annotations],[(0,'in'),(1,'out')])
        p['arguments']=annotations
        validate_arguments(p,{'src.f90'})
        markup=signature_markup(p)
        self.assertEqual(markup.count('data-argument-intent="in"'),1)
        self.assertEqual(markup.count('data-argument-intent="out"'),1)

    def test_operator_positional_names_and_result_exclusion(self):
        text='''function add(left,right) result(value)
real,intent(in)::left,right
real::value
value=left+right
end function
'''
        p=self.procedure('C = A + B',name='operator(+)')
        annotations,result=inspect(p,{'src.f90':scopes(text,'src.f90')})
        self.assertEqual(result['status'],'checked')
        self.assertEqual([(a['name'],a['dummy']) for a in annotations],[('A','left'),('B','right')])
        p['arguments']=annotations
        validate_arguments(p,{'src.f90'})
        self.assertTrue(signature_markup(p).startswith('C = '))

    def test_missing_scopes_conflicting_intents_and_unmatched_names_need_review(self):
        p=self.procedure()
        self.assertEqual(inspect(p,{})[1]['status'],'partial')
        text='''subroutine solve(x,y)
#ifdef A
real,intent(in)::x
#else
real,intent(out)::x
#endif
real::y
end subroutine
'''
        annotations,result=inspect(p,{'src.f90':scopes(text,'src.f90')})
        self.assertEqual(result['status'],'partial')
        self.assertEqual(annotations,[])
        self.assertIn('conflicting',result['issues'][0])

    def test_type_bound_passed_object_and_nopass_matching_arity(self):
        text='''subroutine set(self,value)
class(box),intent(inout)::self
real,intent(in)::value
end subroutine
'''
        p=self.procedure('CALL p%set(VALUE)',derived_type='box')
        annotations,result=inspect(p,{'src.f90':scopes(text,'src.f90')})
        self.assertEqual(result['status'],'checked')
        self.assertEqual([(a['name'],a['intent']) for a in annotations],[('VALUE','in')])
        p['signature']='CALL p%set(SELF,VALUE)'
        annotations,result=inspect(p,{'src.f90':scopes(text,'src.f90')})
        self.assertEqual(len(annotations),2)

    def test_semicolon_and_quoted_exclamation(self):
        parts=list(statements("subroutine f(x); real,intent(in)::x ! a comment\nprint *, 'a!b;c'\nend subroutine"))
        self.assertEqual(len(parts),4)
        self.assertEqual(parts[2][2],"print *, 'a!b;c'")

    def test_generic_selects_matching_arity_and_ignores_documentation(self):
        text='''interface solve
module procedure solve_one,solve_two
end interface
subroutine solve_one(x)
real,intent(in)::x
end subroutine
subroutine solve_two(x,y)
real,intent(in)::x
real,intent(out)::y
end subroutine
'''
        p=self.procedure(declarations=[{'path':'src.f90','line_start':1,'line_end':4}])
        annotations,result=inspect(p,{'src.f90':scopes(text,'src.f90')})
        self.assertEqual(result['status'],'checked')
        self.assertEqual([(a['name'],a['intent']) for a in annotations],[('X','in'),('Y','out')])
        self.assertEqual(scopes(text,'README.md'),[])

    def test_templates_no_arg_subroutines_and_free_source_with_f_extension(self):
        text='''module example
contains
subroutine init
end subroutine
function evaluate_\u0024{kind}\u0024(x) result(value)
\u0024{type}\u0024,intent(in)::x
real::value
end function
end module
'''
        items=scopes(text,'src.f')
        self.assertEqual([(s.name,s.dummies) for s in items],[('init',[]),('evaluate_zztemplate',['x'])])
        self.assertEqual(items[1].declarations['x'][0]['intent'],'in')
