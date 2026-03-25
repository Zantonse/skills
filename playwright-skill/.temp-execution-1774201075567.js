const { chromium } = require('playwright');

const TARGET_URL = 'https://roku-discovery.vercel.app';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });

  await page.goto(TARGET_URL, { waitUntil: 'networkidle', timeout: 30000 });
  console.log('Page loaded:', await page.title());

  // Click Architecture nav tab
  await page.click('button:has-text("Architecture")');
  await page.waitForTimeout(500);
  console.log('Clicked Architecture tab');

  // Click Protocols sub-tab
  await page.click('button:has-text("Protocols")');
  await page.waitForTimeout(1000);
  console.log('Clicked Protocols sub-tab');

  await page.screenshot({ path: '/tmp/roku-protocols-tab.png', fullPage: true });
  console.log('Screenshot saved: /tmp/roku-protocols-tab.png');

  // Click Decision Matrix sub-tab
  await page.click('button:has-text("Decision Matrix")');
  await page.waitForTimeout(1000);
  console.log('Clicked Decision Matrix sub-tab');

  await page.screenshot({ path: '/tmp/roku-decisionmatrix-tab.png', fullPage: true });
  console.log('Screenshot saved: /tmp/roku-decisionmatrix-tab.png');

  await browser.close();
  console.log('Done!');
})();
