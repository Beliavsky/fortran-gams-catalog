import hashlib
from io import BytesIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from intent_coverage import records, write_reports
from xargument_intents import load_source


class IntentCoverageTests(unittest.TestCase):
    def test_pinned_source_loader_verifies_cache_and_downloaded_encoding(self):
        text='! café\nsubroutine f()\nend subroutine\n'
        sha=hashlib.sha256(text.encode()).hexdigest()
        evidence={'url':'https://github.com/example/test/blob/'+'a'*40+'/src.f90','sha256':sha}
        with tempfile.TemporaryDirectory() as tmp:
            cache=Path(tmp)
            with self.assertRaises(ValueError):load_source(evidence,cache,False)
            with patch('xargument_intents.urllib.request.urlopen',return_value=BytesIO(text.replace('\n','\r\n').encode('latin-1'))):
                self.assertEqual(load_source(evidence,cache,True),text)
            self.assertEqual(load_source(evidence,cache,False),text)
            (cache/(sha+'.txt')).write_text('modified',encoding='utf-8')
            with self.assertRaises(ValueError):load_source(evidence,cache,False)

    def test_unmatched_download_cannot_become_reviewed_source(self):
        with tempfile.TemporaryDirectory() as tmp,patch('xargument_intents.urllib.request.urlopen',return_value=BytesIO(b'wrong file')):
            with self.assertRaises(ValueError):
                load_source({'url':'https://github.com/a/b/blob/'+'a'*40+'/f.f90','sha256':'b'*64},Path(tmp),True)

    def test_reports_classify_new_interfaces_and_exclude_command_usage(self):
        p={'id':'github:example/test','local':{'classifications':[{'code':'N3','revision':'a'*40,'procedures':[
            {'procedure':'solve','role':'public-entry-point','signature':'CALL solve(X)','path':'s.f90','line_start':1},
            {'procedure':'main','role':'program-entry-point','signature':'calculator expression','path':'main.f90','line_start':1}]}]}}
        rows=records([p])
        self.assertEqual([r['status'] for r in rows],['unreviewed','not-applicable'])
        with tempfile.TemporaryDirectory() as tmp:
            summary=write_reports(rows,tmp)
            self.assertEqual(summary['status_counts']['unreviewed'],1)
            saved=json.loads((Path(tmp)/'argument-intent-review.json').read_text(encoding='utf-8'))
            self.assertEqual(len(saved['records']),2)
            self.assertIn('solve',(Path(tmp)/'argument-intent-review.md').read_text(encoding='utf-8'))
