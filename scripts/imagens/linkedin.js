// Gera imagens para a página do LinkedIn em imagens/redes/: capa (1128x191), perfil (400x400) e card de post (1200x627).
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const out = path.resolve(__dirname, '../../imagens/redes');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const page = await browser.newPage({ viewport: { width: 1300, height: 1400 } });
  await page.goto('file://' + path.resolve(__dirname, 'linkedin.html'));
  await page.locator('#capa').screenshot({ path: path.join(out, 'linkedin-capa.png') });
  await page.locator('#perfil').screenshot({ path: path.join(out, 'linkedin-perfil.png') });
  await page.locator('#post').screenshot({ path: path.join(out, 'linkedin-post-ia.png') });
  await browser.close();
})();
