const fs = require('fs');
const translations = require('./js/translations.js');

const langs = ['en', 'zh-CN', 'ja', 'ko', 'ru', 'fr', 'de', 'es'];
const keysToAdd = {
  ogTitleArchitecture: 'Chinese Architecture - Forbidden City, Temple of Heaven & Classical Design',
  ogDescArchitecture: 'Explore Chinese architecture — from the Forbidden City\'s imperial grandeur to Temple of Heaven geometry and traditional courtyard houses.'
};

langs.forEach(lang => {
  // For each language, add the two keys if missing
  Object.keys(keysToAdd).forEach(key => {
    if (!translations.translations[lang].hasOwnProperty(key)) {
      translations.translations[lang][key] = keysToAdd[key];
    }
  });
});

// Now we need to write back the file in the same format.
// Read the original file to extract carouselData and cityDetails
const original = fs.readFileSync('./js/translations.js', 'utf8');

// Extract carouselData: looks like: const carouselData = [ ... ];
// Extract cityDetails: const cityDetails = { ... };
const carouselDataMatch = original.match(/const carouselData = \[[\s\S]*?\];/);
const cityDetailsMatch = original.match(/const cityDetails = \{[\s\S]*?\};/);

if (!carouselDataMatch || !cityDetailsMatch) {
  console.error('Could not extract carouselData or cityDetails');
  process.exit(1);
}

const carouselData = carouselDataMatch[0];
const cityDetails = cityDetailsMatch[0];

// Build the translations object string.
const translationsObject = `const translations = ${JSON.stringify(translations.translations, null, 2)};`;

// Build the new file content.
const newContent = [
  original.split('\n')[0], // first line comment
  original.split('\n')[1], // second line comment
  '',
  carouselData,
  '',
  cityDetails,
  '',
  translationsObject,
  '',
  'if (typeof module !== \"undefined\" && module.exports) {',
  '  module.exports = { translations, cityDetails };',
  '}'
].join('\n');

fs.writeFileSync('./js/translations.js', newContent);
console.log('Updated translations.js with missing keys');