(() => {
  'use strict';
  const main = document.querySelector('[data-search-index]'), input = document.getElementById('wiki-search');
  if (!main || !input) return;
  const ua = document.documentElement.lang === 'uk', menu = document.querySelector('.guide-menu'), media = matchMedia('(max-width: 900px)');
  function updateMenu() { menu.open = !media.matches; } updateMenu(); media.addEventListener('change', updateMenu);
  const results = document.getElementById('search-results'), status = document.querySelector('.search-status'), nav = document.querySelector('.guide-nav');
  let index, request, version = 0;
  const normalize = text => text.toLocaleLowerCase().normalize('NFKC').replace(/[’‘ʼ`]/g, "'");
  async function load() {
    if (index) return index;
    if (!request) request = fetch(main.dataset.searchIndex).then(r => { if (!r.ok) throw new Error('Search unavailable'); return r.json(); }).then(data => { index = data; return data; }).catch(error => { request = null; throw error; });
    return request;
  }
  input.addEventListener('focus', () => load().catch(() => {}));
  input.addEventListener('input', async () => {
    const turn = ++version, query = normalize(input.value.trim()); results.replaceChildren(); results.hidden = !query; nav.hidden = !!query; status.textContent = ''; if (!query) return;
    try {
      const pages = await load(); if (turn !== version) return;
      const words = query.split(/\s+/), matches = pages.filter(p => words.every(w => normalize(`${p.title} ${p.summary} ${p.text}`).includes(w)));
      matches.sort((a,b) => Number(normalize(b.title).includes(query)) - Number(normalize(a.title).includes(query)));
      for (const page of matches) {
        const link = document.createElement('a'), title = document.createElement('strong'), summary = document.createElement('span');
        link.href = page.url; title.textContent = page.title; summary.textContent = page.summary; link.append(title, summary); results.append(link);
      }
      status.textContent = matches.length ? (ua ? `Знайдено статей: ${matches.length}` : `Articles found: ${matches.length}`) : (ua ? 'Нічого не знайдено. Спробуй інше слово.' : 'No results. Try another word.');
    } catch { if (turn !== version) return; nav.hidden = false; status.textContent = ua ? 'Пошук недоступний. Скористайся розділами нижче.' : 'Search is unavailable. Browse the contents below.'; }
  });
  input.addEventListener('keydown', event => { if (event.key === 'Escape') { input.value = ''; input.dispatchEvent(new Event('input')); } });
})();
