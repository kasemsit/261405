#!/usr/bin/env node
/* Audit which rendered Reveal slides overflow the 1280x720 page.
 *
 * Usage:
 *   npm install puppeteer-core           # once
 *   CHROME=$(which google-chrome) node tools/measure-overflow.js "$PWD/ml-intro.html"
 *
 * It visits every leaf slide, reveals all fragments, and measures the true
 * content height (dividing out Reveal's scale). Slides over 720px need fixing.
 */
const puppeteer = require('puppeteer-core');
(async () => {
  const html = process.argv[2];
  if (!html) { console.error('pass the path to ml-intro.html'); process.exit(1); }
  const browser = await puppeteer.launch({
    executablePath: process.env.CHROME || '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-gpu'],
    defaultViewport: { width: 1280, height: 720 },
  });
  const page = await browser.newPage();
  await page.goto('file://' + html, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 1200));
  await page.evaluate(() => { Reveal.configure({ fragments: false }); Reveal.slide(0, 0); });
  const rows = []; let prev = '';
  for (let n = 0; n < 200; n++) {
    await page.evaluate(() => document.querySelectorAll('.fragment').forEach(f => f.classList.add('visible')));
    await new Promise(r => setTimeout(r, 60));
    const m = await page.evaluate(() => {
      const sec = Reveal.getCurrentSlide();
      if (!sec) return null;
      const scale = Reveal.getScale();
      const top = sec.getBoundingClientRect().top;
      let bottom = 0;
      sec.querySelectorAll(':scope > *').forEach(c => {
        const r = c.getBoundingClientRect();
        if (r.height > 0) bottom = Math.max(bottom, r.bottom - top);
      });
      const t = (sec.querySelector('h1,h2') || {}).textContent || '(divider)';
      const s = Reveal.getState();
      return { key: s.indexh + '.' + (s.indexv || 0), title: t.trim().slice(0, 44), content: Math.round(bottom / scale) };
    });
    if (m) { rows.push(m); if (m.key === prev && n > 2) break; prev = m.key; }
    await page.evaluate(() => Reveal.next());
  }
  const seen = {};
  rows.forEach(r => { if (!seen[r.key] || r.content > seen[r.key].content) seen[r.key] = r; });
  const all = Object.values(seen);
  const over = all.filter(r => r.content > 720).sort((a, b) => b.content - a.content);
  console.log('=== OVERFLOW (>720px, FIX) ===');
  over.forEach(r => console.log(`  ${r.content}px (+${r.content - 720})  ${r.title}`));
  if (!over.length) console.log('  (none — all slides fit)');
  console.log(`measured ${all.length} leaf slides`);
  await browser.close();
})();
