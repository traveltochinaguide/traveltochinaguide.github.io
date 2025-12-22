/* Shared helper for city pages
   - Provides getLang() and applyCityContent(t, options)
   - options: { canonicalPath, ogImage, heroImage }
*/
(function () {
  function getLang() {
    try {
      const params = new URLSearchParams(window.location.search);
      const l = params.get('lang');
      if (l) return l;
    } catch (e) { }
    try {
      const ls = localStorage.getItem('preferredLanguage');
      if (ls) return ls;
    } catch (e) { }
    return navigator.language || navigator.userLanguage || 'en';
  }

  function upsertMetaByProperty(prop, content) {
    let m = document.querySelector(`meta[property="${prop}"]`);
    if (!m) { m = document.createElement('meta'); m.setAttribute('property', prop); document.head.appendChild(m); }
    m.setAttribute('content', content);
  }
  function upsertMetaByName(name, content) {
    let m = document.querySelector(`meta[name="${name}"]`);
    if (!m) { m = document.createElement('meta'); m.setAttribute('name', name); document.head.appendChild(m); }
    m.setAttribute('content', content);
  }

  function applyCityContent(t, options) {
    const lang = getLang();
    // Title and meta
    if (t.pageTitle) document.getElementById('page-title').textContent = t.pageTitle;
    const metaDesc = document.getElementById('meta-desc'); if (metaDesc && t.metaDesc) metaDesc.setAttribute('content', t.metaDesc);

    // City header and content
    const nameEl = document.getElementById('city-name'); if (nameEl) nameEl.innerHTML = t.cityName || '';
    const contentEl = document.getElementById('city-content'); if (contentEl) contentEl.innerHTML = t.contentHtml || t.longDesc || '';

    // Canonical + OG/Twitter url
    const canonical = document.querySelector('link[rel="canonical"]');
    // Best practice: set canonical to the clean, language-agnostic URL (no ?lang param).
    // Use hreflang alternates to point to localized variants.
    if (canonical && options && options.canonicalPath) {
      canonical.href = `https://www.travelchinaguide.dpdns.org/${options.canonicalPath}`;
    }
    const canonicalHref = canonical ? canonical.href : window.location.href;

    // Ensure hreflang alternate links exist for supported locales (helps Google pick correct language URLs)
    (function ensureHreflang() {
      if (!options || !options.canonicalPath) return;
      const langs = ['en', 'zh-CN', 'ja', 'ko', 'fr', 'de', 'es', 'ru'];
      langs.forEach(code => {
        const rel = document.querySelector(`link[rel="alternate"][hreflang="${code}"]`);
        const href = `https://www.travelchinaguide.dpdns.org/${options.canonicalPath}?lang=${encodeURIComponent(code)}`;
        if (rel) {
          rel.href = href;
        } else {
          const l = document.createElement('link');
          l.setAttribute('rel', 'alternate');
          l.setAttribute('hreflang', code);
          l.setAttribute('href', href);
          document.head.appendChild(l);
        }
      });
      // x-default fallback
      let xdef = document.querySelector('link[rel="alternate"][hreflang="x-default"]');
      const xhref = `https://www.travelchinaguide.dpdns.org/${options.canonicalPath}`;
      if (xdef) xdef.href = xhref; else { const xd = document.createElement('link'); xd.setAttribute('rel', 'alternate'); xd.setAttribute('hreflang', 'x-default'); xd.setAttribute('href', xhref); document.head.appendChild(xd); }
    })();
    upsertMetaByProperty('og:url', canonicalHref);
    upsertMetaByName('twitter:url', canonicalHref);

    // OG/image and twitter image
    const ogImage = options && options.ogImage ? options.ogImage : (options && options.heroImage ? options.heroImage : '');
    if (ogImage) {
      upsertMetaByProperty('og:image', ogImage);
      upsertMetaByName('twitter:image', ogImage);
    }

    // If a heroImage is provided, set the main image src
    if (options && options.heroImage) {
      const heroImg = document.getElementById('city-image');
      if (heroImg) {
        heroImg.setAttribute('src', options.heroImage);
        heroImg.setAttribute('alt', t.cityName || '');
      }
    }

    // hero subtitle
    const citySub = document.getElementById('city-sub'); if (citySub) citySub.textContent = t.heroSubtitle || t.metaDesc || '';

    // badges
    const badges = [
      { icon: '🗓️', en: 'Best: Apr–May, Sep–Oct', zh: '最佳: 4-5月, 9-10月' },
      { icon: '🕒', en: 'Time zone: UTC+8', zh: '时区: UTC+8' },
      { icon: '💱', en: 'Currency: CNY (¥)', zh: '货币: 人民币 (¥)' }
    ];
    const badgesContainer = document.getElementById('hero-badges');
    if (badgesContainer) {
      badgesContainer.innerHTML = badges.map(b => `<span class="bg-white/10 backdrop-blur-sm text-sm px-3 py-1 rounded-full">${b.icon} ${lang === 'zh-CN' ? b.zh : b.en}</span>`).join('');
    }

    // back link
    const backLink = document.getElementById('back-link');
    if (backLink) {
      backLink.setAttribute('href', `./index.html?lang=${encodeURIComponent(lang)}`);
      backLink.textContent = t.backText || '← Back';
    }

    // apply navigation labels (use t where available, otherwise language map)
    function applyNavLabels(translationsForPage) {
      const navMap = {
        'en': { navHome: 'Home', navCities: 'Popular Cities', navNature: 'Nature', navCulture: 'Culture' },
        'zh-CN': { navHome: '首页', navCities: '热门城市', navNature: '自然风光', navCulture: '文化' },
        'ja': { navHome: 'ホーム', navCities: '人気の都市', navNature: '自然', navCulture: '文化' },
        'ko': { navHome: '홈', navCities: '인기 도시', navNature: '자연', navCulture: '문화' },
        'ru': { navHome: 'Главная', navCities: 'Популярные города', navNature: 'Природа', navCulture: 'Культура' },
        'fr': { navHome: 'Accueil', navCities: 'Villes populaires', navNature: 'Nature', navCulture: 'Culture' },
        'de': { navHome: 'Startseite', navCities: 'Beliebte Städte', navNature: 'Natur', navCulture: 'Kultur' },
        'es': { navHome: 'Inicio', navCities: 'Ciudades populares', navNature: 'Naturaleza', navCulture: 'Cultura' }
      };
      const chosen = navMap[lang] || navMap[lang.split('-')[0]] || navMap['en'];
      document.querySelectorAll('[data-lang-key]').forEach(el => {
        const key = el.getAttribute('data-lang-key');
        if (!key) return;
        // prefer page translations (t) if they include the key (e.g., city names)
        if (translationsForPage && translationsForPage[key]) {
          el.textContent = translationsForPage[key];
        } else if (chosen && chosen[key]) {
          el.textContent = chosen[key];
        }
      });
    }

    // call with the page translations object if present
    try { applyNavLabels(t); } catch (e) { applyNavLabels(null); }
  }

  // expose
  window.getLang = getLang;
  window.applyCityContent = applyCityContent;
})();

/* Language Switcher Module for City Pages */
(function () {
  const supportedLangs = { 'en': 'English', 'zh-CN': '中文', 'ja': '日本語', 'ko': '한국어', 'ru': 'Русский', 'fr': 'Français', 'de': 'Deutsch', 'es': 'Español' };

  function initLanguageSwitcher() {
    const container = document.getElementById('language-switcher');
    if (!container) return;
    if (container.children.length > 0) return; // Already populated

    let currentLang = document.documentElement.lang || 'en';

    // Build Dropdown
    const dropdown = document.createElement('div');
    dropdown.className = 'relative inline-block text-left lang-dropdown';

    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'lang-btn text-sm font-semibold py-2 px-4 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 flex items-center gap-2 bg-white';
    toggle.innerHTML = `
      <svg class="h-4 w-4 text-gray-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path><path d="M2.05 6.05h19.9M2.05 17.95h19.9M12 2.05v19.9"/></svg>
      <span class="ml-2">${supportedLangs[currentLang] || currentLang.toUpperCase()}</span>
      <svg class="h-4 w-4 text-gray-600 ml-2" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.24a.75.75 0 01-1.06 0L5.21 8.29a.75.75 0 01.02-1.08z" clip-rule="evenodd" /></svg>`;

    const menu = document.createElement('div');
    menu.className = 'hidden origin-top-right absolute right-0 mt-2 w-36 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50';
    const menuInner = document.createElement('div');
    menuInner.className = 'py-1';

    Object.entries(supportedLangs).forEach(([code, name]) => {
      const item = document.createElement('button');
      item.className = 'w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center justify-between';
      item.innerHTML = `<span>${name}</span>${code === currentLang ? '<svg class="h-4 w-4 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>' : ''}`;

      item.addEventListener('click', () => {
        // Navigate to static page
        const pathParts = window.location.pathname.split('/').filter(p => p);
        let pageName = pathParts.pop() || 'index.html';

        // If current path ends in a lang code (root dirs), pageName might be the code.
        if (Object.keys(supportedLangs).includes(pageName)) {
          // e.g. /fr/ -> pop is 'fr'. Page is index.html
          pageName = 'index.html';
        }
        // If pageName is just empty (root /), handled by || 'index.html'

        // Clean pageName of any existing lang prefix logic?
        // Actually, we just want the filename.
        // If we are at /zh-CN/beijing.html, pageName is beijing.html.

        let newUrl = '';
        if (code === 'en') {
          newUrl = '/' + pageName;
        } else {
          newUrl = '/' + code + '/' + pageName;
        }
        window.location.href = newUrl;
      });
      menuInner.appendChild(item);
    });

    menu.appendChild(menuInner);
    dropdown.appendChild(toggle);
    dropdown.appendChild(menu);
    container.appendChild(dropdown);

    // Toggle logic
    toggle.addEventListener('click', (e) => { e.stopPropagation(); menu.classList.toggle('hidden'); });
    document.addEventListener('click', () => menu.classList.add('hidden'));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLanguageSwitcher);
  } else {
    initLanguageSwitcher();
  }
})();
