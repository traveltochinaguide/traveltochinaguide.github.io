const fs = require('fs-extra');
const path = require('path');
const cheerio = require('cheerio');

const langs = ['zh-CN', 'ja', 'ko', 'ru', 'fr', 'de', 'es'];
const rootDir = '/home/ubuntu/traveltochinaguide.github.io';

// Proper translations for Chongqing-specific keys
// longDescChongqing is already correct in each language - only fix the short keys
const translations = {
  'zh-CN': {
    'pageTitleChongqing': '重庆 - 中国旅游',
    'metaDescriptionChongqing': '山城重庆，以火锅和长江、嘉陵江交汇闻名，拥有30万人口的超大城市。',
    'ogTitleChongqing': '重庆旅游指南 - 山城、火锅与长江风光',
    'ogDescChongqing': '探索重庆——一座位于长江和嘉陵江交汇处的3000万人口山城，以火锅和壮丽的江景闻名。',
    'twitterTitleChongqing': '重庆旅游指南 - 山城、火锅与长江风光',
    'twitterDescChongqing': '探索重庆——一座位于长江和嘉陵江交汇处的3000万人口山城，以火锅和壮丽的江景闻名。',
    'cityChongqing': '重庆',
    'descChongqing': '山城重庆，以火锅和长江、嘉陵江交汇闻名。',
  },
  'ja': {
    'pageTitleChongqing': '重慶 - 中国旅行',
    'metaDescriptionChongqing': '山城重慶、火鍋と長江・嘉陵江の合流点で有名な3000万都市。',
    'ogTitleChongqing': '重慶旅行ガイド - 山城、火鍋と長江の景色',
    'ogDescChongqing': '重慶を探索——長江と嘉陵江の合流点に位置する3000万人の山城、火鍋と壮大な川辺の景観で有名。',
    'twitterTitleChongqing': '重慶旅行ガイド - 山城、火鍋と長江の景色',
    'twitterDescChongqing': '重慶を探索——長江と嘉陵江の合流点に位置する3000万人の山城、火鍋と壮大な川辺の景観で有名。',
    'cityChongqing': '重慶',
    'descChongqing': '山城重慶、火鍋と長江・嘉陵江の絶景が魅力。',
  },
  'ko': {
    'pageTitleChongqing': '충칭 - 중국 여행',
    'metaDescriptionChongqing': '산성 충칭, 훠궈와 장강·자링강 합류점으로 유명한 3000만 대도시.',
    'ogTitleChongqing': '충칭 여행 가이드 - 산성, 훠궈와 장강 풍경',
    'ogDescChongqing': '충칭 탐험——장강과 자링강이 만나는 3000만 인구의 산성, 훠궈와 장엄한 강변 풍경으로 유명합니다.',
    'twitterTitleChongqing': '충칭 여행 가이드 - 산성, 훠궈와 장강 풍경',
    'twitterDescChongqing': '충칭 탐험——장강과 자링강이 만나는 3000만 인구의 산성, 훠궈와 장엄한 강변 풍경으로 유명합니다.',
    'cityChongqing': '충칭',
    'descChongqing': '산성 충칭, 훠궈와 장강·자링강의 장관이 어우러진 곳.',
  },
  'ru': {
    'pageTitleChongqing': 'Чунцин - Китайское путешествие',
    'metaDescriptionChongqing': 'Горный город Чунцин, знаменитый хого и слиянием рек Янцзы и Цзялин. Город с населением 30 млн.',
    'ogTitleChongqing': 'Путеводитель по Чунцину - Горный город, хого и река Янцзы',
    'ogDescChongqing': 'Исследуйте Чунцин — горный город с населением 30 млн человек у слияния рек Янцзы и Цзялин, знаменитый хого и захватывающими видами на реку.',
    'twitterTitleChongqing': 'Путеводитель по Чунцину - Горный город, хого и река Янцзы',
    'twitterDescChongqing': 'Исследуйте Чунцин — горный город с населением 30 млн человек у слияния рек Янцзы и Цзялин, знаменитый хого и захватывающими видами на реку.',
    'cityChongqing': 'Чунцин',
    'descChongqing': 'Горный город Чунцин, знаменитый хого и живописным слиянием рек Янцзы и Цзялин.',
  },
  'fr': {
    'pageTitleChongqing': 'Chongqing - Circuit Chine',
    'metaDescriptionChongqing': 'La ville montagneuse de Chongqing, célèbre pour son fondue chinoise et la confluence du Yangtsé et de la rivière Jialing.',
    'ogTitleChongqing': 'Guide de Chongqing - Ville montagneuse, fondue et fleuve Yangtsé',
    'ogDescChongqing': 'Découvrez Chongqing — une ville montagneuse de 30 millions d\'habitants au confluent du Yangtsé et de la Jialing, célèbre pour sa fondue chinoise et ses paysages fluviaux spectaculaires.',
    'twitterTitleChongqing': 'Guide de Chongqing - Ville montagneuse, fondue et fleuve Yangtsé',
    'twitterDescChongqing': 'Découvrez Chongqing — une ville montagneuse de 30 millions d\'habitants au confluent du Yangtsé et de la Jialing, célèbre pour sa fondue chinoise.',
    'cityChongqing': 'Chongqing',
    'descChongqing': 'La ville montagneuse célèbre pour sa fondue chinoise et la confluence des fleuves.',
  },
  'de': {
    'pageTitleChongqing': 'Chongqing - China-Reise',
    'metaDescriptionChongqing': 'Die Bergstadt Chongqing, berühmt für Hotpot und den Zusammenfluss von Jangtse und Jialing-Fluss.',
    'ogTitleChongqing': 'Chongqing Reiseführer - Bergstadt, Hotpot und Jangtse-Fluss',
    'ogDescChongqing': 'Entdecken Sie Chongqing — eine 30-Millionen-Bergstadt am Zusammenfluss von Jangtse und Jialing, berühmt für Hotpot und dramatische Flussuferlandschaften.',
    'twitterTitleChongqing': 'Chongqing Reiseführer - Bergstadt, Hotpot und Jangtse-Fluss',
    'twitterDescChongqing': 'Entdecken Sie Chongqing — eine 30-Millionen-Bergstadt am Zusammenfluss von Jangtse und Jialing.',
    'cityChongqing': 'Chongqing',
    'descChongqing': 'Die Bergstadt, berühmt für Hotpot und den Zusammenfluss von Jangtse und Jialing.',
  },
  'es': {
    'pageTitleChongqing': 'Chongqing - Viaje a China',
    'metaDescriptionChongqing': 'La ciudad montañosa de Chongqing, famosa por su hot pot y la confluencia del Yangtsé y el río Jialing.',
    'ogTitleChongqing': 'Guía de Chongqing - Ciudad montañosa, hot pot y río Yangtsé',
    'ogDescChongqing': 'Explore Chongqing — una ciudad montañosa de 30 millones de habitantes en la confluencia del Yangtsé y el Jialing, famosa por su hot pot y sus espectaculares paisajes ribereños.',
    'twitterTitleChongqing': 'Guía de Chongqing - Ciudad montañosa, hot pot y río Yangtsé',
    'twitterDescChongqing': 'Explore Chongqing — una ciudad montañosa de 30 millones de habitantes en la confluencia del Yangtsé y el Jialing.',
    'cityChongqing': 'Chongqing',
    'descChongqing': 'La ciudad montañosa famosa por su hot pot y la confluencia del Yangtsé y el Jialing.',
  }
};

const keysToFix = [
  'pageTitleChongqing',
  'metaDescriptionChongqing',
  'ogTitleChongqing',
  'ogDescChongqing',
  'twitterTitleChongqing',
  'twitterDescChongqing',
  'cityChongqing',
  'descChongqing'
];

let fixedCount = 0;

for (const lang of langs) {
  const filePath = path.join(rootDir, lang, 'chongqing.html');
  if (!fs.existsSync(filePath)) {
    console.log(`SKIP: ${filePath} not found`);
    continue;
  }
  
  let html = fs.readFileSync(filePath, 'utf-8');
  const origHtml = html;
  
  const langTrans = translations[lang];
  
  for (const key of keysToFix) {
    const newValue = langTrans[key];
    // Replace the string in window.translations
    // Pattern: "key":"old_value"
    const regex = new RegExp(`"${key}"\\s*:\\s*"[^"]*"`, 'g');
    const replacement = `"${key}":"${newValue.replace(/"/g, '\\"')}"`;
    html = html.replace(regex, replacement);
  }
  
  // Also fix the data-lang-key attributes in the body (for city-sub text and h1 fallback)
  // Find: data-lang-key="descChongqing">some text</p>
  // Replace the display text for descChongqing (city-sub)
  const descRegex = new RegExp(`(data-lang-key="descChongqing"[^>]*>)[^<]+(<)`);
  html = html.replace(descRegex, `$1${langTrans['descChongqing']}$2`);
  
  if (html !== origHtml) {
    fs.writeFileSync(filePath, html, 'utf-8');
    console.log(`FIXED: ${filePath}`);
    fixedCount++;
  } else {
    console.log(`UNCHANGED: ${filePath}`);
  }
}

console.log(`\nDone! Fixed ${fixedCount} files.`);