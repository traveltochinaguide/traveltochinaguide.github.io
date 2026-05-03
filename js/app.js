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
            dot.setAttribute('aria-pressed', String(i === index));
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

 // Language switcher dropdown is now created exclusively by lang-switcher.js
 // (Previously both app.js and lang-switcher.js created duplicate dropdowns)

 // Carousel Init
    const carouselData = [
        { id: 'great-wall', titleKey: 'carouselTitle1', subtitleKey: 'carouselSubtitle1', altKey: 'carouselAlt1', dotKey: 'carouselDot1', imgQuery: 'great wall,china' },
        { id: 'shanghai', titleKey: 'carouselTitle2', subtitleKey: 'carouselSubtitle2', altKey: 'carouselAlt2', dotKey: 'carouselDot2', imgQuery: 'shanghai,skyline' },
        { id: 'guilin', titleKey: 'carouselTitle3', subtitleKey: 'carouselSubtitle3', altKey: 'carouselAlt3', dotKey: 'carouselDot3', imgQuery: 'guilin,li river' },
        { id: 'xian', titleKey: 'carouselTitle4', subtitleKey: 'carouselSubtitle4', altKey: 'carouselAlt4', dotKey: 'carouselDot4', imgQuery: 'terracotta army,xian' }
    ];

    if (carouselContainer && window.translations && window.translations[currentLang]) {
        const t = window.translations[currentLang];
        const fragment = document.createDocumentFragment();
        const dotsFragment = document.createDocumentFragment();
        carouselData.forEach((slide, index) => {
            // All 4 slides are now created dynamically (incl. index 0 = Great Wall).
            // The first slide starts visible (opacity-100); rest are hidden (opacity-0).
            const slideEl = document.createElement('div');
            slideEl.className = `carousel-slide absolute inset-0 w-full h-full ${index === 0 ? 'opacity-100' : 'opacity-0'}`;

            const shanghaiImg = '/images/hero-shanghai.webp';
            const guilinImg = '/images/hero-guilin.webp';
            const xianImg = '/images/hero-xian.webp';
            let imgSrc = '/images/hero-great-wall.webp';

            if (slide.id === 'shanghai') imgSrc = shanghaiImg;
            if (slide.id === 'guilin') imgSrc = guilinImg;
            if (slide.id === 'xian') imgSrc = xianImg;

            slideEl.innerHTML = `<div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <img loading="${index === 0 ? 'eager' : 'lazy'}" decoding="async" src="${imgSrc}" width="1920" height="1080" class="w-full h-full object-cover" alt="${t[slide.altKey] || slide.imgQuery}"${index === 0 ? ' fetchpriority="high"' : ''}>
            <div class="absolute inset-0 flex items-center justify-center"><div class="text-center text-white p-8 max-w-3xl">
            <h2 class="text-5xl md:text-7xl font-extrabold mb-4 text-shadow-lg">${t[slide.titleKey]}</h2>
            <p class="text-xl md:text-2xl text-shadow">${t[slide.subtitleKey]}</p></div></div>`;

            // Use DocumentFragment to batch DOM insertions (single reflow)
            fragment.appendChild(slideEl);

            const dot = document.createElement('button');
            dot.className = 'carousel-dot w-3 h-3 bg-white/50 rounded-full';
            dot.setAttribute('role', 'button');
            dot.setAttribute('tabindex', '0');
            dot.setAttribute('aria-label', t[slide.dotKey] || ('Slide ' + (index + 1)));
            dot.setAttribute('aria-pressed', String(index === 0));
            dot.addEventListener('click', () => { showSlide(index); stopCarousel(); startCarousel(); });
            dot.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') { showSlide(index); stopCarousel(); startCarousel(); e.preventDefault(); }
            });
            dotsFragment.appendChild(dot);
        });
        // Append all carousel slides and dots in single DOM operations
        if (carouselDotsContainer) {
            carouselDotsContainer.appendChild(dotsFragment);
        }
        carouselContainer.insertBefore(fragment, carouselDotsContainer);
    }

    if (document.getElementById('prev-slide')) document.getElementById('prev-slide').addEventListener('click', () => { prevSlide(); stopCarousel(); startCarousel(); });
    if (document.getElementById('next-slide')) document.getElementById('next-slide').addEventListener('click', () => { nextSlide(); stopCarousel(); startCarousel(); });
    if (carouselContainer) {
        carouselContainer.addEventListener('mouseenter', stopCarousel);
        carouselContainer.addEventListener('mouseleave', startCarousel);
    }
    // Keyboard accessibility: arrow key navigation when carousel container is focused
    if (carouselContainer) {
        carouselContainer.setAttribute('tabindex', '0');
        carouselContainer.setAttribute('role', 'region');
        carouselContainer.setAttribute('aria-label', 'Carousel');
        carouselContainer.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') { prevSlide(); stopCarousel(); startCarousel(); e.preventDefault(); }
            if (e.key === 'ArrowRight') { nextSlide(); stopCarousel(); startCarousel(); e.preventDefault(); }
        });
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
