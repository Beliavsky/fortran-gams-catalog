// Exercise the shipped script with DOM fixtures; no browser packages required.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const cards = [
  {dataset:{search:'ffte certik fourier transform',collection:'independent'}},
  {dataset:{search:'fortran-lapack perazz federico perini linear algebra',collection:'imported'}}
];
const query = {value:'',addEventListener:(event,handler)=>query.handler=handler};
const collection = {value:'',addEventListener:(event,handler)=>collection.handler=handler};
const matches = {};
const form = {addEventListener:(event,handler)=>form.handler=handler};
let saved;
const context = {
  document: {
    querySelector:()=>form,
    querySelectorAll:()=>cards,
    getElementById:id=>({query,collection,matches})[id]
  },
  location: {href:'https://example.org/catalog/projects/?q=Federico&collection=imported&keep=yes',
             search:'?q=Federico&collection=imported&keep=yes'},
  history: {replaceState:(state,title,url)=>saved=url},
  URL,URLSearchParams
};
vm.runInNewContext(fs.readFileSync('assets/search.js','utf8'),context);
assert.equal(cards[0].hidden,true);
assert.equal(cards[1].hidden,false);
assert.equal(matches.textContent,'1 of 2 repositories shown');
query.value='FOURIER certik';collection.value='independent';query.handler();
assert.equal(cards[0].hidden,false);assert.equal(cards[1].hidden,true);
assert.equal(saved.searchParams.get('keep'),'yes');
assert.equal(saved.searchParams.get('q'),'FOURIER certik');
query.value='nonexistent';query.handler();
assert.equal(matches.textContent,'0 of 2 repositories shown');
query.value='';collection.value='';collection.handler();
assert.equal(matches.textContent,'2 of 2 repositories shown');
assert.equal(saved.searchParams.has('q'),false);
console.log('Search: restored filters, owner names, multiple words, collection and empty results passed.');
