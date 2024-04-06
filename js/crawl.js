const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://docs.opengauss.org/zh/docs/5.0.0/docs/GettingStarted/GettingStarted.html', {waitUntil: 'networkidle2'});
  await page.pdf({path: 'opengauss.pdf', format: 'A4'});

  await browser.close();
})();

