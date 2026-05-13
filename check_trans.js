const data = require('./js/translations.js');
const en = data.translations.en;
const zhCn = data.translations['zh-CN'];
const cities = ['chongqing', 'guangzhou', 'shenzhen', 'kunming', 'dali', 'lijiang'];
cities.forEach(city => {
  const key = 'longDesc' + city[0].toUpperCase() + city.slice(1);
  const enVal = en[key];
  const zhCnVal = zhCn[key];
  if (enVal === zhCnVal) {
    console.log(`MISSING: ${key} is identical in EN and zh-CN`);
  } else {
    console.log(`OK: ${key} is different`);
  }
});