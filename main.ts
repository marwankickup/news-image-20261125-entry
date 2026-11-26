import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { crc32 } from "node:zlib";

const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const HERE = new URL(".", import.meta.url).pathname;
const PYTHON = "/home/hatch/workspace/makefun/.venv/bin/python";

function fail(message: string): never {
  throw new Error(`entry.png validation failed: ${message}`);
}

// Draw the front page with Pillow, then validate the PNG bytes ourselves.
execFileSync(PYTHON, [join(HERE, "draw_image.py"), join(HERE, "entry.png")],
  { stdio: "inherit" });

const png = readFileSync(join(HERE, "entry.png"));

// PNG magic: 89 50 4E 47 0D 0A 1A 0A
const MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!png.subarray(0, 8).equals(MAGIC)) fail("bad PNG magic bytes");
if (png.length > 1_048_576) fail(`file too large: ${png.length} bytes`);

// First chunk must be IHDR, 13 bytes: width and height as big-endian u32.
if (png.readUInt32BE(8) !== 13) fail("IHDR length is not 13");
if (png.toString("ascii", 12, 16) !== "IHDR") fail("first chunk is not IHDR");
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  fail(`expected 1024x1024, got ${width}x${height}`);
}
// IHDR payload: bit depth 8, colour type 2 (RGB) or 6 (RGBA) only.
const bitDepth = png[24];
const colorType = png[25];
if (bitDepth !== 8) fail(`unexpected bit depth ${bitDepth}`);
if (colorType !== 2 && colorType !== 6) {
  fail(`unexpected colour type ${colorType}`);
}
// CRC32 over the IHDR chunk type + data must match the stored CRC.
const storedCrc = png.readUInt32BE(29);
const actualCrc = crc32(png.subarray(12, 29));
if (storedCrc !== actualCrc) fail("IHDR CRC mismatch");
// Walk every chunk and verify each chunk's CRC over its type + data.
let offset = 8;
let sawIend = false;
while (offset + 8 <= png.length) {
  const len = png.readUInt32BE(offset);
  const type = png.toString("ascii", offset + 4, offset + 8);
  if (offset + 12 + len > png.length) fail(`truncated chunk ${type}`);
  const chunkCrc = png.readUInt32BE(offset + 8 + len);
  if (crc32(png.subarray(offset + 4, offset + 8 + len)) !== chunkCrc) {
    fail(`${type} chunk CRC mismatch`);
  }
  offset += 12 + len;
  if (type === "IEND") { sawIend = true; break; }
}
if (!sawIend) fail("no IEND chunk found");
if (offset !== png.length) fail("trailing bytes after IEND");
// File must end with a well-formed IEND chunk.
const tail = png.subarray(png.length - 12);
if (tail.readUInt32BE(0) !== 0 || tail.toString("ascii", 4, 8) !== "IEND") {
  fail("missing IEND trailer");
}

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(join(OUTPUT_DIR, "entry.png"), png);
console.log(`wrote ${OUTPUT_DIR}/entry.png (${png.length} bytes, 1024x1024)`);
