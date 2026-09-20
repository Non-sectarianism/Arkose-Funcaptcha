package arkose

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"os"
	"time"

	"github.com/google/uuid"
)

// BDA_PROFILE=/path/to/real_bda_plaintext.json replays a REAL captured (coherent, tell-free) BDA,
// refreshing only per-session fields. Every hash stays internally consistent (came from a real
// browser), so there are no synthetic tells. See Funcaptcha/info.txt.
func profileOverride(buildID string) []Item {
	pf := os.Getenv("BDA_PROFILE")
	if pf == "" {
		return nil
	}
	raw, err := os.ReadFile(pf)
	if err != nil {
		return nil
	}
	var arr []Item
	if err := json.Unmarshal(raw, &arr); err != nil {
		return nil
	}
	// BDA_NOMUTATE=1 replays the captured plaintext verbatim - no refreshed n, no new
	// session uuid. Isolates "our mutations break trust" from "our encryption does".
	if os.Getenv("BDA_NOMUTATE") == "1" {
		return arr
	}
	nowSec := time.Now().Unix()
	nowMs := time.Now().UnixMilli()
	for i := range arr {
		switch arr[i].Key {
		case "n":
			arr[i].Value = base64.StdEncoding.EncodeToString([]byte(fmt.Sprintf("%d", nowSec)))
		case "enhanced_fp":
			ef, ok := arr[i].Value.([]interface{})
			if !ok {
				continue
			}
			for _, e := range ef {
				m, ok := e.(map[string]interface{})
				if !ok {
					continue
				}
				switch m["key"] {
				case "1l2l5234ar2":
					m["value"] = fmt.Sprintf("%d⁣", nowMs)
				case "4b4b269e68":
					m["value"] = uuid.New().String()
				// 6a62b2a558 is the ENFORCEMENT HASH (32 hex, e.g.
				// ca3b41bdbcb85e7c7fb7892a970c52e8), NOT the ark-build-id UUID.
				// Overwriting it with buildID put a value in the BDA that Arkose knows
				// it never served -> punishing tier (waves=10 extendedshadows instead
				// of waves=2 3DRollball). Keep the captured value; only replace it when
				// BDA_ENFHASH is supplied.
				case "6a62b2a558":
					if eh := os.Getenv("BDA_ENFHASH"); eh != "" {
						m["value"] = eh
					}
				}
			}
		}
	}
	return arr
}
