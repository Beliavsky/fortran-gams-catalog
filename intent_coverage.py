"""Publish intent-review coverage from saved metadata, without source access."""
import json
from pathlib import Path

CALLABLE_ROLES={'public-entry-point','public-adapter','implementation-helper'}


def records(projects):
    result=[]
    for project in projects:
        for claim in project['local'].get('classifications',[]):
            for proc in claim.get('procedures',[]):
                if not proc.get('signature'):continue
                row={'project':project['id'],'procedure':proc['procedure'],'path':proc['path'],
                     'line_start':proc['line_start'],'signature':proc['signature'],'revision':claim['revision'],
                     'gams_code':claim['code'],'argument_count':len(proc.get('arguments',[]))}
                review=proc.get('argument_intent_review')
                if proc.get('role') not in CALLABLE_ROLES:
                    row.update(status='not-applicable',issues=[],notes='Command usage, data or template syntax, not a Fortran procedure call.')
                elif review:row.update(review)
                else:row.update(status='unreviewed',issues=['Pinned declaration intent review not yet recorded.'])
                result.append(row)
    return result


def write_reports(rows,output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    rows=sorted(rows,key=lambda r:(r['project'],r['path'],r['line_start'],r['procedure'],r.get('gams_code','')))
    counts={status:sum(r['status']==status for r in rows) for status in ('checked','partial','unreviewed','not-applicable')}
    summary={'usage_record_count':len(rows),'status_counts':counts,
             'annotated_argument_count':sum(r.get('argument_count',0) for r in rows),
             'annotated_usage_count':sum(bool(r.get('argument_count')) for r in rows),
             'annotated_project_count':len({r['project'] for r in rows if r.get('argument_count')}),
             'records':rows}
    (output/'argument-intent-review.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    lines=['# Argument-intent review coverage','','Explicit INTENT only; unspecified intent is never inferred. A checked record can legitimately have no explicit intents. Counts refer to metadata usage records, which can repeat an interface under different GAMS classes, not unique upstream routines. This audits recorded signatures, not every upstream procedure.','']
    lines += [f'- {status}: {count}' for status,count in counts.items()]
    lines += [f'- annotated usage records: {summary["annotated_usage_count"]}',f'- argument annotations: {summary["annotated_argument_count"]}',
              f'- projects with annotations: {summary["annotated_project_count"]}','','## Cases needing review','','| Repository | Procedure | Reason |','| --- | --- | --- |']
    pending=[r for r in rows if r['status'] in {'partial','unreviewed'}]
    for r in pending:
        lines.append('| '+r['project'][7:]+' | '+r['procedure']+' | '+'; '.join(r['issues']).replace('|','&#124;')+' |')
    if not pending:lines.append('| — | — | No recorded usage remains unreviewed. |')
    special=[r for r in rows if r.get('notes') and r.get('sources')]
    lines += ['','## Special cases','']
    for r in special:lines.append('- `'+r['project'][7:]+'` / `'+r['procedure']+'`: '+r['notes'])
    (output/'argument-intent-review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return {key:value for key,value in summary.items() if key!='records'}
