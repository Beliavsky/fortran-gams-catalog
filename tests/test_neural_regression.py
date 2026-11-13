import unittest
from catalog import assemble, belongs


class NeuralRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree, cls.projects, _ = assemble()
        cls.by_id = {p['id']: p for p in cls.projects}

    def test_squared_error_training_is_discoverable_under_nonlinear_regression(self):
        for name in ('thchang/nn_mod', 'modern-fortran/neural-fortran', 'nedtaylor/athena'):
            project = self.by_id['github:' + name]
            claim = next(c for c in project['local']['classifications'] if c['code'] == 'L8e1b1')
            self.assertEqual(claim['level'], 'source-reviewed')
            self.assertTrue(belongs(self.tree, claim['code'], 'L8e'))
            public = [p for p in claim['procedures'] if p.get('role') == 'public-entry-point']
            self.assertTrue(public)
            for procedure in public:
                self.assertEqual(procedure['procedure'].lower(), 'train')
                self.assertEqual(procedure['argument_intent_review']['status'], 'checked')
                self.assertTrue(procedure.get('argument_details'))
            self.assertNotIn('L8e1b2', {c['code'] for c in project['local']['classifications']})

    def test_inference_review_does_not_claim_a_fitting_algorithm(self):
        for name, binding in [('scientific-computing/fkb', 'output'), ('berkeleylab/fiats', 'infer')]:
            project = self.by_id['github:' + name]
            claim = next(c for c in project['local']['classifications'] if c['code'] == 'L8e')
            self.assertEqual([p['procedure'] for p in claim['procedures']], [binding])
            self.assertIn('inference', claim['notes'])
            self.assertFalse(any(c['code'].startswith('L8e1') for c in project['local']['classifications']))

    def test_layer_kernels_and_derivative_tools_are_not_blanket_regression_mappings(self):
        for name in ('metoffice/ennuf', 'samhatfield/nn_tl_ad', 'cerea-daml/fnn'):
            self.assertFalse(any(c['code'].startswith('L8e')
                                 for c in self.by_id['github:' + name]['local']['classifications']))
        self.assertTrue(any(c['code'] == 'L8e' for c in
                            self.by_id['github:zhoutengye/fsklearn']['local']['classifications']))
