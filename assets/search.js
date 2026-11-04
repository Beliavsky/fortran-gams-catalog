'use strict';
const form = document.querySelector('.search');
const excludeFpm = document.getElementById('exclude-fpm');
if (excludeFpm) {
  const query = document.getElementById('query');
  const collection = document.getElementById('collection');
  const cards = [...document.querySelectorAll('article[data-search]')];
  const classCounts = [...document.querySelectorAll('[data-class-count]')];
  const navigation = [...document.querySelectorAll('a[href]')].flatMap(link => {
    const href = link.getAttribute('href');
    if (/^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i.test(href)) return [];
    const url = new URL(href, location.href);
    return url.origin === new URL(location.href).origin &&
      (url.pathname.endsWith('/') || url.pathname.endsWith('/index.html')) ? [{link, url}] : [];
  });
  const params = new URLSearchParams(location.search);
  if (query) query.value = params.get('q') || '';
  if (collection && ['independent', 'imported'].includes(params.get('collection'))) collection.value = params.get('collection');
  excludeFpm.checked = params.get('exclude_fpm') === '1';
  function update() {
    const terms = (query?.value || '').toLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const card of cards) {
      card.hidden = !(terms.every(term => card.dataset.search.includes(term)) &&
        (!collection?.value || card.dataset.collection === collection.value) &&
        (!excludeFpm.checked || card.dataset.fpm !== 'true'));
      if (!card.hidden) count++;
    }
    const matches = document.getElementById('matches');
    if (matches) matches.textContent = `${count} of ${cards.length} repositories shown`;
    for (const label of classCounts) {
      label.textContent = `(${excludeFpm.checked ? label.dataset.withoutFpm : label.dataset.classCount})`;
    }
    for (const {link, url: original} of navigation) {
      const target = new URL(original);
      if (excludeFpm.checked) target.searchParams.set('exclude_fpm', '1');
      else target.searchParams.delete('exclude_fpm');
      link.href = target.href;
    }
    const url = new URL(location.href);
    for (const [name, value] of [['q', query?.value.trim() || ''], ['collection', collection?.value || ''],
                                 ['exclude_fpm', excludeFpm.checked ? '1' : '']]) {
      if (value) url.searchParams.set(name, value); else url.searchParams.delete(name);
    }
    history.replaceState(null, '', url);
  }
  form?.addEventListener('submit', event => { event.preventDefault(); update(); });
  query?.addEventListener('input', update);
  collection?.addEventListener('change', update);
  excludeFpm.addEventListener('change', update);
  update();
}
