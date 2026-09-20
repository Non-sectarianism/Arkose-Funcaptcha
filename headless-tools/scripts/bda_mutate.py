#!/usr/bin/env python3
"""Mutate a captured BDA plaintext and repair its internal hashes.

Both recipes verified against a real capture (Funcaptcha/bda_gen):
    f        = x64hash128( ";".join(value-part of each fe entry), 0 )
    ife_hash = x64hash128( ", ".join(full fe entries), 38 )
The value-part is everything after the first ':' in an entry like "H:32".
Anything touching `fe` MUST repair both or the BDA is self-inconsistent.
NOT repairable here (leave alone): wh (hashes window property names), and the
enhanced_fp digests webgl_hash_webgl / webgl_extensions_hash /
audio_codecs_extended_hash / math_fingerprint / supported_math_functions.

usage: bda_mutate.py <in.json> <out.json> FEKEY=value [FEKEY=value ...]
       bda_mutate.py <in.json> --show
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import murmur


def fe_val(entry):
    return entry.split(":", 1)[1] if ":" in entry else entry


def fe_key(entry):
    return entry.split(":", 1)[0] if ":" in entry else entry


def recompute(arr):
    m = {e["key"]: e["value"] for e in arr}
    fe = m["fe"]
    f = murmur.x64hash128(";".join(fe_val(x) for x in fe), 0)
    ife = murmur.x64hash128(", ".join(fe), 38)
    for e in arr:
        if e["key"] == "f":
            e["value"] = f
        elif e["key"] == "ife_hash":
            e["value"] = ife
    return f, ife


def main():
    src = sys.argv[1]
    arr = json.load(open(src))
    m = {e["key"]: e["value"] for e in arr}
    if len(sys.argv) > 2 and sys.argv[2] == "--show":
        for x in m["fe"]:
            print("   %-6s %s" % (fe_key(x), fe_val(x)))
        print("   f        =", m["f"])
        print("   ife_hash =", m["ife_hash"])
        # confirm the stored hashes are self-consistent before we touch anything
        f2 = murmur.x64hash128(";".join(fe_val(x) for x in m["fe"]), 0)
        i2 = murmur.x64hash128(", ".join(m["fe"]), 38)
        print("   self-consistent: f=%s ife=%s" % (f2 == m["f"], i2 == m["ife_hash"]))
        return
    out = sys.argv[2]
    edits = dict(a.split("=", 1) for a in sys.argv[3:])
    fe = m["fe"]
    changed = []
    for i, x in enumerate(fe):
        k = fe_key(x)
        if k in edits:
            fe[i] = "%s:%s" % (k, edits[k])
            changed.append("%s %s -> %s" % (k, fe_val(x), edits[k]))
    for e in arr:
        if e["key"] == "fe":
            e["value"] = fe
    f, ife = recompute(arr)
    json.dump(arr, open(out, "w"), separators=(",", ":"))
    print("mutated: %s" % ("; ".join(changed) if changed else "NOTHING MATCHED"))
    print("  new f        = %s" % f)
    print("  new ife_hash = %s" % ife)
    print("  wrote %s" % out)


main()
