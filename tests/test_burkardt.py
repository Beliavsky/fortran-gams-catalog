import unittest
from catalog import assemble
from xbuild import supports_fpm
from licenses import license_group
from review_export import build_review_feed


class BurkardtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree, projects, _ = assemble()
        records = [p for p in projects if p['id'] == 'github:beliavsky/burkardt-fortran-90-codes']
        if len(records) != 1:
            raise AssertionError('The collection needs one canonical repository identity')
        cls.project = records[0]
        cls.claims = cls.project['local']['classifications']

    def test_reviewed_components_keep_source_pins_and_external_interfaces(self):
        expected = set('asa006 asa007 asa047 asa063 asa066 asa091 asa109 asa136 asa241 asa245 bisection_rc zero_brent rkf45 ode qr_solve jacobi_eigenvalue toeplitz_cholesky fftpack5 fft_serial hermite_cubic spline lagrange_interp_1d pwl_interp_1d legendre_polynomial kronrod quadpack sobol halton normal sort_rc'.split())
        seen = {p['path'].split('/')[0] for c in self.claims for p in c['procedures']}
        self.assertTrue(expected <= seen)
        self.assertFalse(supports_fpm(self.project))
        self.assertEqual(self.project['drivers'], [])
        for claim in self.claims:
            self.assertEqual(claim['level'], 'source-reviewed')
            self.assertEqual(len(claim['revision']), 40)
            for evidence in claim['evidence']:
                self.assertIn('/blob/' + claim['revision'] + '/', evidence['url'])
            for procedure in claim['procedures']:
                self.assertNotIn('local_driver', procedure)
                self.assertNotIn('module', procedure)
                if procedure.get('role') == 'public-entry-point':
                    self.assertTrue(procedure['signature'])
                    self.assertTrue(procedure['declarations'])
                    self.assertEqual(procedure['argument_intent_review']['status'], 'checked')
        asa006 = next(p for c in self.claims for p in c['procedures'] if p['path'] == 'asa006/asa006.f90')
        # Input/output descriptions in legacy comments are not Fortran INTENT.
        self.assertFalse(asa006.get('arguments'))

    def test_gams_scopes_distinguish_rules_solvers_and_sampling(self):
        def codes(name):
            return {c['code'] for c in self.claims for p in c['procedures'] if p['procedure'] == name}
        for name, expected in [('nelmin', 'G1b2'), ('zero_brent', 'F1b'), ('rkf45', 'I1a1a'),
                               ('ode', 'I1a1b'), ('cfft1f', 'J1a2'), ('rfft1f', 'J1a1'),
                               ('p_quadrature_rule', 'H2c'), ('kronrod', 'H2c'),
                               ('i8_sobol', 'L6'), ('halton', 'L6'), ('sort_safe_rc', 'N6a2')]:
            self.assertEqual(codes(name), {expected})
        self.assertEqual(codes('dqagi'), {'H2a3', 'H2a4'})
        self.assertIn('deterministic', next(c['notes'] for c in self.claims if c['code'] == 'L6').lower())

    def test_standalone_fft_is_not_exported_as_a_callable_library(self):
        main = next(p for c in self.claims for p in c['procedures']
                    if p['path'] == 'fft_serial/fft_serial.f90' and p['procedure'] == 'main')
        self.assertEqual(main['role'], 'program-entry-point')
        self.assertNotIn('signature', main)
        feed = build_review_feed([self.project])
        public = [p for c in feed['projects'][0]['classifications'] for p in c['procedures']]
        self.assertFalse(any(p['path'] == 'fft_serial/fft_serial.f90' for p in public))
        self.assertTrue(any(p['procedure'] == 'cfft1f' for p in public))

    def test_license_is_component_scoped_not_blanket_mit(self):
        license_data = self.project['license']
        self.assertEqual(license_group(self.project), 'custom-mixed')
        self.assertIsNone(license_data['spdx_expression'])
        self.assertIn('FFTPACK5', license_data['notes'])
        self.assertIn('GPL', license_data['notes'])
        self.assertIn('QUADPACK', license_data['notes'])
        self.assertIn('DGTSL and TIMESTAMP helpers', license_data['notes'])
        self.assertIn('not treated as a blanket grant', license_data['notes'])
        self.assertIn('not a repository-wide', license_data['notes'])
