#!/usr/bin/env python3
"""Arkose FunCaptcha dataset collector.

Renders a site's Arkose challenge in a stealth browser, solves it in-UI with a
pluggable labeler, submits the answer, and saves each image with the *Arkose-verified*
verdict (correct / wrong / ambiguous) — building a labeled dataset you can train on.

    python arkose_collector.py --adapter roblox --proxies proxies.txt --usernames users.txt

The site-specific bits (public key, api.js, enforcement blob) live in adapters/;
the collection loop here is site-agnostic. See README.md.
"""
import asyncio, json, os, re, sys, time, random, hashlib, argparse, itertools
from PIL import Image
import io

from camoufox.async_api import AsyncCamoufox
from adapters import load as load_adapter
import labelers

# ----- injected page: load the site's real api.js and hand it our blob (inline mode) -----
def build_html(api_js, blob):
    data_line = f"data: {{ blob: {json.dumps(blob)} }}," if blob else ""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title> </title>
<script>
  window.__ARK = {{token:null, err:null, ready:false, suppressed:null, shown:false}};
  function setupEnforcement(enf) {{
    try {{
      enf.setConfig({{
        selector:'#ark', mode:'inline', {data_line}
        onReady:function(){{window.__ARK.ready=true;}},
        onShown:function(){{window.__ARK.shown=true;}},
        onSuppress:function(){{window.__ARK.suppressed=true;}},
        onCompleted:function(r){{window.__ARK.token=(r&&r.token)||'EMPTY';}},
        onError:function(r){{window.__ARK.err='error:'+JSON.stringify(r);}},
        onFailed:function(r){{window.__ARK.err='failed:'+JSON.stringify(r);}},
      }});
    }} catch (e) {{ window.__ARK.err='setConfig:'+String(e); }}
  }}
</script>
<script src="{api_js}" data-callback="setupEnforcement" async defer></script>
</head><body><div id="ark"></div></body></html>"""


def mkproxy(raw):
    from urllib.parse import urlparse
    u = urlparse(raw)
    if not u.hostname:
        return None
    return {"server": f"http://{u.hostname}:{u.port}", "username": u.username, "password": u.password}


def instruction_of(gfct):
    """Arkose's own task text for this variant, from the gfct string_table (best effort)."""
    gd = gfct.get("game_data", {})
    variant = gd.get("instruction_string", "")
    st = gfct.get("string_table", {}) or {}
    for k, v in st.items():
        if "instruction" in k.lower() and v and (not variant or variant.split("_")[0].lower() in k.lower()):
            return re.sub(r"<[^>]+>", "", str(v)).strip()
    return variant


class Collector:
    def __init__(self, adapter, labeler_fn, out_dir):
        self.ad = adapter
        self.label = labeler_fn
        self.out = out_dir
        self.img_dir = os.path.join(out_dir, "images")
        self.manifest = os.path.join(out_dir, "manifest.jsonl")
        os.makedirs(self.img_dir, exist_ok=True)
        self._mlock = asyncio.Lock()

    async def save_label(self, variant, img_bytes, guess, n_cand, verdict, waves, wave):
        vdir = os.path.join(self.img_dir, re.sub(r"[^A-Za-z0-9_]", "_", variant or "unknown"))
        os.makedirs(vdir, exist_ok=True)
        iid = hashlib.md5(img_bytes).hexdigest()[:16] + f"_w{wave}"
        path = os.path.join(vdir, iid + ".png")
        if not os.path.exists(path):
            with open(path, "wb") as f:
                f.write(img_bytes)
        rec = {"id": iid, "variant": variant, "guess": guess, "n_cand": n_cand,
               "verdict": verdict, "waves": waves, "wave": wave, "ts": int(time.time())}
        async with self._mlock:
            with open(self.manifest, "a") as f:
                f.write(json.dumps(rec) + "\n")

    async def collect_one(self, browser, blob, proxy, stats):
        px = mkproxy(proxy)
        ctx = await browser.new_context(proxy=px, bypass_csp=True)   # bypass_csp lets the inline PoW script run
        page = await ctx.new_page()
        gt2 = {"tok": None}; gfctc = {"raw": None}; imgcap = {}; ca_seen = []
        DOM = self.ad.arkose_host

        async def onresp(r):
            try:
                if "/fc/gt2/public_key/" in r.url and gt2["tok"] is None:
                    d = json.loads(await r.text())
                    if d.get("token"): gt2["tok"] = d["token"]
                elif "/fc/gfct/" in r.url and gfctc["raw"] is None:
                    gfctc["raw"] = json.loads(await r.text())
                elif "/fc/ca/" in r.url:
                    try: ca_seen.append(json.loads(await r.text()))
                    except Exception: pass
                if "/rtig/image" in r.url and r.status == 200:
                    m = re.search(r"challenge=(\d+)", r.url)
                    idx = int(m.group(1)) if m else len(imgcap)
                    if idx not in imgcap:
                        try: imgcap[idx] = await r.body()
                        except Exception: pass
            except Exception: pass
        page.on("response", lambda r: asyncio.create_task(onresp(r)))

        served = {"d": False}
        html = build_html(self.ad.api_js, blob)
        async def route(rt, rq):
            if not served["d"] and rq.resource_type == "document":
                served["d"] = True
                await rt.fulfill(status=200, content_type="text/html", body=html)
            else:
                await rt.continue_()
        await page.route("**/*", route)

        try:
            await page.goto(self.ad.site_url, wait_until="commit")
            for _ in range(40):
                if gt2["tok"]: break
                await asyncio.sleep(0.4)
            if not gt2["tok"]: return "no-gt2"
            if "sup=1" in gt2["tok"]: return "suppressed-sup1"

            for _ in range(110):                 # wait for gfct (~44s)
                if gfctc["raw"]: break
                await asyncio.sleep(0.4)
            if not gfctc["raw"]:
                return "no-gfct"

            g = gfctc["raw"]; gd = g.get("game_data", {}); cg = gd.get("customGUI", {})
            gtok = g.get("challengeID", ""); waves = gd.get("waves", 1)
            instruction = instruction_of(g)
            imgs = cg.get("_challenge_imgs", [])
            if not (gtok and imgs): return "gfct-missing"

            # Start the game with a TRUSTED click (only real input events start the engine).
            FIND = """() => {
                const els=[...document.querySelectorAll('button,[role=button],a,div,span')]
                  .filter(e=>{const t=(e.innerText||e.textContent||'').trim().toLowerCase();
                    return t.includes('start puzzle') && e.offsetParent!==null;});
                if(!els.length) return null;
                els.sort((a,b)=>(a.innerText||'').length-(b.innerText||'').length);
                return els[0];
            }"""
            clicked = False
            for _ in range(20):
                if clicked: break
                for f in page.frames:
                    if not any(k in (f.url or "") for k in ("arkoselabs", "game-core", "enforcement")): continue
                    try:
                        h = await f.evaluate_handle(FIND); el = h.as_element()
                        if not el: continue
                        bb = await el.bounding_box()
                        if bb:
                            await page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
                            clicked = True
                        else:
                            await el.click(timeout=2500, force=True); clicked = True
                        break
                    except Exception: pass
                if clicked: break
                await asyncio.sleep(0.4)
            for _ in range(15):
                if imgcap: break
                await asyncio.sleep(0.4)

            # in-UI solve: for each wave, capture image -> labeler -> arrows + Submit
            gameframe = None
            for f in page.frames:
                if "game-core" in (f.url or ""): gameframe = f; break
            if gameframe is None:
                for f in page.frames:
                    if "enforcement" in (f.url or "") or "arkoselabs" in (f.url or ""): gameframe = f; break
            NEXT = 'a[aria-label="Navigate to next image"]'; SUBMIT = 'button:has-text("Submit")'
            async def _click(loc):
                bb = await loc.first.bounding_box()
                if bb: await page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
                else: await loc.first.click(timeout=2500, force=True)

            wave_imgs = []
            for wave in range(waves):
                body = imgcap.get(wave)
                for _ in range(20):
                    if body is not None: break
                    await asyncio.sleep(0.4); body = imgcap.get(wave)
                if body is None:
                    return f"img{wave}-denied" if wave == 0 else "img-partial"
                n_cand = max(1, Image.open(io.BytesIO(body)).width // 200)
                guess = await asyncio.get_event_loop().run_in_executor(None, self.label, body, n_cand, instruction)
                guess = max(0, min(int(guess), n_cand - 1))
                wave_imgs.append((body, guess, n_cand))
                try:
                    for _ in range(guess):
                        await _click(gameframe.locator(NEXT)); await asyncio.sleep(0.22)
                    await _click(gameframe.locator(SUBMIT))
                except Exception as ex:
                    return f"ui-err:{str(ex)[:40]}"
                prev = len(ca_seen)
                for _ in range(25):
                    if len(ca_seen) > prev: break
                    await asyncio.sleep(0.3)
                if wave < waves - 1:
                    for _ in range(20):
                        if (wave + 1) in imgcap: break
                        await asyncio.sleep(0.4)

            solved = None
            for ca in reversed(ca_seen):
                if ca.get("response") == "answered": solved = ca.get("solved"); break
            if solved is True:
                for w, (b, gs, nc) in enumerate(wave_imgs):
                    await self.save_label(instruction, b, gs, nc, "correct", waves, w)
                stats["correct"] += len(wave_imgs)
            elif solved is False and waves == 1:
                await self.save_label(instruction, wave_imgs[0][0], wave_imgs[0][1], wave_imgs[0][2], "wrong", 1, 0)
                stats["wrong"] += 1
            else:
                for w, (b, gs, nc) in enumerate(wave_imgs):
                    await self.save_label(instruction, b, gs, nc, "ambiguous", waves, w)
                stats["ambiguous"] += len(wave_imgs)
            return "done"
        except Exception as e:
            return f"exc:{str(e)[:50]}"
        finally:
            try: await ctx.close()
            except Exception: pass


async def main():
    ap = argparse.ArgumentParser(description="Arkose FunCaptcha dataset collector")
    ap.add_argument("--adapter", required=True, help="site adapter: roblox | noblob")
    ap.add_argument("--proxies", required=True, help="file of proxy URLs (http://user:pass@host:port)")
    ap.add_argument("--usernames", help="file of usernames (required by blob adapters like roblox)")
    ap.add_argument("--labeler", default="dino", choices=["dino", "openrouter", "random"])
    ap.add_argument("--out", default="./dataset", help="dataset output dir")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--limit", type=int, default=100000, help="stop after this many completed challenges")
    ap.add_argument("--recycle", type=int, default=60, help="recycle each browser every N solves")
    args = ap.parse_args()

    adapter = load_adapter(args.adapter)
    proxies = [l.strip() for l in open(args.proxies) if l.strip()]
    users = [l.strip() for l in open(args.usernames) if l.strip()] if args.usernames else []
    used_file = os.path.join(args.out, ".used_usernames.txt")
    os.makedirs(args.out, exist_ok=True)
    used = set(l.strip() for l in open(used_file)) if os.path.exists(used_file) else set()
    fresh = [u for u in users if u not in used] or users   # recycle when exhausted (a reuse just re-fires the captcha)

    label_fn = labelers.get_labeler(args.labeler)
    print(f"adapter={adapter.name} labeler={args.labeler} proxies={len(proxies)} users={len(fresh)} -> {args.out}", flush=True)
    if args.labeler == "dino":
        print("loading DINOv2...", flush=True)
        await asyncio.get_event_loop().run_in_executor(None, labelers.preload, "dino")
        print("DINOv2 ready.", flush=True)

    col = Collector(adapter, label_fn, args.out)
    stats = {"correct": 0, "wrong": 0, "ambiguous": 0}; fails = {}; prog = {"done": 0}

    async def new_browser():
        return await AsyncCamoufox(headless="virtual").start()

    async def worker(wid):
        browser = await new_browser(); solves = 0
        try:
            while prog["done"] < args.limit:
                if args.recycle and solves and solves % args.recycle == 0:
                    try: await browser.close()
                    except Exception: pass
                    browser = await new_browser()
                proxy = random.choice(proxies)
                username = fresh.pop(random.randrange(len(fresh))) if fresh else ""
                if username:
                    with open(used_file, "a") as uf: uf.write(username + "\n")
                blob, info = await asyncio.get_event_loop().run_in_executor(None, adapter.get_blob, proxy, username)
                if not blob and info not in ("noblob",):
                    fails[info] = fails.get(info, 0) + 1
                    if not fresh and username:      # exhausted -> recycle usernames
                        fresh.extend(users)
                    continue
                try:
                    res = await col.collect_one(browser, blob, proxy, stats)
                except Exception as e:
                    res = f"exc:{str(e)[:40]}"
                    try: await browser.close()
                    except Exception: pass
                    browser = await new_browser()
                solves += 1
                if res != "done":
                    fails[res] = fails.get(res, 0) + 1; continue
                prog["done"] += 1
                print(f"  [done {prog['done']}] w{wid} correct={stats['correct']} wrong={stats['wrong']} "
                      f"ambig={stats['ambiguous']} fails={dict(list(fails.items())[:5])}", flush=True)
        finally:
            try: await browser.close()
            except Exception: pass

    async def stall_guard():
        last, stamp = -1, time.time()
        while True:
            await asyncio.sleep(60)
            if prog["done"] > last: last, stamp = prog["done"], time.time()
            elif time.time() - stamp > 420:
                print("STALL: no progress 7min — exiting", flush=True); os._exit(1)
    asyncio.create_task(stall_guard())

    await asyncio.gather(*[worker(w) for w in range(args.workers)])
    print(f"\nDONE: correct={stats['correct']} wrong={stats['wrong']} ambiguous={stats['ambiguous']} -> {args.out}")


if __name__ == "__main__":
    asyncio.run(main())
