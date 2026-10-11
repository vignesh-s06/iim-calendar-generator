const fs = require('fs');
const p = 'D:/demo_retailer_updated/package.json';
let s = fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
if (!s.includes('"tslint": "5.18.0"')) throw new Error('expected tslint 5.18.0 not found');
s = s.replace('"tslint": "5.18.0"', '"tslint": "6.1.3"');
JSON.parse(s);
fs.writeFileSync(p, s, 'utf8');
console.log('package ok');
