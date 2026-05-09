const fs = require('fs-extra');
const path = require('path');
const cheerio = require('cheerio');
// Import the new external translations (contains index.html data + global nav)
const { translations: globalTranslations, cityDetails } = require('../js/translations.js');

const langs = ['en', 'zh-CN', 'ja', 'ko', 'ru', 'fr', 'de', 'es'];
const pages = [
 'index.html',
 'beijing.html',
 'shanghai.html',
 'xian.html',
 'guilin.html',
 'zhangjiajie.html',
 'jiuzhaigou.html',
 'yangtze.html',
 'chengdu.html',
 'hangzhou.html',
 'xiamen.html',
 'suzhou.html',
 'iching.html',
 'food.html',
 'peking-duck.html',
 'dim-sum.html',
 'hotpot.html',
 'dumplings.html',
 'visa.html',
 'greatwall.html',
 'architecture.html',
 'calligraphy.html',
 'chongqing.html',
 'clothing.html',
 'dali.html',
 'festivals.html',
 'gardens.html',
 'guangzhou.html',
 'huangshan.html',
 'kunming.html',
 'language.html',
 'lijiang.html',
 'martialarts.html',
 'medicine.html',
 'music.html',
 'opera.html',
 'painting.html',
 'paper.html',
 'pottery.html',
 'shenzhen.html',
 'silk.html',
 'tea.html'
];

// Sitemap configuration
const sitemapPriorities = {
    'index.html': '1.0',
    'default': '0.8'
};
const sitemapFreq = {
    'index.html': 'daily',
    'default': 'weekly'
};

const rootDir = path.resolve(__dirname, '..');
const baseUrl = 'https://travelchinaguide.dpdns.org'; // Custom domain

function getTodayStr() {
    return new Date().toISOString().split('T')[0];
}

(async () => {
    console.log('Starting multi-language static generation with SEO optimizations...');

    // Store sitemap entries: { loc, lastmod, changefreq, priority }
    const sitemapEntries = [];

    for (const pageName of pages) {
        const filePath = path.join(rootDir, pageName);
        if (!await fs.pathExists(filePath)) {
            console.warn(`File not found: ${filePath}`);
            continue;
        }

        console.log(`Processing ${pageName}...`);
        const html = await fs.readFile(filePath, 'utf-8');

        // --- 1. PRE-PROCESS HTML (WebP Replacement) ---

        let localTranslations = {};

        // Extract inline translations if present (for legacy pages)
        const $temp = cheerio.load(html);
        if (pageName !== 'index.html') {
            const scriptContent = $temp('script').filter((i, el) => {
                const content = $temp(el).html();
                return content && content.includes('const translations =');
            }).html();

            if (scriptContent) {
                try {
                    const match = scriptContent.match(/const translations\s*=\s*(\{[\s\S]*?\});/);
                    if (match && match[1]) {
                        const getTrans = new Function(`return ${match[1]}`);
                        localTranslations = getTrans();
                    }
                } catch (e) {
                    console.error(`Failed to parse inline translations for ${pageName}`, e);
                }
            }
        }

        // Generate files for each lang
        for (const lang of langs) {
            const globalForLang = globalTranslations[lang] || globalTranslations['en'] || {};
            const localForLang = (lang === 'en' && localTranslations['en']) ? localTranslations['en'] : (localTranslations[lang] || localTranslations['en'] || {});

            // Merge global + local + cityDetails for this lang (for the modal)
            const t = { ...globalForLang, ...localForLang };

            // Prepare the minimal data object to be injected
            // We need to provide 'translations[lang]' and 'cityDetails' for the modal to work client-side
            const allCityDetails = { beijing: { imgQuery: 'forbidden city,beijing', localImg: '/images/hero-great-wall.webp', nameKey: 'cityBeijing', descKey: 'descBeijing', longDescKey: 'longDescBeijing' }, shanghai: { imgQuery: 'the bund,shanghai', localImg: '/images/hero-shanghai.webp', nameKey: 'cityShanghai', descKey: 'descShanghai', longDescKey: 'longDescShanghai' }, xian: { imgQuery: 'terracotta army,xian', localImg: '/images/hero-xian.webp', nameKey: 'cityXian', descKey: 'descXian', longDescKey: 'longDescXian' }, guilin: { imgQuery: 'li river,guilin,china', localImg: '/images/hero-guilin.webp', nameKey: 'cityGuilin', descKey: 'descGuilin', longDescKey: 'longDescGuilin' }, zhangjiajie: { imgQuery: 'zhangjiajie,avatar mountain,china', localImg: '/images/hero-zhangjiajie.webp', nameKey: 'cityZhangjiajie', descKey: 'descZhangjiajie', longDescKey: 'longDescZhangjiajie' }, jiuzhaigou: { imgQuery: 'jiuzhaigou,colorful lake,china', localImg: '/images/hero-jiuzhaigou.webp', nameKey: 'cityJiuzhaigou', descKey: 'descJiuzhaigou', longDescKey: 'longDescJiuzhaigou' }, yangtze: { imgQuery: 'yangtze river,three gorges,china', localImg: '/images/hero-yangtze.webp', nameKey: 'cityYangtze', descKey: 'descYangtze', longDescKey: 'longDescYangtze' }, chengdu: { imgQuery: 'chengdu,panda,china', localImg: '/images/hero-chengdu.webp', nameKey: 'cityChengdu', descKey: 'descChengdu', longDescKey: 'longDescChengdu' }, hangzhou: { imgQuery: 'hangzhou,west lake,china', localImg: '/images/hero-hangzhou.webp', nameKey: 'cityHangzhou', descKey: 'descHangzhou', longDescKey: 'longDescHangzhou' }, xiamen: { imgQuery: 'xiamen,gulangyu,china', localImg: '/images/hero-xiamen.webp', nameKey: 'cityXiamen', descKey: 'descXiamen', longDescKey: 'longDescXiamen' }, iching: { imgQuery: 'iching,book of changes,china', localImg: '/images/hero-iching.webp', nameKey: 'cityIching', descKey: 'descIching', longDescKey: 'longDescIching' }, suzhou: { imgQuery: 'suzhou,classical garden,china', localImg: '/images/hero-suzhou.webp', nameKey: 'citySuzhou', descKey: 'descSuzhou', longDescKey: 'longDescSuzhou' } };
            const clientData = {
                translations: {
                    [lang]: t
                },
                cityDetails: allCityDetails
            };

            const langDir = path.join(rootDir, lang);
            await fs.ensureDir(langDir);

            const destPath = path.join(langDir, pageName);
            const $page = cheerio.load(html);

            // Calculate correct URL for this page/lang combination
            const pageUrl = `${baseUrl}/${lang}/${pageName}`;

            // --- A. HTML Structure Updates ---
            $page('html').attr('lang', lang);

            // SEO: Canonical
            let $canonical = $page('link[rel="canonical"]');
            if ($canonical.length === 0) {
                $page('head').append(`<link rel="canonical" href="${pageUrl}">`);
            } else {
                $canonical.attr('href', pageUrl);
            }

            // SEO: OpenGraph & Twitter URL — use language-specific URL
            $page('meta[property="og:url"], meta[property="twitter:url"]').each((i, el) => {
                $page(el).attr('content', pageUrl);
            });

 

            // --- B. CSS/JS Cleanup ---
 // Remove the massive external translations.js
 $page('script[src="/js/translations.js"]').remove();
 // Remove inline translations script (both `const translations =` and `window.translations =`)
 $page('script').each((i, el) => {
 const scriptContent = $page(el).html();
 if (scriptContent && (scriptContent.includes('const translations =') || scriptContent.includes('window.translations =') || scriptContent.includes('window.cityDetails ='))) {
 $page(el).remove();
 }
 });

 // Inject Minimal Data
 const dataScript = `<script>
 window.translations = ${JSON.stringify(clientData.translations)};
 window.cityDetails = ${JSON.stringify(clientData.cityDetails)};
 window.currentLang = '${lang}';
 </script>`;
 $page('body').append(dataScript);

 // Inject language switcher + persist-lang scripts (replaces old city.js)
 if (!$page('script[src="/js/lang-switcher.js"]').length) {
 $page('body').append('<script src="/js/lang-switcher.js" defer></script>');
 }
 if (!$page('script[src="/js/persist-lang.js"]').length) {
 $page('body').append('<script src="/js/persist-lang.js" defer></script>');
 }


            // --- C. Content Localization (Server-Side Rendering) ---
            if (t) {
                $page('[data-lang-key]').each((i, el) => {
                    const key = $page(el).attr('data-lang-key');
                    if (t[key]) {
                        if (el.tagName === 'meta') {
                            $page(el).attr('content', t[key]);
} else if (el.tagName === 'input' || el.tagName === 'textarea') {
                            $page(el).attr('placeholder', t[key]);
                        } else if (el.tagName === 'img') {
                            // Translate img alt text (accessibility — localized alt for all languages)
                            $page(el).attr('alt', t[key]);
                        } else if ($page(el).attr('aria-label') !== undefined) {
                            // Translate aria-label (e.g. icon-only buttons like carousel prev/next)
                            $page(el).attr('aria-label', t[key]);
                        } else {
 if (typeof t[key] === 'string' && /<[a-z][\s\S]*>/i.test(t[key])) {
 $page(el).html(t[key]);
 } else if ($page(el).attr('aria-haspopup')) {
 // Dropdown toggle button: rebuild with text + chevron SVG preserved
 const chevronSvg = '<svg class="w-3 h-3 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 20 20"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.24a.75.75 0 01-1.06 0L5.21 8.29a.75.75 0 01.02-1.08z"/></svg>';
 $page(el).html(t[key] + '\n' + chevronSvg);
 } else {
 $page(el).text(t[key]);
 }
 }
                    }
                });

                // Special handling for specific IDs
                if (t.metaTitle) {
                    if ($page('#page-title').length) $page('#page-title').text(t.metaTitle);
                    else $page('title').text(t.metaTitle);
                }
                if (t.metaDescription) {
                    if ($page('#meta-desc').length) $page('#meta-desc').attr('content', t.metaDescription);
                }
                // Translate #city-name using cityDetails mapping (city page)
                const pageNameWithoutExt = pageName.replace(/\.html$/, '');
                const pageCityMap = {
                    'beijing': 'cityBeijing', 'shanghai': 'cityShanghai', 'xian': 'cityXian',
                    'guilin': 'cityGuilin', 'zhangjiajie': 'cityZhangjiajie', 'jiuzhaigou': 'cityJiuzhaigou',
                    'yangtze': 'cityYangtze', 'chengdu': 'cityChengdu', 'hangzhou': 'cityHangzhou',
                    'xiamen': 'cityXiamen', 'iching': 'cityIching'
                };
                const nameKey = pageCityMap[pageNameWithoutExt];
                if (nameKey && t[nameKey]) {
                    $page('#city-name').text(t[nameKey]);
                }
// Translate #city-sub from descKey (city description), NOT metaDesc (SEO description)
                const pageCityData = allCityDetails[pageNameWithoutExt];
                if (pageCityData && pageCityData.descKey && t[pageCityData.descKey]) {
                    $page('#city-sub').text(t[pageCityData.descKey]);
                }
                // Translate #city-content body text
                // Priority: contentHtml (food pages) > longDescKey (city pages)
                if (pageCityData && pageCityData.longDescKey && t[pageCityData.longDescKey]) {
                    $page('#city-content').html(t[pageCityData.longDescKey]);
                } else if (t.contentHtml) {
                    $page('#city-content').html(t.contentHtml);
                }
                if (t.backText && $page('.back-link').length) {
                    $page('.back-link').text(t.backText);
                }
            }

            // --- C1. WebSite JSON-LD Localization (index.html only) ---
            // The WebSite schema in index.html has hardcoded EN name/description.
            // Update them from the already-localized translations.
            if (pageName === 'index.html') {
                $page('script[type="application/ld+json"]').each((i, el) => {
                    const raw = $page(el).html();
                    if (!raw) return;
                    try {
                        const data = JSON.parse(raw);
                        if (data['@type'] === 'WebSite') {
                            if (t.siteTitle) data.name = t.siteTitle;
                            if (t.metaDescription) data.description = t.metaDescription;
                            $page(el).html('\n        ' + JSON.stringify(data, null, 4) + '\n    ');
                        }
                    } catch (e) {
                        // Not JSON or parse error — leave unchanged
                    }
                });
            }

            // --- C2. JSON-LD Schema — Upgrade Article → Recipe (Food Pages) ---
            const foodPageJsonLdMap = {
                'peking-duck': { titleKey: 'titlePekingDuck', descKey: 'metaDescPekingDuck',
                  ingredientsKey: 'recipeIngredientPekingDuck', instructionsKey: 'recipeInstructionsPekingDuck',
                  contentKey: 'contentPekingDuck' },
                'dim-sum':     { titleKey: 'titleDimSum',     descKey: 'metaDescDimSum',
                  ingredientsKey: 'recipeIngredientDimSum',     instructionsKey: 'recipeInstructionsDimSum',
                  contentKey: 'contentDimSum' },
                'hotpot':      { titleKey: 'titleHotpot',      descKey: 'metaDescHotpot',
                  ingredientsKey: 'recipeIngredientHotpot',    instructionsKey: 'recipeInstructionsHotpot',
                  contentKey: 'contentHotpot' },
                'dumplings':   { titleKey: 'titleDumplings',   descKey: 'metaDescDumplings',
                  ingredientsKey: 'recipeIngredientDumplings', instructionsKey: 'recipeInstructionsDumplings',
                  contentKey: 'contentDumplings' }
            };
            const pageNameBase = pageName.replace(/\.html$/, '');
            const foodPageData = foodPageJsonLdMap[pageNameBase];
            if (foodPageData && t[foodPageData.titleKey] && t[foodPageData.descKey]) {
                $page('script[type="application/ld+json"]').each((i, el) => {
                    const raw = $page(el).html();
                    if (!raw) return;
                    try {
                        const data = JSON.parse(raw);
                        if (data['@type'] === 'Article' || data['@type'] === 'Recipe') {
                            // Upgrade to Recipe schema
                            data['@type'] = 'Recipe';
                            data.name = t[foodPageData.titleKey];
                            data.headline = t[foodPageData.titleKey];
                            data.description = t[foodPageData.descKey];
                            // Add recipeIngredient if present
                            if (t[foodPageData.ingredientsKey]) {
                                data.recipeIngredient = t[foodPageData.ingredientsKey].split(',').map(s => s.trim());
                            }
                            // Add recipeInstructions if present (array of strings or already-structured)
                            if (t[foodPageData.instructionsKey]) {
                                const rawSteps = t[foodPageData.instructionsKey];
                                let steps = typeof rawSteps === 'string' ? JSON.parse(rawSteps) : rawSteps;
                                data.recipeInstructions = steps.map((step, idx) => ({
                                    '@type': 'HowToStep',
                                    'name': String(idx + 1),
                                    'text': step
                                }));
                            }
                            // Add articleBody for full content
                            if (t[foodPageData.contentKey]) {
                                data.articleBody = t[foodPageData.contentKey].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
                            }
                            $page(el).html('\n        ' + JSON.stringify(data, null, 4) + '\n    ');
                        }
                    } catch (e) {
                        // Not JSON or parse error — leave unchanged
                    }
                });
            }

// --- C3. BreadcrumbList JSON-LD Schema ---
            // pageNameBase already declared above (line ~228) for food pages

            // Determine breadcrumb items based on page type
            let breadcrumbItems = null;

            if (['beijing','shanghai','xian','guilin','zhangjiajie','jiuzhaigou','yangtze'].includes(pageNameBase)) {
                // City pages: Home → Popular Cities → [City]
                const cityNameMap = {
                    'beijing': 'cityBeijing', 'shanghai': 'cityShanghai', 'xian': 'cityXian',
                    'guilin': 'cityGuilin', 'zhangjiajie': 'cityZhangjiajie',
                    'jiuzhaigou': 'cityJiuzhaigou', 'yangtze': 'cityYangtze'
                };
                const cityNameKey = cityNameMap[pageNameBase];
                const cityName = t[cityNameKey] || pageNameBase.charAt(0).toUpperCase() + pageNameBase.slice(1);
                breadcrumbItems = [
                    { name: t.navHome || 'Home', path: 'index.html' },
                    { name: t.navCities || 'Popular Cities', path: 'index.html' },
                    { name: cityName, path: pageName }
                ];
            } else if (['iching'].includes(pageNameBase)) {
                // Culture page: Home → Culture → I Ching
                const ichingNameKey = 'cityIching';
                const ichingName = t[ichingNameKey] || 'I Ching';
                breadcrumbItems = [
                    { name: t.navHome || 'Home', path: 'index.html' },
                    { name: t.navCulture || 'Culture', path: 'iching.html' },
                    { name: ichingName, path: pageName }
                ];
            } else if (['peking-duck','dim-sum','dumplings','hotpot'].includes(pageNameBase)) {
                // Food detail pages: Home → Cuisine → [Dish]
                const foodTitleMap = {
                    'peking-duck': 'titlePekingDuck', 'dim-sum': 'titleDimSum',
                    'dumplings': 'titleDumplings', 'hotpot': 'titleHotpot'
                };
                const foodNameKey = foodTitleMap[pageNameBase];
                const foodName = t[foodNameKey] || pageNameBase;
                breadcrumbItems = [
                    { name: t.navHome || 'Home', path: 'index.html' },
                    { name: t.navFood || 'Cuisine', path: 'food.html' },
                    { name: foodName, path: pageName }
                ];
            } else if (pageName === 'food.html') {
                // Food listing page: Home → Cuisine
                breadcrumbItems = [
                    { name: t.navHome || 'Home', path: 'index.html' },
                    { name: t.navFood || 'Cuisine', path: 'food.html' }
                ];
            }

            if (breadcrumbItems) {
                const breadcrumbSchema = {
                    '@context': 'https://schema.org',
                    '@type': 'BreadcrumbList',
                    'itemListElement': breadcrumbItems.map((item, idx) => {
                        const itemUrl = `${baseUrl}/${lang}/${item.path}`;
                        return {
                            '@type': 'ListItem',
                            'position': idx + 1,
                            'name': item.name,
                            'item': itemUrl
                        };
                    })
                };
                const breadcrumbScript = `\n  <script type="application/ld+json">\n  ${JSON.stringify(breadcrumbSchema, null, 4)}\n  </script>\n`;
                // Remove any existing BreadcrumbList JSON-LD scripts first (make idempotent — running multiple times won't duplicate)
                $page('head').find('script[type="application/ld+json"]').each((i, el) => {
                    try {
                        const data = JSON.parse($page(el).html());
                        if (data['@type'] === 'BreadcrumbList') {
                            $page(el).remove();
                        }
                    } catch (e) { /* not JSON, leave it */ }
                });
                $page('head').append(breadcrumbScript);
            }

            // --- C4. FAQPage JSON-LD Schema (visa.html only) ---
            if (pageName === 'visa.html' && t.visaFreeCountriesTitle) {
                const faqItems = [];

                // Q1: Visa-free entry
                if (t.visaFreeCountriesTitle && t.visaFreeCountriesDesc) {
                    const q1Parts = [t.visaFreeCountriesDesc || ''];
                    if (t.visaEurope) q1Parts.push(`${t.visaEurope}`);
                    if (t.visaAsia) q1Parts.push(`${t.visaAsia}`);
                    if (t.visaAmericas) q1Parts.push(`${t.visaAmericas}`);
                    if (t.visaOceania) q1Parts.push(`${t.visaOceania}`);
                    if (t.visaOther) q1Parts.push(`${t.visaOther}`);
                    faqItems.push({
                        '@type': 'Question',
                        'name': t.visaFreeCountriesTitle,
                        'acceptedAnswer': {
                            '@type': 'Answer',
                            'text': q1Parts.filter(Boolean).join(' ')
                        }
                    });
                }

                // Q2: Common visa types
                if (t.visaTypesTitle) {
                    const q2Parts = [];
                    if (t.visaTypeL && t.visaTypeLDesc) q2Parts.push(`${t.visaTypeL}: ${t.visaTypeLDesc}`);
                    if (t.visaTypeM && t.visaTypeMDesc) q2Parts.push(`${t.visaTypeM}: ${t.visaTypeMDesc}`);
                    if (t.visaTypeF && t.visaTypeFDesc) q2Parts.push(`${t.visaTypeF}: ${t.visaTypeFDesc}`);
                    if (t.visaTypeQ2 && t.visaTypeQ2Desc) q2Parts.push(`${t.visaTypeQ2}: ${t.visaTypeQ2Desc}`);
                    if (q2Parts.length > 0) {
                        faqItems.push({
                            '@type': 'Question',
                            'name': t.visaTypesTitle,
                            'acceptedAnswer': { '@type': 'Answer', 'text': q2Parts.join(' ') }
                        });
                    }
                }

                // Q3: Document requirements
                if (t.visaReqTitle) {
                    const q3Parts = [];
                    if (t.visaReqPassport) q3Parts.push(t.visaReqPassport);
                    if (t.visaReqPhoto) q3Parts.push(t.visaReqPhoto);
                    if (t.visaReqForm) q3Parts.push(t.visaReqForm);
                    if (t.visaReqItinerary) q3Parts.push(t.visaReqItinerary);
                    if (t.visaReqProof) q3Parts.push(t.visaReqProof);
                    if (t.visaReqFee) q3Parts.push(t.visaReqFee);
                    if (q3Parts.length > 0) {
                        faqItems.push({
                            '@type': 'Question',
                            'name': t.visaReqTitle,
                            'acceptedAnswer': { '@type': 'Answer', 'text': q3Parts.join('. ') }
                        });
                    }
                }

                // Q4: How to apply
                if (t.visaApplyTitle) {
                    const q4Parts = [];
                    if (t.visaApplyStep1Title && t.visaApplyStep1Desc) q4Parts.push(`${t.visaApplyStep1Title}: ${t.visaApplyStep1Desc}`);
                    if (t.visaApplyStep2Title && t.visaApplyStep2Desc) q4Parts.push(`${t.visaApplyStep2Title}: ${t.visaApplyStep2Desc}`);
                    if (t.visaApplyStep3Title && t.visaApplyStep3Desc) q4Parts.push(`${t.visaApplyStep3Title}: ${t.visaApplyStep3Desc}`);
                    if (t.visaApplyStep4Title && t.visaApplyStep4Desc) q4Parts.push(`${t.visaApplyStep4Title}: ${t.visaApplyStep4Desc}`);
                    if (t.visaApplyStep5Title && t.visaApplyStep5Desc) q4Parts.push(`${t.visaApplyStep5Title}: ${t.visaApplyStep5Desc}`);
                    if (q4Parts.length > 0) {
                        faqItems.push({
                            '@type': 'Question',
                            'name': t.visaApplyTitle,
                            'acceptedAnswer': { '@type': 'Answer', 'text': q4Parts.join(' ') }
                        });
                    }
                }

                // Q5: Essential travel tips
                if (t.visaTipsTitle) {
                    const q5Parts = [];
                    if (t.visaTip1Title && t.visaTip1Desc) q5Parts.push(`${t.visaTip1Title}: ${t.visaTip1Desc}`);
                    if (t.visaTip2Title && t.visaTip2Desc) q5Parts.push(`${t.visaTip2Title}: ${t.visaTip2Desc}`);
                    if (t.visaTip3Title && t.visaTip3Desc) q5Parts.push(`${t.visaTip3Title}: ${t.visaTip3Desc}`);
                    if (t.visaTip4Title && t.visaTip4Desc) q5Parts.push(`${t.visaTip4Title}: ${t.visaTip4Desc}`);
                    if (q5Parts.length > 0) {
                        faqItems.push({
                            '@type': 'Question',
                            'name': t.visaTipsTitle,
                            'acceptedAnswer': { '@type': 'Answer', 'text': q5Parts.join(' ') }
                        });
                    }
                }

                if (faqItems.length > 0) {
                    const faqSchema = {
                        '@context': 'https://schema.org',
                        '@type': 'FAQPage',
                        'mainEntity': faqItems
                    };
                    const faqScript = `\n  <script type="application/ld+json">\n  ${JSON.stringify(faqSchema, null, 4)}\n  </script>\n`;
                    // Remove any existing FAQPage JSON-LD scripts first (make idempotent)
                    $page('head').find('script[type="application/ld+json"]').each((i, el) => {
                        try {
                            const data = JSON.parse($page(el).html());
                            if (data['@type'] === 'FAQPage') {
                                $page(el).remove();
                            }
                        } catch (e) { /* not JSON, leave it */ }
                    });
                    $page('head').append(faqScript);
                }
            }

            // --- D. Link Localization ---
// Rewrite local links: href="beijing.html" -> href="/beijing.html" (en) or href="/zh-CN/beijing.html"
 $page('a[href]').each((i, el) => {
 const href = $page(el).attr('href');
 if (href && !href.startsWith('http') && !href.startsWith('#') && !href.startsWith('mailto:')) {
 // Normalize: remove leading ./ or single /
 let cleanHref = href.replace(/^\.\//, '').replace(/^\//, '');

 if (cleanHref.includes('#')) {
  // Handle anchor links: food.html#hotpot
  const parts = cleanHref.split('#');
  cleanHref = parts[0];
  const hash = parts[1];

  if (pages.includes(cleanHref)) {
   const prefix = `/${lang}`;
   $page(el).attr('href', `${prefix}/${cleanHref}#${hash}`);
  }
 } else {
  if (pages.includes(cleanHref)) {
   const prefix = `/${lang}`;
   $page(el).attr('href', `${prefix}/${cleanHref}`);
  }
 }
 }
 });

            // --- E. Image Optimization (WebP) ---
            $page('img[src$=".jpg"], img[src$=".png"]').each((i, el) => {
                const src = $page(el).attr('src');
                if (src && !src.startsWith('http') && !src.startsWith('data:')) {
                    // Check if webp exists (we assume it does if the optimizer ran)
                    const webpSrc = src.replace(/\.(jpg|png)$/i, '.webp');
                    $page(el).attr('src', webpSrc);
                }
            });

            // --- E5. Remove decoding="sync" from LCP images ---
            // decoding="sync" blocks rendering while the image is decoded (10-50ms on mobile).
            // For the LCP hero image (loading="eager"), we want non-blocking decode (default: async).
            $page('img[loading="eager"]').removeAttr('decoding');
            // Add fetchpriority="high" to above-the-fold hero images (the LCP elements)
            // 1. Explicitly eager-loaded images (e.g. index.html carousel)
            $page('img[loading="eager"]').attr('fetchpriority', 'high');
            // 2. City-page hero images (id="city-image") — these are above the fold
            $page('img#city-image').attr('fetchpriority', 'high');


            // --- E3. Preload type hints ---
            // Add explicit type="image/webp" to WebP preloads so browsers don't need to content-sniff
            $page('link[rel="preload"][href$=".webp"]').attr('type', 'image/webp');


            // --- E4. Mobile Browser Chrome: theme-color + color-scheme + iOS PWA + viewport-fit ---
            // Sets browser chrome color on mobile devices (improves UX/brand feel)
            // Remove any existing ones first (in case of re-runs)
            $page('meta[name="theme-color"]').remove();
            $page('meta[name="color-scheme"]').remove();
            $page('meta[name="apple-mobile-web-app-capable"]').remove();
            $page('meta[name="apple-mobile-web-app-status-bar-style"]').remove();

            // Update viewport to include viewport-fit=cover (notch/Dynamic Island support on iPhone)
            const $viewport = $page('meta[name="viewport"]');
            if ($viewport.length) {
                const currentContent = $viewport.attr('content') || 'width=device-width, initial-scale=1.0';
                $viewport.attr('content', currentContent.includes('viewport-fit') ? currentContent : currentContent + ', viewport-fit=cover');
            }

            // Insert after viewport meta tag for correct ordering
            if (t.themeColor) {
                $page('meta[name="viewport"]').after(
                    `\n    <meta name="theme-color" content="${t.themeColor}">`
                );
            }
            if (t.colorScheme) {
                $page('meta[name="viewport"]').after(
                    `\n    <meta name="color-scheme" content="${t.colorScheme}">`
                );
            }
            // iOS Add-to-Home-Screen: enables standalone mode without Safari chrome
            // Insert in reverse order so they end up as: apple-mobile-web-app-capable first, then status-bar-style
            $page('meta[name="viewport"]').after(
                `\n    <meta name="apple-mobile-web-app-status-bar-style" content="default">`
            );
            $page('meta[name="viewport"]').after(
                `\n    <meta name="apple-mobile-web-app-capable" content="yes">`
            );

            // --- E5. Web App Manifest (PWA installability on Android/Chrome) ---
            $page('meta[name="viewport"]').after(
                `\n    <link rel="manifest" href="/manifest.json">`
            );


            // --- F. SEO: hreflang ---
            $page('link[rel="alternate"][hreflang]').remove();
            const hreflangs = [];
            hreflangs.push({ lang: 'x-default', url: `${baseUrl}/${pageName}` });
            hreflangs.push({ lang: 'en', url: `${baseUrl}/${pageName}` });

            for (const l of langs) {
                if (l === 'en') continue;
                hreflangs.push({ lang: l, url: `${baseUrl}/${l}/${pageName}` });
            }

            hreflangs.forEach(h => {
                $page('head').append(`<link rel="alternate" href="${h.url}" hreflang="${h.lang}">\n  `);
            });

            // --- Z. Source Template Cleanup ---
            // Remove <!-- hreflang alternates --> placeholder comments and trailing blank lines
            // from the generated HTML (these confuse readers and add noise to output).
            // Also collapse multiple consecutive 4-space blank lines in <head> to just one
            // (Section E4 inserts meta tags with leading \n, producing excess blank lines).
            let finalHtml = $page.html().replace(
                /<!-- hreflang alternates -->\s*/g,
                ''
            );
            // Collapse 2+ consecutive 4-space blank lines (\n    \n    \n...) to a single \n    \n
            // Pattern breakdown: \n    ((\n    ){2,}) = \n + 4sp + one \n, then 2+ more (\n + 4sp) pairs
            finalHtml = finalHtml.replace(/\n    ((\n    ){2,})/g, '\n    \n');
            // Collapse 3+ plain consecutive newlines anywhere to 2 (extra body/section spacing)
            finalHtml = finalHtml.replace(/\n{3,}/g, '\n\n');

            // Write File
            await fs.writeFile(destPath, finalHtml, 'utf-8');

            // Add to Sitemap Entries
            sitemapEntries.push({
                loc: pageUrl,
                lastmod: getTodayStr(),
                changefreq: sitemapFreq[pageName] || sitemapFreq['default'],
                priority: sitemapPriorities[pageName] || sitemapPriorities['default']
            });
        }
        // console.log(`Processed ${pageName}`);
    }

    // Generate Sitemap.xml
    console.log('Generating sitemap.xml...');
    const sitemapContent = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${sitemapEntries.map(entry => `  <url>
    <loc>${entry.loc}</loc>
    <lastmod>${entry.lastmod}</lastmod>
    <changefreq>${entry.changefreq}</changefreq>
    <priority>${entry.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

    await fs.writeFile(path.join(rootDir, 'sitemap.xml'), sitemapContent, 'utf-8');
    console.log('sitemap.xml updated.');
    console.log('Done.');
})();
