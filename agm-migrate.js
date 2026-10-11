const fs = require('fs');
const path = require('path');
const root = 'D:/demo_retailer_updated';
function file(rel) { return path.join(root, rel); }
function read(rel) { return fs.readFileSync(file(rel), 'utf8'); }
function write(rel, text) { fs.writeFileSync(file(rel), text, 'utf8'); }
function replaceOnce(rel, search, replacement) {
  const before = read(rel);
  const after = before.replace(search, replacement);
  if (after === before) throw new Error(`No replacement made in ${rel}: ${search}`);
  write(rel, after);
}

replaceOnce('package.json', '        "@agm/core": "1.1.0",', '        "@angular/google-maps": "9.2.4",');

replaceOnce('src/app/dashboard/dashboard.module.ts', 'import { AgmCoreModule } from "@agm/core";', 'import { GoogleMapsModule } from "@angular/google-maps";');
replaceOnce('src/app/dashboard/dashboard.module.ts', '        CommonModule,AgmCoreModule,', '        CommonModule,GoogleMapsModule,');

replaceOnce('src/app/main/apps/dashboards/analytics/analytics.module.ts', "import { AgmCoreModule } from '@agm/core';", "import { GoogleMapsModule } from '@angular/google-maps';");
replaceOnce('src/app/main/apps/dashboards/analytics/analytics.module.ts', `        AgmCoreModule.forRoot({
            apiKey: 'AIzaSyD81ecsCj4yYpcXSLFcYU97PvRsE_X8Bx8'
        }),`, '        GoogleMapsModule,');

replaceOnce('src/app/main/apps/e-commerce/e-commerce.module.ts', "import { AgmCoreModule } from '@agm/core';", "import { GoogleMapsModule } from '@angular/google-maps';");
replaceOnce('src/app/main/apps/e-commerce/e-commerce.module.ts', `        AgmCoreModule.forRoot({
            apiKey: 'AIzaSyD81ecsCj4yYpcXSLFcYU97PvRsE_X8Bx8'
        }),`, '        GoogleMapsModule,');

let analytics = read('src/app/main/apps/dashboards/analytics/analytics.component.html');
analytics = analytics.replace(/<agm-map class="h-640 w-100-p"\s+\[minZoom\]="2"\s+\[maxZoom\]="2"\s+\[fullscreenControl\]="false"\s+\[rotateControl\]="false"\s+\[zoomControl\]="false"\s+\[scaleControl\]="false"\s+\[streetViewControl\]="false"\s+\[scrollwheel\]="false"\s+\[styles\]="widgets\.widget6\.styles">/, '<google-map class="h-640 w-100-p" [options]="{minZoom: 2, maxZoom: 2, fullscreenControl: false, rotateControl: false, zoomControl: false, scaleControl: false, streetViewControl: false, scrollwheel: false, styles: widgets.widget6.styles}">');
analytics = analytics.replace(/<agm-marker\s+\*ngFor="let marker of widgets\.widget6\.markers"\s+\[latitude\]="marker\.lat"\s+\[longitude\]="marker\.lng">/, '<map-marker\r\n                        *ngFor="let marker of widgets.widget6.markers"\r\n                        [position]="{lat: marker.lat, lng: marker.lng}">');
analytics = analytics.replace(/<\/agm-marker>/g, '</map-marker>');
analytics = analytics.replace(/<agm-info-window>/g, '<map-info-window>');
analytics = analytics.replace(/<\/agm-info-window>/g, '</map-info-window>');
analytics = analytics.replace(/<\/agm-map>/g, '</google-map>');
write('src/app/main/apps/dashboards/analytics/analytics.component.html', analytics);

let order = read('src/app/main/apps/e-commerce/order/order.component.html');
order = order.replace(/<agm-map class="w-100-p h-400" \[zoom\]="15"\s+\[latitude\]="order\.customer\.shippingAddress\.lat"\s+\[longitude\]="order\.customer\.shippingAddress\.lng">\s+<agm-marker \[latitude\]="order\.customer\.shippingAddress\.lat"\s+\[longitude\]="order\.customer\.shippingAddress\.lng">\s+<\/agm-marker>\s+<\/agm-map>/, '<google-map class="w-100-p h-400" [zoom]="15" [center]="{lat: order.customer.shippingAddress.lat, lng: order.customer.shippingAddress.lng}">\r\n                                                <map-marker [position]="{lat: order.customer.shippingAddress.lat, lng: order.customer.shippingAddress.lng}">\r\n                                                </map-marker>\r\n                                            </google-map>');
order = order.replace(/<agm-map class="w-100-p h-400" \[zoom\]="15"\s+\[latitude\]="order\.customer\.invoiceAddress\.lat"\s+\[longitude\]="order\.customer\.invoiceAddress\.lng">\s+<agm-marker \[latitude\]="order\.customer\.invoiceAddress\.lat"\s+\[longitude\]="order\.customer\.invoiceAddress\.lng">\s+<\/agm-marker>\s+<\/agm-map>/, '<google-map class="w-100-p h-400" [zoom]="15" [center]="{lat: order.customer.invoiceAddress.lat, lng: order.customer.invoiceAddress.lng}">\r\n                                                <map-marker [position]="{lat: order.customer.invoiceAddress.lat, lng: order.customer.invoiceAddress.lng}">\r\n                                                </map-marker>\r\n                                            </google-map>');
write('src/app/main/apps/e-commerce/order/order.component.html', order);
