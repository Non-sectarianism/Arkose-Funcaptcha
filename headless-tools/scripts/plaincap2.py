# Capture the EXACT plaintext the Arkose VM encrypts.
# ue() builds  R={pl,cbid,caasgs,basdga,aagesg}  and publishes it as window.arkl.
# The VM turns its serialised payload into bytes via aagesg(str) before encrypting.
# We patch api.js SOURCE at the unique literal `R={};R.pl=t` (native hooks and
# window traps are defeated: api.js re-imports pristine natives and runs the mint
# in a realm add_init_script cannot reach), wrap aagesg via a property setter, and
# EXFILTRATE the string through a sentinel fetch that our route intercepts - so
# readback does not depend on the realm either.
import asyncio, json, os, random, sys, time, urllib.parse
sys.path.insert(0, "/root/arkose")
from collector import get_blob, HTML, API_JS, mkproxy
from camoufox.async_api import AsyncCamoufox

OUT = "/root/plaincap"
os.makedirs(OUT, exist_ok=True)
PROX = [l.strip() for l in open("/root/arkose/good_proxies.txt") if l.strip()]
USERS = [l.strip() for l in open("/root/arkose/usernames_fresh.txt") if l.strip()]
random.shuffle(USERS)

SENTINEL = "https://arkoselabs.roblox.com/__plaincap__"
ANCHOR = "R={};R.pl=t,"
TRAP = (
    "R={};R.pl=t,(function(){try{var _a=null,_c=null,_seq=0;"
    "function _post(tag,val){try{fetch('" + SENTINEL + "?t='+tag+'&i='+(_seq++),"
    "{method:'POST',body:val});}catch(e){}}"
    "Object.defineProperty(R,'aagesg',{configurable:true,"
    "get:function(){return _a;},"
    "set:function(fn){_a=function(x){try{if(typeof x==='string'&&x.length>800)"
    "_post('plain',x);}catch(e){}return fn.apply(this,arguments);};}});"
    "Object.defineProperty(R,'caasgs',{configurable:true,"
    "get:function(){return _c;},"
    "set:function(fn){_c=function(x){var r=fn.apply(this,arguments);"
    "try{_post('b64',(x&&x.byteLength!==undefined?x.byteLength:-1)+'|'+r);}catch(e){}"
    "return r;};}});"
    "}catch(e){}})(),"
)



async def main():
    want = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    got = 0
    async with AsyncCamoufox(headless="virtual") as browser:
        for _ in range(want * 4):
            if got >= want or not USERS:
                break
            user = USERS.pop()
            proxy = random.choice(PROX)
            blob, info = await asyncio.get_event_loop().run_in_executor(
                None, get_blob, proxy, user)
            if not blob:
                print("blobfail", info, flush=True)
                continue
            ctx = await browser.new_context(proxy=mkproxy(proxy), bypass_csp=True)
            page = await ctx.new_page()
            cap = {"c": None, "plain": None, "patched": 0}

            def onreq(rq):
                try:
                    if "/fc/gt2/" in rq.url and not cap["c"]:
                        d = dict(urllib.parse.parse_qsl(rq.post_data or "", keep_blank_values=True))
                        if d.get("c"):
                            cap["c"] = d["c"]
                except Exception:
                    pass

            page.on("request", onreq)
            served = {"d": False}
            html = HTML.replace("%BLOB%", json.dumps(blob)).replace("%API%", API_JS)

            async def route(rt, rq):
                try:
                    if "__plaincap__" in rq.url:
                        q = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(rq.url).query))
                        body = rq.post_data
                        if q.get("t") == "plain" and body and not cap["plain"]:
                            cap["plain"] = body
                        elif q.get("t") == "b64" and body:
                            cap.setdefault("b64", []).append((int(q.get("i", "0")), body))
                        await rt.fulfill(status=200, body="")
                        return
                    if not served["d"] and rq.resource_type == "document":
                        served["d"] = True
                        await rt.fulfill(status=200, content_type="text/html", body=html)
                        return
                    if "arkoselabs" in rq.url and "/api.js" in rq.url:
                        resp = await rt.fetch()
                        body = await resp.text()
                        if ANCHOR in body:
                            body = body.replace(ANCHOR, TRAP, 1)
                            cap["patched"] = 1
                        h = {k: v for k, v in resp.headers.items() if k.lower() != "cache-control"}
                        h["cache-control"] = "no-store"
                        await rt.fulfill(response=resp, body=body, headers=h)
                        return
                    await rt.continue_()
                except Exception:
                    try:
                        await rt.continue_()
                    except Exception:
                        pass

            await page.route("**/*", route)
            try:
                await page.goto("https://www.roblox.com/", wait_until="commit")
                for _ in range(70):
                    await asyncio.sleep(0.5)
                    if cap["c"] and cap["plain"]:
                        break
                await asyncio.sleep(0.6)
            except Exception as e:
                print("nav err", str(e)[:70], flush=True)
            try:
                await ctx.close()
            except Exception:
                pass

            if cap["c"]:
                got += 1
                ts = int(time.time())
                ctb = (len(cap["c"]) - 384) // 4 * 3
                open("%s/c_%d.txt" % (OUT, ts), "w").write(cap["c"])
                pl = None
                if cap["plain"]:
                    open("%s/plain_%d.json" % (OUT, ts), "w", encoding="utf8").write(cap["plain"])
                    pl = len(cap["plain"].encode("utf8"))
                print("PAIR %d patched=%d  c=%d -> ct~%dB   plaintext=%sB  delta=%s"
                      % (got, cap["patched"], len(cap["c"]), ctb, pl,
                         (ctb - pl) if pl else None), flush=True)
                if cap["plain"]:
                    print("   plaintext head:", cap["plain"][:90], flush=True)
                pieces = sorted(cap.get("b64", []))
                print("   caasgs calls (bytes-in | b64-out len):", flush=True)
                for i, v in pieces:
                    nb, _, b64 = v.partition("|")
                    print("      #%d  in=%sB  outb64=%d  %s" % (i, nb, len(b64), b64[:36]), flush=True)
                joined = "".join(b for _, v in pieces for b in [v.partition("|")[2]])
                print("   concat(b64 pieces) len=%d   actual c len=%d   equal=%s"
                      % (len(joined), len(cap["c"]), joined == cap["c"]), flush=True)
                open("%s/pieces_%d.json" % (OUT, ts), "w").write(
                    json.dumps([{"i": i, "v": v} for i, v in pieces]))
    print("PLAINCAPDONE got=%d" % got, flush=True)


asyncio.run(main())
