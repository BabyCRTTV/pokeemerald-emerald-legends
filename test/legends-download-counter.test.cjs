'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const code = fs.readFileSync('docs/download-counter.js', 'utf8');
const settle = () => new Promise(resolve => setImmediate(resolve));

function harness(fetch, withBadge = true) {
  const badge = { textContent: '…', attrs: {}, setAttribute(k, v) { this.attrs[k] = v; } };
  const documentEvents = {}, windowEvents = {}, calls = [];
  vm.runInNewContext(code, {
    document: {
      getElementById() { return withBadge ? badge : null; },
      addEventListener(name, cb) { documentEvents[name] = cb; }
    },
    window: { addEventListener(name, cb) { windowEvents[name] = cb; } },
    fetch(url, options) { calls.push({ url, options }); return fetch(url, options); },
    AbortController, setTimeout, clearTimeout, Intl
  });
  return { badge, calls, documentEvents, windowEvents };
}
const response = (value, status = 200) => ({ ok: status === 200, status, json: async () => ({ value }) });

test('display reads the shared total without incrementing; refresh remains a read', async () => {
  for (let i = 0; i < 2; i++) {
    const h = harness(async () => response(42));
    await settle();
    assert.match(h.calls[0].url, /\/get\//);
    assert.equal(h.calls.length, 1);
    assert.equal(h.badge.textContent, '↓ 42');
    assert.equal(h.calls[0].options.credentials, 'omit');
  }
});

test('only patch download links and verified patcher events increment', async () => {
  const h = harness(async () => response(8), false);
  assert.equal(h.calls.length, 0);
  h.documentEvents.click({ button: 0, target: { closest: () => null } });
  h.documentEvents.click({ button: 2, target: { closest: () => ({}) } });
  h.documentEvents.click({ button: 0, defaultPrevented: true, target: { closest: () => ({}) } });
  assert.equal(h.calls.length, 0);
  h.documentEvents.click({ button: 0, target: { closest: selector => selector.includes('.bps') ? {} : null } });
  h.windowEvents['legends:download-started']();
  await settle();
  assert.equal(h.calls.length, 2);
  assert.ok(h.calls.every(c => c.url.includes('/hit/') && c.options.keepalive));
});

test('new total shows zero; unavailable or malformed totals never fabricate a number', async () => {
  const empty = harness(async () => ({ ok: false, status: 404, json: async () => ({ error: 'Key not found' }) }));
  const offline = harness(async () => { throw new Error('offline'); });
  const malformed = harness(async () => response('not a count'));
  await settle();
  assert.equal(empty.badge.textContent, '↓ 0');
  for (const h of [offline, malformed]) {
    assert.equal(h.badge.textContent, '—');
    assert.match(h.badge.attrs['aria-label'], /unavailable/);
    h.windowEvents['legends:download-started']();
  }
  await settle();
  assert.equal(offline.calls.length, 2); // No automatic hit retry.
});

test('a delayed initial read cannot overwrite a newer download total', async () => {
  let resolveRead;
  const h = harness(url => url.includes('/get/') ? new Promise(resolve => { resolveRead = resolve; }) : Promise.resolve(response(12345)));
  h.windowEvents['legends:download-started']();
  await settle();
  const updated = h.badge.textContent;
  assert.match(h.badge.attrs['aria-label'], /12,345/);
  assert.ok(updated.length < 10);
  resolveRead(response(0));
  await settle();
  assert.equal(h.badge.textContent, updated);
});
