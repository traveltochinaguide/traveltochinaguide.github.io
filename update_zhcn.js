const fs = require('fs');
const path = require('path');

// Load translations.js
const translationsPath = './js/translations.js';
let content = fs.readFileSync(translationsPath, 'utf8');

// Evaluate the translations object
// We'll use a simple approach: find the module.exports assignment and extract the object.
// Since the file ends with: };\n\nif (typeof module !== 'undefined' && module.exports) { module.exports = translations; }
// We can extract the object by matching from the start to the }; before the if statement.
// But easier: we can require it and then stringify it back? However, we need to preserve the format.
// Let's do a require and then write back with the same format? That might change formatting.
// Instead, we'll do a targeted replacement for each key.

const cities = ['chongqing', 'guangzhou', 'shenzhen', 'kunming', 'dali', 'lijiang'];

for (const city of cities) {
  const key = 'longDesc' + city[0].toUpperCase() + city.slice(1);
  const filePath = `zh-CN/${city}.html`;
  if (!fs.existsSync(filePath)) {
    console.log(`File not found: ${filePath}`);
    continue;
  }
  const fileContent = fs.readFileSync(filePath, 'utf8');
  // Extract the window.translations object
  const match = fileContent.match(/window\.translations = ({[^}]+});/s);
  if (!match) {
    console.log(`Could not find window.translations in ${filePath}`);
    continue;
  }
  const objStr = match[1];
  // Parse the JSON-like string. Note: it's not valid JSON because of trailing commas? Actually it is valid JSON? It seems to be a JS object.
  // We'll use a simple regex to extract the value for the key.
  // The pattern: "longDescChongqing":"<value>" but the value may contain quotes and backslashes escaped.
  // Instead, we can use the same method as before: evaluate the object in a sandbox.
  // We'll create a function that returns the object.
  let transObj;
  try {
    transObj = new Function(`return ${objStr}`)();
  } catch (e) {
    console.log(`Failed to parse translations object in ${filePath}: ${e.message}`);
    continue;
  }
  const zhCnObj = transObj['zh-CN'];
  if (!zhCnObj) {
    console.log(`No zh-CN section in ${filePath}`);
    continue;
  }
  const value = zhCnObj[key];
  if (value === undefined) {
    console.log(`Key ${key} not found in zh-CN section of ${filePath}`);
    continue;
  }
  console.log(`Extracted ${key} from ${filePath}, length: ${value.length}`);

  // Now we need to update the translations.js file: replace the value for this key in the zh-CN section.
  // We'll do a regex replacement: find the zh-CN section and replace the key's value.
  // We'll be careful to preserve the structure.
  // We'll replace: "longDescChongqing":"old value" with "longDescChongqing":"new value"
  // We need to escape the new value for inclusion in a JS string: we need to escape backslashes and quotes.
  // Since the value is already a string that was extracted from a JS string, it should be properly escaped.
  // However, when we extracted it via new Function, we got the actual string (with quotes unescaped).
  // We need to re-escape it for inclusion in a JS string literal.
  const escapedValue = value
    .replace(/\\/g, '\\\\') // escape backslashes
    .replace(/"/g, '\\"')   // escape double quotes
    .replace(/\n/g, '\\n')  // escape newlines
    .replace(/\r/g, '\\r'); // escape carriage returns

  // Now replace in the translations.js content.
  // We'll target the zh-CN section. We'll find the pattern: \"zh-CN\":{ ... } and replace inside.
  // To avoid messing up other sections, we'll do a replacement that is specific to the key.
  // We'll replace: \"longDescChongqing\":\"[^\"]*\" but the value may contain escaped quotes.
  // Instead, we'll do a more robust approach: find the zh-CN section and then replace the key-value pair.
  // We'll split the content into lines and process? Might be heavy.

  // Let's do a regex that matches the key and its value in the zh-CN section.
  // We'll assume the zh-CN section is the first occurrence of \"zh-CN\":{ ... } followed by a comma and then the next language or the end of the translations object.
  // We'll do a global search for the key and replace its value, but only if it's inside the zh-CN section.
  // We'll first isolate the zh-CN section.

  const zhCnSectionMatch = content.match(/(\"zh-CN\":{)[^}]+(}})/s);
  if (!zhCnSectionMatch) {
    console.log(`Could not find zh-CN section in translations.js`);
    continue;
  }
  const zhCnSection = zhCnSectionMatch[0];
  // Now replace the key-value pair in this section.
  // We'll look for: \"longDescChongqing\":\"[^\"]*\" but again, the value may contain escaped quotes.
  // Instead, we can replace the entire key-value pair by matching the key and then everything until the next comma or closing brace.
  // We'll use: (\"longDescChongqing\":\")[^\"]*(\") but the value may contain escaped quotes.
  // Given that we have the exact value we want to replace, we can do:
  const oldPattern = new RegExp(`(\\\"${key}\\\":\\\")[^\\"]*(\\\")`, 'g');
  // But the value may contain escaped quotes, so [^"]* will stop at the first escaped quote.
  // We need to match until we see an unescaped quote.
  // Let's do a simpler approach: we know the current value in translations.js (we can get it from the en translation? but we want to replace whatever is there).
  // Instead, we'll just replace the entire zh-Cn section with a newly constructed one? That might be too heavy.

  // Given the time, we'll do a simpler approach: we'll replace the value by searching for the key and then replacing the substring between the quotes after the colon, assuming there are no escaped quotes in the value.
  // However, the value may contain escaped quotes (e.g., from HTML). In the extracted value, the quotes are not escaped because they are part of the string.
  // When we re-escape, we are escaping the quotes, so the new value will have escaped quotes.
  // The old value in translations.js also has escaped quotes.
  // So we can do: find the pattern: \"longDescChongqing\":\" then match until we see a \" that is not preceded by a \\.
  // We'll write a helper function to escape the regex.

  // Let's do a different approach: we'll reconstruct the entire translations.js object by requiring it and then updating the zh-Cn section and then writing it back with the same formatting? That might lose formatting but is acceptable.

  // We'll break and do that instead.
}

console.log('Processing complete.');

// Now, let's actually do the require and write back approach.