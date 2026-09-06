# Arkose FunCaptcha Dataset Collector

Build a **labeled** image dataset from Arkose FunCaptcha challenges — where every label
is verified by Arkose itself.

It renders a site's real Arkose challenge in a stealth browser, solves it in-UI with a
pluggable labeler, submits the answer, and **saves each image with Arkose's own verdict**
(`correct` / `wrong` / `ambiguous`). Even a weak labeler works: it's just a bootstrap, and
Arkose's verdict is the ground truth. Train a model on the result, plug it back in, repeat.

> **Use responsibly.** This is a research/dataset tool. Only run it against services you are
> authorized to test, and follow their terms and the law. It ships no proxies, keys, accounts,
> or data  ; ) — you supply your own.

---

## How it works

```
 adapter.get_blob()         arkose_collector.py (site-agnostic)
 ───────────────────        ─────────────────────────────────────────────
 mint enforcement    ─▶     render api.js ─▶ Start Puzzle (trusted click)
 blob (site-specific)          ─▶ capture challenge image
                               ─▶ labeler picks a tile
                               ─▶ drive arrows + Submit
                               ─▶ read /fc/ca verdict ─▶ save image + label
```

The only site-specific piece is the **enforcement blob** (`data[blob]`). Everything else —
rendering, clicking, capturing, solving, reading the verdict, saving — is generic.

### Challenge layout it understands
A top row of `n` **square** candidate tiles (indexed `0…n-1`, left to right) with the
**reference** below on the left. `n` is inferred per image.

---

## Install

```bash
pip install -r requirements.txt
python -m camoufox fetch          # download the stealth browser
# Linux headless: also install Xvfb   (apt install xvfb)  — camoufox headless="virtual" needs it
```

Python 3.10+. The `dino` labeler pulls PyTorch + DINOv2 on first run (CPU is fine).

---

## Usage

```bash
# Roblox (reference adapter — mints the blob via the login-challenge flow)
python arkose_collector.py \
    --adapter roblox \
    --proxies proxies.txt \
    --usernames usernames.txt \
    --labeler dino \
    --workers 4 --out ./dataset

# A site that needs no blob (bring your own key)
ARKOSE_PUBLIC_KEY=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX \
python arkose_collector.py --adapter noblob --proxies proxies.txt --labeler dino
```

`proxies.txt` — one proxy per line, `http://user:pass@host:port`. Residential proxies work
far better; the blob mint and the image server both check the IP.

`usernames.txt` — one per line (blob adapters only). They don't need to be real accounts; a
login attempt with a wrong password is enough to trigger the captcha.

### Options
| flag | default | meaning |
| --- | --- | --- |
| `--adapter` | — | `roblox` or `noblob` (or your own) |
| `--labeler` | `dino` | `dino` (free, CPU) · `openrouter` · `random` |
| `--proxies` | — | proxy list file |
| `--usernames` | — | username list (blob adapters) |
| `--workers` | 3 | parallel browsers (one Camoufox each) |
| `--limit` | 100000 | stop after N solved challenges |
| `--out` | `./dataset` | output dir |

`openrouter` labeler reads `OPENROUTER_API_KEY` (and optional `OPENROUTER_MODEL`).

---

## Output

```
dataset/
  manifest.jsonl                    one row per wave
  images/<variant>/<id>.png         the challenge image
```

```json
{"id":"a1b2c3d4e5f6a7b8_w0","variant":"...","guess":3,"n_cand":8,
 "verdict":"correct","waves":1,"wave":0,"ts":1750000000}
```

| verdict | meaning | use |
| --- | --- | --- |
| `correct` | Arkose confirmed the solve; **`guess` is the right tile** | positive label |
| `wrong` | single-wave miss; `guess` is a **wrong** tile | negative |
| `ambiguous` | multi-wave miss — can't tell which wave failed | unlabeled (label by hand) |

> `guess` is **0-based**. Only single-wave (`waves:1`) `correct`/`wrong` rows are cleanly
> labeled; multi-wave `correct` rows are all-correct, but multi-wave failures are ambiguous.

---

## Adding a site

Copy `adapters/roblox.py`, implement `get_blob(proxy, username) -> (blob, info)` for the
site's enforcement flow, set the four fields, and register it in `adapters/__init__.py`.
If the site needs no blob, `noblob` may already work with just `ARKOSE_PUBLIC_KEY`.

## Notes
- **Camoufox is the stealth layer.** Arkose detects patched/instrumented browsers; vanilla
  Playwright gets flagged. Don't swap it out unless you replace the anti-detection too.
- A per-browser pool + a stall-guard keep long unattended runs alive (one hung browser can't
  wedge the rest; a fully stalled process exits so a supervisor can restart it).

## License
MIT
