const fs = require('fs');
const path = require('path');
const filePath = path.join(__dirname, 'js/translations.js');

try {
  const data = require(filePath);
  const en = data.translations.en;
  const langs = ['zh-CN','ja','ko','ru','fr','de','es'];
  let placeholderCount = 0;
  let untranslatedCount = 0;
  langs.forEach(lang => {
    const langSection = data.translations[lang];
    Object.keys(en).forEach(key => {
      const val = langSection[key];
      if (val === key) {
        placeholderCount++;
      } else if (val === en[key] && val !== '' && val !== key) {
        untranslatedCount++;
      }
    });
  });
  console.log('Placeholders (value equals key):', placeholderCount);
  console.log('Untranslated (value equals English value, not empty, not placeholder):', untranslatedCount);
  console.log('English total keys:', Object.keys(en).length);
} catch (error) {
  console.error('Error:', error.message);
}