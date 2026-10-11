const fs = require('fs');
const p = 'D:/demo_retailer_updated/src/@fuse/scss/core.scss';
let s = fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
s = s.replace("@import '~@swimlane/ngx-datatable/themes/material.scss';", "@import '../../../node_modules/@swimlane/ngx-datatable/themes/material.scss';");
if (!s.includes("@import '../../../node_modules/@swimlane/ngx-datatable/themes/material.scss';")) throw new Error('replacement failed');
fs.writeFileSync(p, s, 'utf8');
console.log('core.scss import fixed');
