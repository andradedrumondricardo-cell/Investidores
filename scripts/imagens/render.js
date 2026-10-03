// Renderiza as cenas de render.html em imagens/*.jpg (precisa de playwright).
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const out = path.resolve(__dirname, '../../imagens');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  await page.goto('file://' + path.resolve(__dirname, 'render.html'));
  const names = await page.evaluate(() => window.sceneNames);
  for (const name of names) {
    const data = await page.evaluate(n => window.renderScene(n), name);
    fs.writeFileSync(path.join(out, name + '.jpg'), Buffer.from(data.split(',')[1], 'base64'));
    console.log('ok', name);
  }
  await browser.close();
})();
