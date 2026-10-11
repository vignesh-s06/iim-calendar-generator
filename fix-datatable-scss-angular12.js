const fs = require('fs');
const p = 'D:/demo_retailer_updated/src/@fuse/scss/core.scss';
let s = fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
if (!s.includes("@import '~@swimlane/ngx-datatable/themes/material';")) throw new Error('expected ngx-datatable material import not found');
s = s.replace("@import '~@swimlane/ngx-datatable/themes/material';", "@import '~@swimlane/ngx-datatable/themes/material.scss';");
fs.writeFileSync(p, s, 'utf8');
console.log('core.scss ok');
