import sys
p = "/root/arkose-solver/cmd/robloxtest/main.go"
s = open(p).read()
if "REQDUMP" in s:
    print("already patched"); sys.exit(0)

a = "\treturn c.Do(r)\n}"
assert a in s, "doFF return anchor"
new = '''	if df := os.Getenv("REQDUMP"); df != "" && r != nil {
		reqBody := ""
		if r.Body != nil && r.GetBody != nil {
			if rc, e := r.GetBody(); e == nil {
				b, _ := io.ReadAll(rc)
				rc.Close()
				reqBody = string(b)
			}
		}
		resp, err := c.Do(r)
		var status int
		respBody, respHdr := "", ""
		if err == nil && resp != nil {
			status = resp.StatusCode
			rb, _ := io.ReadAll(resp.Body)
			resp.Body.Close()
			resp.Body = io.NopCloser(bytes.NewReader(rb))
			respBody = string(rb)
			var hb strings.Builder
			for k, v := range resp.Header {
				if len(v) > 0 {
					fmt.Fprintf(&hb, "%s: %.200s\\n", k, v[0])
				}
			}
			respHdr = hb.String()
		}
		dumpEntry(df, r, reqBody, status, respHdr, respBody, err)
		return resp, err
	}
	return c.Do(r)
}

// dumpEntry appends one request/response pair to the shareable transcript.
// The BDA ciphertext (`c=` on /fc/gt2) is REDACTED - it is the fingerprint.
func dumpEntry(path string, r *http.Request, reqBody string, status int, respHdr, respBody string, err error) {
	f, e := os.OpenFile(path, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if e != nil {
		return
	}
	defer f.Close()
	dumpSeq++
	ord := r.Header[http.HeaderOrderKey]
	fmt.Fprintf(f, "\\n===== #%d  %s %s  -> %d %v\\n", dumpSeq, r.Method, r.URL.String(), status, err)
	fmt.Fprintf(f, "--- request headers (in send order) ---\\n")
	for _, k := range ord {
		if v, ok := r.Header[k]; ok && len(v) > 0 {
			fmt.Fprintf(f, "%s: %.220s\\n", k, v[0])
		}
	}
	if reqBody != "" {
		fmt.Fprintf(f, "--- request body (%d B) ---\\n%s\\n", len(reqBody), redactBDA(reqBody))
	}
	if respHdr != "" {
		fmt.Fprintf(f, "--- response headers ---\\n%s", respHdr)
	}
	if respBody != "" {
		b := respBody
		if len(b) > 4000 {
			b = b[:4000] + fmt.Sprintf("\\n...[truncated, total %d B]", len(respBody))
		}
		fmt.Fprintf(f, "--- response body (%d B) ---\\n%s\\n", len(respBody), b)
	}
}

var dumpSeq int

func redactBDA(s string) string {
	for _, key := range []string{"c=", "bda="} {
		if i := strings.Index(s, key); i >= 0 {
			j := strings.Index(s[i:], "&")
			end := len(s)
			if j >= 0 {
				end = i + j
			}
			s = s[:i] + key + "<REDACTED-BDA-" + fmt.Sprint(end-i-len(key)) + "-chars>" + s[end:]
		}
	}
	return s
}'''
s = s.replace(a, new, 1)
open(p, "w").write(s)
print("patched OK")
