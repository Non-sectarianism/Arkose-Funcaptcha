# Arkose-Funcaptcha
Repo for funcaptcha fun



## State of the work at snapshot time

**Solved / proven:**
- Trust tier is set by the BDA ciphertext. Replaying an encrypted VM-captured plaintext yields
  `3DRollball_v2_var2, waves=1-2, difficulty=8` — identical to real Chrome (4/4 matched pairs).
- No VM reverse was needed: plaintext is `JSON.stringify(bda_array)`, delta 0 vs capture.
  Envelope = `b64(iv12)+b64(tag16)+b64(rsaKey256)+b64(ct)`, confirmed via the `caasgs` trap.
- `f = x64hash128(";".join(value-part of each fe entry), 0)`;
  `ife_hash = x64hash128(", ".join(full fe entries), 38)` — both byte-for-byte verified,
  so `fe` can be mutated freely (`bda_mutate.py`); a mutant held the tier 4/4.
- dapib fully decoded, sandbox no longer flagged.
- PoW shared-file race fixed via `POWDIR` — completion 19.4% -> 37.5%, waves=0 47% -> 2%.
  (This race contaminated the earlier 198-session seed study, the proxy clustering test and
  the 50-run; treat any conclusion from before the fix as void.)
- Parallel harness: 198 sessions in ~11 minutes.

**Ruled out by measurement (do not retest):** headers/order/TLS, `expires`, the HTTP client,
the answer path (52% of denials happen at wave 0), `tguess`, seeds (chi2=28.2 df=21),
proxies (chi2=8.9 df=8, exit IPs stable), username freshness, ciphertext reuse, pacing,
asset ordering, HARFAITHFUL ordering, single-vs-double mint, ecsv2/metrics/PerimeterX,
`gp` (gamepad), `lowSecRandomId`, image AES-CBC decryption, OAEP hash / AES key size.

**Open — `action:block`.** Perfect correlation over 6 runs: PoW `exec` <=100 ms -> verdict
`challenge`; `exec` in seconds -> escalate -> `block`.

    g4 challenge  exec: 9
    g1 challenge  exec: 11, 60
    g2 block      exec: 25, 3822, 12800
    g3 block      exec: 21, 4978, 8237
    g5 block      exec: 41, 2660, 10015
    g6 block      exec: 19, 7485, 4421

Causation direction is unknown — either Arkose escalates for its own reasons and `exec` is a
symptom, or my honest multi-second `execution_time` is itself the trigger.
**Untested fix:** clamp reported `execution_time`/`hash_rate` to browser-plausible values.
Real browser reported `hash_rate: 5.309`; `session_200.har` showed `exec=4` and `exec=126`,
never seconds.

**Also open:** Arkose reportedly binds signed `/rtig/image` URLs to the *route*, not the IP —
a fresh CONNECT tunnel may take a different upstream path while emerging from the same exit IP.
Untested: whether the image
