"""No-blob adapter — bring your own key, no enforcement blob.

For Arkose deployments that don't gate the mint on a `data[blob]` (many demos and
some sites), or for experimenting against the standalone Arkose client. You supply
the public key and host via environment variables:

    ARKOSE_PUBLIC_KEY   the site key (required)
    ARKOSE_HOST         Arkose host (default: client-api.arkoselabs.com)
    ARKOSE_SITE_URL     page to open / Referer (default: https://<host>/)

If a target actually requires a blob, gt2 will return DENIED ACCESS and you'll see
`no-gt2` — that's the signal you need a real adapter (see roblox.py as a template).
"""
import os


def make():
    from .base import Adapter
    pk = os.environ.get("ARKOSE_PUBLIC_KEY", "").strip()
    if not pk:
        raise SystemExit("noblob adapter needs ARKOSE_PUBLIC_KEY=<site key>")
    host = os.environ.get("ARKOSE_HOST", "client-api.arkoselabs.com").strip()
    site = os.environ.get("ARKOSE_SITE_URL", f"https://{host}/").strip()
    api_js = f"https://{host}/v2/{pk}/api.js"

    a = Adapter(name="noblob", public_key=pk, api_js=api_js, arkose_host=host, site_url=site)
    a.get_blob = lambda proxy, username: (None, "noblob")   # render without a blob
    return a
