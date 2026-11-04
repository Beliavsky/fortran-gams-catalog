"""Build the independent static catalog without network or compilation."""
import argparse
from html import escape
import json
from pathlib import Path
import shutil
from urllib.parse import quote

from catalog import ROOT, assemble, belongs, lineage, matching_drivers

TITLE = 'Fortran software by GAMS classification'


def e(value):
    return escape(str(value), quote=True)


def link(url, text):
    return f'<a href="{e(url)}">{e(text)}</a>'


def project_path(project):
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


def build(destination, root=ROOT):
    destination, root = Path(destination), Path(root)
    tree, projects, merged = assemble(root)
    reviewed_codes = {p['id']: source_codes(p) for p in projects}
    destination.mkdir(parents=True, exist_ok=True)
    for asset in ('catalog.css', 'search.js'):
        shutil.copy2(root/'assets'/asset, destination/asset)
    (destination/'.nojekyll').touch()
    (destination/'catalog.json').write_text(json.dumps(merged, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    (destination/'taxonomy.json').write_text(json.dumps(tree, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
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
<title>{e(title)}</title><link rel="stylesheet" href="{prefix}catalog.css"><script defer src="{prefix}search.js"></script></head>
<body><a class="skip" href="#content">Skip to content</a><header>{link(prefix or './', TITLE)}
<nav>{link(prefix+'projects/', 'Repositories')} · {link(prefix+'review/', 'Review policy')} ·
{link('https://beliavsky.github.io/fortran-playground/gams/', 'Playground package catalog')} ·
{link('https://gams.nist.gov/cgi-bin/serve.cgi', 'About GAMS')}</nav>
<div class="build-filter"><label class="checkbox-label"><input type="checkbox" id="exclude-fpm" aria-describedby="fpm-filter-help"> Exclude known FPM packages</label>
<span class="muted" id="fpm-filter-help">Repositories with unreviewed build support remain included.</span></div>
<div class="build-filter"><label class="checkbox-label"><input type="checkbox" id="source-reviewed" aria-describedby="source-filter-help"> Only source-reviewed mappings</label>
<span class="muted" id="source-filter-help">Evidence in the source supports the classification; compilation and numerical testing are separate.</span></div></header>
<main id="content">{body}</main><footer>{link(prefix+'catalog.json','Download layered metadata')} ·
{link(prefix+'taxonomy.json','GAMS taxonomy')}<p>Classification describes documented functionality. A checked driver verifies only its recorded problem and configuration.</p></footer></body></html>
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
<label>Collection <select id="collection" name="collection"><option value="">All repositories</option><option value="independent">Independent reviews</option><option value="imported">Playground imports</option></select></label><button type="submit">Search</button></form>
<p id="matches" aria-live="polite"></p><noscript>All entries are listed below. Use your browser’s Find command to search this page.</noscript>'''
        cards = []
        for p in items:
            repo = p['repository']
            codes = p['codes']
            search = ' '.join([p['name'], p['description'], repo['owner'], p['owner_label'],
                               *p['topics'], *codes, *(tree[c]['label'] for c in codes),
                               *(proc['procedure'] for proc in p['procedures'])])
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
                                      *(proc['procedure'] for proc in p['procedures']
                                        if proc.get('origin') == 'local' or proc.get('review_level') == 'source-reviewed')])
            reviewed_leaves = specific_codes(tree, reviewed)
            source_labels = ' · '.join(link(prefix+'classes/'+c+'/', c)
                                        for c in reviewed_leaves[:8])
            if len(reviewed_leaves) > 8:
                source_labels += ' · '+link(prefix+project_path(p), f'{len(reviewed_leaves)-8} more reviewed classes')
            cards.append(f'''<article data-search="{e(search.lower())}" data-source-search="{e(source_search.lower())}" data-source-match="{str(source_match).lower()}" data-collection="{collection}" data-fpm="{str(supports_fpm(p)).lower()}">
<h2>{link(prefix+project_path(p),p['name'])}</h2><p class="muted">{link(repo['url'],repo['owner']+'/'+repo['name'])} · {e(p['owner_label'])}</p>
<p>{e(p['description'])}</p><div data-all-mappings><p class="status">{e(status(p,code))}</p><p>{labels}</p>{driver_links}</div>
<div data-source-mappings hidden><p class="status">Source-reviewed mapping evidence</p><p>{source_labels}</p></div></article>''')
        return controls+''.join(cards)

    def class_links(parent, prefix):
        codes = [c for c in tree if tree[c]['parent'] == parent]
        rows = []
        for c in codes:
            members = [p for p in projects if any(belongs(tree, k, c) for k in p['codes'])]
            without_fpm = sum(not supports_fpm(p) for p in members)
            reviewed = [p for p in members if any(belongs(tree, k, c) for k in reviewed_codes[p['id']])]
            rows.append('<li>'+link(prefix+'classes/'+c+'/',c+' — '+tree[c]['label'])+
                        f' <span class="muted" data-class-count="{len(members)}" data-without-fpm="{without_fpm}" data-source-count="{len(reviewed)}" data-source-without-fpm="{sum(not supports_fpm(p) for p in reviewed)}">({len(members)})</span></li>')
        return '<ul class="classes">'+''.join(rows)+'</ul>'

    page('', TITLE, f'<h1>{TITLE}</h1><p class="lede">Find numerical methods and supporting software, including repositories that do not use FPM.</p>'
         f'<p>{len(projects)} repositories: {sum(bool(p.get("playground")) for p in projects)} imported playground packages and '
         f'{sum(not bool(p.get("playground")) for p in projects)} independent repository reviews.</p>'
         '<p>Browse by problem below, or '+link('projects/', 'search all repositories')+'. '
         'New independent entries begin with pinned documentation reviews. Source mappings and local drivers can be added as they are checked.</p>'
         '<h2>Main GAMS classes</h2>'+class_links(None, ''))
    page('projects', 'Fortran repositories', '<h1>Fortran repositories</h1>'+listing(projects, '../'))
    for code, info in tree.items():
        subset = [p for p in projects if any(belongs(tree, c, code) for c in p['codes'])]
        crumbs = ' / '.join(link('../../classes/'+c+'/', c) for c in reversed(lineage(tree, code)[1:]))
        intro = '<nav aria-label="Breadcrumb">'+link('../../','All classes')+' / '+crumbs+'</nav>'
        intro += '<h1>'+e(code+' — '+info['label'])+'</h1><p>Includes explicitly mapped descendants. Driver links below match this class or a narrower problem.</p>'
        page('classes/'+code, code+' — '+info['label'], intro+class_links(code, '../../')+
             (listing(subset, '../../', code) if subset else '<p>No repository is mapped here yet.</p>'))
    for p in projects:
        prefix = '../../../'
        repo = p['repository']
        body = '<h1>'+e(p['name'])+'</h1><p class="lede">'+e(p['description'])+'</p>'
        body += '<p>'+link(repo['url'], repo['owner']+'/'+repo['name'])+' · '+e(p['origin'])+'</p>'
        body += '<p>Repository owner: '+e(p['owner_label'])+'</p><p>Build systems: '+e(', '.join(p.get('build_systems', [])) or 'Not yet reviewed')+'</p>'
        body += '<p>Topics: '+e(', '.join(p['topics']))+'</p><h2>Classifications</h2><ul>'
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
                body += '<h3>Reviewed procedures and source ranges</h3><ul>'
                for procedure in claim['procedures']:
                    evidence = next(v for v in claim['evidence'] if v['path'] == procedure['path'])
                    start, end = procedure['line_start'], procedure['line_end']
                    body += '<li><code>'+e(procedure['procedure'])+'</code> — '+link(
                        evidence['url']+f'#L{start}-L{end}', procedure['path']+f':{start}–{end}')+'</li>'
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
