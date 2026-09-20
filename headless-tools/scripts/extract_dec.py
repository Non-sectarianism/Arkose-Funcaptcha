# Extract a string-array decoder (array fn + decoder fn + its rotation IIFE) from
# api.js so it can be evaluated standalone in node, instead of reimplementing the
# rotation by hand.
import re, sys, json

src = open("/root/apijs_live.js").read()

def block(start):
    """Return the source of a function starting at `start` (at 'function')."""
    i = src.index("{", start)
    d = 0
    j = i
    instr = None
    esc = False
    while j < len(src):
        c = src[j]
        if instr:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == instr: instr = None
        else:
            if c in "\"'`": instr = c
            elif c == "{": d += 1
            elif c == "}":
                d -= 1
                if d == 0:
                    return src[start:j+1]
            elif c == "/" and j+1 < len(src) and src[j+1] == "/":
                while j < len(src) and src[j] != "\n": j += 1
        j += 1
    raise ValueError("unbalanced")

def find_fn(name):
    m = re.search(r"function\s+%s\s*\(" % re.escape(name), src)
    if not m: return None
    return block(m.start())

dec, arr = sys.argv[1], sys.argv[2]
parts = []
a = find_fn(arr); d = find_fn(dec)
if not a or not d:
    print("MISSING", arr, a is not None, dec, d is not None); sys.exit(1)
parts += [a, d]

# the rotation IIFE: !function(t,e){ ... }(arr, NUMBER)  — find one that calls arr(
rot = None
for m in re.finditer(r"!function\s*\(", src):
    try: b = block(m.start()+1)
    except Exception: continue
    tail = src[m.start()+1+len(b): m.start()+1+len(b)+80]
    if re.match(r"\s*\(\s*%s\s*[,)]" % re.escape(arr), tail):
        end = tail.index(")") + 1
        rot = "!function(" + b[b.index("(")+1:] if False else src[m.start(): m.start()+1+len(b)+end]
        break
if rot: parts.append(rot)
print("EXTRACTED arr=%dB dec=%dB rot=%s" % (len(a), len(d), (len(rot) if rot else None)), file=sys.stderr)
open("/root/dec_%s.js" % dec, "w").write(
    ";\n".join(parts) + ";\nmodule.exports = " + dec + ";\n")
print("/root/dec_%s.js" % dec)
