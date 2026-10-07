'use strict';
const assert = require('node:assert/strict');
const test = require('node:test');
const fs = require('node:fs');
const vm = require('node:vm');
const { URLSearchParams } = require('node:url');

const code = fs.readFileSync('docs/patcher.js', 'utf8');
assert.match(code, /\}\)\(\);\s*$/);
const instrumented = code.replace(/\}\)\(\);\s*$/, 'globalThis.__legendsTest = { applyBps, crc32 };\n})();');

function harness() {
  const nodes = {};
  for (const id of ['rom-file', 'patch-button', 'patch-status', 'build-version', 'build-label', 'build-description', 'build-footer']) {
    nodes[id] = {
      textContent: '', className: '', disabled: false, files: [], callbacks: {},
      addEventListener(event, cb) { this.callbacks[event] = cb; }
    };
  }
  const sha = Buffer.from('f3ae088181bf583e55daf962a92bb46f4f1d07b7', 'hex');
  const ctx = {
    document: { title: '', getElementById(id) { return nodes[id]; } },
    URLSearchParams,
    window: { location: { search: '' } },
    crypto: { subtle: { async digest() { return Uint8Array.from(sha).buffer; } } },
    fetch: async () => { throw new Error('Unexpected fetch'); },
    URL: { createObjectURL() { return 'blob:test'; }, revokeObjectURL() {} },
    Blob, setTimeout() {}
  };
  vm.runInNewContext(instrumented, ctx, { filename: 'docs/patcher.js' });
  return { nodes, bps: ctx.__legendsTest };
}
function varint(v) {
  const output = [];
  while (true) {
    const low = v & 127;
    v = Math.floor(v / 128);
    if (v === 0) { output.push(low | 128); return output; }
    output.push(low);
    v--;
  }
}
function le32(v) { return [v & 255, (v >>> 8) & 255, (v >>> 16) & 255, (v >>> 24) & 255]; }
function fixture(bps, source, target, commands) {
  const bytes = [66, 80, 83, 49, ...varint(source.length), ...varint(target.length), ...varint(0), ...commands];
  bytes.push(...le32(bps.crc32(source)), ...le32(bps.crc32(target)));
  bytes.push(...le32(bps.crc32(Uint8Array.from(bytes))));
  return Uint8Array.from(bytes);
}
test('BPS SourceRead + TargetRead reconstruct exact output', () => {
  const { bps } = harness();
  const source = Uint8Array.from([1, 2, 3, 4]), target = Uint8Array.from([1, 2, 3, 4, 9, 10]);
  const patch = fixture(bps, source, target, [...varint(12), ...varint(5), 9, 10]);
  assert.deepEqual(Array.from(bps.applyBps(source, patch)), Array.from(target));
});
test('BPS TargetCopy supports valid overlapping repeat', () => {
  const { bps } = harness();
  const source = Uint8Array.from([99]), target = Uint8Array.from([65, 65, 65, 65, 65]);
  const patch = fixture(bps, source, target, [...varint(1), 65, ...varint(15), ...varint(0)]);
  assert.deepEqual(Array.from(bps.applyBps(source, patch)), Array.from(target));
});
test('BPS rejects source mismatch and corrupted patch CRC', () => {
  const { bps } = harness();
  const source = Uint8Array.from([1, 2]), target = Uint8Array.from([7, 8]);
  const patch = fixture(bps, source, target, [...varint(5), 7, 8]);
  assert.throws(() => bps.applyBps(Uint8Array.from([1, 3]), patch), /source expected/);
  const corrupted = Uint8Array.from(patch);
  corrupted[corrupted.length - 13] ^= 1;
  assert.throws(() => bps.applyBps(source, corrupted), /checksum failed/);
});
test('BPS rejects wrong output CRC even with correct patch CRC', () => {
  const { bps } = harness();
  const source = Uint8Array.from([1]), target = Uint8Array.from([7]);
  const patch = fixture(bps, source, target, [...varint(1), 8]);
  assert.throws(() => bps.applyBps(source, patch), /Patched ROM checksum failed/);
});
test('old ROM validation cannot override newer invalid file', async () => {
  const { nodes } = harness(), input = nodes['rom-file'];
  let resolveOld;
  input.files = [{ arrayBuffer: () => new Promise(resolve => { resolveOld = resolve; }) }];
  const older = input.callbacks.change();
  input.files = [{ arrayBuffer: async () => new ArrayBuffer(3) }];
  await input.callbacks.change();
  assert.equal(nodes['patch-button'].disabled, true);
  assert.match(nodes['patch-status'].textContent, /expected 16 MiB/);
  resolveOld(new ArrayBuffer(16777216));
  await older;
  assert.equal(nodes['patch-button'].disabled, true);
  assert.match(nodes['patch-status'].textContent, /expected 16 MiB/);
});
