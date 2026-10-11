const fs = require('fs');
const p = 'D:/demo_retailer_updated/package.json';
let s = fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
const replacements = new Map([
  ['"@ag-grid-community/all-modules": "24.1.0"', '"@ag-grid-community/all-modules": "25.0.1"'],
  ['"@angular/google-maps": "10.2.7"', '"@angular/google-maps": "11.2.13"'],
  ['"@angular/animations": "10.2.5"', '"@angular/animations": "11.2.14"'],
  ['"@angular/cdk": "10.2.7"', '"@angular/cdk": "11.2.13"'],
  ['"@angular/common": "10.2.5"', '"@angular/common": "11.2.14"'],
  ['"@angular/compiler": "10.2.5"', '"@angular/compiler": "11.2.14"'],
  ['"@angular/core": "10.2.5"', '"@angular/core": "11.2.14"'],
  ['"@angular/flex-layout": "10.0.0-beta.32"', '"@angular/flex-layout": "11.0.0-beta.33"'],
  ['"@angular/forms": "10.2.5"', '"@angular/forms": "11.2.14"'],
  ['"@angular/material": "10.2.7"', '"@angular/material": "11.2.13"'],
  ['"@angular/material-moment-adapter": "10.2.7"', '"@angular/material-moment-adapter": "11.2.13"'],
  ['"@angular/platform-browser": "10.2.5"', '"@angular/platform-browser": "11.2.14"'],
  ['"@angular/platform-browser-dynamic": "10.2.5"', '"@angular/platform-browser-dynamic": "11.2.14"'],
  ['"@angular/router": "10.2.5"', '"@angular/router": "11.2.14"'],
  ['"@ngrx/effects": "10.1.2"', '"@ngrx/effects": "11.1.1"'],
  ['"@ngrx/router-store": "10.1.2"', '"@ngrx/router-store": "11.1.1"'],
  ['"@ngrx/store": "10.1.2"', '"@ngrx/store": "11.1.1"'],
  ['"@ngrx/store-devtools": "10.1.2"', '"@ngrx/store-devtools": "11.1.1"'],
  ['"@swimlane/ngx-charts": "16.0.0"', '"@swimlane/ngx-charts": "17.0.1"'],
  ['"@swimlane/ngx-datatable": "18.0.0"', '"@swimlane/ngx-datatable": "19.0.0"'],
  ['"ag-grid-angular": "24.1.0"', '"ag-grid-angular": "25.0.1"'],
  ['"ag-grid-community": "24.1.0"', '"ag-grid-community": "25.0.1"'],
  ['"angular-gridster2": "10.1.7"', '"angular-gridster2": "11.1.5"'],
  ['"ngx-quill": "12.0.1"', '"ngx-quill": "13.4.0"'],
  ['"tslib": "2.0.3"', '"tslib": "2.1.0"'],
  ['"zone.js": "0.10.3"', '"zone.js": "0.11.4"'],
  ['"@angular-devkit/build-angular": "0.1002.4"', '"@angular-devkit/build-angular": "0.1102.19"'],
  ['"@angular/cli": "10.2.4"', '"@angular/cli": "11.2.19"'],
  ['"@angular/compiler-cli": "10.2.5"', '"@angular/compiler-cli": "11.2.14"'],
  ['"@angular/language-service": "10.2.5"', '"@angular/language-service": "11.2.14"'],
  ['"typescript": "3.9.10"', '"typescript": "4.1.6"']
]);
for (const [from, to] of replacements) {
  if (!s.includes(from)) throw new Error(`Missing expected package string: ${from}`);
  s = s.replace(from, to);
}
JSON.parse(s);
fs.writeFileSync(p, s, 'utf8');
