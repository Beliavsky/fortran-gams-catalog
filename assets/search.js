'use strict';
const form = document.querySelector('.search');
const excludeFpm = document.getElementById('exclude-fpm');
const sourceReviewed = document.getElementById('source-reviewed');
const license = document.getElementById('license');
const licenseReviewed = document.getElementById('license-reviewed');
const legacyGams = document.getElementById('legacy-gams');
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
  if (sourceReviewed) sourceReviewed.checked = params.get('source_reviewed') === '1';
  if (license && ['permissive', 'weak-copyleft', 'strong-copyleft', 'custom-mixed', 'unclear'].includes(params.get('license'))) license.value = params.get('license');
  if (licenseReviewed) licenseReviewed.checked = params.get('license_reviewed') === '1';
  if (legacyGams) legacyGams.checked = params.get('legacy_gams') === '1';
  function update() {
    const sourceOnly = Boolean(sourceReviewed?.checked);
    const licenseOnly = license?.value || '';
    const reviewedLicenseOnly = Boolean(licenseReviewed?.checked);
    const includeLegacy = Boolean(legacyGams?.checked);
    const terms = (query?.value || '').toLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const card of cards) {
      const search = sourceOnly ? card.dataset.sourceSearch : card.dataset.search;
      card.hidden = !((!sourceOnly || card.dataset.sourceMatch === 'true') &&
        (includeLegacy || card.dataset.legacy !== 'true') &&
        (!licenseOnly || card.dataset.license === licenseOnly) &&
        (!reviewedLicenseOnly || card.dataset.licenseReviewed === 'true') &&
        terms.every(term => search.includes(term)) &&
        (!collection?.value || card.dataset.collection === collection.value) &&
        (!excludeFpm.checked || card.dataset.fpm !== 'true'));
      if (!card.hidden) count++;
      for (const section of card.querySelectorAll('[data-all-mappings]')) section.hidden = sourceOnly;
      for (const section of card.querySelectorAll('[data-source-mappings]')) section.hidden = !sourceOnly;
    }
    const matches = document.getElementById('matches');
    const total = cards.filter(card => includeLegacy || card.dataset.legacy !== 'true').length;
    if (matches) matches.textContent = `${count} of ${total} ${includeLegacy ? 'entries' : 'repositories'} shown`;
    for (const label of classCounts) {
      const key = sourceOnly ? (excludeFpm.checked ? 'sourceWithoutFpm' : 'sourceCount') :
        (excludeFpm.checked ? 'withoutFpm' : 'classCount');
      const licenseKey = [licenseOnly, Number(reviewedLicenseOnly), Number(sourceOnly), Number(excludeFpm.checked)].join('|');
      let count = label.dataset.licenseCounts ? (JSON.parse(label.dataset.licenseCounts)[licenseKey] || 0) : Number(label.dataset[key]);
      if (includeLegacy && !sourceOnly && !reviewedLicenseOnly && (!licenseOnly || licenseOnly === 'unclear')) count += Number(label.dataset.legacyCount || 0);
      label.textContent = `(${count})`;
    }
    for (const {link, url: original} of navigation) {
      const target = new URL(original);
      if (excludeFpm.checked) target.searchParams.set('exclude_fpm', '1');
      else target.searchParams.delete('exclude_fpm');
      if (sourceOnly) target.searchParams.set('source_reviewed', '1');
      else target.searchParams.delete('source_reviewed');
      if (licenseOnly) target.searchParams.set('license', licenseOnly);
      else target.searchParams.delete('license');
      if (reviewedLicenseOnly) target.searchParams.set('license_reviewed', '1');
      else target.searchParams.delete('license_reviewed');
      if (includeLegacy) target.searchParams.set('legacy_gams', '1');
      else target.searchParams.delete('legacy_gams');
      link.href = target.href;
    }
    const url = new URL(location.href);
    for (const [name, value] of [['q', query?.value.trim() || ''], ['collection', collection?.value || ''],
                                 ['exclude_fpm', excludeFpm.checked ? '1' : ''],
                                 ['source_reviewed', sourceOnly ? '1' : ''],
                                 ['license', licenseOnly], ['license_reviewed', reviewedLicenseOnly ? '1' : ''],
                                 ['legacy_gams', includeLegacy ? '1' : '']]) {
      if (value) url.searchParams.set(name, value); else url.searchParams.delete(name);
    }
    history.replaceState(null, '', url);
  }
  form?.addEventListener('submit', event => { event.preventDefault(); update(); });
  query?.addEventListener('input', update);
  collection?.addEventListener('change', update);
  excludeFpm.addEventListener('change', update);
  sourceReviewed?.addEventListener('change', update);
  license?.addEventListener('change', update);
  licenseReviewed?.addEventListener('change', update);
  legacyGams?.addEventListener('change', update);
  update();
}
