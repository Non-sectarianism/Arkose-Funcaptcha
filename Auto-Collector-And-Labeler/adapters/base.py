"""Adapter interface.

An adapter tells the collector everything site-specific about an Arkose deployment:
the public key, where api.js lives, the Arkose host, the page to open, and — the
only genuinely hard part — how to mint the site's enforcement blob (`data[blob]`).

The Arkose *collection engine* (rendering api.js, clicking Start Puzzle, capturing
the challenge image, driving arrows + Submit, reading the /fc/ca verdict, saving the
dataset) is entirely site-agnostic. Only this adapter changes per site.
"""
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Adapter:
    name: str
    public_key: str          # Arkose site key (visible in the target site's page source)
    api_js: str              # full api.js URL, e.g. https://<host>/v2/<public_key>/api.js
    arkose_host: str         # Arkose host, e.g. arkoselabs.roblox.com  (image-server referer)
    site_url: str            # page to navigate to (also the document Referer)

    def get_blob(self, proxy: str, username: str) -> Tuple[Optional[str], str]:
        """Mint the site's enforcement blob.

        Returns (blob, info). `blob` is the data-exchange string passed to
        setConfig({data:{blob}}); return (None, reason) on failure. A site that
        needs no blob should return (None, "noblob") — the engine then renders
        without one.
        """
        raise NotImplementedError
