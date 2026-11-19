// Рендер макетов в PNG: node render.js [файлы...]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const files = process.argv.slice(2).length ? process.argv.slice(2)
    : fs.readdirSync(__dirname).filter(f => /^\d\d-.*\.html$/.test(f));
  fs.mkdirSync(path.join(__dirname, 'png'), { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: Number(process.env.DSF || 2) });
  for (const f of files) {
    await page.goto('file://' + path.join(__dirname, f));
    const out = path.join(__dirname, 'png', f.replace('.html', '.png'));
    await page.locator('.app').screenshot({ path: out });
    console.log('ok', out);
  }
  await browser.close();
})();
