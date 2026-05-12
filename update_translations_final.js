const fs = require('fs');
const vm = require('vm');

// Read the file
const original = fs.readFileSync('./js/translations.js', 'utf8');

// Create a sandbox
const sandbox = {};
try {
  vm.runInNewContext(original, sandbox);
} catch (e) {
  console.error('Error running the script:', e);
  process.exit(1);
}

// Extract the translations and cityDetails
let translations = sandbox.translations;
const cityDetails = sandbox.cityDetails;

// If we couldn't extract, exit
if (typeof translations === 'undefined' || typeof cityDetails === 'undefined') {
  console.error('Could not extract translations or cityDetails from the sandbox.');
  process.exit(1);
}

// Now we have the translations object from the sandbox
// Add the missing keys to each language
const langs = ['en', 'zh-CN', 'ja', 'ko', 'ru', 'fr', 'de', 'es'];
const keysToAdd = {
  ogTitleArchitecture: 'Chinese Architecture - Forbidden City, Temple of Heaven & Classical Design',
  ogDescArchitecture: 'Explore Chinese architecture — from the Forbidden City\\'s imperial grandeur to Temple of Heaven geometry and traditional courtyard houses.'
};

langs.forEach(lang => {
  Object.keys(keysToAdd).forEach(key => {
    if (!translations[lang].hasOwnProperty(key)) {
      translations[lang][key] = keysToAdd[key];
    }
  });
});

// Now rebuild the file
const translationsString = `let translations = ${JSON.stringify(translations, null, 2)};`;
const cityDetailsString = `let cityDetails = ${JSON.stringify(cityDetails, null, 2)};`;

const newContent = [
  // Preserve the first two comment lines
  original.split('\n')[0],
  original.split('\n')[1],
  '',
  translationsString,
  '',
  cityDetailsString,
  '',
  'if (typeof module !== \"undefined\" && module.exports) {',
  '  module.exports = { translations, cityDetails };',
  '}'
].join('\n');

fs.writeFileSync('./js/translations.js', newContent);
console.log('Updated translations.js with missing keys');