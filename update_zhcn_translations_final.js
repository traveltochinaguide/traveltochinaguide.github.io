const fs = require('fs');

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

// Load the translations.js file
const translationsPath = './js/translations.js';
let translationsContent = fs.readFileSync(translationsPath, 'utf8');

// Find the translations object in the file: look for the pattern: var translations = {
const transMatch = translationsContent.match(/(\bvar\s+translations\s*=\s*)({[\s\S]*?})(\s*;)/);
if (!transMatch) {
  throw new Error('Could not find translations object in translations.js');
}
const prefixBefore = transMatch[1]; // "var translations = "
const translationsObjStr = transMatch[2]; // the object string
const suffixAfter = transMatch[3]; // ";"

// Parse the translations object string
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
    
  } catch (e) {
    console.log(`Error processing ${filePath}: ${e.message}`);
  }
}

// Now we need to rebuild the translations object string with the updated values.
// We'll use JSON.stringify to produce a valid JSON object, but note that the original may have specific formatting.
// We'll try to keep the same structure by using JSON.stringify with 2 spaces, but note that the original uses trailing commas? 
// Actually, the original file we saw does not have trailing commas in the object (it's valid JSON).
// However, the original file has the translations object as part of a larger structure with other consts.
// We are only replacing the object assigned to translations.

// Serialize the updated translations object
const newTranslationsObjStr = JSON.stringify(translationsObj, null, 2);
// Note: JSON.stringify produces a string with double quotes and no trailing commas.
// This should be valid for the assignments we saw.

// Reconstruct the file content
const newContent = prefixBefore + newTranslationsObjStr + suffixAfter;

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