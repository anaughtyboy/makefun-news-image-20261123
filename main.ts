import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry point for the Monday Globe front page: validate the bundled
// entry.png (a real PNG, at most 1024x1024 and 1 MiB) and copy it
// unchanged to the output directory. Two runs write identical bytes.

const MAX_BYTES = 1024 * 1024;
const MAX_SIDE = 1024;
const PNG_MAGIC = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, "entry.png");

function die(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

function readPngSize(buf: Buffer): { width: number; height: number } {
  if (buf.length < 33) die("entry.png is too short to be a PNG");
  if (!buf.subarray(0, 8).equals(PNG_MAGIC)) die("entry.png is not a PNG");
  if (buf.toString("ascii", 12, 16) !== "IHDR") {
    die("entry.png has no IHDR chunk where one belongs");
  }
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

const image = readFileSync(sourcePath);
if (image.length > MAX_BYTES) {
  die(`entry.png is ${image.length} bytes, over the 1 MiB limit`);
}
const { width, height } = readPngSize(image);
if (width > MAX_SIDE || height > MAX_SIDE) {
  die(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const destPath = join(outDir, "entry.png");
writeFileSync(destPath, image);

const written = readFileSync(destPath);
if (!written.equals(image)) die("the copied file differs from entry.png");
const digest = createHash("sha256").update(written).digest("hex");
console.log(
  `main.ts: wrote ${destPath} (${width}x${height}, ${written.length} bytes, sha256 ${digest})`,
);
