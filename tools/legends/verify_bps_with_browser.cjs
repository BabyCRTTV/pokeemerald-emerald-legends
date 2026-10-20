'use strict';
// Apply real Release/Debug patches with the committed browser decoder.
// Compare against independently compiled native ROMs; never publish those ROMs.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');

const args = process.argv.slice(2);
if (args.length !== 6) {
  throw new Error('Usage: node verify_bps_with_browser.cjs clean.gba release.bps debug.bps release.gba debug.gba receipt.json');
}
const [basePath, releasePatch, debugPatch, releaseRom, debugRom, outputPath] = args;
const root = path.resolve(__dirname, '../..');
const code = fs.readFileSync(path.join(root, 'docs/patcher.js'), 'utf8');
assert.match(code, /\}\)\(\);\s*$/);
const instrumented = code.replace(/\}\)\(\);\s*$/,
  'globalThis.__legendsBps = { applyBps };\n})();');
const node = {textContent: '', className: '', disabled: false, files: [], addEventListener() {}, click() {}, remove() {}};
const context = {
  document: {title: '', getElementById() {return node;}, createElement() {return node;}, body: {appendChild() {}}},
  window: {location: {search: ''}, dispatchEvent() {}}, URLSearchParams,
  crypto: crypto.webcrypto,
  fetch: async () => {throw new Error('Unexpected network access');},
  URL: {createObjectURL() {return 'blob:verification';}, revokeObjectURL() {}},
  Blob, Event, setTimeout() {}
};
vm.runInNewContext(instrumented, context, {filename: 'docs/patcher.js'});
const hash = (algorithm, data) => crypto.createHash(algorithm).update(data).digest('hex');
const base = fs.readFileSync(basePath);
assert.equal(hash('sha1', base), 'f3ae088181bf583e55daf962a92bb46f4f1d07b7');
const results = {};
for (const [patchPath, romPath] of [[releasePatch, releaseRom], [debugPatch, debugRom]]) {
  const patch = fs.readFileSync(patchPath);
  const target = Buffer.from(context.__legendsBps.applyBps(Uint8Array.from(base), Uint8Array.from(patch)));
  assert(target.equals(fs.readFileSync(romPath)), path.basename(patchPath));
  results[path.basename(patchPath)] = {
    patch_sha256: hash('sha256', patch), target_sha256: hash('sha256', target),
    target_bytes: target.length, exact_native_ROM_match: true
  };
}
const proof = {
  passed: true, source_SHA1: hash('sha1', base),
  decoder: 'Actual committed docs/patcher.js applyBps executed in Node VM; independent of Floating IPS',
  decoder_sha256: hash('sha256', code), verifier_sha256: hash('sha256', fs.readFileSync(__filename)),
  results, limits: 'Byte-decoder test; physical browser file-picker/download and Pizza Boy execution are separate checks.'
};
fs.writeFileSync(outputPath, JSON.stringify(proof, null, 2) + '\n');
console.log(JSON.stringify(proof, null, 2));
