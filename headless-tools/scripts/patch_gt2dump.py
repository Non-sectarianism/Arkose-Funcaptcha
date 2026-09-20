import sys
p = "/root/arkose-solver/arkose/solver.go"
s = open(p).read()
if "ARKDUMP" in s:
    print("already patched"); sys.exit(0)
a = "\tt0 = time.Now()\n\tdata := s.buildPayload(encryptedBDA, payloadKey, capiVersion)\n\tencoded := arkoseFormEncode(data)\n\theaders := s.buildHeaders()"
if a not in s:
    # fall back to a looser anchor
    a = "\tdata := s.buildPayload(encryptedBDA, payloadKey, capiVersion)"
    assert a in s, "buildPayload anchor"
    new = a + '''
	// ARKDUMP: the mint does NOT go through the doFF chokepoint, so record it here
	// for the shareable transcript. The BDA ciphertext is redacted - it is the
	// fingerprint; everything else (field set and ORDER) is what matters to a reader.
	if df := os.Getenv("ARKDUMP"); df != "" {
		if f, e := os.OpenFile(df, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644); e == nil {
			fmt.Fprintf(f, "\\n===== #0  POST %s/fc/gt2/public_key/%s\\n", s.cfg.Surl, s.cfg.PublicKey)
			fmt.Fprintf(f, "--- request headers ---\\n")
			for k, v := range s.buildHeaders() {
				fmt.Fprintf(f, "%s: %.200s\\n", k, v)
			}
			fmt.Fprintf(f, "--- request body: fields IN ORDER ---\\n")
			for _, k := range data.Keys() {
				val := data.Get(k)
				if k == "c" || k == "bda" {
					val = fmt.Sprintf("<REDACTED-BDA-%d-chars>", len(val))
				} else if len(val) > 160 {
					val = val[:160] + "..."
				}
				fmt.Fprintf(f, "  %-14s %s\\n", k, val)
			}
			f.Close()
		}
	}'''
    s = s.replace(a, new, 1)
open(p, "w").write(s)
print("patched OK")
