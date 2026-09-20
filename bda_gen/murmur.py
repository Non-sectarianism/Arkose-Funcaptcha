"""x64hash128 (MurmurHash3 x64 128-bit) — Arkose api.js module 5194 Kt.K.
Ported verbatim from the reversed source; cross-checked against murmur_oracle.js.
Operates on charCodeAt semantics (UTF-16 code units, &255 per byte as the source does)."""

M32 = 0xFFFFFFFF


def _add(a, b):
    a = [a[0] >> 16, a[0] & 0xFFFF, a[1] >> 16, a[1] & 0xFFFF]
    b = [b[0] >> 16, b[0] & 0xFFFF, b[1] >> 16, b[1] & 0xFFFF]
    n = [0, 0, 0, 0]
    n[3] += a[3] + b[3]; n[2] += n[3] >> 16; n[3] &= 0xFFFF
    n[2] += a[2] + b[2]; n[1] += n[2] >> 16; n[2] &= 0xFFFF
    n[1] += a[1] + b[1]; n[0] += n[1] >> 16; n[1] &= 0xFFFF
    n[0] += a[0] + b[0]; n[0] &= 0xFFFF
    return [((n[0] << 16 | n[1]) & M32), ((n[2] << 16 | n[3]) & M32)]


def _mul(a, b):
    a = [a[0] >> 16, a[0] & 0xFFFF, a[1] >> 16, a[1] & 0xFFFF]
    b = [b[0] >> 16, b[0] & 0xFFFF, b[1] >> 16, b[1] & 0xFFFF]
    n = [0, 0, 0, 0]
    n[3] += a[3] * b[3]; n[2] += n[3] >> 16; n[3] &= 0xFFFF
    n[2] += a[2] * b[3]; n[1] += n[2] >> 16; n[2] &= 0xFFFF
    n[2] += a[3] * b[2]; n[1] += n[2] >> 16; n[2] &= 0xFFFF
    n[1] += a[1] * b[3]; n[0] += n[1] >> 16; n[1] &= 0xFFFF
    n[1] += a[2] * b[2]; n[0] += n[1] >> 16; n[1] &= 0xFFFF
    n[1] += a[3] * b[1]; n[0] += n[1] >> 16; n[1] &= 0xFFFF
    n[0] += a[0] * b[3] + a[1] * b[2] + a[2] * b[1] + a[3] * b[0]; n[0] &= 0xFFFF
    return [((n[0] << 16 | n[1]) & M32), ((n[2] << 16 | n[3]) & M32)]


def _rotl(t, e):
    e %= 64
    if e == 32:
        return [t[1], t[0]]
    if e < 32:
        return [((t[0] << e | t[1] >> (32 - e)) & M32), ((t[1] << e | t[0] >> (32 - e)) & M32)]
    e -= 32
    return [((t[1] << e | t[0] >> (32 - e)) & M32), ((t[0] << e | t[1] >> (32 - e)) & M32)]


def _shl(t, e):
    e %= 64
    if e == 0:
        return t
    if e < 32:
        return [((t[0] << e | t[1] >> (32 - e)) & M32), ((t[1] << e) & M32)]
    return [((t[1] << (e - 32)) & M32), 0]


def _xor(a, b):
    return [a[0] ^ b[0], a[1] ^ b[1]]


def _fmix(t):
    t = _xor(t, [0, t[0] >> 1])
    t = _mul(t, [4283543511, 3981806797]); t = _xor(t, [0, t[0] >> 1])
    t = _mul(t, [3301882366, 444984403]); t = _xor(t, [0, t[0] >> 1])
    return t


def _cc(s, i):
    # charCodeAt: UTF-16 code unit (source masks &255 per byte in block reads)
    return ord(s[i]) if i < len(s) else 0


def x64hash128(t, seed=0):
    t = t or ""
    n = len(t) % 16
    end = len(t) - n
    f = [0, seed]; l = [0, seed]
    v = [2277735313, 289559509]; h = [1291169091, 658871167]
    g = 0
    while g < end:
        d = [(_cc(t, g+4) & 255) | (_cc(t, g+5) & 255) << 8 | (_cc(t, g+6) & 255) << 16 | (_cc(t, g+7) & 255) << 24,
             (_cc(t, g) & 255) | (_cc(t, g+1) & 255) << 8 | (_cc(t, g+2) & 255) << 16 | (_cc(t, g+3) & 255) << 24]
        p = [(_cc(t, g+12) & 255) | (_cc(t, g+13) & 255) << 8 | (_cc(t, g+14) & 255) << 16 | (_cc(t, g+15) & 255) << 24,
             (_cc(t, g+8) & 255) | (_cc(t, g+9) & 255) << 8 | (_cc(t, g+10) & 255) << 16 | (_cc(t, g+11) & 255) << 24]
        d = _rotl(_mul(d, v), 31)
        f = _rotl(_xor(f, _mul(d, h)), 27)
        f = _add(f, l)
        f = _add(_mul(f, [0, 5]), [0, 1390208809])
        p = _rotl(_mul(p, h), 33)
        l = _rotl(_xor(l, _mul(p, v)), 31)
        l = _add(l, f)
        l = _add(_mul(l, [0, 5]), [0, 944331445])
        g += 16
    d = [0, 0]; p = [0, 0]
    # tail
    if n >= 15: p = _xor(p, _shl([0, _cc(t, g+14)], 48))
    if n >= 14: p = _xor(p, _shl([0, _cc(t, g+13)], 40))
    if n >= 13: p = _xor(p, _shl([0, _cc(t, g+12)], 32))
    if n >= 12: p = _xor(p, _shl([0, _cc(t, g+11)], 24))
    if n >= 11: p = _xor(p, _shl([0, _cc(t, g+10)], 16))
    if n >= 10: p = _xor(p, _shl([0, _cc(t, g+9)], 8))
    if n >= 9:
        p = _xor(p, [0, _cc(t, g+8)])
        p = _rotl(_mul(p, h), 33)
        l = _xor(l, _mul(p, v))
    if n >= 8: d = _xor(d, _shl([0, _cc(t, g+7)], 56))
    if n >= 7: d = _xor(d, _shl([0, _cc(t, g+6)], 48))
    if n >= 6: d = _xor(d, _shl([0, _cc(t, g+5)], 40))
    if n >= 5: d = _xor(d, _shl([0, _cc(t, g+4)], 32))
    if n >= 4: d = _xor(d, _shl([0, _cc(t, g+3)], 24))
    if n >= 3: d = _xor(d, _shl([0, _cc(t, g+2)], 16))
    if n >= 2: d = _xor(d, _shl([0, _cc(t, g+1)], 8))
    if n >= 1:
        d = _xor(d, [0, _cc(t, g)])
        d = _rotl(_mul(d, v), 31)
        f = _xor(f, _mul(d, h))
    f = _xor(f, [0, len(t)])
    l = _xor(l, [0, len(t)])
    f = _add(f, l); l = _add(l, f)
    f = _fmix(f); l = _fmix(l)
    f = _add(f, l); l = _add(l, f)
    return ("%08x" % (f[0] & M32)) + ("%08x" % (f[1] & M32)) + ("%08x" % (l[0] & M32)) + ("%08x" % (l[1] & M32))


if __name__ == "__main__":
    tests = [("", 0), ("test", 0), ("DNT:unknown;L:en-US;D:24", 0), ("hello world", 38), ("x", 420)]
    for t, s in tests:
        print(repr(t), s, "=>", x64hash128(t, s))
