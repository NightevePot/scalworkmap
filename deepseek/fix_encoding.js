const fs = require('fs');
const path = require('path');

const base = 'E:/code/scal-pda-f/workspace/deepseek';
const files = [
  'demo-cs-mfg-order.html',
  'demo-cs-pz-output.html',
  'demo-cs-equipment-start.html',
  'demo-cs-weighing-test.html',
  'demo-cs-surplus-material.html',
  'demo-cs-bpr-record.html',
  'demo-cs-template.html',
];

let fixed = 0;
for (const fname of files) {
  const fp = path.join(base, fname);
  const raw = fs.readFileSync(fp);
  // Fix double-encoded UTF-8: decode as UTF-8 → encode as Latin1 → decode as UTF-8
  const broken = raw.toString('utf-8');
  const latin1 = Buffer.from(broken, 'latin1');
  const result = latin1.toString('utf-8');
  if (result.includes('微软雅黑') && !result.includes('寰')) {
    fs.writeFileSync(fp, result, 'utf-8');
    console.log('OK:', fname);
    fixed++;
  } else {
    console.log('SKIP:', fname, '- encoding differs');
  }
}
console.log(`\nFixed ${fixed}/${files.length} files`);
