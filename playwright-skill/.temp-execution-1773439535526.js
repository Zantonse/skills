const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newContext({ viewport: { width: 1920, height: 1080 } }).then(c => c.newPage());
  await page.goto('http://localhost:4444', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await page.click('body');
  // Navigate to slide 11 (cheat sheet)
  for (let i = 0; i < 10; i++) {
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(500);
  }
  await page.waitForTimeout(1000);
  await page.screenshot({ path: '/tmp/cheatsheet-new.png' });
  console.log('Screenshot saved');
  await browser.close();
})();
