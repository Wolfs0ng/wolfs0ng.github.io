(() => {
  'use strict';
  const root = document.documentElement;
  const supported = new Set(['ua', 'en']);
  const fixed = root.dataset.fixedLang;
  const query = new URLSearchParams(location.search).get('lang');
  let saved;
  try { saved = localStorage.getItem('site_lang'); } catch { /* Optional storage. */ }
  let lang = fixed || (supported.has(query) ? query : supported.has(saved) ? saved : navigator.language.toLowerCase().startsWith('uk') ? 'ua' : 'en');
  function applyLanguage(next) {
    lang = supported.has(next) ? next : 'ua';
    root.lang = lang === 'ua' ? 'uk' : 'en';
    document.querySelector('.main-nav')?.setAttribute('aria-label', lang === 'ua' ? 'Основна навігація' : 'Main navigation');
    document.querySelector('.brand')?.setAttribute('aria-label', lang === 'ua' ? 'Дмитро Тарасенко — головна' : 'Dmytro Tarasenko — home');
    document.querySelector('.lightbox')?.setAttribute('aria-label', lang === 'ua' ? 'Перегляд зображення' : 'Image viewer');
    document.querySelectorAll('[data-i18n]').forEach(el => { el.hidden = el.dataset.i18n !== lang; });
    document.querySelectorAll('[data-lang]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.lang === lang)));
    document.querySelectorAll('[data-keep-lang]').forEach(link => {
      const url = new URL(link.href, location.href); url.searchParams.set('lang', lang); link.href = url.href;
    });
    document.querySelectorAll('[data-wiki-entry]').forEach(link => { link.href = link.href.replace(/\/wiki\/(ua|en)\//, `/wiki/${lang}/`); });
    const title = document.body.dataset[lang === 'ua' ? 'titleUa' : 'titleEn']; if (title) document.title = title;
    try { localStorage.setItem('site_lang', lang); } catch { /* Optional storage. */ }
  }
  applyLanguage(lang);
  document.querySelectorAll('[data-lang]').forEach(button => button.addEventListener('click', () => {
    applyLanguage(button.dataset.lang); const url = new URL(location.href); url.searchParams.set('lang', lang); history.replaceState(null, '', url);
  }));
  document.querySelectorAll('[data-locale]').forEach(link => link.addEventListener('click', event => {
    if (link.getAttribute('aria-current') === 'true') { event.preventDefault(); return; }
    try { localStorage.setItem('site_lang', link.dataset.locale); } catch { /* Optional storage. */ }
  }));
  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
  const modal = document.querySelector('.lightbox');
  if (modal && typeof modal.showModal === 'function') {
    const image = modal.querySelector('img'), caption = modal.querySelector('p'); let origin;
    document.querySelectorAll('[data-lightbox]').forEach(link => link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault(); origin = link; image.src = link.href; image.alt = link.querySelector('img')?.alt || '';
      caption.textContent = link.dataset[lang === 'ua' ? 'captionUa' : 'captionEn'] || image.alt;
      modal.querySelector('button').setAttribute('aria-label', lang === 'ua' ? 'Закрити' : 'Close');
      modal.showModal(); document.body.classList.add('modal-open');
    }));
    modal.querySelector('button').addEventListener('click', () => modal.close());
    modal.addEventListener('click', event => { if (event.target === modal) modal.close(); });
    modal.addEventListener('close', () => { document.body.classList.remove('modal-open'); image.removeAttribute('src'); origin?.focus({ preventScroll: true }); });
  }
  document.querySelectorAll('img[src^="https:"]').forEach(img => {
    const fail = () => img.classList.add('image-unavailable'); img.addEventListener('error', fail); if (img.complete && !img.naturalWidth) fail();
  });
})();
