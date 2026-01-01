document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const languageSwitcher = document.getElementById('language-switcher');
    const mainContent = document.getElementById('main-content');
    const carouselContainer = document.getElementById('hero-carousel');
    const carouselDotsContainer = document.getElementById('carousel-dots');
    const cityGrid = document.getElementById('city-card-grid');
    const modal = document.getElementById('city-detail-modal');
    const modalContent = document.getElementById('city-detail-modal-content');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const modalCityName = document.getElementById('modal-city-name');
    const modalCityImage = document.getElementById('modal-city-image');
    const modalCityDescription = document.getElementById('modal-city-description');

    // Get current language from the injected global variable (set by build script)
    // Fallback to 'en' if undefined (e.g. local dev without build)
    const currentLang = window.currentLang || 'en';

    let currentSlide = 0;
    let slideInterval;
    let currentOpenCityId = null;

    // --- CORE FUNCTIONS ---

    // Note: client-side text replacement (translateElement, updateMetaTags) is REMOVED 
    // because the HTML is now statically generated with the correct language content.

    const updateActiveButton = (activeLang) => {
        // update the compact toggle label
        const langCurrent = document.getElementById('lang-current');
        if (langCurrent && supportedLangs[activeLang]) langCurrent.textContent = supportedLangs[activeLang];

        // update menu items
        document.querySelectorAll('.lang-option').forEach(item => {
            const check = item.querySelector('.check-icon');
            if (item.getAttribute('data-lang') === activeLang) {
                check && check.classList.remove('hidden');
                item.classList.add('font-semibold');
                item.setAttribute('aria-checked', 'true');
            } else {
                check && check.classList.add('hidden');
                item.classList.remove('font-semibold');
                item.setAttribute('aria-checked', 'false');
            }
        });

        const toggleEl = document.getElementById('lang-toggle');
        if (toggleEl) {
            toggleEl.setAttribute('data-lang', activeLang);
        }
    };

    // Carousel Functions
    const updateCarouselDots = (index) => {
        document.querySelectorAll('.carousel-dot').forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
    };

    const showSlide = (index) => {
        const slides = document.querySelectorAll('.carousel-slide');
        if (index >= slides.length) index = 0;
        if (index < 0) index = slides.length - 1;
        slides.forEach((slide, i) => {
            slide.classList.toggle('opacity-0', i !== index);
            slide.classList.toggle('opacity-100', i === index);
        });
        currentSlide = index;
        updateCarouselDots(index);
    };
    const nextSlide = () => showSlide(currentSlide + 1);
    const prevSlide = () => showSlide(currentSlide - 1);
    const startCarousel = () => { stopCarousel(); slideInterval = setInterval(nextSlide, 5000); };
    const stopCarousel = () => clearInterval(slideInterval);

    // City Detail Modal Functions
    const showCityModal = (cityId) => {
        // Use injected window.cityDetails and window.translations
        if (!window.cityDetails || !window.translations) return;

        const city = window.cityDetails[cityId];
        if (!city) return;
        currentOpenCityId = cityId;

        const t = window.translations[currentLang];

        if (t && t[city.nameKey]) {
            modalCityName.textContent = t[city.nameKey];
            // Use WebP if available (simple check: replace ext)
            let imgSrc = city.localImg || '/images/hero-great-wall.webp';
            if (imgSrc.endsWith('.jpg')) imgSrc = imgSrc.replace('.jpg', '.webp');

            modalCityImage.src = imgSrc;
            modalCityImage.alt = t[city.nameKey];
            modalCityDescription.innerHTML = t[city.longDescKey];

            modal.classList.remove('hidden');
            setTimeout(() => {
                modal.classList.remove('opacity-0');
                modalContent.classList.remove('scale-95', 'opacity-0');
            }, 10);
        }
    };

    const hideCityModal = () => {
        modal.classList.add('opacity-0');
        modalContent.classList.add('scale-95', 'opacity-0');
        setTimeout(() => {
            modal.classList.add('hidden');
        }, 300);
    };

    // --- INITIALIZATION ---
    const supportedLangs = { 'en': 'EN', 'zh-CN': '中', 'ja': '日', 'ko': '한', 'ru': 'РУ', 'fr': 'FR', 'de': 'DE', 'es': 'ES' };

    // Build an accessible dropdown language selector
    const dropdown = document.createElement('div');
    dropdown.className = 'relative inline-block text-left lang-dropdown';

    const toggle = document.createElement('button');
    toggle.id = 'lang-toggle';
    toggle.type = 'button';
    toggle.setAttribute('aria-haspopup', 'true');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.className = 'lang-btn text-sm font-semibold py-2 px-4 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 flex items-center gap-2 bg-white';
    toggle.innerHTML = `
    <svg class="h-4 w-4 text-gray-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path><path d="M2.05 6.05h19.9M2.05 17.95h19.9M12 2.05v19.9"/></svg>
    <span id="lang-current" class="ml-2">${supportedLangs[currentLang] || 'EN'}</span>
    <svg class="h-4 w-4 text-gray-600 ml-2" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.24a.75.75 0 01-1.06 0L5.21 8.29a.75.75 0 01.02-1.08z" clip-rule="evenodd" /></svg>`;

    dropdown.appendChild(toggle);

    const menu = document.createElement('div');
    menu.id = 'lang-menu';
    menu.className = 'hidden origin-top-right absolute right-0 mt-2 w-36 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50';
    const menuInner = document.createElement('div');
    menuInner.className = 'py-1';
    menuInner.setAttribute('role', 'menu');
    menuInner.setAttribute('aria-orientation', 'vertical');
    menuInner.setAttribute('aria-labelledby', 'lang-toggle');

    Object.entries(supportedLangs).forEach(([code, name]) => {
        const item = document.createElement('button');
        item.type = 'button';
        item.className = 'w-full text-left px-4 py-2 text-sm lang-option';
        item.setAttribute('data-lang', code);
        item.setAttribute('role', 'menuitem');
        item.setAttribute('aria-checked', 'false');
        item.innerHTML = `
        <span class="flex items-center justify-between w-full">
            <span class="truncate">${name} <span class="ml-2 text-xs text-gray-500">(${code})</span></span>
            <svg class="check-icon hidden h-4 w-4 text-green-600 flex-shrink-0" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="4 11 8 15 16 6"></polyline></svg>
        </span>`;
        item.addEventListener('click', () => {
            // Save preference
            localStorage.setItem('preferredLanguage', code);

            // Static URL Navigation Logic
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
    if (languageSwitcher) languageSwitcher.appendChild(dropdown);

    // Dropdown open/close helpers
    const langToggle = document.getElementById('lang-toggle');
    const langMenu = document.getElementById('lang-menu');
    function openLangMenu() { langMenu.classList.remove('hidden'); langToggle.setAttribute('aria-expanded', 'true'); }
    function closeLangMenu() { langMenu.classList.add('hidden'); langToggle.setAttribute('aria-expanded', 'false'); }
    function toggleLangMenu() { if (langMenu.classList.contains('hidden')) openLangMenu(); else closeLangMenu(); }

    if (langToggle) langToggle.addEventListener('click', (e) => { e.stopPropagation(); toggleLangMenu(); });
    document.addEventListener('click', (e) => { if (dropdown && !dropdown.contains(e.target)) closeLangMenu(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeLangMenu(); });

    // Carousel Init
    const carouselData = [
        { id: 'great-wall', titleKey: 'carouselTitle1', subtitleKey: 'carouselSubtitle1', imgQuery: 'great wall,china' },
        { id: 'shanghai', titleKey: 'carouselTitle2', subtitleKey: 'carouselSubtitle2', imgQuery: 'shanghai,skyline' },
        { id: 'guilin', titleKey: 'carouselTitle3', subtitleKey: 'carouselSubtitle3', imgQuery: 'guilin,li river' },
        { id: 'xian', titleKey: 'carouselTitle4', subtitleKey: 'carouselSubtitle4', imgQuery: 'terracotta army,xian' }
    ];

    if (carouselContainer && window.translations && window.translations[currentLang]) {
        const t = window.translations[currentLang];
        carouselData.forEach((slide, index) => {
            if (index === 0) return; // Skip first slide
            const slideEl = document.createElement('div');
            slideEl.className = 'carousel-slide absolute inset-0 w-full h-full opacity-0';

            const shanghaiImg = '/images/hero-shanghai.webp';
            const guilinImg = '/images/hero-guilin.webp';
            const xianImg = '/images/hero-xian.webp';
            let imgSrc = '/images/hero-great-wall.webp';

            if (slide.id === 'shanghai') imgSrc = shanghaiImg;
            if (slide.id === 'guilin') imgSrc = guilinImg;
            if (slide.id === 'xian') imgSrc = xianImg;

            slideEl.innerHTML = `<div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <img loading="lazy" decoding="async" src="${imgSrc}" width="1920" height="1080" class="w-full h-full object-cover" alt="${slide.imgQuery}">
            <div class="absolute inset-0 flex items-center justify-center"><div class="text-center text-white p-8 max-w-3xl">
            <h2 class="text-5xl md:text-7xl font-extrabold mb-4 text-shadow-lg">${t[slide.titleKey]}</h2>
            <p class="text-xl md:text-2xl text-shadow">${t[slide.subtitleKey]}</p></div></div>`;

            carouselContainer.insertBefore(slideEl, carouselDotsContainer);

            const dot = document.createElement('button');
            dot.className = 'carousel-dot w-3 h-3 bg-white/50 rounded-full';
            dot.addEventListener('click', () => { showSlide(index); stopCarousel(); });
            if (carouselDotsContainer) carouselDotsContainer.appendChild(dot);
        });
    }

    if (document.getElementById('prev-slide')) document.getElementById('prev-slide').addEventListener('click', () => { prevSlide(); stopCarousel(); startCarousel(); });
    if (document.getElementById('next-slide')) document.getElementById('next-slide').addEventListener('click', () => { nextSlide(); stopCarousel(); startCarousel(); });
    if (carouselContainer) {
        carouselContainer.addEventListener('mouseenter', stopCarousel);
        carouselContainer.addEventListener('mouseleave', startCarousel);
    }

    // CITY MODAL TRIGGERS
    if (cityGrid) {
        cityGrid.addEventListener('click', (e) => {
            const btn = e.target.closest('button[data-city-id]');
            if (btn) {
                const cityId = btn.getAttribute('data-city-id');
                showCityModal(cityId);
            }
        });
    }

    if (modalCloseBtn) modalCloseBtn.addEventListener('click', hideCityModal);
    if (modal) modal.addEventListener('click', (e) => { if (e.target === modal) hideCityModal(); });

    // Initialize UI
    updateActiveButton(currentLang);
    showSlide(0);
    startCarousel();
});
