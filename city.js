/* Shared helper for city pages
   - Provides getLang() and applyCityContent(t, options)
   - options: { canonicalPath, ogImage, heroImage }
*/
(function(){
  function getLang() {
    try {
      const params = new URLSearchParams(window.location.search);
      const l = params.get('lang');
      if (l) return l;
    } catch(e) {}
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

  function applyCityContent(t, options){
    const lang = getLang();
    // Title and meta
    if (t.pageTitle) document.getElementById('page-title').textContent = t.pageTitle;
    const metaDesc = document.getElementById('meta-desc'); if (metaDesc && t.metaDesc) metaDesc.setAttribute('content', t.metaDesc);

    // City header and content
    const nameEl = document.getElementById('city-name'); if (nameEl) nameEl.innerHTML = t.cityName || '';
    const contentEl = document.getElementById('city-content'); if (contentEl) contentEl.innerHTML = t.contentHtml || t.longDesc || '';

    // Canonical + OG/Twitter url
    const canonical = document.querySelector('link[rel="canonical"]');
    if (canonical && options && options.canonicalPath) {
      canonical.href = `https://www.travelchinaguide.dpdns.org/${options.canonicalPath}${lang ? `?lang=${encodeURIComponent(lang)}` : ''}`;
    }
    const canonicalHref = canonical ? canonical.href : window.location.href;
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
    function applyNavLabels(translationsForPage){
      const navMap = {
        'en': { navHome: 'Home', navCities: 'Popular Cities', navNature: 'Nature' },
        'zh-CN': { navHome: '首页', navCities: '热门城市', navNature: '自然风光' },
        'ja': { navHome: 'ホーム', navCities: '人気の都市', navNature: '自然' },
        'ko': { navHome: '홈', navCities: '인기 도시', navNature: '자연' },
        'ru': { navHome: 'Главная', navCities: 'Популярные города', navNature: 'Природа' },
        'fr': { navHome: 'Accueil', navCities: 'Villes populaires', navNature: 'Nature' },
        'de': { navHome: 'Startseite', navCities: 'Beliebte Städte', navNature: 'Natur' },
        'es': { navHome: 'Inicio', navCities: 'Ciudades populares', navNature: 'Naturaleza' }
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
