const data = require('./js/translations.js');
const zhCn = data.translations['zh-CN'];
const cities = ['chongqing', 'guangzhou', 'shenzhen', 'kunming', 'dali', 'lijiang'];
cities.forEach(city => {
  const key = 'longDesc' + city[0].toUpperCase() + city.slice(1);
  const value = zhCn[key];
  if (value === undefined) {
    console.log(`${key}: MISSING`);
    return;
  }
  // Check for English words: we'll look for the word 'the ' as a simple indicator
  if (value.includes('the ')) {
    console.log(`${key}: contains English word 'the'`);
    // Show a snippet
    const idx = value.indexOf('the ');
    const snippet = value.substring(Math.max(0, idx - 30), Math.min(value.length, idx + 30));
    console.log(`  Snippet: ...${snippet}...`);
  } else {
    console.log(`${key}: OK (no 'the' found)`);
  }
});