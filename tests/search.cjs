// Exercise the shipped script with DOM fixtures; no browser packages required.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const cards = [
  {dataset:{search:'ffte certik fourier transform',collection:'independent',fpm:'false'}},
  {dataset:{search:'fortran-lapack perazz federico perini linear algebra',collection:'imported',fpm:'true'}},
  {dataset:{search:'independent fpm sorting module',collection:'independent',fpm:'true'}}
];
for (const [i, card] of cards.entries()) {
  card.dataset.sourceMatch = i === 2 ? 'false' : 'true';
  card.dataset.sourceSearch = card.dataset.search.replace('linear algebra', 'D2 source-procedure').toLowerCase();
  card.all = {hidden:false}; card.source = {hidden:true};
  card.querySelectorAll = selector => selector === '[data-all-mappings]' ? [card.all] : [card.source];
}
const query = {value:'',addEventListener:(event,handler)=>query.handler=handler};
const collection = {value:'',addEventListener:(event,handler)=>collection.handler=handler};
const excludeFpm = {checked:false,addEventListener:(event,handler)=>excludeFpm.handler=handler};
const sourceReviewed = {checked:false,addEventListener:(event,handler)=>sourceReviewed.handler=handler};
const classCount = {dataset:{classCount:'3',withoutFpm:'1',sourceCount:'2',sourceWithoutFpm:'1'}};
function anchor(href) { return {getAttribute:()=>href,href}; }
const links = [anchor('../classes/D/'),anchor('../projects/?keep=yes'),anchor('#content'),
               anchor('../catalog.json'),anchor('https://example.org/playground/')];
const matches = {};
const form = {addEventListener:(event,handler)=>form.handler=handler};
let saved;
const context = {
  document: {
    querySelector:()=>form,
    querySelectorAll:selector=>({'article[data-search]':cards,'[data-class-count]':[classCount],'a[href]':links})[selector],
    getElementById:id=>({query,collection,matches,'exclude-fpm':excludeFpm,'source-reviewed':sourceReviewed})[id]
  },
  location: {href:'https://example.org/catalog/projects/?q=Federico&collection=imported&keep=yes',
             search:'?q=Federico&collection=imported&keep=yes'},
  history: {replaceState:(state,title,url)=>saved=url},
  URL,URLSearchParams
};
vm.runInNewContext(fs.readFileSync('assets/search.js','utf8'),context);
assert.equal(cards[0].hidden,true);
assert.equal(cards[1].hidden,false);
assert.equal(matches.textContent,'1 of 3 repositories shown');
query.value='FOURIER certik';collection.value='independent';query.handler();
assert.equal(cards[0].hidden,false);assert.equal(cards[1].hidden,true);
assert.equal(saved.searchParams.get('keep'),'yes');
assert.equal(saved.searchParams.get('q'),'FOURIER certik');
query.value='nonexistent';query.handler();
assert.equal(matches.textContent,'0 of 3 repositories shown');
query.value='';collection.value='';collection.handler();
assert.equal(matches.textContent,'3 of 3 repositories shown');
assert.equal(saved.searchParams.has('q'),false);
excludeFpm.checked=true;excludeFpm.handler();
assert.deepEqual(cards.map(c=>c.hidden),[false,true,true]);
assert.equal(matches.textContent,'1 of 3 repositories shown');
assert.equal(saved.searchParams.get('exclude_fpm'),'1');
assert.equal(classCount.textContent,'(1)');
assert.equal(new URL(links[0].href).searchParams.get('exclude_fpm'),'1');
assert.equal(new URL(links[1].href).searchParams.get('keep'),'yes');
assert.equal(links[2].href,'#content');
assert.equal(links[3].href,'../catalog.json');
assert.equal(links[4].href,'https://example.org/playground/');
collection.value='imported';collection.handler();
assert.equal(matches.textContent,'0 of 3 repositories shown');
excludeFpm.checked=false;excludeFpm.handler();
assert.equal(matches.textContent,'1 of 3 repositories shown');
assert.equal(classCount.textContent,'(3)');
assert.equal(saved.searchParams.has('exclude_fpm'),false);
assert.equal(new URL(links[0].href).searchParams.has('exclude_fpm'),false);

collection.value='';sourceReviewed.checked=true;sourceReviewed.handler();
assert.deepEqual(cards.map(c=>c.hidden),[false,false,true]);
assert.equal(classCount.textContent,'(2)');
assert.equal(saved.searchParams.get('source_reviewed'),'1');
assert.equal(new URL(links[0].href).searchParams.get('source_reviewed'),'1');
assert.equal(cards[0].all.hidden,true);assert.equal(cards[0].source.hidden,false);
query.value='linear algebra';query.handler();
assert.equal(matches.textContent,'0 of 3 repositories shown');
query.value='source-procedure';query.handler();
assert.equal(matches.textContent,'1 of 3 repositories shown');
query.value='';excludeFpm.checked=true;excludeFpm.handler();
assert.deepEqual(cards.map(c=>c.hidden),[false,true,true]);
assert.equal(classCount.textContent,'(1)');
sourceReviewed.checked=false;sourceReviewed.handler();
assert.equal(saved.searchParams.has('source_reviewed'),false);
assert.equal(new URL(links[0].href).searchParams.has('source_reviewed'),false);
assert.equal(cards[0].all.hidden,false);assert.equal(cards[0].source.hidden,true);

// Taxonomy and project pages have the global toggle but no search form.
const homeToggle={checked:false,addEventListener:(event,handler)=>homeToggle.handler=handler};
const homeSource={checked:false,addEventListener:(event,handler)=>homeSource.handler=handler};
const home={
  ...context,
  document:{querySelector:()=>null,
    querySelectorAll:selector=>({'article[data-search]':[],'[data-class-count]':[classCount],'a[href]':links})[selector],
    getElementById:id=>({'exclude-fpm':homeToggle,'source-reviewed':homeSource})[id]},
  location:{href:'https://example.org/catalog/?exclude_fpm=1&source_reviewed=1',search:'?exclude_fpm=1&source_reviewed=1'}
};
vm.runInNewContext(fs.readFileSync('assets/search.js','utf8'),home);
assert.equal(homeToggle.checked,true);
assert.equal(homeSource.checked,true);
assert.equal(classCount.textContent,'(1)');
assert.equal(new URL(links[0].href).searchParams.get('exclude_fpm'),'1');
assert.equal(new URL(links[0].href).searchParams.get('source_reviewed'),'1');
console.log('Search: combined filters, FPM exclusions, taxonomy counts, navigation and restored state passed.');

// License filters restore from shared URLs, combine with the other filters,
// update taxonomy counts, and propagate through internal navigation.
const license = {value:'',addEventListener:(event,handler)=>license.handler=handler};
const licenseReviewed = {checked:false,addEventListener:(event,handler)=>licenseReviewed.handler=handler};
cards.forEach((card, i) => {
  card.dataset.license = ['permissive','strong-copyleft','unclear'][i];
  card.dataset.licenseReviewed = i === 1 ? 'false' : 'true';
});
classCount.dataset.licenseCounts = JSON.stringify({
  '|0|0|0':3, '|0|0|1':1, '|0|1|0':2, '|1|0|0':2,
  'permissive|0|0|0':1, 'permissive|1|0|0':1,
  'permissive|1|1|0':1, 'permissive|1|1|1':1,
  'strong-copyleft|0|0|0':1, 'unclear|1|0|0':1
});
query.value=''; collection.value='';
const licensed = {
  ...context,
  document:{...context.document,
    getElementById:id=>({license,'license-reviewed':licenseReviewed})[id] || context.document.getElementById(id)},
  location:{href:'https://example.org/catalog/projects/?license=permissive&license_reviewed=1',
    search:'?license=permissive&license_reviewed=1'}
};
vm.runInNewContext(fs.readFileSync('assets/search.js','utf8'),licensed);
assert.equal(license.value,'permissive'); assert.equal(licenseReviewed.checked,true);
assert.deepEqual(cards.map(c=>c.hidden),[false,true,true]);
assert.equal(classCount.textContent,'(1)');
assert.equal(new URL(links[0].href).searchParams.get('license'),'permissive');
assert.equal(new URL(links[0].href).searchParams.get('license_reviewed'),'1');
assert.equal(saved.searchParams.get('license'),'permissive');
sourceReviewed.checked=true; excludeFpm.checked=true; sourceReviewed.handler();
assert.deepEqual(cards.map(c=>c.hidden),[false,true,true]);
assert.equal(classCount.textContent,'(1)');
license.value='strong-copyleft'; license.handler();
assert.equal(matches.textContent,'0 of 3 repositories shown');
assert.equal(classCount.textContent,'(0)');
licenseReviewed.checked=false; excludeFpm.checked=false; sourceReviewed.checked=false; licenseReviewed.handler();
assert.deepEqual(cards.map(c=>c.hidden),[true,false,true]);
assert.equal(classCount.textContent,'(1)');
license.value='unclear'; licenseReviewed.checked=true; license.handler();
assert.deepEqual(cards.map(c=>c.hidden),[true,true,false]);
license.value=''; licenseReviewed.checked=false; license.handler();
assert.equal(matches.textContent,'3 of 3 repositories shown');
assert.equal(saved.searchParams.has('license'),false);
assert.equal(saved.searchParams.has('license_reviewed'),false);
assert.equal(new URL(links[0].href).searchParams.has('license'),false);
assert.equal(new URL(links[0].href).searchParams.has('license_reviewed'),false);
const licenseHome = {...home,
  document:{...home.document,
    getElementById:id=>({license,'license-reviewed':licenseReviewed})[id] || home.document.getElementById(id)},
  location:licensed.location};
vm.runInNewContext(fs.readFileSync('assets/search.js','utf8'),licenseHome);
assert.equal(license.value,'permissive'); assert.equal(licenseReviewed.checked,true);
assert.equal(classCount.textContent,'(1)');
console.log('License filters: restored state, combined exclusions, counts, and navigation passed.');

const legacyToggle = {checked:false,addEventListener:(event,handler)=>legacyToggle.handler=handler};
const legacyCard = {dataset:{legacy:'true',search:'dqags quadpack quadrature',sourceSearch:'',sourceMatch:'false',
  license:'unclear',licenseReviewed:'false',collection:'legacy',fpm:'false'},querySelectorAll:()=>[]};
cards.push(legacyCard);
classCount.dataset.legacyCount = '1';
classCount.dataset.licenseCounts = JSON.stringify({...JSON.parse(classCount.dataset.licenseCounts), 'unclear|0|0|0':1});
license.value=''; query.value=''; collection.value='';
const legacyContext = {...licensed,
  document:{...licensed.document,
    getElementById:id=>id === 'legacy-gams' ? legacyToggle : licensed.document.getElementById(id)},
  location:{href:'https://example.org/catalog/projects/',search:''}};
vm.runInNewContext(fs.readFileSync('assets/search.js','utf8'),legacyContext);
assert.equal(legacyCard.hidden,true);
assert.equal(matches.textContent,'3 of 3 repositories shown');
legacyToggle.checked=true; legacyToggle.handler();
assert.equal(legacyCard.hidden,false);
assert.equal(matches.textContent,'4 of 4 entries shown');
assert.equal(classCount.textContent,'(4)');
assert.equal(saved.searchParams.get('legacy_gams'),'1');
assert.equal(new URL(links[0].href).searchParams.get('legacy_gams'),'1');
license.value='permissive'; license.handler(); assert.equal(legacyCard.hidden,true);
license.value='unclear'; license.handler(); assert.equal(legacyCard.hidden,false);
assert.equal(classCount.textContent,'(2)');
licenseReviewed.checked=true; licenseReviewed.handler(); assert.equal(legacyCard.hidden,true);
assert.equal(classCount.textContent,'(1)');
licenseReviewed.checked=false; sourceReviewed.checked=true; sourceReviewed.handler(); assert.equal(legacyCard.hidden,true);
assert.equal(classCount.textContent,'(0)');
sourceReviewed.checked=false; license.value=''; collection.value='independent'; collection.handler();
assert.equal(legacyCard.hidden,true);
collection.value=''; excludeFpm.checked=true; excludeFpm.handler();
assert.equal(legacyCard.hidden,false); assert.equal(classCount.textContent,'(2)');

// AD facets use exact curated tags, combine with existing filters, restore from
// URLs, update hierarchy counts, and persist on pages without a search form.
const method = {value:'',addEventListener:(event,handler)=>method.handler=handler};
const methodExclude = {checked:false,addEventListener:(event,handler)=>methodExclude.handler=handler};
const methodSource = {checked:false,addEventListener:(event,handler)=>methodSource.handler=handler};
const methodLicense = {value:'',addEventListener:(event,handler)=>methodLicense.handler=handler};
const methodLegacy = {checked:false,addEventListener:(event,handler)=>methodLegacy.handler=handler};
const methodCards = [
  {dataset:{search:'forward AD',topics:'automatic-differentiation forward-mode',sourceMatch:'true',sourceSearch:'forward ad',fpm:'false',license:'permissive'}},
  {dataset:{search:'reverse AD',topics:'automatic-differentiation reverse-mode',sourceMatch:'false',sourceSearch:'',fpm:'true',license:'strong-copyleft'}},
  {dataset:{search:'finite differences',topics:'forward-mode-ish',sourceMatch:'true',sourceSearch:'finite differences',fpm:'false',license:'permissive'}},
  {dataset:{search:'legacy',legacy:'true',topics:'',sourceMatch:'false',sourceSearch:'',fpm:'false',license:'unclear'}}
];
methodCards.forEach(card=>card.querySelectorAll=()=>[]);
const methodCount = {dataset:{classCount:'3',legacyCount:'1',sourceCount:'2',withoutFpm:'2',sourceWithoutFpm:'2',
  licenseCounts:JSON.stringify({'permissive|0|1|0':2}),topicCounts:JSON.stringify({
  'forward-mode':{'|0|0|0':1,'|0|1|0':1,'permissive|0|1|0':1},
  'reverse-mode':{'|0|0|0':1},
  'automatic-differentiation':{'|0|0|0':2}
})}};
const methodMatches = {};
const methodLink = anchor('../classes/H1/');
const methodContext = {
  ...context,
  document:{querySelector:()=>null,
    querySelectorAll:selector=>({'article[data-search]':methodCards,'[data-class-count]':[methodCount],'a[href]':[methodLink]})[selector],
    getElementById:id=>({topic:method,'exclude-fpm':methodExclude,'source-reviewed':methodSource,
      license:methodLicense,'legacy-gams':methodLegacy,matches:methodMatches})[id]},
  location:{href:'https://example.org/catalog/?topic=forward-mode&keep=yes&legacy_gams=1',
    search:'?topic=forward-mode&keep=yes&legacy_gams=1'}
};
vm.runInNewContext(fs.readFileSync('assets/search.js','utf8'),methodContext);
assert.equal(method.value,'forward-mode');
assert.deepEqual(methodCards.map(c=>c.hidden),[false,true,true,true]);
assert.equal(methodCount.textContent,'(1)');
assert.equal(methodMatches.textContent,'1 of 4 entries shown');
assert.equal(saved.searchParams.get('keep'),'yes');
assert.equal(new URL(methodLink.href).searchParams.get('topic'),'forward-mode');
method.value='reverse-mode'; method.handler();
assert.deepEqual(methodCards.map(c=>c.hidden),[true,false,true,true]);
assert.equal(methodCount.textContent,'(1)');
methodExclude.checked=true; methodExclude.handler();
assert.equal(methodMatches.textContent,'0 of 4 entries shown');
assert.equal(methodCount.textContent,'(0)');
methodExclude.checked=false; methodSource.checked=true; methodSource.handler();
assert.equal(methodCount.textContent,'(0)');
method.value='forward-mode'; methodLicense.value='permissive'; method.handler();
assert.deepEqual(methodCards.map(c=>c.hidden),[false,true,true,true]);
assert.equal(methodCount.textContent,'(1)');
method.value=''; method.handler();
assert.equal(methodCount.textContent,'(2)');
assert.equal(saved.searchParams.has('topic'),false);
assert.equal(new URL(methodLink.href).searchParams.has('topic'),false);
method.value=''; methodContext.location.search='?topic=unknown';
vm.runInNewContext(fs.readFileSync('assets/search.js','utf8'),{...methodContext});
assert.equal(method.value,''); assert.equal(saved.searchParams.has('topic'),false);
console.log('AD topics: exact facets, combined filters, counts, URL restoration and navigation passed.');
query.value='dqags'; query.handler(); assert.equal(matches.textContent,'1 of 4 entries shown');
legacyToggle.checked=false; legacyToggle.handler();
assert.equal(legacyCard.hidden,true);
assert.equal(saved.searchParams.has('legacy_gams'),false);
assert.equal(new URL(links[0].href).searchParams.has('legacy_gams'),false);
legacyContext.location={href:'https://example.org/catalog/projects/?legacy_gams=1',search:'?legacy_gams=1'};
vm.runInNewContext(fs.readFileSync('assets/search.js','utf8'),{...legacyContext});
assert.equal(legacyToggle.checked,true); assert.equal(legacyCard.hidden,false);
console.log('Legacy GAMS: hidden default, URL restore, search, combined filters, counts and navigation passed.');

// Compact header: only valid optional filters expand the panel. Home searches
// route to the repository listing, retaining the current query and filters.
function compactPage(search = '', home = false) {
  const controls = Object.fromEntries(['query', 'collection', 'exclude-fpm',
    'source-reviewed', 'license', 'license-reviewed', 'legacy-gams', 'topic'].map(id => {
    const control = {value:'', checked:false, addEventListener:(event, fn)=>control.handler=fn};
    return [id, control];
  }));
  controls.filters = {open:false};
  const searchForm = {dataset:home ? {destination:'projects/'} : {},
    addEventListener:(event, fn)=>searchForm.handler=fn};
  let destination;
  const pageLocation = {href:`https://example.org/catalog/${home ? '' : 'projects/'}${search}`,
    search, assign:url=>destination=url};
  vm.runInNewContext(fs.readFileSync('assets/search.js','utf8'), {
    document:{querySelector:()=>searchForm, querySelectorAll:()=>[], getElementById:id=>controls[id]},
    location:pageLocation, history:{replaceState:(state, title, url)=>{
      pageLocation.href=String(url); pageLocation.search=new URL(url).search;
    }}, URL, URLSearchParams
  });
  return {controls, searchForm, location:pageLocation, destination:()=>destination};
}
for (const search of ['', '?q=solver', '?topic=unknown&license=unknown&collection=unknown', '?exclude_fpm=0']) {
  assert.equal(compactPage(search).controls.filters.open, false, search);
}
for (const filter of ['exclude_fpm=1', 'source_reviewed=1', 'license=permissive',
  'license_reviewed=1', 'legacy_gams=1', 'topic=forward-mode', 'collection=independent']) {
  const page = compactPage(`?${filter}`);
  assert.equal(page.controls.filters.open, true, filter);
  page.controls.filters.open=false;
  page.controls.query.value='solver'; page.controls.query.handler();
  assert.equal(page.controls.filters.open, false);
}
const compactHome = compactPage('?license=permissive&collection=imported&keep=yes', true);
compactHome.controls.query.value='  nonlinear solver  ';
compactHome.searchForm.handler({preventDefault:()=>{}});
const homeDestination = new URL(compactHome.destination());
assert.equal(homeDestination.pathname, '/catalog/projects/');
assert.equal(homeDestination.searchParams.get('q'), 'nonlinear solver');
assert.equal(homeDestination.searchParams.get('license'), 'permissive');
assert.equal(homeDestination.searchParams.get('collection'), 'imported');
assert.equal(homeDestination.searchParams.get('keep'), 'yes');
const compactListing = compactPage('?q=solver');
compactListing.searchForm.handler({preventDefault:()=>{}});
assert.equal(compactListing.destination(), undefined);
console.log('Compact header: filter expansion and home/listing search behavior passed.');
