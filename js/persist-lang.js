(function () {
 'use strict';

 // Only run on the root/English page to determine if a redirect is needed
 // The static pages (e.g. /zh-CN/) have their own lang attribute set and shouldn't redirect back to English automatically

 const htmlLang = document.documentElement.lang;
 const isRoot = (!htmlLang || htmlLang === 'en');

 if (isRoot) {
  try {
   // 1. Check Local Storage
   const stored = localStorage.getItem('preferredLanguage');

   // 2. Check Browser Language if no storage
   const browser = navigator.language || navigator.userLanguage;
   // Extract primary language tag (e.g. 'zh-CN' -> 'zh', 'zh-Hans' -> 'zh')
   const parts = browser ? browser.split('-') : [];
   const shortBrowser = parts[0] || null;
   const region = parts[1] || null;

   let targetLang = null;

   if (stored && stored !== 'en') {
    targetLang = stored;
   } else if (!stored && shortBrowser) {
    // Map browser language to our supported langs
    // zh-CN: Simplified Chinese (our site uses zh-CN)
    // zh-Hans: also Simplified Chinese
    // zh-Hant: Traditional Chinese (not supported, fall back to zh-CN)
    if (shortBrowser === 'zh') {
     // If browser specifies region (e.g. zh-CN, zh-SG, zh-Hans), prefer it
     // Otherwise default to zh-CN
     targetLang = (region && ['CN', 'SG', 'Hans'].includes(region)) ? 'zh-CN' : 'zh-CN';
    } else if (['ja', 'ko', 'ru', 'fr', 'de', 'es'].includes(shortBrowser)) {
     targetLang = shortBrowser;
    }
   }

   if (targetLang) {
    // Get current filename
    const path = window.location.pathname;
    const filename = path.split('/').pop() || 'index.html';

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