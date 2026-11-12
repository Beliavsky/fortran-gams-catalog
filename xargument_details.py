"""Backfill source declarations/comments from hash-verified pinned evidence."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from catalog import ROOT, assemble, read, validate_local
from intent_sources import inspect, scopes
from xargument_intents import load_source


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch',action='store_true')
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    local=read(ROOT/'data/local.json');requests={}
    for p in local['projects']:
        for c in p['local']['classifications']:
            paths={s['path'] for q in c.get('procedures',[]) if q.get('signature') and q.get('argument_intent_review',{}).get('status')=='checked'
                   for s in [q,*q.get('declarations',[])]}
            for e in c['evidence']:
                if e['path'] in paths:requests[(e['sha256'],e['path'])]=e
    def load(item):
        key,e=item
        try:return key,scopes(load_source(e,ROOT/'.bootstrap/argument-intents',args.fetch),e['path']),None
        except (OSError,ValueError,UnicodeError) as error:return key,[],str(error)
    with ThreadPoolExecutor(max_workers=8) as pool:loaded={key:(items,error) for key,items,error in pool.map(load,requests.items())}
    count=comments=usages=0;projects=set();missing=[]
    for p in local['projects']:
        for c in p['local']['classifications']:
            documents={e['path']:loaded[(e['sha256'],e['path'])][0] for e in c['evidence'] if (e['sha256'],e['path']) in loaded}
            for q in c.get('procedures',[]):
                if not q.get('signature') or q.get('argument_intent_review',{}).get('status')!='checked':continue
                details=[];inspect(q,documents,details)
                if details:
                    q['argument_details']=details;count+=len(details);usages+=1;projects.add(p['id'])
                    comments+=sum(bool(d.get('comments')) for a in details for d in a['declarations'])
                elif q.get('arguments'):missing.append({'project':p['id'],'procedure':q['procedure']})
    validate_local(local,assemble()[0])
    report=dict(argument_details=count,usage_records=usages,projects=len(projects),declarations_with_comments=comments,
                missing=missing,source_errors=[{'source':key[1],'error':err} for key,(_,err) in loaded.items() if err])
    (ROOT/'.bootstrap/argument-details-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report,indent=2))
    if args.write:(ROOT/'data/local.json').write_text(json.dumps(local,indent=2,ensure_ascii=False)+'\n',encoding='utf8')


if __name__=='__main__':main()
