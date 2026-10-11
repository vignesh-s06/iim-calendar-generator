const fs = require('fs');
const p = 'D:/demo_retailer_updated/package.json';
let s = fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
if (!s.includes('"angular-google-charts": "2.0.1"')) throw new Error('expected angular-google-charts 2.0.1 not found');
s = s.replace('"angular-google-charts": "2.0.1"', '"angular-google-charts": "12.0.0"');
JSON.parse(s);
fs.writeFileSync(p, s, 'utf8');
console.log('package ok');
