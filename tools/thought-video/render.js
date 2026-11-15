/* 사용법
 *   미리보기(PNG 몇 장):  NODE_PATH=$(npm root -g) node render.js stills 3 9 15 ...   (초 단위, 결과는 frames/)
 *   전체 영상(MP4):       NODE_PATH=$(npm root -g) node render.js video ../../app/media/thought-to-matter.mp4
 * 필요: ffmpeg, Playwright(chromium). 글꼴은 `npm install`로 설치됩니다.
 */
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = 30;
const mode = process.argv[2] || 'stills';

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => { console.error('PAGEERR', e.message); process.exitCode = 1; });
  await page.goto('file://' + path.resolve(__dirname, 'index.html'));
  await page.waitForFunction('window.READY===true', null, { timeout: 30000 });
  const dur = await page.evaluate('window.DURATION');

  if (mode === 'stills') {
    fs.mkdirSync(path.join(__dirname, 'frames'), { recursive: true });
    for (const s of process.argv.slice(3)) {
      const t = parseFloat(s);
      const data = await page.evaluate(t => window.stillData(t), t);
      fs.writeFileSync(path.join(__dirname, 'frames', `t${String(t).padStart(5, '0')}.png`), Buffer.from(data.split(',')[1], 'base64'));
    }
  } else {
    const out = path.resolve(process.argv[3] || 'thought-to-matter.mp4');
    fs.mkdirSync(path.dirname(out), { recursive: true });
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const total = Math.round(dur * FPS);
    for (let f = 0; f < total; f++) {
      const data = await page.evaluate(t => window.frameData(t, 0.95), f / FPS);
      if (!ff.stdin.write(Buffer.from(data.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
      if (f % 150 === 0) console.log(`frame ${f}/${total}`);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
    console.log('saved', out);
  }
  await browser.close();
})();
