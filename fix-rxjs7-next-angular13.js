const fs = require('fs');
const path = require('path');
const root = 'D:/demo_retailer_updated/src';
const files = [];
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (entry.isFile() && entry.name.endsWith('.ts')) files.push(full);
  }
}
walk(root);
let changed = 0;
for (const file of files) {
  const before = fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
  let after = before
    .replace(/from 'rxjs\/internal\/operators'/g, "from 'rxjs/operators'")
    .replace(/from "rxjs\/internal\/operators"/g, 'from "rxjs/operators"')
    .replace(/\.next\(\);/g, '.next(undefined);');
  if (after !== before) {
    fs.writeFileSync(file, after, 'utf8');
    changed++;
    console.log(file);
  }
}
console.log(`changed files: ${changed}`);
