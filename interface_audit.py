"""Offline coverage audit of explicitly recorded public calling interfaces."""
from collections import Counter
import json
from pathlib import Path
from urllib.parse import quote

from catalog import procedure_label

STATUSES = {
    'missing-callable-sequences': 'Public callable interfaces without a complete usage line',
    'partial-callable-sequences': 'Some public callable interfaces still need usage lines',
    'no-public-interface-reviewed': 'Public interface not yet identified',
    'adapter-only': 'Adapter usage only; upstream callable interface not recorded',
    'program-entry-points': 'Program entry points recorded; review library applicability',
    'noncallable-interface': 'Data or templates recorded; review callable applicability',
    'callable-covered': 'Recorded public callable interfaces have usage lines',
}


def audit(projects):
    """Do not mistake a driver, private helper, CLI or USE line for an API call.

    Coverage is limited to interfaces already identified in the metadata. It
    cannot establish that every procedure in an upstream repository is covered.
    """
    rows = []
    for project in sorted(projects, key=lambda p: (p['name'].casefold(), p['id'])):
        interfaces = {}
        for proc in project.get('procedures', []):
            # A procedure may be attached to several classifications. Preserve
            # distinct overloads/ranges, but count an identical record once.
            key = tuple(proc.get(k) for k in ('role', 'module', 'derived_type',
                'procedure', 'path', 'line_start', 'line_end', 'signature', 'origin'))
            interfaces.setdefault(key, proc)
        procedures = list(interfaces.values())
        public = [p for p in procedures if p.get('role') == 'public-entry-point']

        def has_signature(p):
            return bool(str(p.get('signature') or '').strip())

        def linked(p):
            return has_signature(p) and bool(p.get('declarations'))

        missing = []
        for p in public:
            if not linked(p):
                missing.append({'procedure': procedure_label(p), 'path': p.get('path', ''),
                    'reason': 'No calling sequence' if not has_signature(p) else 'No argument-declaration link'})
        calls = sum(linked(p) for p in public)
        programs = [p for p in procedures if p.get('role') == 'program-entry-point']
        noncallable = [p for p in procedures if p.get('role') in {'public-data', 'public-template'}]
        adapters = [p for p in procedures if p.get('role') == 'public-adapter']
        if public:
            status = ('partial-callable-sequences' if missing else 'callable-covered') if calls else 'missing-callable-sequences'
        elif adapters:
            status = 'adapter-only'
        elif programs:
            status = 'program-entry-points'
        elif noncallable:
            status = 'noncallable-interface'
        else:
            status = 'no-public-interface-reviewed'
        rows.append({
            'id': project['id'], 'name': project['name'],
            'repository_url': project['repository']['url'],
            'catalog_path': 'projects/'+quote(project['id'][7:], safe='/')+'/',
            'status': status, 'gams_codes': project.get('codes', []),
            'public_callable_count': len(public), 'calling_sequence_count': calls,
            'missing_calling_sequences': missing,
            'program_count': len(programs), 'command_sequence_count': sum(has_signature(p) for p in programs),
            'noncallable_interface_count': len(noncallable),
            'adapter_count': len(adapters), 'adapter_sequence_count': sum(linked(p) for p in adapters),
            'other_procedure_count': len(procedures)-len(public)-len(programs)-len(noncallable)-len(adapters),
            'hosted_driver_count': len(project.get('drivers', [])),
            'review_levels': sorted({c['level'] for c in project.get('local', {}).get('classifications', [])}),
        })
    counts = Counter(row['status'] for row in rows)
    return {'schema_version': 1, 'project_count': len(rows),
        'scope': 'Recorded public callable signatures with argument-declaration links. No source scanning or compilation. Coverage does not establish that all upstream procedures or GAMS classes have interfaces.',
        'status_counts': {status: counts[status] for status in STATUSES}, 'projects': rows}


def detail(row):
    if row['missing_calling_sequences']:
        return '; '.join(p['procedure']+': '+p['reason'] for p in row['missing_calling_sequences'])
    if row['status'] == 'no-public-interface-reviewed':
        return ('Named procedure evidence exists, but public API roles/usage are not established.'
                if row['other_procedure_count'] else 'No reviewed public interface records.')
    if row['status'] == 'adapter-only':
        return 'Adapter signatures: '+str(row['adapter_sequence_count'])+'. These do not document the upstream API.'
    if row['status'] == 'program-entry-points':
        return f"Program records: {row['program_count']}; command usage lines: {row['command_sequence_count']}. A standalone program is not a callable library API."
    if row['status'] == 'noncallable-interface':
        return 'Data/template records: '+str(row['noncallable_interface_count'])+'. USE or instantiation syntax is not a procedure call.'
    return 'Calling sequences: '+str(row['calling_sequence_count'])+'. Coverage is limited to recorded public interfaces.'


def markdown(report):
    lines = ['# Calling-sequence coverage audit', '', report['scope'], '',
        'Generated from the same saved metadata as the site. Missing documentation does not mean a repository lacks a usable API. '
        'A hosted driver or calling sketch alone is not a source-linked calling sequence. '
        'Program/data/template cases are review queues, not automatic defects or blanket exemptions.', '',
        f"Repositories audited: **{report['project_count']}**.", '', '| Status | Repositories |', '| --- | ---: |']
    lines.extend(f'| {label} | {report["status_counts"][status]} |' for status, label in STATUSES.items())
    for status, label in STATUSES.items():
        if status == 'callable-covered':
            continue
        lines += ['', '## '+label, '', '| Repository | GAMS | Review finding |', '| --- | --- | --- |']
        rows = [row for row in report['projects'] if row['status'] == status]
        for row in rows:
            escape = lambda s: s.replace('|', '&#124;').replace('\n', ' ')
            lines.append(f'| [{escape(row["id"][7:])}]({row["repository_url"]}) | '
                         +', '.join(row['gams_codes'])+' | '+escape(detail(row))+' |')
        if not rows:
            lines.append('| — | — | None recorded. |')
    return '\n'.join(lines)+'\n'


def write_report(destination, report):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    (destination/'calling-sequence-audit.json').write_text(
        json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    (destination/'calling-sequence-audit.md').write_text(markdown(report), encoding='utf-8')
