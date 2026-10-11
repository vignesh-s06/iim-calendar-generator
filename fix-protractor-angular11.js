const fs = require('fs');
const p = 'D:/demo_retailer_updated/package.json';
let s = fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
if (!s.includes('"protractor": "5.4.3"')) throw new Error('expected protractor 5.4.3 not found');
s = s.replace('"protractor": "5.4.3"', '"protractor": "7.0.0"');
JSON.parse(s);
fs.writeFileSync(p, s, 'utf8');
console.log('package ok');
