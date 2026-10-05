// Gera imagens/og-padrao.png (1200x630, compartilhamento) e imagens/logo.png (512x512, dados estruturados).
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const out = path.resolve(__dirname, '../../imagens');
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const page = await browser.newPage({ viewport: { width: 1200, height: 1200 } });
  await page.goto('file://' + path.resolve(__dirname, 'marca.html'));
  await page.locator('#og').screenshot({ path: path.join(out, 'og-padrao.png') });
  await page.locator('#logo').screenshot({ path: path.join(out, 'logo.png'), omitBackground: true });
  await browser.close();
})();
