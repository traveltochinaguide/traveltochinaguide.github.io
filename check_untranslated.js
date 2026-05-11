const fs = require('fs');
const path = require('path');
const filePath = path.join(__dirname, 'js/translations.js');
const data = require(filePath);

const en = data.translations.en;
const langs = ['zh-CN','ja','ko','ru','fr','de','es'];

// We'll check a subset of keys that are likely to be content (longDesc, content, title, metaDesc, etc.)
const prefixFilters = ['longDesc', 'content', 'title', 'metaDesc', 'desc', 'recipe'];
const keysToCheck = Object.keys(en).filter(key => {
  return prefixFilters.some(prefix => key.startsWith(prefix));
});

console.log(`Checking ${keysToCheck.length} keys for untranslated content...`);

let untranslatedCount = 0;
langs.forEach(lang => {
  const langSection = data.translations[lang];
  keysToCheck.forEach(key => {
    if (langSection[key] === en[key]) {
      console.log(`UNTRANSLATED: ${lang}.${key}`);
      untranslatedCount++;
    }
  });
});

console.log(`Total untranslated keys found: ${untranslatedCount}`);

// Also, let's check for any keys that are empty in non-EN sections
let emptyCount = 0;
langs.forEach(lang => {
  const langSection = data.translations[lang];
  keysToCheck.forEach(key => {
    if (!langSection[key] || langSection[key] === '') {
      console.log(`EMPTY: ${lang}.${key}`);
      emptyCount++;
    }
  });
});
console.log(`Total empty keys found: ${emptyCount}`);
