"""Roblox adapter — the reference implementation of a blob-minting adapter.

`data[blob]` for Roblox comes from the Roblox *login* flow: attempt a login with a
wrong password, which returns a challenge; solve the challenge service's small
proof-of-work; continue the challenge; and read `dataExchangeBlob` out of the
response. No real account is created or accessed — a wrong password is enough to
trigger the captcha, which is all we need.

Use this file as the template for other Arkose sites: implement `get_blob` for
that site's enforcement flow and fill in the four fields at the bottom.
"""
import urllib.request, urllib.error, ssl, http.cookiejar, json, base64, random

# Roblox's Arkose public key — this is public (it appears in Roblox's own page source).
PUBLIC_KEY = "476068BF-9607-4799-B53D-966BE98E2B81"
ARKOSE_HOST = "arkoselabs.roblox.com"
API_JS = f"https://{ARKOSE_HOST}/v2/{PUBLIC_KEY}/api.js"
SITE_URL = "https://www.roblox.com/"

POW_CAP = 8_000_000    # skip an IP whose proof-of-work ramps too high (degraded/flagged proxy)

_UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
]


def _get_blob(proxy, username):
    """Roblox login (wrong password) -> dataExchangeBlob. Returns (blob, info)."""
    ua = random.choice(_UA_POOL)
    ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    cj = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": proxy, "https": proxy}),
        urllib.request.HTTPSHandler(context=ctx),
        urllib.request.HTTPCookieProcessor(cj))
    csrf = [None]

    def req(method, url, body=None):
        h = {"User-Agent": ua, "Accept": "application/json, text/plain, */*",
             "Content-Type": "application/json;charset=UTF-8",
             "Origin": "https://www.roblox.com", "Referer": "https://www.roblox.com/"}
        if csrf[0]: h["x-csrf-token"] = csrf[0]
        data = json.dumps(body).encode() if body is not None else None
        for _ in range(2):
            r = urllib.request.Request(url, data=data, headers=h, method=method)
            try:
                resp = op.open(r, timeout=25)
                nc = resp.headers.get("x-csrf-token")
                if nc: csrf[0] = nc
                return resp.status, dict(resp.headers), resp.read().decode()
            except urllib.error.HTTPError as e:
                nc = e.headers.get("x-csrf-token")
                if e.code == 403 and nc and nc != h.get("x-csrf-token"):
                    csrf[0] = nc; continue          # retry once with the fresh CSRF token
                if nc: csrf[0] = nc
                return e.code, dict(e.headers), e.read().decode()
        return 0, {}, ""

    try:
        req("POST", "https://auth.roblox.com/v2/login", body={})   # warm up / seed CSRF
        login = {"ctype": "Username", "cvalue": username,
                 "password": "Xk" + str(random.randint(10000, 99999)) + "!q"}   # deliberately wrong
        st, hd, _ = req("POST", "https://auth.roblox.com/v2/login", body=login)
        cid = hd.get("rblx-challenge-id"); ctype = hd.get("rblx-challenge-type"); cmeta = hd.get("rblx-challenge-metadata")
        if not cid:
            return None, f"no-challenge(st={st})"
        meta = json.loads(base64.b64decode(cmeta + "==" * (-len(cmeta) % 4)))
        sid = meta.get("sessionId")

        st, hd, pz = req("GET", f"https://apis.roblox.com/proof-of-work-service/v1/pow-puzzle?urlLocale=en_us&sessionID={sid}")
        art = json.loads(json.loads(pz)["artifacts"])
        N, A, T = int(art["N"]), int(art["A"]), int(art["T"])
        if T > POW_CAP:
            return None, f"pow-too-high(T={T})"
        x = A
        for _ in range(T):                          # sequential squaring VDF
            x = (x * x) % N
        st, hd, pw2 = req("POST", "https://apis.roblox.com/proof-of-work-service/v1/pow-puzzle?urlLocale=en_us",
                          body={"sessionID": sid, "solution": str(x)})
        rtok = json.loads(pw2).get("redemptionToken")
        if not rtok:
            return None, "no-redemption"

        cm = json.dumps({"redemptionToken": rtok, "sessionId": sid})
        st, hd, r3 = req("POST", "https://apis.roblox.com/challenge/v1/continue?urlLocale=en_us",
                         body={"challengeId": cid, "challengeType": ctype, "challengeMetadata": cm})
        if "challengeMetadata" not in r3:
            return None, f"no-meta(st={st})"
        m2 = json.loads(json.loads(r3)["challengeMetadata"])
        blob = m2.get("dataExchangeBlob")
        return (blob, m2.get("unifiedCaptchaId", "ok")) if blob else (None, "no-blob")
    except Exception as e:
        return None, f"exc:{str(e)[:40]}"


def make():
    from .base import Adapter
    a = Adapter(name="roblox", public_key=PUBLIC_KEY, api_js=API_JS,
                arkose_host=ARKOSE_HOST, site_url=SITE_URL)
    a.get_blob = _get_blob      # bind the site-specific minter
    return a
