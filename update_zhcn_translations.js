const fs = require('fs');
const path = require('path');

// Function to extract the translations object from a file's window.translations
function extractTranslationsFromFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const match = content.match(/window\.translations = ({[^}]+});/s);
  if (!match) {
    throw new Error(`Could not find window.translations in ${filePath}`);
  }
  const objStr = match[1];
  // Use Function constructor to parse the object string (it's a valid JS object)
  // Note: This is safe because we trust the source.
  const transObj = new Function(`return ${objStr}`)();
  return transObj;
}

// Function to escape a string for inclusion in a JS double-quoted string
function escapeJsString(str) {
  return str
    .replace(/\\/g, '\\\\') // escape backslashes
    .replace(/"/g, '\\"')   // escape double quotes
    .replace(/\n/g, '\\n')  // escape newlines
    .replace(/\r/g, '\\r'); // escape carriage returns
}

// Load the current translations.js
const translationsPath = './js/translations.js';
let translationsContent = fs.readFileSync(translationsPath, 'utf8');

// Parse the translations object from translations.js
// We'll extract the object similarly: find the assignment to translations variable
// The file structure: ... var translations = { ... };
// We'll look for the pattern: translations = { ... };
const transMatch = translationsContent.match(/translations\s*=\s*({[^}]+});/s);
if (!transMatch) {
  throw new Error('Could not find translations object in translations.js');
}
const translationsObjStr = transMatch[1];
const translationsObj = new Function(`return ${translationsObjStr}`)();

// Cities to process
const cities = ['chongqing', 'guangzhou', 'shenzhen', 'kunming', 'dali', 'lijiang'];

for (const city of cities) {
  const key = 'longDesc' + city[0].toUpperCase() + city.slice(1);
  const filePath = `zh-CN/${city}.html`;
  
  if (!fs.existsSync(filePath)) {
    console.log(`Warning: File not found: ${filePath}`);
    continue;
  }
  
  try {
    const fileTrans = extractTranslationsFromFile(filePath);
    const zhCnSection = fileTrans['zh-CN'];
    if (!zhCnSection) {
      console.log(`Warning: No zh-CN section in ${filePath}`);
      continue;
    }
    const value = zhCnSection[key];
    if (value === undefined) {
      console.log(`Warning: Key ${key} not found in zh-CN section of ${filePath}`);
      continue;
    }
    
    console.log(`Updating ${key} in translations.js with value from ${filePath} (length: ${value.length})`);
    
    // Update the translations object in memory
    translationsObj['zh-CN'][key] = value;
    
    // Now we need to update the translationsContent string.
    // We'll replace the value for this key in the zh-Cn section.
    // We'll do a regex replacement that targets the zh-Cn section and then the specific key.
    // We'll construct a regex that matches: "key":"old_value" and replace with "key":"new_value"
    // We must escape the old value for regex, but we don't have the old value easily.
    // Instead, we can replace the entire zh-Cn section with a newly constructed one? That might be too heavy.
    
    // Let's do a regex that matches the key and its value in the zh-Cn section.
    // We'll assume the value does not contain unescaped quotes (they are escaped in the JS string).
    // We'll replace: "longDescChongqing":"[^"]*" but note the value may contain escaped quotes.
    // We'll use a more robust method: we know the current value in the translationsObj (before update) but we didn't save it.
    // We'll instead reconstruct the entire translations object and write it back, preserving the rest of the file.
    // This is acceptable because the file is not too large and we are the only ones modifying it.
    
    // We'll break out of the loop and do a full replacement after processing all cities.
  } catch (e) {
    console.log(`Error processing ${filePath}: ${e.message}`);
  }
}

// If we got here, we have updated the translationsObj in memory.
// Now we need to write it back to translations.js, preserving the rest of the file.
// We'll replace the old translations object with the new one.
// We'll keep the prefix (everything before the translations object) and the suffix (everything after).
const prefix = translationsContent.substring(0, transMatch.index);
const suffix = translationsContent.substring(transMatch.index + transMatch[0].length);

// Now we need to serialize the translationsObj back to a string.
// We'll use JSON.stringify but note that the original file has a specific format:
//   - It uses single quotes for property names? Actually it uses double quotes.
//   - It has trailing commas? Let's check: the original file we saw uses double quotes and no trailing commas in the object.
//   - However, the original file has a comment at the top and a specific structure.
// We'll try to mimic the original by using JSON.stringify and then adjusting.
// But note: the original file has the translations object as part of a larger structure:
//   var translations = {
//     en: { ... },
//     'zh-CN': { ... },
//     ...,
//     cityDetails: { ... },
//     carouselData: [ ... ]
//   };
// Our translationsObj only has the 'translations' property? Actually, the variable we extracted is the entire object assigned to translations.
// Let's look at the original: the translations object includes en, zh-Cn, ja, etc., and also cityDetails and carouselData.
// Our extracted translationsObj is exactly that object.

// We'll serialize with JSON.stringify, but we lose the formatting (spaces, indentation).
// The original file uses 2-space indentation? We can try to beautify, but for now, let's produce valid JSON and hope the generator doesn't care about formatting.
// However, note that the original file has a comment at the top and the object ends with }; and then an if statement for module.exports.
// We must preserve the file structure exactly: we are only replacing the object assigned to translations.

// Let's serialize the translationsObj to a JS object string with the same formatting as the original? We'll do a simple approach:
//   - Use JSON.stringify with 2 spaces.
//   - Then replace the outermost braces to match the original? Actually, the original is exactly a JSON object (with the exception that it might have trailing commas? We'll avoid that).
//   - We'll wrap in 'var translations = ' and then add ';'

const newTranslationsStr = 'var translations = ' + JSON.stringify(translationsObj, null, 2) + ';';

// Now reconstruct the file:
const newContent = prefix + newTranslationsStr + suffix;

// Write back to translations.js
fs.writeFileSync(translationsPath, newContent, 'utf8');
console.log('Updated translations.js');

// Validate the syntax
const { execSync } = require('child_process');
try {
  execSync('node -e \"require(\\\"./js/translations.js\\\")\"', { stdio: 'ignore' });
  console.log('Syntax check passed');
} catch (e) {
  console.log('Syntax check failed:');
  console.log(e.message);
  // Restore the original? We'll exit with error.
  process.exit(1);
}