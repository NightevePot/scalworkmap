const fs = require('fs');
const path = require('path');

const fp = 'E:/code/scal-pda-f/workspace/deepseek/demo-cs-surplus-material.html';
const raw = fs.readFileSync(fp);

// Show raw bytes around the garbled font name
const str = raw.toString('utf-8');
const idx = str.indexOf('寰');
if (idx >= 0) {
  const snippet = str.substring(idx, idx + 60);
  console.log('Garbled snippet:', snippet);
  console.log('Bytes (hex):', Buffer.from(snippet, 'utf-8').toString('hex').substring(0, 80));
}

// Try different encodings
const tests = ['latin1', 'cp1252', 'gbk', 'gb2312', 'binary'];
for (const enc of tests) {
  try {
    const buf = Buffer.from(str, enc);
    const result = buf.toString('utf-8');
    const msyh = result.includes('微软雅黑');
    const hasGarbled = result.includes('寰');
    console.log(`${enc}: 微软雅黑=${msyh}, hasGarbled=${hasGarbled}`);
    if (msyh) {
      const idx2 = result.indexOf('微软雅黑');
      console.log(`  Found at: "${result.substring(idx2 - 10, idx2 + 20)}"`);
    }
  } catch (e) {
    console.log(`${enc}: ERROR - ${e.message}`);
  }
}
