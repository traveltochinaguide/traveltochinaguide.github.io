const fs = require('fs-extra');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const baseUrl = 'https://www.travelchinaguide.dpdns.org';
const langs = ['zh-CN', 'ja', 'ko', 'ru', 'fr', 'de', 'es']; // 'en' is root
const pages = [
    { name: 'index.html', freq: 'daily', priority: 1.0 },
    { name: 'beijing.html', freq: 'weekly', priority: 0.9 },
    { name: 'shanghai.html', freq: 'weekly', priority: 0.9 },
    { name: 'xian.html', freq: 'weekly', priority: 0.9 },
    { name: 'guilin.html', freq: 'weekly', priority: 0.8 },
    { name: 'zhangjiajie.html', freq: 'weekly', priority: 0.8 },
    { name: 'jiuzhaigou.html', freq: 'weekly', priority: 0.8 },
    { name: 'yangtze.html', freq: 'weekly', priority: 0.8 },
    { name: 'iching.html', freq: 'monthly', priority: 0.7 }
];

(async () => {
    console.log('Generating sitemap.xml...');

    let xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
`;

    const today = new Date().toISOString().split('T')[0];

    // Helper to add a url
    const addUrl = (relativePath, freq, priority) => {
        const fullUrl = `${baseUrl}/${relativePath}`;
        xml += `  <url>
    <loc>${fullUrl}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>${freq}</changefreq>
    <priority>${priority.toFixed(1)}</priority>
  </url>
`;
    };

    // 1. Root Pages (English)
    addUrl('', 'daily', 1.0); // Root /
    pages.forEach(p => {
        // index.html at root is redundant if we have /, but good practice to include /index.html if generic
        // Usually / is enough. But let's verify canonicals. 
        // Our site uses .html canonicals. So let's include canonical form.
        addUrl(p.name, p.freq, p.priority);
    });

    // 2. Localized Pages
    for (const lang of langs) {
        for (const p of pages) {
            // Localized home page is usually /zh-CN/index.html, but served as /zh-CN/?
            // Let's explicitly list the .html files to be safe static file style
            addUrl(`${lang}/${p.name}`, p.freq, p.priority);
        }
    }

    xml += `</urlset>`;

    await fs.writeFile(path.join(rootDir, 'sitemap.xml'), xml, 'utf-8');
    console.log('Done. Sitemap generated at sitemap.xml');
})();
