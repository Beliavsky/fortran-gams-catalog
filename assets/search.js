'use strict';
const form = document.querySelector('.search');
if (form) {
  const query = document.getElementById('query');
  const collection = document.getElementById('collection');
  const cards = [...document.querySelectorAll('article[data-search]')];
  const params = new URLSearchParams(location.search);
  query.value = params.get('q') || '';
  if (['independent', 'imported'].includes(params.get('collection'))) collection.value = params.get('collection');
  function update() {
    const terms = query.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const card of cards) {
      card.hidden = !(terms.every(term => card.dataset.search.includes(term)) &&
        (!collection.value || card.dataset.collection === collection.value));
      if (!card.hidden) count++;
    }
    document.getElementById('matches').textContent = `${count} of ${cards.length} repositories shown`;
    const url = new URL(location.href);
    for (const [name, value] of [['q', query.value.trim()], ['collection', collection.value]]) {
      if (value) url.searchParams.set(name, value); else url.searchParams.delete(name);
    }
    history.replaceState(null, '', url);
  }
  form.addEventListener('submit', event => { event.preventDefault(); update(); });
  query.addEventListener('input', update);
  collection.addEventListener('change', update);
  update();
}
