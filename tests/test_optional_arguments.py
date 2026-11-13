import copy
from html.parser import HTMLParser
import unittest
from argument_intents import signature_markup, optional_notation_markup, declared_optional


class OptionalArgumentTests(unittest.TestCase):
    def procedure(self, signature='call solve(a, tol, info)', **fields):
        return {'signature':signature,'procedure':'solve','argument_details':[
            self.detail('a','real, intent(in) :: a(:)'),
            self.detail('tol','real, intent(in), optional :: tol'),
            self.detail('info','integer, optional :: info')],
            'usage':'call solve(a, tol, info)',**fields}

    def detail(self,name,text,**fields):
        return {'name':name,'declarations':[{'text':text,'path':'src.f90','line_start':1,'line_end':1}],**fields}

    def visible(self,procedure):
        class Text(HTMLParser):
            def __init__(self):super().__init__();self.text=[]
            def handle_data(self,text):self.text.append(text)
        parser=Text();parser.feed(signature_markup(procedure));return ''.join(parser.text)

    def test_explicit_optional_only_and_nonmutating_display(self):
        p=self.procedure();original=copy.deepcopy(p)
        self.assertEqual(self.visible(p),'call solve(a, [tol], [info])')
        self.assertEqual(p,original)
        self.assertIn('not literal Fortran syntax',optional_notation_markup(p))
        p['argument_details']=[self.detail('a','real :: a'),self.detail('tol','real :: tol')]
        p['argument_details'][1]['declarations'][0]['comments']=[{'text':'Optional tolerance.'}]
        self.assertEqual(self.visible(p),p['signature'])
        self.assertEqual(optional_notation_markup(p),'')

    def test_keywords_aliases_and_calls_have_correct_boundaries(self):
        p=self.procedure('call solve(a, tolerance=tol, info=code)',argument_details=[
            self.detail('tol','real, optional :: tolerance',dummy='tolerance'),
            self.detail('code','integer, optional :: info',dummy='info')])
        self.assertEqual(self.visible(p),'call solve(a, [tolerance=tol], [info=code])')
        p=self.procedure('call init(tol)\ncall solve(tol)',argument_details=[self.detail('tol','real, optional :: tol',call_index=1)])
        self.assertEqual(self.visible(p),'call init(tol)\ncall solve([tol])')
        p=self.procedure('call solve(tolerance=max(1.0, f(a,b)))',argument_details=[self.detail('tolerance','real, optional :: tolerance')])
        self.assertEqual(self.visible(p),'call solve([tolerance=max(1.0, f(a,b))])')
        p=self.procedure('call solve(values=[1, 2])',argument_details=[self.detail('values','integer, optional :: values(:)')])
        self.assertEqual(self.visible(p),'call solve([values=[1, 2]])')

    def test_existing_groups_arrays_comments_strings_and_continuations(self):
        for signature in ['call solve(a, [tol], info)', 'call solve(a[,tol,info])',
                          'call solve([a, b], tol)', "call solve('tol, info', tol)"]:
            p=self.procedure(signature)
            text=self.visible(p)
            self.assertNotIn('[[',text)
            if signature=='call solve(a, [tol], info)':self.assertEqual(text,'call solve(a, [tol], [info])')
            if signature=='call solve(a[,tol,info])':self.assertEqual(text,signature)
            if signature=='call solve([a, b], tol)':self.assertEqual(text,'call solve([a, b], [tol])')
        p=self.procedure('call solve(a, &\n  tol, info) ! tol is documented here')
        self.assertEqual(self.visible(p),'call solve(a, &\n  [tol], [info]) ! tol is documented here')

    def test_separate_optional_and_conflicting_or_misleading_declarations(self):
        self.assertTrue(declared_optional(self.detail('x','OPTIONAL x')))
        d=self.detail('x','real :: x');d['declarations'].append({'text':'optional :: x'})
        self.assertTrue(declared_optional(d))
        self.assertFalse(declared_optional(self.detail('optional','real :: optional')))
        self.assertFalse(declared_optional(self.detail('x',"character(len=len('optional')) :: x")))
        self.assertFalse(declared_optional(self.detail('x','real :: x ! optional argument')))
        d=self.detail('x','real, optional :: x');d['declarations'].append({'text':'integer :: x'})
        self.assertFalse(declared_optional(d))


if __name__=='__main__':unittest.main()
