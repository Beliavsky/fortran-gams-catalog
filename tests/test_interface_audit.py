import copy
import json
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

from interface_audit import audit, markdown, write_report
from catalog import ROOT


def project(name, procedures=(), drivers=()):
    return {'id': 'github:example/'+name, 'name': name,
            'repository': {'url': 'https://github.com/example/'+name},
            'procedures': list(procedures), 'drivers': list(drivers),
            'local': {'classifications': [{'level':'source-reviewed'}]}, 'codes':['N3']}


def procedure(role='public-entry-point', signature='CALL solve(X)', declarations=True, name='solve'):
    value = {'procedure':name, 'module':'solver', 'role':role, 'path':'src.f90',
             'line_start':1, 'line_end':9, 'origin':'local'}
    if signature is not None:
        value['signature']=signature
    if declarations:
        value['declarations']=[{'path':'src.f90','line_start':2,'line_end':3}]
    return value


class InterfaceAuditTests(unittest.TestCase):
    def test_deduplicates_shared_classes_but_retains_distinct_overloads(self):
        first=procedure()
        repeated={**first,'gams_codes':['D2']}
        other={**first,'line_start':20,'line_end':30}
        report=audit([project('library',[first,repeated,other])])
        row=report['projects'][0]
        self.assertEqual(row['public_callable_count'],2)
        self.assertEqual(row['calling_sequence_count'],2)
        self.assertEqual(row['status'],'callable-covered')

    def test_reports_missing_signatures_and_missing_declaration_links(self):
        unsigned=procedure(signature=None)
        unlinked=procedure(declarations=False,name='other')
        row=audit([project('missing',[unsigned,unlinked])])['projects'][0]
        self.assertEqual(row['status'],'missing-callable-sequences')
        self.assertEqual([p['reason'] for p in row['missing_calling_sequences']],
                         ['No calling sequence','No argument-declaration link'])
        row=audit([project('partial',[procedure(),{**unsigned,'procedure':'second'}])])['projects'][0]
        self.assertEqual(row['status'],'partial-callable-sequences')
        self.assertEqual(row['calling_sequence_count'],1)

    def test_cli_data_templates_adapters_and_helpers_are_not_library_calls(self):
        cases={
            'program-entry-point':'program-entry-points',
            'public-data':'noncallable-interface',
            'public-template':'noncallable-interface',
            'public-adapter':'adapter-only',
            'implementation-helper':'no-public-interface-reviewed',
            'callback':'no-public-interface-reviewed',
        }
        for role,status in cases.items():
            with self.subTest(role=role):
                row=audit([project(role,[procedure(role)],drivers=[{'name':'checked'}])])['projects'][0]
                self.assertEqual(row['status'],status)
                self.assertEqual(row['calling_sequence_count'],0)
                self.assertEqual(row['hosted_driver_count'],1)
        # A named imported procedure or unchecked sketch is not a reviewed public API.
        imported={'procedure':'solve','usage':'call solve(x)','review_level':'source-reviewed'}
        row=audit([project('imported',[imported])])['projects'][0]
        self.assertEqual(row['status'],'no-public-interface-reviewed')
        self.assertEqual(audit([project('docs-only')])['projects'][0]['status'],
                         'no-public-interface-reviewed')

    def test_output_is_deterministic_read_only_and_round_trips(self):
        projects=[project('z',[procedure()]),project('a',[procedure(signature='   ')])]
        original=copy.deepcopy(projects)
        report=audit(projects)
        self.assertEqual(audit(list(reversed(projects))),report)
        self.assertEqual(projects,original)
        self.assertEqual(sum(report['status_counts'].values()),report['project_count'])
        self.assertIn('example/a',markdown(report))
        with tempfile.TemporaryDirectory() as tmp:
            write_report(tmp,report)
            self.assertEqual(json.loads((Path(tmp)/'calling-sequence-audit.json').read_text()),report)
            self.assertEqual((Path(tmp)/'calling-sequence-audit.md').read_text(),markdown(report))

    def test_cli_writes_to_requested_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=subprocess.run([sys.executable, '-X', 'utf8', 'xinterface_audit.py', '--output', tmp],
                                  cwd=ROOT, capture_output=True, text=True, check=True, timeout=30)
            saved=json.loads((Path(tmp)/'calling-sequence-audit.json').read_text(encoding='utf-8'))
            self.assertIn('Repositories audited: '+str(saved['project_count']),result.stdout)
            self.assertGreater(saved['project_count'],0)
            self.assertTrue((Path(tmp)/'calling-sequence-audit.md').is_file())
