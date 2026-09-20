# Decode one obfuscated function: resolve its local index vars and every x(N)
# call through the extracted string-array decoder.
import re, sys, json, subprocess

src = open("/root/apijs_live.js").read()

def block(start):
    i = src.index("{", start); d = 0; j = i; instr = None; esc = False
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
                if d == 0: return src[start:j+1]
        j += 1
    raise ValueError

name = sys.argv[1]
m = re.search(r"\b%s\s*=\s*function" % re.escape(name), src) or \
    re.search(r"function\s+%s\s*\(" % re.escape(name), src)
body = block(m.start())
print("=== %s : %d bytes @%d ===" % (name, len(body), m.start()), file=sys.stderr)

# which decoder alias does it use?  e.g.  x=ie   /   $=de
al = re.findall(r"(\w+)\s*=\s*(ie|de|m|Lt|un|yn|Wn|\$t)\b", body[:400])
alias, dec = (al[0] if al else (None, "ie"))
# local numeric index vars
consts = dict((k, int(v, 0)) for k, v in re.findall(r"(\w+)\s*=\s*(0x[0-9a-f]+|\d+)\s*[,;]", body[:900]))

tbl = {}
out = subprocess.run(["node", "-e",
    "const d=require('/root/dec_%s.js');let o={};for(let i=100;i<1200;i++){try{const v=d(i);if(typeof v==='string')o[i]=v}catch(e){}};console.log(JSON.stringify(o))" % dec],
    capture_output=True, text=True)
try: tbl = json.loads(out.stdout)
except Exception: print("decoder load failed:", out.stderr[:200], file=sys.stderr)

def sub(mm):
    inner = mm.group(1).strip()
    if re.fullmatch(r"0x[0-9a-f]+|\d+", inner): idx = int(inner, 0)
    elif inner in consts: idx = consts[inner]
    else: return mm.group(0)
    v = tbl.get(str(idx))
    return ("'" + v + "'") if v is not None else mm.group(0)

txt = body
if alias:
    txt = re.sub(r"\b%s\(([^()]{1,20})\)" % re.escape(alias), sub, txt)
txt = re.sub(r"\b%s\(([^()]{1,20})\)" % re.escape(dec), sub, txt)
print(txt)
