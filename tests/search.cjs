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
