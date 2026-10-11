const fs = require('fs');
const p = 'D:/demo_retailer_updated/package.json';
let s = fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
if (!s.includes('"ngx-pinch-zoom": "2.5.4"')) {
  throw new Error('expected ngx-pinch-zoom 2.5.4 not found');
}
s = s.replace('"ngx-pinch-zoom": "2.5.4"', '"ngx-pinch-zoom": "2.6.0"');
JSON.parse(s);
fs.writeFileSync(p, s, 'utf8');
console.log('package ok');
