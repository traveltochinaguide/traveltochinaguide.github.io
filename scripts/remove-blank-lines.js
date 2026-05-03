/**
 * Remove-placeholder-blank-lines.js
 * Removes excessive blank lines between Google AdSense script tag and hreflang <link> tags
 * in the HTML <head> section. These were placeholder lines from development that add
 * ~150-200 wasted blank lines per file (~8-15KB of bloat per file).
 *
 * Applies to: All 15 source HTML files (which then get regenerated into 120+ output files).
 */
const fs = require('fs');
const path = require('path');

const sourceFiles = [
    'index.html',
    'beijing.html',
    'shanghai.html',
    'guilin.html',
    'xian.html',
    'zhangjiajie.html',
    'jiuzhaigou.html',
    'yangtze.html',
    'iching.html',
    'food.html',
    'peking-duck.html',
    'dim-sum.html',
    'hotpot.html',
    'dumplings.html',
    'visa.html'
];

function removeBlankLinesBetweenAdScriptAndHreflang(content) {
    // Match: </script> followed by one or more blank/comment lines, then <link rel="alternate" hreflang
    // This targets specifically the blank-line section between the adsbygoogle script and hreflang links
    const pattern = /(<\/script>)(\s*<!--[\s\S]*?-->)?(\s*\n(?:[ \t]*\n)*)(\s*<link rel="alternate" hreflang)/;
    const replacement = '$1$4';

    const newContent = content.replace(pattern, (match, closingScript, comment, blankLines, hreflangLink) => {
        return closingScript + '\n' + hreflangLink;
    });

    return newContent;
}

let totalSaved = 0;

for (const file of sourceFiles) {
    const filePath = path.join(__dirname, '..', file);
    if (!fs.existsSync(filePath)) {
        console.warn(`File not found: ${filePath}`);
        continue;
    }

    const originalSize = fs.statSync(filePath).size;
    let content = fs.readFileSync(filePath, 'utf-8');

    const newContent = removeBlankLinesBetweenAdScriptAndHreflang(content);

    if (content === newContent) {
        console.log(`  [SKIP] ${file} - no blank lines to remove`);
        continue;
    }

    fs.writeFileSync(filePath, newContent, 'utf-8');
    const newSize = fs.statSync(filePath).size;
    const saved = originalSize - newSize;
    totalSaved += saved;
    console.log(`  [FIXED] ${file} - saved ${saved} bytes (${originalSize} → ${newSize})`);
}

console.log(`\nTotal bytes saved: ${totalSaved} bytes (~${(totalSaved / 1024).toFixed(1)} KB)`);