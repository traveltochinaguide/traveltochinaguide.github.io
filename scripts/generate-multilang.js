const fs = require('fs-extra');
const path = require('path');
const cheerio = require('cheerio');
// Import the new external translations (contains index.html data + global nav)
const { translations: globalTranslations } = require('../js/translations.js');

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
    'yangtze.html',
    'iching.html',
    'food.html',
    'peking-duck.html',
    'dim-sum.html',
    'hotpot.html',
    'dumplings.html'
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
const baseUrl = 'https://www.travelchinaguide.dpdns.org';

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
        const $ = cheerio.load(html);

        let localTranslations = {};

        // Extract inline translations if present (for legacy pages)
        if (pageName !== 'index.html') {
            const scriptContent = $('script').filter((i, el) => {
                const content = $(el).html();
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
            const t = { ...globalForLang, ...localForLang };

            const langDir = (lang === 'en') ? rootDir : path.join(rootDir, lang);
            await fs.ensureDir(langDir);

            const destPath = path.join(langDir, pageName);
            const $page = cheerio.load(html);

            // Calculate correct URL for this page/lang combination
            const pageUrl = (lang === 'en') ? `${baseUrl}/${pageName}` : `${baseUrl}/${lang}/${pageName}`;

            // 1. Update HTML Lang Attribute
            $page('html').attr('lang', lang);

            // 2. SEO: Update Canonical Tag
            let $canonical = $page('link[rel="canonical"]');
            if ($canonical.length === 0) {
                $page('head').append(`<link rel="canonical" href="${pageUrl}">`);
            } else {
                $canonical.attr('href', pageUrl);
            }

            // 3. SEO: Update JSON-LD URLs (localize them)
            $page('script[type="application/ld+json"]').each((i, el) => {
                try {
                    const jsonContent = $(el).html();
                    const data = JSON.parse(jsonContent);
                    let modified = false;

                    // Helper to recursively update URLs in the object
                    const updateUrls = (obj) => {
                        for (const key in obj) {
                            if (typeof obj[key] === 'string') {
                                // If string starts with baseUrl, replace it with localized version
                                // We check if it matches the current page's generic EN url structure
                                if (obj[key].startsWith(baseUrl)) {
                                    // Basic logic: if we are in 'zh-CN', replace 'baseUrl/' with 'baseUrl/zh-CN/'
                                    // but careful not to double-inject if not needing it (e.g. assets)
                                    // We focus on page URLs ending in .html or root
                                    const val = obj[key];
                                    if ((val.endsWith('.html') || val.endsWith('/')) && !val.match(/\.(jpg|png|svg)$/)) {
                                        // Construct localized URL
                                        // remove baseUrl
                                        const relative = val.replace(baseUrl, '');
                                        // relative might be '/index.html' or '/beijing.html'
                                        // new url = baseUrl + (lang=='en'?'':'/'+lang) + relative
                                        const newUrl = baseUrl + (lang === 'en' ? '' : '/' + lang) + relative;
                                        if (obj[key] !== newUrl) {
                                            obj[key] = newUrl;
                                            modified = true;
                                        }
                                    }
                                }
                            } else if (typeof obj[key] === 'object' && obj[key] !== null) {
                                updateUrls(obj[key]);
                            }
                        }
                    };

                    updateUrls(data);

                    if (modified) {
                        $(el).html(JSON.stringify(data, null, 2));
                    }
                } catch (e) {
                    // ignore parse errors or non-json contents
                }
            });

            // 4. Content Replacement (data-lang-key)
            if (t) {
                $page('[data-lang-key]').each((i, el) => {
                    const key = $(el).attr('data-lang-key');
                    if (t[key]) {
                        if (el.tagName === 'meta') {
                            $(el).attr('content', t[key]);
                        } else if (el.tagName === 'input' || el.tagName === 'textarea') {
                            $(el).attr('placeholder', t[key]);
                        } else {
                            if (typeof t[key] === 'string' && /<[a-z][\s\S]*>/i.test(t[key])) {
                                $(el).html(t[key]);
                            } else {
                                $(el).text(t[key]);
                            }
                        }
                    }
                });

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
                    $page('#city-sub').text(t.metaDesc);
                }
                if (t.contentHtml) {
                    $page('#city-content').html(t.contentHtml);
                }
                if (t.backText && $page('.back-link').length) {
                    $page('.back-link').text(t.backText);
                }
            }

            // 5. Update Hreflang Tags
            $page('link[rel="alternate"][hreflang]').remove();

            // Build map of all localized URLs for this page
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

            // 6. Client-side JS Compatibility
            let finalHtml = $page.html();
            finalHtml = finalHtml.replace(/const\s+lang\s*=\s*['"]en['"]\s*;/g, `const lang = '${lang}';`);
            finalHtml = finalHtml.replace(/let\s+currentLang\s*=\s*['"]en['"]\s*;/g, `let currentLang = '${lang}';`);

            // Write File
            await fs.writeFile(destPath, finalHtml, 'utf-8');
            // console.log(`  -> Generated ${lang === 'en' ? '(Root)' : lang}/${pageName}`);

            // Add to Sitemap Entries
            sitemapEntries.push({
                loc: pageUrl,
                lastmod: getTodayStr(),
                changefreq: sitemapFreq[pageName] || sitemapFreq['default'],
                priority: sitemapPriorities[pageName] || sitemapPriorities['default']
            });
        }
        console.log(`Processed ${pageName} (${langs.length} languages)`);
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

