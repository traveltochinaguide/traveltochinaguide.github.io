const { translations } = require('./js/translations.js');
const langs = ['en', 'zh-CN', 'es', 'de', 'fr', 'ru', 'ko', 'ja'];
const keys = [
  'navCities',
  'cityBeijing',
  'cityShanghai',
  'cityXian',
  'cityGuilin',
  'cityZhangjiajie',
  'cityJiuzhaigou',
  'cityYangtze',
  'cityChengdu',
  'cityHangzhou',
  'cityXiamen',
  'cityChongqing',
  'cityGuangzhou',
  'cityShenzhen',
  'cityKunming',
  'cityDali',
  'cityLijiang',
  'citySuzhou',
  'cityHuangshan'
];
console.log('Checking translations for dropdown menu items...');
langs.forEach(lang => {
  const section = translations[lang];
  if (!section) {
    console.log(`${lang}: SECTION MISSING`);
    return;
  }
  let missing = [];
  let placeholders = [];
  keys.forEach(key => {
    const val = section[key];
    if (val === undefined) {
      missing.push(key);
    } else if (val === key) {
      placeholders.push(key);
    });
  if (missing.length > 0) {
    console.log(`${lang}: MISSING KEYS: ${missing.join(', ')}`);
  }
  if (placeholders.length > 0) {
    console.log(`${lang}: PLACEHOLDERS (value equals key): ${placeholders.join(', ')}`);
  }
  if (missing.length === 0 && placeholders.length === 0) {
    console.log(`${lang}: OK`);
  }
});
