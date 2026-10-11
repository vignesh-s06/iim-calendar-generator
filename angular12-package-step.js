const fs = require('fs');
const p = 'D:/demo_retailer_updated/package.json';
let s = fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
const replacements = new Map([
  ['"@ag-grid-community/all-modules": "25.0.1"', '"@ag-grid-community/all-modules": "26.0.0"'],
  ['"@angular/google-maps": "11.2.13"', '"@angular/google-maps": "12.2.13"'],
  ['"@angular/animations": "11.2.14"', '"@angular/animations": "12.2.17"'],
  ['"@angular/cdk": "11.2.13"', '"@angular/cdk": "12.2.13"'],
  ['"@angular/common": "11.2.14"', '"@angular/common": "12.2.17"'],
  ['"@angular/compiler": "11.2.14"', '"@angular/compiler": "12.2.17"'],
  ['"@angular/core": "11.2.14"', '"@angular/core": "12.2.17"'],
  ['"@angular/flex-layout": "11.0.0-beta.33"', '"@angular/flex-layout": "12.0.0-beta.35"'],
  ['"@angular/forms": "11.2.14"', '"@angular/forms": "12.2.17"'],
  ['"@angular/material": "11.2.13"', '"@angular/material": "12.2.13"'],
  ['"@angular/material-moment-adapter": "11.2.13"', '"@angular/material-moment-adapter": "12.2.13"'],
  ['"@angular/platform-browser": "11.2.14"', '"@angular/platform-browser": "12.2.17"'],
  ['"@angular/platform-browser-dynamic": "11.2.14"', '"@angular/platform-browser-dynamic": "12.2.17"'],
  ['"@angular/router": "11.2.14"', '"@angular/router": "12.2.17"'],
  ['"@ngrx/effects": "11.1.1"', '"@ngrx/effects": "12.5.1"'],
  ['"@ngrx/router-store": "11.1.1"', '"@ngrx/router-store": "12.5.1"'],
  ['"@ngrx/store": "11.1.1"', '"@ngrx/store": "12.5.1"'],
  ['"@ngrx/store-devtools": "11.1.1"', '"@ngrx/store-devtools": "12.5.1"'],
  ['"@swimlane/ngx-charts": "17.0.1"', '"@swimlane/ngx-charts": "18.0.1"'],
  ['"@swimlane/ngx-datatable": "19.0.0"', '"@swimlane/ngx-datatable": "20.1.0"'],
  ['"ag-grid-angular": "25.0.1"', '"ag-grid-angular": "26.0.0"'],
  ['"ag-grid-community": "25.0.1"', '"ag-grid-community": "26.0.0"'],
  ['"angular-gridster2": "11.1.5"', '"angular-gridster2": "12.1.0"'],
  ['"ngx-red-zoom": "0.6.0"', '"ngx-red-zoom": "0.7.0"'],
  ['"ngx-quill": "13.4.0"', '"ngx-quill": "14.3.0"'],
  ['"typescript": "4.1.6"', '"typescript": "4.3.5"'],
  ['"@angular-devkit/build-angular": "0.1102.19"', '"@angular-devkit/build-angular": "12.2.18"'],
  ['"@angular/cli": "11.2.19"', '"@angular/cli": "12.2.18"'],
  ['"@angular/compiler-cli": "11.2.14"', '"@angular/compiler-cli": "12.2.17"'],
  ['"@angular/language-service": "11.2.14"', '"@angular/language-service": "12.2.17"']
]);
for (const [from, to] of replacements) {
  if (!s.includes(from)) throw new Error(`Missing expected package string: ${from}`);
  s = s.replace(from, to);
}
s = s.replace(/\r?\n        "ngx-pinch-zoom": "2\.6\.0",/, '');
JSON.parse(s);
fs.writeFileSync(p, s, 'utf8');
console.log('package ok');

const cat = 'D:/demo_retailer_updated/src/app/catalogue/catalogue.module.ts';
let c = fs.readFileSync(cat, 'utf8').replace(/^\uFEFF/, '');
c = c.replace(/\r?\nimport \{ PinchZoomModule \} from 'ngx-pinch-zoom';/, '');
c = c.replace(/\r?\n\s*PinchZoomModule,/, '');
fs.writeFileSync(cat, c, 'utf8');
console.log('catalogue module ok');
