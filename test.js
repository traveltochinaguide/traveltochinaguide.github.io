const fs = require('fs');
const content = fs.readFileSync('architecture.html', 'utf8');
const regex = /data-lang-key="([^"])"[^>]*>([^<]*)/g;
let match;
while ((match = regex.exec(content)) !== null) {
  console.log('Key:', match[1], 'Text:', match[2]);
}
