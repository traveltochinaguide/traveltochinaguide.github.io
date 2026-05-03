/**
 * Language Switcher Module
 * Shared across all pages — index and city pages.
 * Reads window.currentLang (injected by generate-multilang.js build).
 */
(function () {
  'use strict';

  const currentLang = window.currentLang || document.documentElement.lang || 'en';

  const supportedLangs = {
    'en': 'EN',
    'zh-CN': '中',
    'ja': '日',
    'ko': '한',
    'ru': 'РУ',
    'fr': 'FR',
    'de': 'DE',
    'es': 'ES'
  };

  function init() {
    const container = document.getElementById('language-switcher');
    if (!container) return;
    // Skip if already populated (e.g. by app.js on index page)
    if (container.querySelector('.lang-dropdown')) return;

    const dropdown = document.createElement('div');
    dropdown.className = 'relative inline-block text-left lang-dropdown';

    const toggle = document.createElement('button');
    toggle.id = 'lang-toggle';
    toggle.type = 'button';
    toggle.setAttribute('aria-haspopup', 'true');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-activedescendant', '');
    toggle.setAttribute('aria-label', 'Select language');
    toggle.className = 'lang-btn text-sm font-semibold py-2 px-4 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 flex items-center gap-2 bg-white';
    toggle.innerHTML = `
      <svg class="h-4 w-4 text-gray-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path><path d="M2.05 6.05h19.9M2.05 17.95h19.9M12 2.05v19.9"/></svg>
      <span id="lang-current" class="ml-2">${supportedLangs[currentLang] || 'EN'}</span>
      <svg class="h-4 w-4 text-gray-600 ml-2" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.24a.75.75 0 01-1.06 0L5.21 8.29a.75.75 0 01.02-1.08z" clip-rule="evenodd" /></svg>`;

    dropdown.appendChild(toggle);

  const menu = document.createElement('div');
  menu.id = 'lang-menu';
  menu.className = 'lang-menu hidden origin-top-right absolute right-0 mt-2 w-36 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50';
  menu.setAttribute('role', 'menu');
  menu.setAttribute('tabindex', '-1');
    const menuInner = document.createElement('div');
    menuInner.className = 'py-1';
    menuInner.setAttribute('role', 'menu');

    Object.entries(supportedLangs).forEach(([code, name]) => {
      const item = document.createElement('button');
      item.type = 'button';
      item.className = 'w-full text-left px-4 py-2 text-sm lang-option lang-menu-item';
      item.setAttribute('data-lang', code);
      item.setAttribute('role', 'menuitem');
      item.id = 'lang-menu-item-' + code;
      item.innerHTML = `
        <span class="flex items-center justify-between w-full">
          <span class="truncate">${name} <span class="ml-2 text-xs text-gray-500">(${code})</span></span>
          ${code === currentLang ? '<svg class="h-4 w-4 text-green-600 flex-shrink-0" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 11 8 15 16 6"></polyline></svg>' : ''}
        </span>`;
      item.addEventListener('click', () => {
        localStorage.setItem('preferredLanguage', code);
        const path = window.location.pathname;
        let parts = path.split('/').filter(p => p);
        const knownLangs = Object.keys(supportedLangs);
        let pageName = 'index.html';
        if (parts.length > 0 && knownLangs.includes(parts[0])) {
          pageName = parts[1] || 'index.html';
        } else {
          pageName = parts[0] || 'index.html';
        }
        const newUrl = (code === 'en') ? '/' + pageName : '/' + code + '/' + pageName;
        window.location.href = newUrl;
      });
      menuInner.appendChild(item);
    });

    menu.appendChild(menuInner);
    dropdown.appendChild(menu);
    container.appendChild(dropdown);

// Toggle open/close
 function openMenu() { menu.classList.remove('hidden'); menu.classList.add('open'); toggle.setAttribute('aria-expanded', 'true'); }
 function closeMenu() { menu.classList.add('hidden'); menu.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
 toggle.addEventListener('click', (e) => { e.stopPropagation(); menu.classList.contains('hidden') ? openMenu() : closeMenu(); });
    document.addEventListener('click', (e) => { if (!dropdown.contains(e.target)) closeMenu(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMenu(); });

    // ── WAI-ARIA menu keyboard navigation ──
    // Tracks which item index is currently "active" (highlighted) for aria-activedescendant
    let activeIndex = -1;
    const menuItems = [];

    // Build the menuItems array after all items are appended
    menuInner.querySelectorAll('.lang-menu-item').forEach((item, i) => {
      menuItems.push(item);
    });

    function setActiveItem(index) {
      // Clear previous active highlight
      menuItems.forEach(mi => mi.classList.remove('lang-menu-item-active'));
      // Wrap around
      if (index < 0) index = menuItems.length - 1;
      if (index >= menuItems.length) index = 0;
      activeIndex = index;
      const item = menuItems[index];
      item.classList.add('lang-menu-item-active');
      // Update aria-activedescendant on the toggle button
      toggle.setAttribute('aria-activedescendant', item.id);
      // Scroll item into view if needed (for long menus)
      item.scrollIntoView({ block: 'nearest' });
    }

    function clickActiveItem() {
      if (activeIndex >= 0 && menuItems[activeIndex]) {
        menuItems[activeIndex].click();
      } else {
        closeMenu();
      }
    }

    menu.addEventListener('keydown', (e) => {
      if (!menu.classList.contains('hidden')) {
        switch (e.key) {
          case 'ArrowDown':
            e.preventDefault();
            setActiveItem(activeIndex + 1);
            break;
          case 'ArrowUp':
            e.preventDefault();
            setActiveItem(activeIndex - 1);
            break;
          case 'Home':
            e.preventDefault();
            setActiveItem(0);
            break;
          case 'End':
            e.preventDefault();
            setActiveItem(menuItems.length - 1);
            break;
          case 'Enter':
          case ' ':
            e.preventDefault();
            clickActiveItem();
            break;
        }
      }
    });

    // When menu opens via toggle click, reset active to current lang
    toggle.addEventListener('click', () => {
      activeIndex = menuItems.findIndex(item => item.getAttribute('data-lang') === currentLang);
      if (activeIndex === -1) activeIndex = 0;
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
