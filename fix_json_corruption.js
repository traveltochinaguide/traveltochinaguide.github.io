const fs = require('fs');
const path = require('path');

const dirs = ['ja', 'ko', 'es', 'fr', 'de', 'ru'];
const cities = ['chongqing', 'guangzhou', 'shenzhen', 'kunming', 'dali', 'lijiang'];

let fixedCount = 0;

for (const d of dirs) {
  for (const city of cities) {
    const filePath = path.join(__dirname, d, `${city}.html`);
    if (!fs.existsSync(filePath)) {
      continue;
    }
    let content = fs.readFileSync(filePath, 'utf8');
    const original = content;

    // The corruption: </p>," (missing closing quote) should be </p>","
    // We'll replace all occurrences
    content = content.replace(/<\/p>,"/g, '</p>","');

    // Some files may have two corruption points. Apply twice to catch any remaining.
    content = content.replace(/<\/p>,"/g, '</p>","');

    if (content !== original) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`Fixed: ${d}/${city}.html`);
      fixedCount++;
    }
  }
}

console.log(`Total files fixed: ${fixedCount}`);

// Now verify
let stillCorrupt = 0;
for (const d of dirs) {
  for (const city of cities) {
    const filePath = path.join(__dirname, d, `${city}.html`);
    if (!fs.existsSync(filePath)) {
      continue;
    }
    const content = fs.readFileSync(filePath, 'utf8');
    const match = content.match(/window\.translations\s*=\s*(\{.*?\})\s*;/s);
    if (match) {
      try {
        JSON.parse(match[1]);
      } catch (e) {
        console.log(`STILL CORRUPT: ${d}/${city}.html — ${e.message}`);
        stillCorrupt++;
      }
    }
  }
}
if (stillCorrupt === 0) {
  console.log('All files are now valid JSON.');
} else {
  console.log(`${stillCorrupt} files still corrupt.`);
}
