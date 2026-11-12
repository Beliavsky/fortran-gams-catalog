'use strict';
const intentControl = document.getElementById('highlight-intents');
if (intentControl) {
  try { intentControl.checked = localStorage.getItem('fortran-catalog-highlight-intents') === '1'; }
  catch (_) { /* Storage may be unavailable; the toggle still works. */ }
  const applyIntents = () => document.documentElement.classList.toggle('highlight-intents', intentControl.checked);
  intentControl.addEventListener('change', () => {
    applyIntents();
    try { localStorage.setItem('fortran-catalog-highlight-intents', intentControl.checked ? '1' : '0'); }
    catch (_) { /* Keep the preference for this page only. */ }
  });
  applyIntents();
}
const form = document.querySelector('.search');
const excludeFpm = document.getElementById('exclude-fpm');
const sourceReviewed = document.getElementById('source-reviewed');
const license = document.getElementById('license');
const licenseReviewed = document.getElementById('license-reviewed');
const legacyGams = document.getElementById('legacy-gams');
const topic = document.getElementById('topic');
const filtersPanel = document.getElementById('filters');
const topics = new Set(['automatic-differentiation', 'forward-mode', 'reverse-mode',
  'higher-derivatives', 'sparse-jacobians', 'matrix-derivatives', 'source-transformation',
  'expression-parser', 'scalar-evaluation', 'array-evaluation', 'complex-evaluation',
  'custom-functions', 'parser-derivatives', 'expression-code-generation',
  'reusable-parser', 'calculator-cli']);
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
  if (topic && topics.has(params.get('topic'))) topic.value = params.get('topic');
  if (filtersPanel && (excludeFpm.checked || sourceReviewed?.checked || license?.value ||
      licenseReviewed?.checked || legacyGams?.checked || topic?.value || collection?.value)) {
    filtersPanel.open = true;
  }
  function update() {
    const sourceOnly = Boolean(sourceReviewed?.checked);
    const licenseOnly = license?.value || '';
    const reviewedLicenseOnly = Boolean(licenseReviewed?.checked);
    const includeLegacy = Boolean(legacyGams?.checked);
    const selectedTopic = topic?.value || '';
    const terms = (query?.value || '').toLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const card of cards) {
      const search = sourceOnly ? card.dataset.sourceSearch : card.dataset.search;
      card.hidden = !((!sourceOnly || card.dataset.sourceMatch === 'true') &&
        (includeLegacy || card.dataset.legacy !== 'true') &&
        (!selectedTopic || (card.dataset.topics || '').split(/\s+/).includes(selectedTopic)) &&
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
      if (selectedTopic) count = (JSON.parse(label.dataset.topicCounts || '{}')[selectedTopic] || {})[licenseKey] || 0;
      if (!selectedTopic && includeLegacy && !sourceOnly && !reviewedLicenseOnly && (!licenseOnly || licenseOnly === 'unclear')) count += Number(label.dataset.legacyCount || 0);
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
      if (selectedTopic) target.searchParams.set('topic', selectedTopic);
      else target.searchParams.delete('topic');
      link.href = target.href;
    }
    const url = new URL(location.href);
    for (const [name, value] of [['q', query?.value.trim() || ''], ['collection', collection?.value || ''],
                                 ['exclude_fpm', excludeFpm.checked ? '1' : ''],
                                 ['source_reviewed', sourceOnly ? '1' : ''],
                                 ['license', licenseOnly], ['license_reviewed', reviewedLicenseOnly ? '1' : ''],
                                 ['legacy_gams', includeLegacy ? '1' : ''], ['topic', selectedTopic]]) {
      if (value) url.searchParams.set(name, value); else url.searchParams.delete(name);
    }
    history.replaceState(null, '', url);
  }
  form?.addEventListener('submit', event => {
    event.preventDefault();
    update();
    if (form.dataset?.destination) {
      const target = new URL(form.dataset.destination, location.href);
      target.search = new URL(location.href).search;
      location.assign(target.href);
    }
  });
  query?.addEventListener('input', update);
  collection?.addEventListener('change', update);
  excludeFpm.addEventListener('change', update);
  sourceReviewed?.addEventListener('change', update);
  license?.addEventListener('change', update);
  licenseReviewed?.addEventListener('change', update);
  legacyGams?.addEventListener('change', update);
  topic?.addEventListener('change', update);
  update();
}
