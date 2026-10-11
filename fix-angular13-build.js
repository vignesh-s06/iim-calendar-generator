const fs = require('fs');
function edit(file, fn) {
  const before = fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
  const after = fn(before);
  fs.writeFileSync(file, after, 'utf8');
}
edit('D:/demo_retailer_updated/package.json', s => {
  if (!s.includes('"rxjs": "6.6.7"')) throw new Error('expected rxjs 6.6.7 not found');
  s = s.replace('"rxjs": "6.6.7"', '"rxjs": "7.5.7"');
  if (s.includes('"tslib": "2.1.0"')) s = s.replace('"tslib": "2.1.0"', '"tslib": "2.3.1"');
  return s;
});
edit('D:/demo_retailer_updated/src/app/main/apps/chat/chat-view/chat-view.component.html', s =>
  s.replace('[matTextareaAutosize]="true"', '[cdkTextareaAutosize]="true"')
);
edit('D:/demo_retailer_updated/src/app/main/apps/chat/chat.module.ts', s => {
  if (!s.includes("import { TextFieldModule } from '@angular/cdk/text-field';")) {
    s = s.replace("import { MatToolbarModule } from '@angular/material/toolbar';", "import { MatToolbarModule } from '@angular/material/toolbar';\r\nimport { TextFieldModule } from '@angular/cdk/text-field';");
  }
  if (!s.includes('TextFieldModule,')) {
    s = s.replace('        MatToolbarModule,', '        MatToolbarModule,\r\n        TextFieldModule,');
  }
  return s;
});
const shim = `declare namespace google.maps.visualization {\r\n    interface WeightedLocation {\r\n        location: google.maps.LatLng;\r\n        weight: number;\r\n    }\r\n\r\n    interface HeatmapLayerOptions {\r\n        data?: google.maps.MVCArray<google.maps.LatLng | WeightedLocation | google.maps.LatLngLiteral> | (google.maps.LatLng | WeightedLocation | google.maps.LatLngLiteral)[];\r\n        dissipating?: boolean;\r\n        gradient?: string[];\r\n        map?: google.maps.Map | null;\r\n        maxIntensity?: number;\r\n        opacity?: number;\r\n        radius?: number;\r\n    }\r\n}\r\n`;
fs.writeFileSync('D:/demo_retailer_updated/src/google-maps-visualization.d.ts', shim, 'utf8');
console.log('angular13 build fixes applied');
