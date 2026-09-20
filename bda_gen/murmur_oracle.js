// real x64hash128 (MurmurHash3 x64 128) extracted verbatim from Arkose api.js module 5194
      function r(t, e) {
        t = [t[0] >>> 16, t[0] & 65535, t[1] >>> 16, t[1] & 65535];
        e = [e[0] >>> 16, e[0] & 65535, e[1] >>> 16, e[1] & 65535];
        var n = [0, 0, 0, 0];
        n[3] += t[3] + e[3];
        n[2] += n[3] >>> 16;
        n[3] &= 65535;
        n[2] += t[2] + e[2];
        n[1] += n[2] >>> 16;
        n[2] &= 65535;
        n[1] += t[1] + e[1];
        n[0] += n[1] >>> 16;
        n[1] &= 65535;
        n[0] += t[0] + e[0];
        n[0] &= 65535;
        return [n[0] << 16 | n[1], n[2] << 16 | n[3]];
      }
      function o(t, e) {
        t = [t[0] >>> 16, t[0] & 65535, t[1] >>> 16, t[1] & 65535];
        e = [e[0] >>> 16, e[0] & 65535, e[1] >>> 16, e[1] & 65535];
        var n = [0, 0, 0, 0];
        n[3] += t[3] * e[3];
        n[2] += n[3] >>> 16;
        n[3] &= 65535;
        n[2] += t[2] * e[3];
        n[1] += n[2] >>> 16;
        n[2] &= 65535;
        n[2] += t[3] * e[2];
        n[1] += n[2] >>> 16;
        n[2] &= 65535;
        n[1] += t[1] * e[3];
        n[0] += n[1] >>> 16;
        n[1] &= 65535;
        n[1] += t[2] * e[2];
        n[0] += n[1] >>> 16;
        n[1] &= 65535;
        n[1] += t[3] * e[1];
        n[0] += n[1] >>> 16;
        n[1] &= 65535;
        n[0] += t[0] * e[3] + t[1] * e[2] + t[2] * e[1] + t[3] * e[0];
        n[0] &= 65535;
        return [n[0] << 16 | n[1], n[2] << 16 | n[3]];
      }
      function i(t, e) {
        if ((e %= 64) === 32) {
          return [t[1], t[0]];
        } else if (e < 32) {
          return [t[0] << e | t[1] >>> 32 - e, t[1] << e | t[0] >>> 32 - e];
        } else {
          e -= 32;
          return [t[1] << e | t[0] >>> 32 - e, t[0] << e | t[1] >>> 32 - e];
        }
      }
      function a(t, e) {
        if ((e %= 64) === 0) {
          return t;
        } else if (e < 32) {
          return [t[0] << e | t[1] >>> 32 - e, t[1] << e];
        } else {
          return [t[1] << e - 32, 0];
        }
      }
      function c(t, e) {
        return [t[0] ^ e[0], t[1] ^ e[1]];
      }
      function u(t) {
        t = c(t, [0, t[0] >>> 1]);
        t = c(t = o(t, [4283543511, 3981806797]), [0, t[0] >>> 1]);
        return t = c(t = o(t, [3301882366, 444984403]), [0, t[0] >>> 1]);
      }
      function s(t, e = 0) {
        e = e || 0;
        var n = (t = t || "").length % 16;
        for (var s = t.length - n, f = [0, e], l = [0, e], d = [0, 0], p = [0, 0], v = [2277735313, 289559509], h = [1291169091, 658871167], g = 0; g < s; g += 16) {
          d = [t.charCodeAt(g + 4) & 255 | (t.charCodeAt(g + 5) & 255) << 8 | (t.charCodeAt(g + 6) & 255) << 16 | (t.charCodeAt(g + 7) & 255) << 24, t.charCodeAt(g) & 255 | (t.charCodeAt(g + 1) & 255) << 8 | (t.charCodeAt(g + 2) & 255) << 16 | (t.charCodeAt(g + 3) & 255) << 24];
          p = [t.charCodeAt(g + 12) & 255 | (t.charCodeAt(g + 13) & 255) << 8 | (t.charCodeAt(g + 14) & 255) << 16 | (t.charCodeAt(g + 15) & 255) << 24, t.charCodeAt(g + 8) & 255 | (t.charCodeAt(g + 9) & 255) << 8 | (t.charCodeAt(g + 10) & 255) << 16 | (t.charCodeAt(g + 11) & 255) << 24];
          d = i(d = o(d, v), 31);
          f = i(f = c(f, d = o(d, h)), 27);
          f = r(f, l);
          f = r(o(f, [0, 5]), [0, 1390208809]);
          p = i(p = o(p, h), 33);
          l = i(l = c(l, p = o(p, v)), 31);
          l = r(l, f);
          l = r(o(l, [0, 5]), [0, 944331445]);
        }
        d = [0, 0];
        p = [0, 0];
        switch (n) {
          case 15:
            p = c(p, a([0, t.charCodeAt(g + 14)], 48));
          case 14:
            p = c(p, a([0, t.charCodeAt(g + 13)], 40));
          case 13:
            p = c(p, a([0, t.charCodeAt(g + 12)], 32));
          case 12:
            p = c(p, a([0, t.charCodeAt(g + 11)], 24));
          case 11:
            p = c(p, a([0, t.charCodeAt(g + 10)], 16));
          case 10:
            p = c(p, a([0, t.charCodeAt(g + 9)], 8));
          case 9:
            p = c(p, [0, t.charCodeAt(g + 8)]);
            p = i(p = o(p, h), 33);
            l = c(l, p = o(p, v));
          case 8:
            d = c(d, a([0, t.charCodeAt(g + 7)], 56));
          case 7:
            d = c(d, a([0, t.charCodeAt(g + 6)], 48));
          case 6:
            d = c(d, a([0, t.charCodeAt(g + 5)], 40));
          case 5:
            d = c(d, a([0, t.charCodeAt(g + 4)], 32));
          case 4:
            d = c(d, a([0, t.charCodeAt(g + 3)], 24));
          case 3:
            d = c(d, a([0, t.charCodeAt(g + 2)], 16));
          case 2:
            d = c(d, a([0, t.charCodeAt(g + 1)], 8));
          case 1:
            d = c(d, [0, t.charCodeAt(g)]);
            d = i(d = o(d, v), 31);
            f = c(f, d = o(d, h));
        }
        f = c(f, [0, t.length]);
        l = c(l, [0, t.length]);
        f = r(f, l);
        l = r(l, f);
        f = u(f);
        l = u(l);
        f = r(f, l);
        l = r(l, f);
        return `00000000${(f[0] >>> 0).toString(16)}`.slice(-8) + `00000000${(f[1] >>> 0).toString(16)}`.slice(-8) + `00000000${(l[0] >>> 0).toString(16)}`.slice(-8) + `00000000${(l[1] >>> 0).toString(16)}`.slice(-8);
      }
module.exports={s};
