const fs = require('fs');
const p = 'D:/demo_retailer_updated/package.json';
let s = fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
const replacements = new Map([
  ['"@ag-grid-community/all-modules": "26.0.0"', '"@ag-grid-community/all-modules": "27.0.0"'],
  ['"@angular/google-maps": "12.2.13"', '"@angular/google-maps": "13.3.9"'],
  ['"@angular/animations": "12.2.17"', '"@angular/animations": "13.3.12"'],
  ['"@angular/cdk": "12.2.13"', '"@angular/cdk": "13.3.9"'],
  ['"@angular/common": "12.2.17"', '"@angular/common": "13.3.12"'],
  ['"@angular/compiler": "12.2.17"', '"@angular/compiler": "13.3.12"'],
  ['"@angular/core": "12.2.17"', '"@angular/core": "13.3.12"'],
  ['"@angular/flex-layout": "12.0.0-beta.35"', '"@angular/flex-layout": "13.0.0-beta.38"'],
  ['"@angular/forms": "12.2.17"', '"@angular/forms": "13.3.12"'],
  ['"@angular/material": "12.2.13"', '"@angular/material": "13.3.9"'],
  ['"@angular/material-moment-adapter": "12.2.13"', '"@angular/material-moment-adapter": "13.3.9"'],
  ['"@angular/platform-browser": "12.2.17"', '"@angular/platform-browser": "13.3.12"'],
  ['"@angular/platform-browser-dynamic": "12.2.17"', '"@angular/platform-browser-dynamic": "13.3.12"'],
  ['"@angular/router": "12.2.17"', '"@angular/router": "13.3.12"'],
  ['"@ngrx/effects": "12.5.1"', '"@ngrx/effects": "13.2.0"'],
  ['"@ngrx/router-store": "12.5.1"', '"@ngrx/router-store": "13.2.0"'],
  ['"@ngrx/store": "12.5.1"', '"@ngrx/store": "13.2.0"'],
  ['"@ngrx/store-devtools": "12.5.1"', '"@ngrx/store-devtools": "13.2.0"'],
  ['"@swimlane/ngx-charts": "18.0.1"', '"@swimlane/ngx-charts": "19.2.0"'],
  ['"ag-grid-angular": "26.0.0"', '"ag-grid-angular": "27.0.0"'],
  ['"ag-grid-community": "26.0.0"', '"ag-grid-community": "27.0.0"'],
  ['"angular-gridster2": "12.1.0"', '"angular-gridster2": "13.3.2"'],
  ['"ngx-red-zoom": "0.7.0"', '"ngx-red-zoom": "0.9.0"'],
  ['"ngx-quill": "14.3.0"', '"ngx-quill": "15.0.0"'],
  ['"zone.js": "0.11.4"', '"zone.js": "0.11.8"'],
  ['"@angular-devkit/build-angular": "12.2.18"', '"@angular-devkit/build-angular": "13.3.11"'],
  ['"@angular/cli": "12.2.18"', '"@angular/cli": "13.3.11"'],
  ['"@angular/compiler-cli": "12.2.17"', '"@angular/compiler-cli": "13.3.12"'],
  ['"@angular/language-service": "12.2.17"', '"@angular/language-service": "13.3.12"'],
  ['"typescript": "4.3.5"', '"typescript": "4.6.4"']
]);
for (const [from, to] of replacements) {
  if (!s.includes(from)) throw new Error(`Missing expected package string: ${from}`);
  s = s.replace(from, to);
}
JSON.parse(s);
fs.writeFileSync(p, s, 'utf8');
console.log('package ok');
