import re, sys
p = "/root/arkose-solver/cmd/robloxtest/main.go"
s = open(p).read()
if "arkTS1 :=" in s:
    print("already patched"); sys.exit(0)

# lib_deob/1609.js: ONE getTimestamp() feeds BOTH the timestamp cookie and the
# X-NewRelic-Timestamp header. Camoufox's captured /fc/ca proves it:
#   x-newrelic-timestamp 178901400126503  /  cookie timestamp=178901400126503
# We were calling arkTimestampNew() and arkTimestampCur() separately.
old = '''			car.Header = http.Header{"accept": {"*/*"}, "content-type": {"application/x-www-form-urlencoded; charset=UTF-8"},
				"cache-control": {"no-cache"},'''
assert old in s, "fc/ca header anchor"
new = '''			// ONE timestamp for both the cookie and the header - lib_deob/1609.js uses a
			// single `var F = getTimestamp()` for both, and Camoufox's capture shows the
			// identical value in x-newrelic-timestamp and cookie: timestamp=.
			arkTS1 := arkTimestampNew()
			car.Header = http.Header{"accept": {"*/*"}, "content-type": {"application/x-www-form-urlencoded; charset=UTF-8"},
				"cache-control": {"no-cache"},'''
s = s.replace(old, new, 1)

# now make the two uses share it, inside the /fc/ca header literal only
i = s.index("arkTS1 := arkTimestampNew()")
j = s.index("cresp, e := doFF(client, car)", i)
seg = s[i:j]
seg = seg.replace('"cookie": {("timestamp=" + arkTimestampNew())}', '"cookie": {("timestamp=" + arkTS1)}')
seg = seg.replace('"x-newrelic-timestamp": {arkTimestampCur()}', '"x-newrelic-timestamp": {arkTS1}')
s = s[:i] + seg + s[j:]

# sc coords: the real client reports a CONSTANT layout position, not a random click
s = s.replace("clickX := 193 + mrand.Intn(9)  // verify-button click x (real HAR: 197)",
              "clickX := 200 // constant in every real capture: {\"sc\":[200,259]}")
s = s.replace("clickY := 250 + mrand.Intn(9)  // verify-button click y (real HAR: 254)",
              "clickY := 259 // constant in every real capture: {\"sc\":[200,259]}")
open(p, "w").write(s)
print("patched OK")
