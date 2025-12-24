(function () {
  'use strict';

  // Only run on the root/English page to determine if a redirect is needed
  // The static pages (e.g. /zh-CN/) have their own lang attribute set and shouldn't redirect back to English automatically
  // unless we wanted to enforce "English preferred" but that's annoying.
  // Usually we only redirect FROM default TO specific.

  const htmlLang = document.documentElement.lang;
  const isRoot = (!htmlLang || htmlLang === 'en');

  if (isRoot) {
    try {
      // 1. Check Local Storage
      const stored = localStorage.getItem('preferredLanguage');

      // 2. Check Browser Language if no storage
      const browser = navigator.language || navigator.userLanguage;
      // Extract 'zh', 'en', etc.
      const shortBrowser = browser ? browser.split('-')[0] : null;

      let targetLang = null;

      if (stored && stored !== 'en') {
        targetLang = stored;
      } else if (!stored && shortBrowser) {
        // List of supported langs matches our build script/folders
        const supported = ['zh', 'ja', 'ko', 'ru', 'fr', 'de', 'es'];

        // specific check for zh-CN vs zh-TW? Our site uses zh-CN.
        // If browser is 'zh', we map to 'zh-CN'.
        if (shortBrowser === 'zh') targetLang = 'zh-CN';
        else if (supported.includes(shortBrowser)) targetLang = shortBrowser;
      }

      if (targetLang) {
        // Construct target URL
        // If current is /index.html, target is /targetLang/index.html
        // If current is /beijing.html, target is /targetLang/beijing.html

        // Get current filename
        const path = window.location.pathname;
        const filename = path.split('/').pop() || 'index.html';

        // Prevent infinite redirect loops if something is wrong
        // (e.g. if we are already in a folder but html lang claims en - shouldn't happen with correct build)

        // Standardize target check
        const validLangs = ['zh-CN', 'ja', 'ko', 'ru', 'fr', 'de', 'es'];
        if (validLangs.includes(targetLang)) {
          const newUrl = `/${targetLang}/${filename}`;
          // Perform redirect
          window.location.replace(newUrl);
        }
      }
    } catch (e) {
      console.warn('Language redirect failed', e);
    }
  }
})();
