"""Build the independent static catalog without network or compilation."""
import argparse
from html import escape
import json
from licenses import license_group, license_reviewed, LICENSE_GROUPS
from legacy_gams import load as load_legacy, listing_records
from pathlib import Path
import shutil
from urllib.parse import quote, urlencode
from review_export import publish_review_feed
from argument_intents import signature_markup, argument_details_markup, optional_notation_markup
from intent_coverage import records as intent_records, write_reports as write_intent_reports
from interface_audit import STATUSES as INTERFACE_STATUSES, audit as audit_interfaces, detail as audit_detail, write_report
from topics import (DIFFERENTIATION_TOPICS, EXPRESSION_TOPICS, DISCOVERY_TOPICS,
                    differentiation_topics, expression_topics, discovery_topics)

from catalog import ROOT, assemble, belongs, lineage, matching_drivers, procedure_label, PROCEDURE_ROLES

TITLE = 'Fortran software by GAMS classification'


def e(value):
    return escape(str(value), quote=True)


def link(url, text):
    return f'<a href="{e(url)}">{e(text)}</a>'


def project_path(project):
    if project.get('legacy_gams'):
        return 'legacy/'+project['id'].split(':', 1)[1]+'/'
    return 'projects/' + quote(project['id'][7:], safe='/') + '/'


def specific_codes(tree, codes):
    return [c for c in codes if not any(c != other and belongs(tree, other, c) for other in codes)]


def supports_fpm(project):
    return any(system.casefold() == 'fpm' for system in project.get('build_systems', []))


def source_codes(project):
    """Only explicitly source-reviewed claims, including imported procedure reviews."""
    return sorted({c['code'] for c in project['local'].get('classifications', [])
                   if c['level'] == 'source-reviewed'} |
                  {c for p in project['procedures'] if p.get('review_level') == 'source-reviewed'
                   for c in p['gams_codes']})


def license_counts(members, reviewed_ids):
    counts = {}
    for member in members:
        for reviewed_only in (False, True):
            if reviewed_only and not license_reviewed(member):
                continue
            for source_only in (False, True):
                if source_only and member['id'] not in reviewed_ids:
                    continue
                for exclude_fpm in (False, True):
                    if exclude_fpm and supports_fpm(member):
                        continue
                    for group in ('', license_group(member)):
                        key = '|'.join((group, str(int(reviewed_only)), str(int(source_only)), str(int(exclude_fpm))))
                        counts[key] = counts.get(key, 0) + 1
    return counts


def license_html(project, detailed=False):
    data = project.get('license') or {}
    label = data.get('spdx_expression') or data.get('label')
    if not label:
        return '<p>License: License not yet reviewed.</p>'
    reviewed = bool(project['local'].get('license'))
    if label.upper() in ('NOASSERTION', 'NONE', 'UNKNOWN'):
        label = 'No license identified'
    evidence = data.get('evidence', []) if reviewed else []
    result = '<p>License: '+(link(evidence[0]['url'], label) if evidence else e(label))
    if not reviewed:
        result += ' <span class="muted">(imported metadata)</span>'
    result += '</p>'
    if detailed and reviewed:
        result += '<p>'+e(data['notes'])+'</p><p>License reviewed '+e(data['reviewed_on'])+' at '+e(data['revision'])+'</p><ul>'
        result += ''.join('<li>'+link(v['url'],v['path'])+' · SHA-256 <code>'+e(v['sha256'])+'</code></li>' for v in evidence)+'</ul>'
    elif detailed:
        result += '<p>The license label comes from the saved playground snapshot; its license files have not been independently reviewed here.</p>'
    return result


def build(destination, root=ROOT):
    destination, root = Path(destination), Path(root)
    tree, projects, merged = assemble(root)
    legacy = load_legacy(root, tree, {p['id'] for p in projects})
    legacy_entries = listing_records(legacy)
    all_entries = projects + legacy_entries
    reviewed_codes = {p['id']: source_codes(p) for p in all_entries}
    destination.mkdir(parents=True, exist_ok=True)
    for asset in ('catalog.css', 'search.js', 'formatting.js'):
        shutil.copy2(root/'assets'/asset, destination/asset)
    copied = set()
    for project in projects:
        for claim in project['local'].get('classifications', []):
            for procedure in claim.get('procedures', []):
                driver = procedure.get('local_driver')
                if driver:
                    for field in ('path', 'runner', 'report', 'readme'):
                        artifact = driver[field]
                        if artifact not in copied:
                            target = destination/artifact
                            target.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(root/artifact, target)
                            copied.add(artifact)
    (destination/'.nojekyll').touch()
    publish_review_feed(destination, projects)
    interface_report = audit_interfaces(projects)
    write_report(destination, interface_report)
    intent_rows=intent_records(projects)
    intent_summary=write_intent_reports(intent_rows,destination)
    (destination/'catalog.json').write_text(json.dumps(merged, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    (destination/'taxonomy.json').write_text(json.dumps(tree, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    (destination/'legacy-gams.json').write_text(json.dumps(legacy, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    shutil.copy2(root/'docs/review-policy.md', destination/'review-policy.md')
    shutil.copy2(root/'docs/local-reviews.md', destination/'local-reviews.md')

    def page(path, title, body):
        prefix = '../' * len(Path(path).parts)
        target = destination/path/'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Browse Fortran numerical software by mathematical problem, with pinned review evidence and driver references.">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'">
<title>{e(title)}</title><link rel="stylesheet" href="{prefix}catalog.css"><script defer src="{prefix}formatting.js"></script><script defer src="{prefix}search.js"></script></head>
<body><a class="skip" href="#content">Skip to content</a><header>{link(prefix or './', 'Fortran software catalog')}
<nav>{link(prefix+'projects/', 'Repositories')} · {link(prefix+'review/', 'Review policy')} ·
{link(prefix+'topics/automatic-differentiation/', 'Automatic differentiation')} ·
{link(prefix+'topics/expression-parsers/', 'Expression parsers')} ·
{link('https://beliavsky.github.io/fortran-playground/gams/', 'Playground package catalog')} ·
{link('https://gams.nist.gov/cgi-bin/serve.cgi', 'About GAMS')}</nav>
<div class="formatting-controls"><label class="checkbox-label"><input type="checkbox" id="original-formatting" aria-describedby="formatting-help"> Original formatting</label>
<span class="muted" id="formatting-help">Default: lowercase code and one space after commas. Display only; comments, strings and examples keep their original text.</span></div>
<noscript>Display formatting requires JavaScript; original text is shown.</noscript>
<details id="filters" class="filters-panel"><summary>Filters</summary>
<div class="build-filter"><label class="checkbox-label">Collection <select id="collection" name="collection"><option value="">All repositories</option><option value="independent">Independent reviews</option><option value="imported">Playground imports</option></select></label></div>
<div class="build-filter"><label class="checkbox-label"><input type="checkbox" id="exclude-fpm" aria-describedby="fpm-filter-help"> Exclude known FPM packages</label>
<span class="muted" id="fpm-filter-help">Repositories with unreviewed build support remain included.</span></div>
<div class="build-filter"><label class="checkbox-label"><input type="checkbox" id="source-reviewed" aria-describedby="source-filter-help"> Only source-reviewed mappings</label>
<span class="muted" id="source-filter-help">Evidence in the source supports the classification; compilation and numerical testing are separate.</span></div>
<div class="build-filter"><label class="checkbox-label">License <select id="license" aria-describedby="license-filter-help">
<option value="">All licenses</option>{''.join('<option value="'+key+'">'+e(label)+'</option>' for key, label in LICENSE_GROUPS.items())}</select></label>
<label class="checkbox-label"><input type="checkbox" id="license-reviewed"> Reviewed license evidence only</label>
<span class="muted" id="license-filter-help">Recorded terms, not a guarantee of compatibility. Check component and dependency notices.</span></div>
<div class="build-filter topic-filter"><label class="checkbox-label">Topic <select id="topic" aria-describedby="topic-filter-help">
<option value="">All software</option><optgroup label="Automatic differentiation">{''.join('<option value="'+key+'">'+e(label)+'</option>' for key, label in DIFFERENTIATION_TOPICS.items())}</optgroup><optgroup label="Expression parsers">{''.join('<option value="'+key+'">'+e(label)+'</option>' for key, label in EXPRESSION_TOPICS.items())}</optgroup></select></label>
<span class="muted" id="topic-filter-help">Curated capabilities, not execution checks. Source-reviewed filtering applies to GAMS mappings.</span></div>
<div class="build-filter"><label class="checkbox-label"><input type="checkbox" id="highlight-intents" aria-describedby="argument-intent-help"> Highlight output arguments</label>
<span class="muted" id="argument-intent-help">Recorded intent only: <em>out</em> is italic; <strong><em>inout</em></strong> is bold italic. Input, unspecified and conditional intents stay unmarked; hover or focus for details.</span></div>
<div class="build-filter"><label class="checkbox-label"><input type="checkbox" id="legacy-gams" aria-describedby="legacy-filter-help"> Include original GAMS/Netlib entries</label>
<span class="muted" id="legacy-filter-help">Source-available pilot; imported classifications, not independent source reviews. {link(prefix+'legacy/', 'About these entries')}</span></div></details></header>
<main id="content">{body}</main><footer>{link(prefix+'catalog.json','Download layered metadata')} ·
{link(prefix+'taxonomy.json','GAMS taxonomy')} · {link(prefix+'calling-sequences/', 'Calling-sequence audit')} · {link(prefix+'argument-intents/', 'Argument-intent coverage')}<p>Classification describes documented functionality. A checked driver verifies only its recorded problem and configuration.</p></footer></body></html>
''', encoding='utf-8')

    def status(project, code=None):
        drivers = matching_drivers(tree, project, code)
        procedures = [p for p in project['procedures']
                      if any(belongs(tree, c, code) for c in p['gams_codes'])]
        local = [c for c in project['local'].get('classifications', []) if belongs(tree, c['code'], code)]
        labels = []
        if drivers:
            labels.append(f'{len(drivers)} checked hosted driver(s)')
        if procedures:
            labels.append('Source-reviewed procedure evidence')
        if local:
            labels.extend(sorted(set(c['level'].replace('-', ' ') for c in local)))
        if not labels:
            labels.append('Imported classification; no matching checked driver')
        return ' · '.join(labels)

    def listing(items, prefix, code=None):
        controls = '''<form class="search" role="search"><label>Find software <input id="query" name="q" type="search" placeholder="Name, author, topic or procedure"></label>
<button type="submit">Search</button></form>
<p id="matches" aria-live="polite"></p><noscript>Repository entries are listed below. Use your browser’s Find command to search. Optional GAMS/Netlib listings require JavaScript.</noscript>'''
        cards = []
        for p in items:
            if p.get('legacy_gams'):
                search = ' '.join([p['procedure'], p['library'], p['description'], *p['codes'], *(tree[c]['label'] for c in p['codes'])])
                cards.append(f'''<article hidden data-legacy="true" data-search="{e(search.lower())}" data-source-search="" data-source-match="false" data-license="unclear" data-license-reviewed="false" data-collection="legacy" data-fpm="false">
<h2>{link(prefix+project_path(p), p['procedure']+' — '+p['library'])}</h2>
<p>{e(p['description'])}</p><p class="status">Imported GAMS/Netlib classification; not independently reviewed or compiled.</p>
<p>{link(p['source_url'], 'Fortran source')} · {e(p['precision'])} precision · License not yet reviewed</p>
<p>{' · '.join(link(prefix+'classes/'+c+'/', c) for c in p['codes'])}</p>
<p>{link(prefix+project_path(p), 'Provenance, source checksum and related modernizations')}</p></article>''')
                continue
            repo = p['repository']
            ad_topics = differentiation_topics(p)
            method_labels = [DIFFERENTIATION_TOPICS[t] for t in ad_topics if t != 'automatic-differentiation']
            ad_description = ('<p class="muted">AD capabilities: '+e(' · '.join(method_labels) or 'Automatic differentiation')+'</p>') if ad_topics else ''
            parser_topics = expression_topics(p)
            parser_labels = [EXPRESSION_TOPICS[t] for t in parser_topics if t != 'expression-parser']
            parser_description = ('<p class="muted">Parser capabilities: '+e(' · '.join(parser_labels))+'</p>') if parser_topics else ''
            codes = p['codes']
            search = ' '.join([p['name'], p['description'], repo['owner'], p['owner_label'],
                               *p['topics'], *codes, *(tree[c]['label'] for c in codes),
                               *(procedure_label(proc)+' '+proc['path'] if proc.get('origin') == 'local'
                                 else procedure_label(proc) for proc in p['procedures'])])
            collection = 'imported' if p.get('playground') else 'independent'
            leaves = specific_codes(tree, codes)
            labels = ' · '.join(link(prefix+'classes/'+c+'/', c) for c in leaves[:8])
            if len(leaves) > 8:
                labels += ' · '+link(prefix+project_path(p), f'{len(leaves)-8} more classes')
            drivers = ''.join('<li>'+link(d['url'], d['gams_code']+' — '+d['name'])+'</li>'
                              for d in matching_drivers(tree, p, code))
            driver_links = '<details><summary>Checked drivers for this scope</summary><ul>'+drivers+'</ul></details>' if drivers else ''
            reviewed = reviewed_codes[p['id']]
            source_match = any(belongs(tree, c, code) for c in reviewed)
            source_search = ' '.join([p['name'], p['description'], repo['owner'], p['owner_label'],
                                      *p['topics'], *reviewed, *(tree[c]['label'] for c in reviewed),
                                      *(procedure_label(proc)+' '+proc.get('path', '') for proc in p['procedures']
                                        if proc.get('origin') == 'local' or proc.get('review_level') == 'source-reviewed')])
            reviewed_leaves = specific_codes(tree, reviewed)
            source_labels = ' · '.join(link(prefix+'classes/'+c+'/', c)
                                        for c in reviewed_leaves[:8])
            if len(reviewed_leaves) > 8:
                source_labels += ' · '+link(prefix+project_path(p), f'{len(reviewed_leaves)-8} more reviewed classes')
            entries = {}
            for claim in p['local'].get('classifications', []):
                if claim['level'] != 'source-reviewed' or not belongs(tree, claim['code'], code):
                    continue
                for proc in claim.get('procedures', []):
                    if proc.get('role') in ('public-entry-point', 'program-entry-point', 'public-data', 'public-template', 'public-adapter'):
                        entries.setdefault((procedure_label(proc), proc['path']), (claim, proc))
            entry_html = ''
            for claim, proc in list(entries.values())[:3]:
                evidence = next(v for v in claim['evidence'] if v['path'] == proc['path'])
                source_url = evidence['url']+f'#L{proc["line_start"]}-L{proc["line_end"]}'
                entry_html += '<li><code>'+e(procedure_label(proc))+'</code> — '+link(
                    source_url, proc['path']+':'+str(proc['line_start']))+' ('+e(PROCEDURE_ROLES[proc['role']].lower())+')'
                if proc.get('signature'):
                    declaration = proc['declarations'][0]
                    source = next(v for v in claim['evidence'] if v['path'] == declaration['path'])
                    url = source['url']+f'#L{declaration["line_start"]}-L{declaration["line_end"]}'
                    label = 'Usage (source declarations)' if proc.get('role') in {'public-data', 'public-template'} else 'Usage (argument declarations)'
                    entry_html += '<p>'+label+':</p><pre><code class="calling-sequence"><a href="'+e(url)+'">'+signature_markup(proc)+'</a></code></pre>'+optional_notation_markup(proc)
                entry_html += '</li>'
            if entries:
                entry_label = 'Reviewed public interfaces:' if any(v[1].get('role') in {'public-data', 'public-template', 'public-adapter'} for v in entries.values()) else 'Reviewed entry points:'
                entry_html = '<div class="entry-points"><p>'+entry_label+'</p><ul>'+entry_html+'</ul><p>'+link(
                    prefix+project_path(p), 'Usage and full procedure evidence')+'</p></div>'
            cards.append(f'''<article data-search="{e(search.lower())}" data-topics="{e(' '.join(discovery_topics(p)))}" data-source-search="{e(source_search.lower())}" data-source-match="{str(source_match).lower()}" data-license="{license_group(p)}" data-license-reviewed="{str(license_reviewed(p)).lower()}" data-collection="{collection}" data-fpm="{str(supports_fpm(p)).lower()}">
<h2>{link(prefix+project_path(p),p['name'])}</h2><p class="muted">{link(repo['url'],repo['owner']+'/'+repo['name'])} · {e(p['owner_label'])}</p>
<p>{e(p['description'])}</p>{ad_description}{parser_description}{license_html(p)}<div data-all-mappings><p class="status">{e(status(p,code))}</p><p>{labels}</p>{driver_links}</div>
<div data-source-mappings hidden><p class="status">Source-reviewed mapping evidence</p><p>{source_labels}</p></div>{entry_html}</article>''')
        return controls+''.join(cards)

    def class_links(parent, prefix):
        codes = [c for c in tree if tree[c]['parent'] == parent]
        rows = []
        for c in codes:
            members = [p for p in projects if any(belongs(tree, k, c) for k in p['codes'])]
            without_fpm = sum(not supports_fpm(p) for p in members)
            reviewed = [p for p in members if any(belongs(tree, k, c) for k in reviewed_codes[p['id']])]
            counts = license_counts(members, {p['id'] for p in reviewed})
            topic_counts = {topic: license_counts(
                [p for p in members if topic in discovery_topics(p)],
                {p['id'] for p in reviewed}) for topic in DISCOVERY_TOPICS}
            legacy_count = sum(any(belongs(tree, k, c) for k in p['codes']) for p in legacy_entries)
            rows.append('<li>'+link(prefix+'classes/'+c+'/',c+' — '+tree[c]['label'])+
                        f' <span class="muted" data-topic-counts="{e(json.dumps(topic_counts))}" data-legacy-count="{legacy_count}" data-license-counts="{e(json.dumps(counts))}" data-class-count="{len(members)}" data-without-fpm="{without_fpm}" data-source-count="{len(reviewed)}" data-source-without-fpm="{sum(not supports_fpm(p) for p in reviewed)}">({len(members)})</span></li>')
        return '<ul class="classes">'+''.join(rows)+'</ul>'

    page('', TITLE, f'<h1>{TITLE}</h1><p class="lede">Find numerical methods and supporting software, including repositories that do not use FPM.</p>'
         f'<p>{len(projects)} repositories: {sum(bool(p.get("playground")) for p in projects)} imported playground packages and '
         f'{sum(not bool(p.get("playground")) for p in projects)} independent repository reviews.</p>'
         '<form class="search" role="search" action="projects/" data-destination="projects/">'
         '<label>Find software <input id="query" name="q" type="search" placeholder="Name, author, topic or procedure"></label>'
         '<button type="submit">Search</button></form>'
         '<p>Browse by problem below, or '+link('projects/', 'search all repositories')+'. '
         'New independent entries begin with pinned documentation reviews. Source mappings and local drivers can be added as they are checked.</p>'
         '<h2>Main GAMS classes</h2>'+class_links(None, ''))
    page('projects', 'Fortran repositories', '<h1>Fortran repositories</h1>'+listing(all_entries, '../'))
    audit_body = '<h1>Calling-sequence coverage audit</h1><p>'+e(interface_report['scope'])+'</p>'
    audit_body += '<p>This report covers all '+str(interface_report['project_count'])+' saved repositories, regardless of discovery filters. '
    audit_body += 'Missing documentation does not mean a repository lacks a usable API. '
    audit_body += 'A driver or calling sketch alone is not a source-linked calling sequence. '
    audit_body += 'Program, data and template entries need separate applicability review.</p>'
    audit_body += '<p>'+link('../calling-sequence-audit.md', 'Download Markdown report')+' · '+link('../calling-sequence-audit.json', 'Download JSON report')+'</p>'
    audit_body += '<ul>'+''.join('<li>'+e(label)+': '+str(interface_report['status_counts'][status])+'</li>'
                               for status, label in INTERFACE_STATUSES.items())+'</ul>'
    for audit_status, label in INTERFACE_STATUSES.items():
        if audit_status == 'callable-covered':
            continue
        rows = [row for row in interface_report['projects'] if row['status'] == audit_status]
        audit_body += '<section><h2>'+e(label)+'</h2>'
        if rows:
            audit_body += '<ul>'
            for row in rows:
                audit_body += '<li>'+link('../'+row['catalog_path'], row['id'][7:])+' — '+e(audit_detail(row))+'</li>'
            audit_body += '</ul>'
        else:
            audit_body += '<p>None recorded.</p>'
        audit_body += '</section>'
    page('calling-sequences', 'Calling-sequence coverage audit', audit_body)
    intent_body='<h1>Argument-intent coverage</h1><p>Every recorded usage line is classified separately from numerical or compilation checks. '
    intent_body+='Only explicit Fortran INTENT is annotated. A checked record may have no explicit intents. Counts refer to metadata usage records, which can repeat an interface under different GAMS classes.</p>'
    intent_body+='<p>Enable <strong>Highlight output arguments</strong> in Filters. Conditional declarations remain unmarked; hover or focus to see the alternatives. '
    intent_body+='The displayed names can differ from the source dummy names; each annotation retains its pinned declaration and call index.</p>'
    intent_body+='<p>'+link('../argument-intent-review.md','Download review summary')+' · '+link('../argument-intent-review.json','Download complete review records')+'</p><ul>'
    intent_body+=''.join('<li>'+e(key)+': '+str(value)+'</li>' for key,value in intent_summary['status_counts'].items())+'</ul>'
    intent_body+='<p>'+str(intent_summary['annotated_argument_count'])+' argument annotations in '+str(intent_summary['annotated_usage_count'])+' usage records across '+str(intent_summary['annotated_project_count'])+' projects.</p>'
    pending=[r for r in intent_rows if r['status'] in {'partial','unreviewed'}]
    intent_body+='<h2>Cases needing review</h2>'
    intent_body+=('<ul>'+''.join('<li>'+link('../projects/'+quote(r['project'][7:],safe='/')+'/',r['project'][7:])+' — '+e(r['procedure']+': '+'; '.join(r['issues']))+'</li>' for r in pending)+'</ul>') if pending else '<p>No recorded usage remains unreviewed.</p>'
    intent_body+='<h2>Special cases</h2><ul>'+''.join('<li>'+e(r['project'][7:]+' / '+r['procedure']+': '+r['notes'])+'</li>' for r in intent_rows if r.get('notes') and r.get('sources'))+'</ul>'
    page('argument-intents','Argument-intent coverage',intent_body)
    ad_projects = [p for p in projects if 'automatic-differentiation' in differentiation_topics(p)]
    page('topics/automatic-differentiation', 'Automatic differentiation in Fortran',
         '<h1>Automatic differentiation in Fortran</h1>'
         '<p>Find derivative libraries, matrix derivative primitives and source-conversion helpers. '
         'Use the Topic selector to compare forward mode, reverse mode, higher derivatives and sparse Jacobians.</p>'
         '<p>Automatic differentiation propagates derivatives through operations on values or a computational graph. '
         'That does not by itself establish symbolic expression manipulation. Numerical differentiation belongs under '
         +link('../../classes/H1/', 'H1 — Numerical differentiation')+'; '
         +link('../../classes/O/', 'O — Symbolic computation')+' remains a separate capability.</p>'
         '<p>Method facets describe recorded capabilities; source-reviewed filtering concerns the GAMS mapping, '
         'not proof that every method or derivative order has been independently checked. '
         'Conversion helpers and application-specific derivatives are not all general-purpose AD engines.</p>'
         '<p>Discovery checklist: '+link('https://beliavsky.github.io/Fortran-code-on-GitHub/#automatic-differentiation',
                                       'Fortran code on GitHub — Automatic differentiation')+'. '
         'The listed m_ad repository link returned 404 when checked on 2026-11-12 and is not added as a verified entry.</p>'
         +listing(ad_projects, '../../'))
    parser_projects = [p for p in projects if expression_topics(p)]
    page('topics/expression-parsers', 'Expression parsers in Fortran',
         '<h1>Expression parsers in Fortran</h1>'
         '<p>Find callable expression evaluators, calculators and embedded mathematical interpreters. '
         'Use the Topic selector to find scalar, array or complex evaluation, user functions, derivatives and code generation.</p>'
         '<p>Capabilities describe pinned author documentation or the narrower source review shown on each project. '
         'A source-reviewed GAMS mapping does not mean every capability or numerical result has been checked. '
         'These implementations have different syntax, precision, state and error-handling contracts.</p>'
         '<p>Parsing and numerical evaluation are recorded under '+link('../../classes/N3/', 'N3 — Character manipulation')+'. '
         'Parsing alone does not establish symbolic algebra under '+link('../../classes/O/', 'O — Symbolic computation')+'. '
         'Derivative functionality is mapped separately when supported by evidence.</p>'
         '<p>Discovery checklist: '+link('https://beliavsky.github.io/Fortran-code-on-GitHub/#expression-parsers',
                                       'Fortran code on GitHub — Expression parsers')+'. '
         'FortFront is a compiler frontend; the FORTRAN IV spreadsheet is a historical application. '
         'They are outside this mathematical-parser selection. Related mirrors and descendants are identified in project notes.</p>'
         +listing(parser_projects, '../../'))
    for code, info in tree.items():
        subset = [p for p in all_entries if any(belongs(tree, c, code) for c in p['codes'])]
        crumbs = ' / '.join(link('../../classes/'+c+'/', c) for c in reversed(lineage(tree, code)[1:]))
        intro = '<nav aria-label="Breadcrumb">'+link('../../','All classes')+' / '+crumbs+'</nav>'
        intro += '<h1>'+e(code+' — '+info['label'])+'</h1><p>Includes explicitly mapped descendants. Driver links below match this class or a narrower problem.</p>'
        intro += '<p>'+link('https://gams.nist.gov/cgi-bin/serve.cgi/Class/'+quote(code, safe=''),
                           'Original GAMS classification at NIST')+'</p>'
        if code in {'O', 'H1'}:
            intro += '<p>Related: '+link('../../topics/automatic-differentiation/', 'Automatic differentiation')+'. '
            intro += ('Derivative propagation alone is not symbolic expression manipulation; AD packages are not automatically mapped to O.'
                      if code == 'O' else 'Browse AD methods separately from finite-difference and complex-step methods. This topic link does not change GAMS classifications.')+'</p>'
        if code in {'N3', 'O'}:
            intro += '<p>Related: '+link('../../topics/expression-parsers/', 'Expression parsers')+'. '
            intro += 'Expression evaluation alone is not evidence of symbolic algebra.</p>'
        page('classes/'+code, code+' — '+info['label'], intro+class_links(code, '../../')+
             (listing(subset, '../../', code) if subset else '<p>No repository is mapped here yet.</p>'))
    page('legacy', 'GAMS/Netlib source-available pilot', '<h1>GAMS/Netlib source-available pilot</h1>'
         '<p>Enable <strong>Include original GAMS/Netlib entries</strong> above to browse these optional records. '
         'This pilot contains nine double-precision QUADPACK entry points. The GAMS codes and descriptions '
         'come from the '+link('https://netlib.org/quadpack/', 'Netlib QUADPACK index')+'. '
         'NIST dynamic pages returned HTTP 403 during setup; no NIST module records were retrieved.</p>'
         '<p>Source links were fetched and checksummed when this snapshot was created. These entries have '
         'not been independently source-reviewed, compiled or numerically checked here. Source availability '
         'does not establish permission to reuse it. No IMSL or NAG references are included.</p>'
         '<p>Existing repository reviews remain separate. Related modernizations may change interfaces, '
         'precision, dependencies and licensing; their existence does not verify the original routine.</p>'
         '<p>'+link('../legacy-gams.json', 'Download the separate import snapshot')+'</p>'+listing(legacy_entries, '../'))
    for item in legacy_entries:
        prefix = '../../../'
        body = '<h1>'+e(item['procedure']+' — '+item['library'])+'</h1><p>'+e(item['description'])+'</p>'
        body += '<p class="status">Imported GAMS/Netlib classification; not independently reviewed or compiled.</p>'
        body += '<p>'+link(item['source_url'], 'Download Fortran source')+' · Double precision · Source available</p>'
        body += '<p>License not yet reviewed. Availability of source is not a reuse grant.</p>'
        body += '<h2>Recorded GAMS classes</h2><ul>'+''.join('<li>'+link(prefix+'classes/'+c+'/', c+' — '+tree[c]['label'])+' · '+link('https://gams.nist.gov/cgi-bin/serve.cgi/Class/'+c, 'Original GAMS class')+'</li>' for c in item['codes'])+'</ul>'
        body += '<h2>Import provenance</h2><p>Classification and description: '+link(item['index_url'], 'Netlib QUADPACK index')+'</p>'
        body += '<p>Retrieved '+e(item['retrieved_at'])+'. Checksums use UTF-8 text normalized to LF line endings.</p>'
        body += '<p>Source SHA-256: <code>'+e(item['source_sha256'])+'</code></p><p>Index SHA-256: <code>'+e(item['index_sha256'])+'</code></p>'
        body += '<p>The original source can change at its URL; this checksum identifies the retrieved version. '
        body += 'A single routine may require additional sources; the download is not a complete standalone program.</p>'
        body += '<h2>Related modernized projects</h2><p>These are related implementations, not identical copies or evidence of source equivalence.</p><ul>'
        body += ''.join('<li>'+link(prefix+'projects/'+ident[7:]+'/', ident[7:])+'</li>' for ident in item.get('related_projects', []))+'</ul>'
        page(project_path(item).rstrip('/'), item['procedure']+' — GAMS/Netlib', body)
    for p in projects:
        prefix = '../../../'
        repo = p['repository']
        body = '<h1>'+e(p['name'])+'</h1><p class="lede">'+e(p['description'])+'</p>'
        body += '<p>'+link(repo['url'], repo['owner']+'/'+repo['name'])+' · '+e(p['origin'])+'</p>'
        body += '<p>Repository owner: '+e(p['owner_label'])+'</p><p>Build systems: '+e(', '.join(p.get('build_systems', [])) or 'Not yet reviewed')+'</p>'
        claims = p['local'].get('classifications', [])
        revision = claims[0]['revision'] if claims else ''
        documentation = 'https://beliavsky.github.io/fortran-playground/documentation/?' + urlencode({'url': repo['url'], 'revision': revision})
        body += '<p>'+link(documentation, 'Generate API documentation with FORD')+' (experimental; upstream source)</p>'
        body += license_html(p, detailed=True)
        body += '<p>Topics: '+e(', '.join(p['topics']))+'</p>'
        if any(proc.get('role') for proc in p['procedures']):
            body += '<p><code>module_name::procedure_name</code> identifies a module procedure in this catalog; '
            body += 'in Fortran, import it with <code>use module_name, only: procedure_name</code> and call the procedure name. '
            body += '<code>module_name::type_name%binding_name</code> identifies a type-bound procedure; its usage line calls the binding on an object. '
            body += 'Entry points and helpers are distinguished only where the interface has been reviewed.</p>'
        body += '<h2>Classifications</h2><ul>'
        specific = specific_codes(tree, p['codes'])
        body += ''.join('<li>'+link(prefix+'classes/'+c+'/', c+' — '+tree[c]['label'])+'</li>' for c in specific[:8])+'</ul>'
        remaining = [c for c in p['codes'] if c not in specific[:8]]
        if remaining:
            body += '<details><summary>All recorded classes, including broader parents</summary><ul>'
            body += ''.join('<li>'+link(prefix+'classes/'+c+'/', c+' — '+tree[c]['label'])+'</li>' for c in p['codes'])+'</ul></details>'
        for claim in p['local'].get('classifications', []):
            body += '<section><h2>'+e(claim['code']+' — '+claim['level'].replace('-', ' '))+'</h2><p>'+e(claim['notes'])+'</p>'
            body += '<p>Reviewed '+e(claim['reviewed_on'])+' at '+link(repo['url']+'/tree/'+claim['revision'], claim['revision'])+'</p><ul>'
            body += ''.join('<li>'+link(v['url'], v['path'])+' · SHA-256 <code>'+e(v['sha256'])+'</code></li>' for v in claim['evidence'])+'</ul>'
            if claim.get('procedures'):
                body += '<h3>Reviewed interfaces and source ranges</h3><ul>'
                for procedure in claim['procedures']:
                    evidence = next(v for v in claim['evidence'] if v['path'] == procedure['path'])
                    start, end = procedure['line_start'], procedure['line_end']
                    role = PROCEDURE_ROLES.get(procedure.get('role'), 'Reviewed procedure; interface role not yet reviewed')
                    body += '<li><strong>'+e(role)+'</strong>: <code>'+e(procedure_label(procedure))+'</code> — '+link(
                        evidence['url']+f'#L{start}-L{end}', procedure['path']+f':{start}–{end}')
                    if procedure.get('summary'):
                        body += '<p>'+e(procedure['summary'])+'</p>'
                    if procedure.get('signature'):
                        declaration = procedure['declarations'][0]
                        source = next(v for v in claim['evidence'] if v['path'] == declaration['path'])
                        url = source['url']+f'#L{declaration["line_start"]}-L{declaration["line_end"]}'
                        label = 'Usage (click for constant declarations)' if procedure.get('role') == 'public-data' else 'Usage (click for template instantiation)' if procedure.get('role') == 'public-template' else 'Usage (click for argument declarations)'
                        body += '<p>'+label+':</p><pre><code class="calling-sequence"><a href="'+e(url)+'">'+signature_markup(procedure)+'</a></code></pre>'+optional_notation_markup(procedure)
                        body += argument_details_markup(procedure, repo['url']+'/blob/'+claim['revision']+'/')
                        for declaration in procedure['declarations']:
                            source = next(v for v in claim['evidence'] if v['path'] == declaration['path'])
                            body += '<p>'+link(source['url']+f'#L{declaration["line_start"]}-L{declaration["line_end"]}',
                                              ('Source declarations: ' if procedure.get('role') in {'public-data', 'public-template'} else 'Argument declarations: ')+declaration['path']+':'+str(declaration['line_start']))+'</p>'
                    if procedure.get('usage'):
                        driver = procedure.get('local_driver')
                        label = 'Locally checked main program' if driver else 'Calling sketch (not a checked driver)'
                        body += '<p>'+label+':</p><pre><code>'+e(procedure['usage'])+'</code></pre>'
                        if driver:
                            body += '<p>'+' ? '.join(link(prefix+driver[field], title) for field, title in (
                                ('path', 'Download main program'), ('report', 'Saved numerical results'),
                                ('readme', 'Build instructions and scope'), ('runner', 'Pinned-source check runner')))+'</p>'
                        body += '<p>'+e(procedure['usage_notes'])+'</p>'
                    for example in procedure.get('examples', []):
                        source = next(v for v in claim['evidence'] if v['path'] == example['path'])
                        body += '<p>'+link(source['url']+f'#L{example["line_start"]}-L{example["line_end"]}',
                                          'Author example: '+example['path']+':'+str(example['line_start']))+' (not run for this catalog).</p>'
                    body += '</li>'
                body += '</ul>'
            body += '</section>'
        if p['local'].get('notes'):
            body += '<p>'+e(p['local']['notes'])+'</p>'
        discovery = p['local'].get('discovery')
        if discovery:
            body += '<p>'+link(discovery['url'],'Discovery source: Fortran code on GitHub (pinned list)')+'</p>'
        if p.get('playground'):
            body += '<h2>Playground review</h2><p>'+link('https://beliavsky.github.io/fortran-playground/gams/packages/'+quote(p['playground']['package_id'],safe='')+'/', 'Full package review, pinned procedures and dependencies')+'</p>'
            body += '<p>The imported snapshot records checked drivers, not a fresh check of live service availability. Its original evidence and source hashes are retained in the downloadable metadata.</p>'
        if p['drivers']:
            body += '<h2>Checked hosted drivers</h2><ul>'+''.join('<li>'+link(d['url'],d['gams_code']+' — '+d['name'])+'</li>' for d in p['drivers'])+'</ul>'
        page(project_path(p).rstrip('/'), p['name']+' — Fortran software', body)
    page('review', 'Review policy', '<h1>Review policy</h1><p>Claims have separate evidence levels:</p><ul>'
         '<li>Documentation reviewed: pinned author documentation supports the stated functionality.</li>'
         '<li>Source reviewed: a pinned procedure and its implementation support a specific class.</li>'
         '<li>Local checked driver: a recorded local build and numerical checks verify one problem/configuration.</li>'
         '<li>Hosted checked driver: the playground export links a checked problem-specific example.</li></ul>'
         '<p>Levels apply to individual claims and drivers. They are not a certification of an entire repository.</p><p>'
         +link('../review-policy.md','Full policy and contribution format')+' · '+link('../local-reviews.md','Independent reviews')+'</p>')
    return len(projects)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'_site')
    args = parser.parse_args()
    print(f'Built {build(args.output)} repositories in {args.output}')
