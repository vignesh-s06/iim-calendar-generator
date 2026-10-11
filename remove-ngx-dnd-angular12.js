const fs = require('fs');
function edit(file, fn) {
  const before = fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
  const after = fn(before);
  fs.writeFileSync(file, after, 'utf8');
}
edit('D:/demo_retailer_updated/package.json', s =>
  s
    .replace(/\r?\n        "@swimlane\/dragula": "3\.8\.0",/, '')
    .replace(/\r?\n        "@swimlane\/ngx-dnd": "9\.0\.0",/, '')
);
edit('D:/demo_retailer_updated/src/app/main/apps/todo/todo.module.ts', s =>
  s
    .replace(/\r?\nimport \{ NgxDnDModule \} from '@swimlane\/ngx-dnd';/, '')
    .replace(/\r?\n\s*NgxDnDModule,/, '')
);
edit('D:/demo_retailer_updated/src/app/main/apps/scrumboard/scrumboard.module.ts', s =>
  s
    .replace(/\r?\nimport \{ NgxDnDModule \} from '@swimlane\/ngx-dnd';/, '')
    .replace(/\r?\n\s*NgxDnDModule,/, '')
);
edit('D:/demo_retailer_updated/src/app/main/apps/todo/todo-list/todo-list.component.html', s =>
  s
    .replace(/ ngxDroppable/g, '')
    .replace(/\s+\[model\]="todos"/g, '')
    .replace(/\s+\(out\)="onDrop\(\$event\)"/g, '')
    .replace(/\s+ngxDraggable/g, '')
    .replace(/\s+\[model\]="todo"/g, '')
);
edit('D:/demo_retailer_updated/src/app/main/apps/scrumboard/board/list/list.component.html', s =>
  s
    .replace(/\s+\[model\]="list\.idCards" ngxDroppable="card" \(out\)="onDrop\(\$event\)"/g, '')
    .replace(/ ngxDraggable/g, '')
    .replace(/\s+\[model\]="cardId"/g, '')
);
edit('D:/demo_retailer_updated/src/app/main/apps/scrumboard/board/board.component.html', s =>
  s
    .replace(/\s+ngxDroppable="list" \[model\]="board\.lists" \(out\)="onDrop\(\$event\)"/g, '')
    .replace(/\s+ngxDraggable/g, '')
    .replace(/\s+\[model\]="list"/g, '')
    .replace(/\s+\[moves\]="false"/g, '')
);
console.log('ngx-dnd cleanup ok');
