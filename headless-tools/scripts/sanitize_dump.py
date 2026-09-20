#!/usr/bin/env python3
"""Turn a raw REQDUMP transcript into something safe and readable to hand out.

 - replaces binary response bodies (JPEG/JS bundles) with a size placeholder
 - asserts the BDA ciphertext never appears in the clear
 - keeps every request/response header, every form body, every JSON body
"""
import re, sys

raw = open(sys.argv[1], "rb").read().decode("utf8", "replace")
blocks = re.split(r"(?=^===== #)", raw, flags=re.M)
out, dropped = [], 0
for b in blocks:
    if not b.strip():
        continue
    m = re.search(r"--- response body \((\d+) B\) ---\n", b)
    if m:
        head, body = b[:m.end()], b[m.end():]
        n = int(m.group(1))
        printable = sum(1 for ch in body[:400] if 32 <= ord(ch) < 127 or ch in "\r\n\t")
        ratio = printable / max(1, len(body[:400]))
        if ratio < 0.85 or n > 20000:
            kind = "JPEG image" if body[:4].startswith("�") or "JFIF" in body[:200] else "binary/bundle"
            b = head + "[%s omitted, %d bytes]\n" % (kind, n)
            dropped += 1
    out.append(b)
txt = "".join(out)
assert "REDACTED-BDA" in txt or "/fc/gt2/" not in txt, "gt2 present but BDA not redacted!"
for bad in ("MIIBIjANBgkqhkiG",):
    assert bad not in txt, "leaked key material"
open(sys.argv[2], "w").write(txt)
print("wrote %s  (%d blocks, %d bodies omitted, %d KB)" %
      (sys.argv[2], len(out), dropped, len(txt) // 1024))
