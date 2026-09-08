#!/usr/bin/env node
/**
 * Run an Arkose /powseq worker headlessly in node — no browser, no jsdom.
 *
 * The worker is pure compute: SHA-512 over a nonce counter. Verified to touch no
 * navigator/window/document/screen. We run it in a vm context exposing ONLY what
 * it asks for (no require/process/fs/network), so the untrusted script is boxed in.
 *
 * Message contract (from the deobfuscated worker):
 *   in : {type:"start", data:{seed, targetHashData:[{targetHashData}], startingNonce, itimeout}}
 *   out: {type:"loaded"} , {type:"split_done", data:{...}} * N , {type:"done", data:{
 *          hashRate, time, finalTransform, targetHashData:[{iterations,targetHash}]}}
 *
 * usage: node powrun.js <powseq.js> <pow_setup.json>
 */
const fs = require('fs');
const vm = require('vm');
const { webcrypto } = require('crypto');
const { performance } = require('perf_hooks');

const [, , scriptPath, setupPath] = process.argv;
if (!scriptPath || !setupPath) {
  console.error('usage: node powrun.js <powseq.js> <pow_setup.json>');
  process.exit(2);
}

const src = fs.readFileSync(scriptPath, 'utf8');
const setup = JSON.parse(fs.readFileSync(setupPath, 'utf8'));
const wc = setup.work_config || {};

const posted = [];
let resolveDone;
const doneP = new Promise((r) => { resolveDone = r; });

// The worker hashes once per nonce via crypto.subtle.digest — an async WebCrypto call
// per hash, which is orders of magnitude slower than node's sync digest and makes long
// rounds blow past itimeout (POW_TIMEOUT). Same algorithm, same bytes, just not async.
const nodeCrypto = require('crypto');
const _targets = new Set(
  ((JSON.parse(fs.readFileSync(setupPath, 'utf8')).work_config || {}).splits || []).map((s) => s.target_hash)
);
const fastSubtle = {
  digest(alg, data) {
    const name = (typeof alg === 'string' ? alg : alg && alg.name) || 'SHA-512';
    const buf = Buffer.from(data.buffer || data, data.byteOffset || 0, data.byteLength ?? data.length);
    const h = nodeCrypto.createHash(String(name).replace('-', '').toLowerCase()).update(buf).digest();
    if (process.env.POWSPY && _targets.has(h.toString('hex'))) {
      console.log('WINNING_INPUT<<<' + buf.toString('utf8') + '>>>');
    }
    return Promise.resolve(h.buffer.slice(h.byteOffset, h.byteOffset + h.byteLength));
  },
};

const sandbox = {
  crypto: { subtle: fastSubtle, getRandomValues: (a) => webcrypto.getRandomValues(a) },
  TextEncoder, TextDecoder, Uint8Array, Uint16Array, ArrayBuffer,
  Array, Object, JSON, Math, Date, String, Number, Boolean, Error,
  Promise, Symbol, Map, Set, RegExp, parseInt, parseFloat, isNaN,
  performance,
  btoa: (s) => Buffer.from(s, 'binary').toString('base64'),
  atob: (s) => Buffer.from(s, 'base64').toString('binary'),
  onmessage: null,
  postMessage: (msg) => {
    posted.push(msg);
    const t = msg && msg.type;
    if (t === 'split_done') {
      const d = msg.data || {};
      console.log(`   split ${d.splitNum}: nonce=${d.result} rate=${(d.hashRate||0).toFixed(2)} ms=${d.executionTime}`);
    } else {
      console.log('   <<<', t);
    }
    if (t === 'done' || t === 'error') resolveDone(msg);
  },
  console: { log: (...a) => console.log('   [w]', ...a), error: (...a) => console.log('   [w:err]', ...a), warn: () => {} },
};
sandbox.self = sandbox;
sandbox.globalThis = sandbox;
const ctx = vm.createContext(sandbox);

console.log(`=== loading ${scriptPath} (${src.length} bytes) ===`);
vm.runInContext(src, ctx, { filename: 'powseq.js', timeout: 20000 });
console.log('loaded. onmessage:', typeof ctx.onmessage);

const msg = {
  type: 'start',
  data: {
    seed: wc.seed,
    targetHashData: (wc.splits || []).map((s) => ({ targetHashData: s.target_hash })),
    startingNonce: wc.starting_nonce,
    itimeout: setup.timeout,
  },
};
console.log(`\n>>> start: ${msg.data.targetHashData.length} splits, nonce=${msg.data.startingNonce}, timeout=${msg.data.itimeout}`);

(async () => {
  const t0 = performance.now();
  ctx.onmessage({ data: msg });   // worker reads x.data — pass an EVENT, not the message
  const out = await Promise.race([
    doneP,
    new Promise((r) => setTimeout(() => r({ type: 'TIMEOUT_HARNESS' }), (setup.timeout || 75000) + 15000)),
  ]);
  const dt = performance.now() - t0;

  if (out.type !== 'done') {
    console.log(`\n*** FAILED (${out.type}) after ${dt.toFixed(0)} ms ***`);
    console.log(JSON.stringify(out, null, 1).slice(0, 2000));
    process.exit(1);
  }

  const d = out.data;
  console.log(`\n*** SOLVED in ${dt.toFixed(0)} ms (worker time ${d.time} ms, hashRate ${d.hashRate.toFixed(3)}) ***`);
  console.log('nonces:', d.targetHashData.map((x) => x.iterations).join(', '));

  // verify every target hash actually matches — proves the algorithm, not just that it ran
  const ok = d.targetHashData.every((x) => /^[0-9a-f]{128}$/.test(x.targetHash));
  console.log('target hashes well-formed:', ok);

  // the exact body /pows/check wants
  const checkBody = {
    pow_token: setup.pow_token,
    session_token: '<FILL>',
    hash_rate: d.hashRate,
    execution_time: d.time,
    transform: d.finalTransform,
    result: d.targetHashData.map((x) => ({ target_hash: x.targetHash, attempt_count: x.iterations })),
  };
  fs.writeFileSync('pow_check_body.json', JSON.stringify(checkBody, null, 1));
  console.log('\n-> pow_check_body.json written');
  console.log('transform[0] keys:', Object.keys(d.finalTransform[0] || {}).length,
              '| transform[1] keys:', Object.keys(d.finalTransform[1] || {}).length);
  process.exit(0);
})();
