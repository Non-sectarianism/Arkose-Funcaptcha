import sys
p = "/root/arkose-solver/arkose/solver.go"
s = open(p).read()
if "NOARID" in s:
    print("already patched"); sys.exit(0)
a = '\tlogInfo("first token not suppressed — retrying with ARID warmup")'
assert a in s, "arid anchor"
new = '''	// NOARID=1 keeps the FIRST token instead of minting a second one.
	// 52% of our image denials happen at wave 0 - before any /fc/ca exists - so the
	// cause is upstream of the game. This retry creates TWO Arkose sessions per
	// attempt from ONE Roblox blob and abandons the first; a real browser mints once.
	if os.Getenv("NOARID") == "1" {
		logPhase(4, 4, "suppress", 0, "skipped (NOARID=1, keeping first token)")
		res.Token = token
		return res, nil
	}
	logInfo("first token not suppressed — retrying with ARID warmup")'''
s = s.replace(a, new, 1)
open(p, "w").write(s)
print("patched OK")
