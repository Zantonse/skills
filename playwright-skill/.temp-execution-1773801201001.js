const { chromium } = require('playwright');
const TARGET_URL = 'https://inner-practice.vercel.app';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 375, height: 812 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
  });

  // Practice page - scroll down to see the sticky type chooser
  const p1 = await context.newPage();
  await p1.goto(`${TARGET_URL}/practice`, { waitUntil: 'networkidle', timeout: 30000 });
  await p1.waitForTimeout(500);
  // Screenshot the top area first
  await p1.screenshot({ path: '/tmp/ui-practice-top.png', clip: { x: 0, y: 0, width: 375, height: 812 } });
  // Scroll down and take another
  await p1.evaluate(() => window.scrollBy(0, 1200));
  await p1.waitForTimeout(500);
  await p1.screenshot({ path: '/tmp/ui-practice-scrolled.png', clip: { x: 0, y: 0, width: 375, height: 812 } });

  // Chakras page - find the Opening & Balancing section
  const p2 = await context.newPage();
  await p2.goto(`${TARGET_URL}/chakras#balancing`, { waitUntil: 'networkidle', timeout: 30000 });
  await p2.waitForTimeout(1000);
  await p2.screenshot({ path: '/tmp/ui-chakras-balancing.png', fullPage: false });
  // Also scroll a bit more to see the full section
  await p2.evaluate(() => window.scrollBy(0, 600));
  await p2.waitForTimeout(300);
  await p2.screenshot({ path: '/tmp/ui-chakras-balancing-2.png', fullPage: false });

  await browser.close();
  console.log('Screenshots saved');
})();
