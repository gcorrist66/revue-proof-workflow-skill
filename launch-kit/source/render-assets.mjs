import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const sourceDir = path.dirname(fileURLToPath(import.meta.url));
const outputDir = path.resolve(sourceDir, "../images");
const executablePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const assets = [
  ["github-social-preview.svg", "github-social-preview.png", 1280, 640],
  ["product-hunt-01-logo.svg", "product-hunt-01-logo.png", 1270, 760],
  ["product-hunt-02-evals.svg", "product-hunt-02-evals.png", 1270, 760],
  ["product-hunt-03-verdicts.svg", "product-hunt-03-verdicts.png", 1270, 760],
  ["product-hunt-04-vip-before-after.svg", "product-hunt-04-vip-before-after.png", 1270, 760],
];

const browser = await chromium.launch({ headless: true, executablePath });
for (const [source, output, width, height] of assets) {
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  await page.goto(`file://${path.join(sourceDir, source)}`);
  await page.screenshot({ path: path.join(outputDir, output) });
  await page.close();
}
await browser.close();
