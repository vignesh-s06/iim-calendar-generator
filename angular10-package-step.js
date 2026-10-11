const fs = require('fs');
const path = 'D:/demo_retailer_updated/package.json';
let text = fs.readFileSync(path, 'utf8');
const replacements = new Map([
  ['"@angular/google-maps": "9.2.4"', '"@angular/google-maps": "10.2.7"'],
  ['"@angular/animations": "9.0.0"', '"@angular/animations": "10.2.5"'],
  ['"@angular/cdk": "9.0.0"', '"@angular/cdk": "10.2.7"'],
  ['"@angular/common": "9.0.0"', '"@angular/common": "10.2.5"'],
  ['"@angular/compiler": "9.0.0"', '"@angular/compiler": "10.2.5"'],
  ['"@angular/core": "9.0.0"', '"@angular/core": "10.2.5"'],
  ['"@angular/flex-layout": "9.0.0-beta.29"', '"@angular/flex-layout": "10.0.0-beta.32"'],
  ['"@angular/forms": "9.0.0"', '"@angular/forms": "10.2.5"'],
  ['"@angular/material": "9.0.0"', '"@angular/material": "10.2.7"'],
  ['"@angular/material-moment-adapter": "9.0.0"', '"@angular/material-moment-adapter": "10.2.7"'],
  ['"@angular/platform-browser": "9.0.0"', '"@angular/platform-browser": "10.2.5"'],
  ['"@angular/platform-browser-dynamic": "9.0.0"', '"@angular/platform-browser-dynamic": "10.2.5"'],
  ['"@angular/router": "9.0.0"', '"@angular/router": "10.2.5"'],
  ['"@ngrx/effects": "8.6.0"', '"@ngrx/effects": "10.1.2"'],
  ['"@ngrx/router-store": "8.6.0"', '"@ngrx/router-store": "10.1.2"'],
  ['"@ngrx/store": "8.6.0"', '"@ngrx/store": "10.1.2"'],
  ['"@ngrx/store-devtools": "8.6.0"', '"@ngrx/store-devtools": "10.1.2"'],
  ['"angular-gridster2": "11.1.5"', '"angular-gridster2": "10.1.7"'],
  ['"angular-in-memory-web-api": "0.9.0"', '"angular-in-memory-web-api": "0.10.0"'],
  ['"rxjs": "6.5.4"', '"rxjs": "6.6.7"'],
  ['"tslib": "1.10.0"', '"tslib": "2.0.3"'],
  ['"zone.js": "0.10.2"', '"zone.js": "0.10.3"'],
  ['"@angular-devkit/build-angular": "0.900.1"', '"@angular-devkit/build-angular": "0.1002.4"'],
  ['"@angular/cli": "9.0.1"', '"@angular/cli": "10.2.4"'],
  ['"@angular/compiler-cli": "9.0.0"', '"@angular/compiler-cli": "10.2.5"'],
  ['"@angular/language-service": "9.0.0"', '"@angular/language-service": "10.2.5"'],
  ['"codelyzer": "5.2.1"', '"codelyzer": "6.0.2"'],
  ['"typescript": "3.7.5"', '"typescript": "3.9.10"']
]);
for (const [from, to] of replacements) {
  if (!text.includes(from)) throw new Error(`Missing expected package string: ${from}`);
  text = text.replace(from, to);
}
text = text.replace(/\r?\n        "ng-image-fullscreen-view": "2\.0\.0",/, '');
fs.writeFileSync(path, text, 'utf8');
