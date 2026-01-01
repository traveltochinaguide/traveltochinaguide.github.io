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
const baseUrl = 'https://www.traveltochinaguide.github.io'; // Updated to GitHub Pages URL standard

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
            const clientData = {
                translations: {
                    [lang]: t
                },
                cityDetails: cityDetails // This is language agnostic or contains keys
            };

            const langDir = (lang === 'en') ? rootDir : path.join(rootDir, lang);
            await fs.ensureDir(langDir);

            const destPath = path.join(langDir, pageName);
            const $page = cheerio.load(html);

            // Calculate correct URL for this page/lang combination
            const pageUrl = (lang === 'en') ? `${baseUrl}/${pageName}` : `${baseUrl}/${lang}/${pageName}`;

            // --- A. HTML Structure Updates ---
            $page('html').attr('lang', lang);

            // SEO: Canonical
            let $canonical = $page('link[rel="canonical"]');
            if ($canonical.length === 0) {
                $page('head').append(`<link rel="canonical" href="${pageUrl}">`);
            } else {
                $canonical.attr('href', pageUrl);
            }

            // --- B. CSS/JS Cleanup ---
            // Remove the massive external translations.js
            $page('script[src="/js/translations.js"]').remove();
            $page('script[src="/js/persist-lang.js"]').remove(); // No longer needed for static nav? Maybe keep for preference saving.
            // Remove inline translations script
            $page('script').each((i, el) => {
                const content = $page(el).html();
                if (content && content.includes('const translations =')) {
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


            // --- C. Content Localization (Server-Side Rendering) ---
            if (t) {
                $page('[data-lang-key]').each((i, el) => {
                    const key = $page(el).attr('data-lang-key');
                    if (t[key]) {
                        if (el.tagName === 'meta') {
                            $page(el).attr('content', t[key]);
                        } else if (el.tagName === 'input' || el.tagName === 'textarea') {
                            $page(el).attr('placeholder', t[key]);
                        } else {
                            if (typeof t[key] === 'string' && /<[a-z][\s\S]*>/i.test(t[key])) {
                                $page(el).html(t[key]);
                            } else {
                                $page(el).text(t[key]);
                            }
                        }
                    }
                });

                // Special handling for specific IDs
                if (t.pageTitle) {
                    if ($page('#page-title').length) $page('#page-title').text(t.pageTitle);
                    else $page('title').text(t.pageTitle);
                }
                if (t.metaDesc) {
                    if ($page('#meta-desc').length) $page('#meta-desc').attr('content', t.metaDesc);
                }
                if (t.cityName) $page('#city-name').text(t.cityName);
                if (t.heroSubtitle) $page('#city-sub').text(t.heroSubtitle);
                else if (t.metaDesc && $page('#city-sub').length && !$page('#city-sub').text().trim()) {
                    // Only fallback if empty
                    $page('#city-sub').text(t.metaDesc);
                }
                if (t.contentHtml) {
                    $page('#city-content').html(t.contentHtml);
                }
                if (t.backText && $page('.back-link').length) {
                    $page('.back-link').text(t.backText);
                }
            }

            // --- D. Link Localization ---
            // Rewrite local links: href="beijing.html" -> href="/beijing.html" (en) or href="/zh-CN/beijing.html"
            $page('a[href]').each((i, el) => {
                const href = $page(el).attr('href');
                if (href && !href.startsWith('http') && !href.startsWith('#') && !href.startsWith('mailto:')) {
                    // Check if it's one of our known pages
                    let cleanHref = href.replace(/^\.\//, '').replace(/^\//, ''); // dim-sum.html

                    if (cleanHref.includes('#')) {
                        // Handle anchor links food.html#hotpot
                        const parts = cleanHref.split('#');
                        cleanHref = parts[0];
                        const hash = parts[1];

                        if (pages.includes(cleanHref)) {
                            const prefix = (lang === 'en') ? '' : `/${lang}`;
                            $page(el).attr('href', `${prefix}/${cleanHref}#${hash}`);
                        }
                    } else {
                        if (pages.includes(cleanHref)) {
                            const prefix = (lang === 'en') ? '' : `/${lang}`;
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

            // Write File
            await fs.writeFile(destPath, $page.html(), 'utf-8');

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
