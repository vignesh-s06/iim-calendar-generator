const fs = require('fs');
const p = 'D:/demo_retailer_updated/package.json';
let s = fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
if (!s.includes('"ngx-red-zoom": "0.4.1"')) throw new Error('expected ngx-red-zoom 0.4.1 not found');
s = s.replace('"ngx-red-zoom": "0.4.1"', '"ngx-red-zoom": "0.6.0"');
JSON.parse(s);
fs.writeFileSync(p, s, 'utf8');
console.log('package ok');
