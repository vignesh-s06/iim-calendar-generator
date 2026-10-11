const fs = require('fs');
const p = 'D:/demo_retailer_updated/package.json';
let s = fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
const replacements = new Map([
  ['"jasmine-core": "3.5.0"', '"jasmine-core": "3.8.0"'],
  ['"karma": "4.3.0"', '"karma": "6.4.4"'],
  ['"karma-coverage-istanbul-reporter": "2.1.1"', '"karma-coverage-istanbul-reporter": "3.0.3"'],
  ['"karma-jasmine": "2.0.1"', '"karma-jasmine": "4.0.2"'],
  ['"karma-jasmine-html-reporter": "1.5.1"', '"karma-jasmine-html-reporter": "1.7.0"']
]);
for (const [from, to] of replacements) {
  if (!s.includes(from)) throw new Error(`missing ${from}`);
  s = s.replace(from, to);
}
JSON.parse(s);
fs.writeFileSync(p, s, 'utf8');
console.log('package ok');
