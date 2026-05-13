const fs = require('fs');

const translationsPath = './js/translations.js';
let content = fs.readFileSync(translationsPath, 'utf8');

// Find the start of the translations object
const startToken = 'const translations = {';
const startIndex = content.indexOf(startToken);
if (startIndex === -1) {
  throw new Error('Could not find translations object start');
}

// Now find the end of the object by matching braces
let braceCount = 0;
let i = startIndex + startToken.length; // position after the opening brace
let endIndex = -1;
while (i < content.length) {
  const ch = content[i];
  if (ch === '{') braceCount++;
  if (ch === '}') {
    braceCount--;
    if (braceCount === 0) {
      endIndex = i; // index of the closing brace
      break;
    }
  }
  i++;
}
if (endIndex === -1) {
  throw new Error('Could not find end of translations object');
}

// Extract the object string (including the braces)
const objStr = content.slice(startIndex, endIndex + 1);
// Parse the object
let translationsObj;
try {
  translationsObj = new Function(`return ${objStr}`)();
} catch (e) {
  throw new Error(`Failed to parse translations object: ${e.message}`);
}

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
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const match = fileContent.match(/window\.translations = ({[^}]+});/s);
    if (!match) {
      console.log(`Warning: Could not find window.translations in ${filePath}`);
      continue;
    }
    const fileObjStr = match[1];
    const fileObj = new Function(`return ${fileObjStr}`)();
    const zhCnSection = fileObj['zh-CN'];
    if (!zhCnSection) {
      console.log(`Warning: No zh-CN section in ${filePath}`);
      continue;
    }
    const value = zhCnSection[key];
    if (value === undefined) {
      console.log(`Warning: Key ${key} not found in zh-CN section of ${filePath}`);
      continue;
    }
    console.log(`Updating ${key} from ${filePath} (length: ${value.length})`);
    // Update the translations object
    translationsObj['zh-CN'][key] = value;
  } catch (e) {
    console.log(`Error processing ${filePath}: ${e.message}`);
  }
}

// Serialize the updated object with 2-space indentation
const newObjStr = JSON.stringify(translationsObj, null, 2);
// Note: JSON.stringify produces a string that includes the outer braces.
// We need to replace the old object string (from startIndex to endIndex+1) with this new string.
const newContent = content.slice(0, startIndex) + newObjStr + content.slice(endIndex + 1);

// Write back to file
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
  process.exit(1);
}