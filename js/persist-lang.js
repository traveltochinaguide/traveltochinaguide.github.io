(function(){
  'use strict';
  function getPreferredLang(){
    try{
      const p = new URLSearchParams(location.search).get('lang');
      if(p) return p;
    }catch(e){}
    try{ const ls = localStorage.getItem('preferredLanguage'); if(ls) return ls; }catch(e){}
    return navigator.language || navigator.userLanguage || 'en';
  }

  function isLocalHtmlLink(href){
    if(!href) return false;
    if(href.startsWith('mailto:') || href.startsWith('tel:')) return false;
    // absolute http(s) to other origin: avoid
    try{
      const u = new URL(href, location.href);
      if(u.origin !== location.origin) return false;
      return u.pathname.endsWith('.html');
    }catch(e){
      // relative link, treat as html if endsWith .html
      return href.split('?')[0].endsWith('.html');
    }
  }

  function ensureLangParam(url, lang){
    if(!lang) return url;
    try{
      const u = new URL(url, location.href);
      if(!u.searchParams.has('lang')) u.searchParams.set('lang', lang);
      return u.pathname + (u.search?('?'+u.searchParams.toString()):'') + (u.hash||'');
    }catch(e){
      // fallback for relative
      if(url.indexOf('?') === -1) return url + '?lang=' + encodeURIComponent(lang);
      return url + '&lang=' + encodeURIComponent(lang);
    }
  }

  // delegated click handler for nav links to preserve current language
  document.addEventListener('click', function(e){
    const a = e.target.closest && e.target.closest('a');
    if(!a) return;
    // only intercept internal html navigation from header/site nav or dropdowns
    const navAreas = ['.site-nav','.nav-links','.dropdown-panel','#primary-nav','header','.site-header'];
    let inNav = false;
    for(const s of navAreas){ if(a.closest && a.closest(s)){ inNav = true; break; } }
    if(!inNav) return;

    const href = a.getAttribute('href');
    if(!href) return;
    if(!isLocalHtmlLink(href)) return;

    // compute lang at click-time so it reflects any recent change
    const lang = getPreferredLang();
    // build final url and navigate
    try{
      const u = new URL(href, location.href);
      if(!u.searchParams.has('lang')) u.searchParams.set('lang', lang);
      e.preventDefault();
      location.href = u.pathname + (u.search?('?'+u.searchParams.toString()):'') + (u.hash||'');
    }catch(err){
      e.preventDefault();
      const final = ensureLangParam(href, lang);
      location.href = final;
    }
  }, true);

  // also update anchor hrefs in the nav so middle-click / open in new tab carry the param
  function patchNavAnchors(){
    const lang = getPreferredLang();
    document.querySelectorAll('.site-nav a, .nav-links a, .dropdown-panel a, #primary-nav a, header a').forEach(a => {
      const href = a.getAttribute('href');
      if(!href) return;
      if(!isLocalHtmlLink(href)) return;
      try{
        const u = new URL(href, location.href);
        if(!u.searchParams.has('lang')){
          a.setAttribute('href', u.pathname + (u.search?('?'+u.searchParams.toString()):'') + (u.hash||''));
          // ensure lang param present
          if(!a.href.includes('lang=')){
            a.setAttribute('href', ensureLangParam(a.getAttribute('href'), lang));
          }
        }
      }catch(e){
        // relative fallback
        if(!href.includes('lang=')) a.setAttribute('href', ensureLangParam(href, lang));
      }
    });
  }

  // run on DOM ready and after a short delay to let other scripts (that set preferredLanguage) run
  document.addEventListener('DOMContentLoaded', function(){
    patchNavAnchors();
    setTimeout(patchNavAnchors, 300);
  });

})();
