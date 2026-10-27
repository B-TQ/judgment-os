/** Optional artwork renderer; not a toolkit runtime dependency. No remote resources. */
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

(async () => {
  const root = path.resolve(__dirname, '..', 'docs', 'launch', 'assets');
  const options = { headless: true };
  if (process.env.BROWSER_EXECUTABLE) options.executablePath = process.env.BROWSER_EXECUTABLE;
  const browser = await chromium.launch(options);
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
    await page.route('**/*', route => {
      const url = new URL(route.request().url());
      return url.protocol === 'file:' || url.protocol === 'data:' ? route.continue() : route.abort();
    });
    for (const file of fs.readdirSync(root).filter(x => x.endsWith('.html')).sort()) {
      await page.goto(pathToFileURL(path.join(root, file)).href);
      await page.evaluate(() => document.fonts.ready);
      const svg = page.locator('svg').first();
      const output = path.join(root, file.replace(/\.html$/, '.png'));
      await svg.screenshot({ path: output, omitBackground: true });
      console.log(path.basename(output));
    }
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error.message); process.exit(1); });
