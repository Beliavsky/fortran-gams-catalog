"""Review all usage signatures against pinned declarations; annotate explicit INTENT only."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import hashlib
import json
from pathlib import Path
import urllib.request

from catalog import ROOT, assemble, read, validate_local
from intent_sources import inspect, scopes
from intent_coverage import write_reports

CALLABLE_ROLES={'public-entry-point','public-adapter','implementation-helper'}


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def load_source(evidence,cache,fetch):
    target=cache/(evidence['sha256']+'.txt')
    if target.exists():
        text=target.read_text(encoding='utf-8')
        if digest(text)!=evidence['sha256']:raise ValueError('Cached source hash mismatch')
        return text
    if not fetch:raise ValueError('Pinned source not cached; use --fetch')
    url=evidence['url'].replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/')
    raw=urllib.request.urlopen(url,timeout=30).read()
    for encoding in dict.fromkeys([evidence.get('source_encoding','utf-8'),'utf-8-sig','cp1252','latin-1']):
        try:text=raw.decode(encoding).replace('\r\n','\n').replace('\r','\n')
        except UnicodeError:continue
        for candidate in (text,text.rstrip('\n'),text.rstrip('\n')+'\n'):
            if digest(candidate)==evidence['sha256']:
                target.write_text(candidate,encoding='utf-8');return candidate
    raise ValueError('Downloaded text does not match pinned source hash')


def review(local,cache,fetch=False,review_date=None):
    cache.mkdir(parents=True,exist_ok=True)
    overrides=read(ROOT/'data/argument-intent-overrides.json')['records']
    override_key=lambda project,claim,proc:(project['id'],claim['revision'],proc['procedure'],proc['path'],proc['line_start'])
    overrides_by_key={(r['project'],r['revision'],r['procedure'],r['path'],r['line_start']):r for r in overrides}
    known={override_key(p,c,f) for p in local['projects'] for c in p['local'].get('classifications',[])
           for f in c.get('procedures',[])}
    if not set(overrides_by_key)<=known:raise ValueError('An intent override no longer matches the pinned catalog')
    requests={}
    for project in local['projects']:
        for claim in project['local'].get('classifications',[]):
            needed={path for proc in claim.get('procedures',[]) if proc.get('signature') and proc.get('role') in CALLABLE_ROLES
                    for path in [proc['path'],*[d['path'] for d in proc.get('declarations',[])]]}
            for e in claim['evidence']:
                if e['path'] in needed:requests[e['url']]=e

    def retrieve(item):
        url,e=item
        try:return url,scopes(load_source(e,cache,fetch),e['path']),None
        except (OSError,UnicodeError,ValueError) as err:return url,[],str(err)
    with ThreadPoolExecutor(max_workers=8) as pool:
        loaded={url:(items,error) for url,items,error in pool.map(retrieve,requests.items())}
    records=[]
    for project in local['projects']:
        for claim in project['local'].get('classifications',[]):
            documents={e['path']:loaded[e['url']][0] for e in claim['evidence'] if e['url'] in loaded}
            for proc in claim.get('procedures',[]):
                if not proc.get('signature'):continue
                row={'project':project['id'],'procedure':proc['procedure'],'path':proc['path'],
                     'line_start':proc['line_start'],'signature':proc['signature'],'revision':claim['revision'],'gams_code':claim['code']}
                if proc.get('role') not in CALLABLE_ROLES:
                    records.append({**row,'status':'not-applicable','issues':['Command usage, data or template syntax, not a Fortran procedure call.']});continue
                override=overrides_by_key.get(override_key(project,claim,proc),{})
                if override.get('not_applicable'):
                    result={'status':'not-applicable','issues':[], 'notes':override['reason'],
                            'sources':[{'path':proc['path'],'procedure':proc['procedure'],
                                        'line_start':proc['line_start'],'line_end':proc['line_end']}]}
                    proc.pop('arguments',None)
                    proc['argument_intent_review']={'reviewed_on':review_date or date.today().isoformat(),**result}
                    records.append({**row,**result,'argument_count':0});continue
                annotations,result=inspect(proc,documents)
                for annotation in override.get('arguments',[]):
                    annotations=[a for a in annotations if a['name'].casefold()!=annotation['name'].casefold()]+[annotation]
                    result['issues']=[issue for issue in result['issues'] if not issue.endswith(' for '+annotation['name'])]
                    result['notes']=override['reason']
                    result['status']='partial' if result['issues'] else 'checked'
                for path in {proc['path'],*[d['path'] for d in proc.get('declarations',[])]}:
                    ev=next((e for e in claim['evidence'] if e['path']==path),None)
                    if ev and ev['url'] in loaded and loaded[ev['url']][1]:
                        result['issues'].append(path+': '+loaded[ev['url']][1]);result['status']='partial'
                # Retain any earlier manually reviewed annotation rather than
                # discarding it when the conservative parser cannot resolve it.
                keys={(a.get('call_index',0),a['name'].casefold()):a for a in annotations}
                for old in proc.get('arguments',[]):
                    key=(old.get('call_index',0),old['name'].casefold())
                    if key in keys and keys[key]['intent']!=old['intent']:
                        result['issues'].append('Conflicts with prior annotation: '+old['name']);result['status']='partial'
                        keys[key]=old
                    else:keys.setdefault(key,old)
                annotations=list(keys.values())
                for a in annotations:
                    if not any(d['path']==a['path'] and d['line_start']<=a['line_start']<=a['line_end']<=d['line_end'] for d in proc['declarations']):
                        proc['declarations'].append({k:a[k] for k in ('path','line_start','line_end')})
                if annotations:proc['arguments']=annotations
                proc['argument_intent_review']={'reviewed_on':review_date or date.today().isoformat(),**result}
                claim['reviewed_on']=review_date or date.today().isoformat()
                records.append({**row,**result,'argument_count':len(annotations)})
    return records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch',action='store_true',help='Download missing pinned sources and verify their hashes')
    parser.add_argument('--write',action='store_true',help='Update local metadata after producing the review')
    parser.add_argument('--cache',type=Path,default=ROOT/'.bootstrap/argument-intents')
    parser.add_argument('--output',type=Path,default=ROOT/'_site')
    args=parser.parse_args()
    local=read(ROOT/'data/local.json')
    records=review(local,args.cache,args.fetch)
    tree,_,_=assemble()
    validate_local(local,tree)
    print(json.dumps(write_reports(records,args.output),indent=2))
    if args.write:
        (ROOT/'data/local.json').write_text(json.dumps(local,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        print('Updated data/local.json; run python xreviews.py to refresh the ledger.')


if __name__=='__main__':main()
