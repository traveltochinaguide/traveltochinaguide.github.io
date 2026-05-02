const cheerio = require('cheerio');
const fs = require('fs-extra');
const path = require('path');

const pages = [
    'index.html', 'beijing.html', 'shanghai.html', 'xian.html', 'guilin.html',
    'zhangjiajie.html', 'jiuzhaigou.html', 'yangtze.html', 'iching.html',
    'food.html', 'peking-duck.html', 'dim-sum.html', 'hotspot.html', 'dumplings.html', 'visa.html'
];

// Correct list based on actual files
const actualPages = [
    'index.html', 'beijing.html', 'shanghai.html', 'xian.html', 'guilin.html',
    'zhangjiajie.html', 'jiuzhaigou.html', 'yangtze.html', 'iching.html',
    'food.html', 'peking-duck.html', 'dim-sum.html', 'hotpot.html', 'dumplings.html', 'visa.html'
];

let totalFixed = 0;
const rootDir = process.cwd();

for (const pageName of actualPages) {
    const filePath = path.join(rootDir, pageName);
    if (!fs.existsSync(filePath)) {
        console.warn('NOT FOUND:', pageName);
        continue;
    }

    const html = fs.readFileSync(filePath, 'utf-8');
    const $ = cheerio.load(html);

    let changed = false;

    // Add role="menu" to each dropdown-panel
    $('.dropdown-panel').each(function(i, el) {
        if (!$(el).attr('role')) {
            $(el).attr('role', 'menu');
            changed = true;
        }
    });

    // Add role="menuitem" to each <a> inside dropdown-panel
    $('.dropdown-panel a').each(function(i, el) {
        if (!$(el).attr('role')) {
            $(el).attr('role', 'menuitem');
            changed = true;
        }
    });

    if (changed) {
        fs.writeFileSync(filePath, $.html());
        totalFixed++;
        console.log('Fixed:', pageName);
    } else {
        console.log('No change:', pageName);
    }
}
console.log('Total files updated:', totalFixed);