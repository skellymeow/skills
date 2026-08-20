#!/usr/bin/env node
/** Record clean browser/app footage with Playwright, then encode to MP4 with FFmpeg. */

import { createRequire } from 'node:module';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

function args(argv) {
  const out = {};
  for (let i = 2; i < argv.length; i++) {
    const key = argv[i];
    if (!key.startsWith('--')) continue;
    const name = key.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) out[name] = true;
    else {
      out[name] = next;
      i++;
    }
  }
  return out;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function smoothScroll(page, durationMs) {
  await page.evaluate(async (duration) => {
    const maxY = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    if (maxY <= 8) return;
    const start = performance.now();
    await new Promise((resolve) => {
      function frame(now) {
        const t = Math.min(1, (now - start) / duration);
        const eased = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
        window.scrollTo(0, maxY * eased);
        if (t < 1) requestAnimationFrame(frame);
        else resolve();
      }
      requestAnimationFrame(frame);
    });
  }, durationMs);
}

async function main() {
  const a = args(process.argv);
  if (!a.url || !a.out) {
    console.error('Usage: capture_browser.mjs --url https://example.com --aspect 9:16 --out capture.mp4 [--duration 8] [--no-scroll]');
    process.exit(2);
  }

  new URL(a.url);
  const aspect = a.aspect || '9:16';
  const portrait = aspect === '9:16';
  if (!portrait && aspect !== '16:9') throw new Error('--aspect must be 9:16 or 16:9');

  const width = Number(a.width || (portrait ? 720 : 1280));
  const height = Number(a.height || (portrait ? 1280 : 720));
  const duration = Math.max(2, Number(a.duration || 8));
  const outPath = path.resolve(a.out);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });

  const requireFromCwd = createRequire(path.join(process.cwd(), 'package.json'));
  let chromium;
  try {
    ({ chromium } = requireFromCwd('playwright'));
  } catch {
    console.error('Playwright is not installed in the current workspace. After user approval run: npm install playwright && npx playwright install chromium');
    process.exit(3);
  }

  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'hermes-video-capture-'));
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 1,
    recordVideo: { dir: tempDir, size: { width, height } },
  });
  const page = await context.newPage();

  await page.goto(a.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  try { await page.waitForLoadState('networkidle', { timeout: 10000 }); } catch {}

  await page.addStyleTag({ content: `
    html { scroll-behavior: auto !important; }
    * { caret-color: transparent !important; }
    ::-webkit-scrollbar { width: 0 !important; height: 0 !important; }
  ` }).catch(() => {});

  await sleep(700);
  const video = page.video();

  if (!a['no-scroll']) {
    await smoothScroll(page, Math.max(1000, Math.round((duration - 1.4) * 1000)));
  } else {
    await sleep(Math.round((duration - 1.4) * 1000));
  }
  await sleep(700);

  await context.close();
  await browser.close();

  const rawPath = path.join(tempDir, 'capture.webm');
  await video.saveAs(rawPath);

  if (path.extname(outPath).toLowerCase() === '.webm') {
    fs.copyFileSync(rawPath, outPath);
  } else {
    const ffmpeg = spawnSync('ffmpeg', [
      '-y', '-loglevel', 'error', '-i', rawPath,
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
      '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', outPath,
    ], { stdio: 'inherit' });
    if (ffmpeg.status !== 0) {
      console.error(`FFmpeg encode failed. Raw capture remains at ${rawPath}`);
      process.exit(ffmpeg.status || 4);
    }
  }

  fs.rmSync(tempDir, { recursive: true, force: true });
  console.log(JSON.stringify({ ok: true, out: outPath, aspect, width, height, duration }, null, 2));
}

main().catch((err) => {
  console.error(err?.stack || String(err));
  process.exit(1);
});
