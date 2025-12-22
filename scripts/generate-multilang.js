const fs = require('fs-extra');
const path = require('path');
const cheerio = require('cheerio');

// Global Navigation Translations (Extracted from index.html)
// These keys are missing in city pages but required for the shared header/nav.
const GLOBAL_NAV_TRANSLATIONS = {
    'en': {
        navHome: "Home", navCities: "Popular Cities", navCulture: "Culture", cultureIching: "I Ching", navNature: "Nature",
        cityBeijing: "Beijing", cityShanghai: "Shanghai", cityXian: "Xi'an", cityGuilin: "Guilin",
        natureZhangjiajie: "Zhangjiajie", natureJiuzhaigou: "Jiuzhaigou", natureYangtze: "Yangtze River"
    },
    'zh-CN': {
        navHome: "首页", navCities: "热门城市", navCulture: "文化", cultureIching: "易经", navNature: "自然风光",
        cityBeijing: "北京", cityShanghai: "上海", cityXian: "西安", cityGuilin: "桂林",
        natureZhangjiajie: "张家界", natureJiuzhaigou: "九寨沟", natureYangtze: "长江"
    },
    'ja': {
        navHome: "ホーム", navCities: "人気の都市", navCulture: "文化", cultureIching: "易経", navNature: "自然",
        cityBeijing: "北京", cityShanghai: "上海", cityXian: "西安", cityGuilin: "桂林",
        natureZhangjiajie: "張家界", natureJiuzhaigou: "九寨溝", natureYangtze: "長江"
    },
    'ko': {
        navHome: "홈", navCities: "인기 도시", navCulture: "문화", cultureIching: "주역", navNature: "자연",
        cityBeijing: "베이징", cityShanghai: "상하이", cityXian: "시안", cityGuilin: "구이린",
        natureZhangjiajie: "장가계", natureJiuzhaigou: "구채구", natureYangtze: "양쯔강"
    },
    'ru': {
        navHome: "Главная", navCities: "Популярные города", navCulture: "Культура", cultureIching: "И-цзин", navNature: "Природа",
        cityBeijing: "Пекин", cityShanghai: "Шанхай", cityXian: "Сиань", cityGuilin: "Гуйлинь",
        natureZhangjiajie: "Чжанцзяцзе", natureJiuzhaigou: "Долина Цзючжайгоу", natureYangtze: "Река Янцзы"
    },
    'fr': {
        navHome: "Accueil", navCities: "Villes populaires", navCulture: "Culture", cultureIching: "I Ching", navNature: "Nature",
        cityBeijing: "Pékin", cityShanghai: "Shanghai", cityXian: "Xi'an", cityGuilin: "Guilin",
        natureZhangjiajie: "Zhangjiajie", natureJiuzhaigou: "Vallée de Jiuzhaigou", natureYangtze: "Fleuve Yangtsé"
    },
    'de': {
        navHome: "Startseite", navCities: "Beliebte Städte", navCulture: "Kultur", cultureIching: "I Ging", navNature: "Natur",
        cityBeijing: "Peking", cityShanghai: "Shanghai", cityXian: "Xi'an", cityGuilin: "Guilin",
        natureZhangjiajie: "Zhangjiajie", natureJiuzhaigou: "Jiuzhaigou-Tal", natureYangtze: "Yangtze-Fluss"
    },
    'es': {
        navHome: "Inicio", navCities: "Ciudades populares", navCulture: "Cultura", cultureIching: "I Ching", navNature: "Naturaleza",
        cityBeijing: "Pekín", cityShanghai: "Shanghái", cityXian: "Xi'an", cityGuilin: "Guilin",
        natureZhangjiajie: "Zhangjiajie", natureJiuzhaigou: "Valle de Jiuzhaigou", natureYangtze: "Río Yangtsé"
    }
};

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
    'iching.html'
];
const rootDir = path.resolve(__dirname, '..');
const baseUrl = 'https://www.travelchinaguide.dpdns.org';

(async () => {
    console.log('Starting multi-language static generation...');

    for (const pageName of pages) {
        const filePath = path.join(rootDir, pageName);
        if (!await fs.pathExists(filePath)) {
            console.warn(`File not found: ${filePath}`);
            continue;
        }

        console.log(`Processing ${pageName}...`);
        const html = await fs.readFile(filePath, 'utf-8');
        const $ = cheerio.load(html);

        // Extract translation object
        const scriptContent = $('script').filter((i, el) => {
            return $(el).html().includes('const translations =');
        }).html();

        let translations = {};
        if (scriptContent) {
            try {
                const match = scriptContent.match(/const translations\s*=\s*(\{[\s\S]*?\});/);
                if (match && match[1]) {
                    const getTrans = new Function(`return ${match[1]}`);
                    translations = getTrans();
                }
            } catch (e) {
                console.error(`Failed to parse translations for ${pageName}`, e);
                continue;
            }
        }

        // Generate files for each lang
        for (const lang of langs) {
            if (lang !== 'en' && !translations[lang]) {
                continue;
                // If a specific language translation is missing for this page, skip it
                // unless it's 'en' which is always expected to be present or derived.
                if (!translations['en']) { // If even 'en' is missing, something is wrong.
                    console.warn(`No translations found for 'en' or '${lang}' for page ${pageName}. Skipping.`);
                    continue;
                }
                // If specific lang is missing, but 'en' exists, we can proceed with 'en' as fallback
                // but the current logic explicitly skips if `translations[lang]` is falsey.
                // For now, keeping the original skip logic for non-en.
                continue;
            }

            // Start with page-specific translations for the current language, falling back to 'en' if needed.
            let pageTranslations = (lang === 'en' && translations['en']) ? translations['en'] : (translations[lang] || translations['en'] || {});

            // Merge GLOBAL_NAV_TRANSLATIONS into pageTranslations
            if (GLOBAL_NAV_TRANSLATIONS[lang]) {
                pageTranslations = { ...GLOBAL_NAV_TRANSLATIONS[lang], ...pageTranslations };
            } else if (GLOBAL_NAV_TRANSLATIONS['en']) { // Fallback for global nav if specific lang is missing
                pageTranslations = { ...GLOBAL_NAV_TRANSLATIONS['en'], ...pageTranslations };
            }

            const t = pageTranslations; // Use the merged translations

            const langDir = (lang === 'en') ? rootDir : path.join(rootDir, lang);
            await fs.ensureDir(langDir);

            const destPath = path.join(langDir, pageName);
            const $page = cheerio.load(html);

            // 1. Update HTML Lang Attribute
            $page('html').attr('lang', lang);

            // 2. Generic data-lang-key substitution
            if (t) {
                $page('[data-lang-key]').each((i, el) => {
                    const key = $(el).attr('data-lang-key');
                    if (t[key]) {
                        if (el.tagName === 'meta') {
                            $(el).attr('content', t[key]);
                        } else if (el.tagName === 'input' || el.tagName === 'textarea') {
                            $(el).attr('placeholder', t[key]);
                        } else {
                            $(el).text(t[key]);
                        }
                    }
                });

                // 3. Helper for generic ID-based content
                if (t.pageTitle) {
                    if ($page('#page-title').length) $page('#page-title').text(t.pageTitle);
                    else $page('title').text(t.pageTitle);
                }
                if (t.metaDesc) {
                    if ($page('#meta-desc').length) $page('#meta-desc').attr('content', t.metaDesc);
                }
                if (t.cityName) $page('#city-name').text(t.cityName);
                if (t.heroSubtitle) $page('#city-sub').text(t.heroSubtitle);
                else if (t.metaDesc && $page('#city-sub').length) {
                    // Ensure subtitle isn't empty if we have metaDesc fallback
                    $page('#city-sub').text(t.metaDesc);
                }
                if (t.contentHtml) {
                    $page('#city-content').html(t.contentHtml);
                }
            }

            // ---------------------------------------------------------
            // 4. Update Hreflang Tags (SEO)
            // ---------------------------------------------------------
            $page('link[rel="alternate"][hreflang]').remove();

            // x-default and en -> root
            const rootUrl = `${baseUrl}/${pageName}`;
            $page('head').append(`<link rel="alternate" href="${rootUrl}" hreflang="x-default">\n  `);
            $page('head').append(`<link rel="alternate" href="${rootUrl}" hreflang="en">\n  `);

            // Other langs
            for (const l of langs) {
                if (l === 'en') continue;
                const url = `${baseUrl}/${l}/${pageName}`;
                $page('head').append(`<link rel="alternate" href="${url}" hreflang="${l}">\n  `);
            }

            // ---------------------------------------------------------
            // 5. Client-side JS Compatibility Fix
            // ---------------------------------------------------------
            let finalHtml = $page.html();

            // Fix for Index
            finalHtml = finalHtml.replace(/let\s+currentLang\s*=\s*['"]en['"]\s*;/g, `let currentLang = '${lang}';`);

            // Fix for City Pages (If 'en', we explicitly set it to 'en' to disable auto-detection loop)
            finalHtml = finalHtml.replace(/const\s+lang\s*=\s*getLang\(\)\s*;/g, `const lang = '${lang}';`);

            // Write File
            await fs.writeFile(destPath, finalHtml, 'utf-8');
            console.log(`  -> Generated ${lang === 'en' ? '(Root)' : lang}/${pageName}`);
        }
    }
    console.log('Done.');
})();
