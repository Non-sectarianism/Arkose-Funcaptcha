"""BDA plaintext generator — assembles the Arkose FunCaptcha `bda` plaintext array
from a device profile, per the fully-reversed api.js (see Funcaptcha/info.txt "FULL BDA REVERSE").

Output = the ordered list of {key,value} that api.js builds at deob line 14089 and then
RSA-OAEP+AES-GCM encrypts into the `c=` field. The existing solver handles encryption; this
module replaces buggerlogger's synthetic fingerprint with a coherent, automation-clean one.

Field order and semantics are taken verbatim from the reverse:
  fe (u.f) 24 components -> f_h = x64hash128(values ";"-joined, 0); fe strings "k:v"; ife_hash=x64hash128(fe ", "-joined, 38)
  enhanced_fp (u.ef): webgl + navigator + media + audio + AUTOMATION SWEEP (all reported clean/absent)
  wh (u.w): x64hash128(sorted window own-prop names, 420) | x64hash128(prototype-chain prop names, 420)
  jsbd (u.js): {HL,NCE,DT,NWD,DMTO,DOTO}  NWD MUST be "undefined" (never "faked")
"""
import base64
import json
import time

from murmur import x64hash128

# ---------------------------------------------------------------------------
# The 24 fe components, in the EXACT source order (deob 12676-12700). Order is
# load-bearing: f_h hashes the values ";"-joined in this order; fe is "k:v" in this order.
FE_ORDER = ["DNT", "L", "D", "PR", "S", "AS", "TO", "SS", "LS", "IDB", "B", "ODB",
            "CPUC", "PK", "CFP", "FR", "FOS", "FB", "JSF", "P", "T", "H", "SWF"]


def build_fe(p):
    """Build the 24-component fp object from a profile `p`. Values mirror the source getters."""
    scr = p["screen"]
    S = sorted([scr["w"], scr["h"]], reverse=True)          # [max,min]
    AS = sorted([scr["aw"], scr["ah"]], reverse=True)
    return {
        "DNT": p.get("dnt", "unknown"),                      # navigator.doNotTrack||"unknown"
        "L": p["language"],                                  # navigator.language
        "D": scr["cd"],                                      # screen.colorDepth
        "PR": p["pixelRatio"],                               # window.devicePixelRatio
        "S": S,                                              # [screen w,h] sorted
        "AS": AS,                                            # [availW,availH] sorted
        "TO": p["tzOffset"],                                 # timezone offset (minutes)
        "SS": True, "LS": True, "IDB": True,                 # storage present
        "B": False,                                          # document.body.addBehavior (IE only)
        "ODB": p.get("openDatabase", False),                 # window.openDatabase (Firefox: false)
        "CPUC": p.get("cpuClass", "unknown"),                # navigator.cpuClass (FF/Chrome: unknown)
        "PK": p["platform"],                                 # navigator.platform
        "CFP": p["canvas_cfp"],                              # canvas fingerprint (NEEDS_REAL: per-hw)
        "FR": False, "FOS": False, "FB": False,              # fake-resolution/OS/browser checks: clean
        "JSF": p["js_fonts"],                                # detected fonts list (string)
        "P": p["plugins_fp"],                                # plugins fingerprint (string)
        "T": p.get("touch", [0, False, False]),              # touch support [maxTouchPoints, ontouchstart, ...]
        "H": p["hardwareConcurrency"],                       # navigator.hardwareConcurrency
        "SWF": False,                                        # typeof window.swfobject!=="undefined"
    }


def _val_str(v):
    """Reproduce JS r.toString() for a fe value (arrays -> "a,b", bools -> "true"/"false")."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return ",".join(_val_str(x) for x in v)
    return str(v)


def fe_values_joined(fe):
    # V.KQ(o).join(";") — the ordered VALUES for f_h
    return ";".join(_val_str(fe[k]) for k in FE_ORDER)


def fe_strings(fe):
    # qt(u.f,true) -> ["k:v",...]  (source: `${n}:${r.toString?r.toString():r}`)
    return [f"{k}:{_val_str(fe[k])}" for k in FE_ORDER]


# ---------------------------------------------------------------------------
# Verbatim enhanced_fp key order (api.js module 7333 C). See bda_gen/enhanced_fp_keys.txt.
EF_KEY_ORDER = [
    "user_agent_data_brands", "user_agent_data_mobile",
    "navigator_connection_downlink", "navigator_connection_downlink_max",
    "network_info_rtt", "network_info_save_data", "network_info_rtt_type",
    "screen_pixel_depth", "navigator_device_memory", "navigator_languages",
    "window_inner_width", "window_inner_height", "window_outer_width", "window_outer_height",
    "browser_detection_firefox", "browser_detection_brave",
    "9f41a2c", "5c273b3", "ce4046e", "f58835f", "browser_object_checks", "29s83ih9",
    "audio_codecs", "audio_codecs_extended_hash", "video_codecs", "video_codecs_extended_hash",
    "media_query_dark_mode", "f9bf2db",
    "headless_browser_phantom", "headless_browser_selenium", "headless_browser_nightmare_js",
    "862f2c1", "1l2l5234ar2",
    "document__referrer", "window__ancestor_origins", "window__tree_index",
    "window__tree_structure", "window__location_href",
    "client_config__sitedata_location_href", "client_config__language",
    "client_config__surl", "client_config__surl_hash", "client_config__triggered_inline",
    "mobile_sdk__is_sdk", "z87b89t5", "audio_fingerprint", "navigator_battery_charging",
    "7541c2s", "1f220c9", "math_fingerprint", "supported_math_functions",
    "3f76dd27", "5dd48ca0", "4b4b269e68", "6a62b2a558", "isKeyless", "waitForSettings",
    "c2d2015", "43f2d94", "20c15922", "4f59ca8",
]
# Hashed-name keys: values are computed detectors (webgl/canvas/bot). Exact value FORMAT pending
# capture — profile supplies them under profile["ef_hashed"][key].
EF_HASHED = {"9f41a2c", "5c273b3", "ce4046e", "f58835f", "29s83ih9", "f9bf2db", "862f2c1",
             "1l2l5234ar2", "7541c2s", "1f220c9", "3f76dd27", "5dd48ca0", "6a62b2a558",
             "c2d2015", "43f2d94", "20c15922", "4f59ca8"}


def build_enhanced_fp(p):
    """u.ef in the VERBATIM 61-key order. Readable keys from the profile (clean automation),
    hashed computed-detector keys from the profile's captured ef_hashed block."""
    scr = p["screen"]
    hashed = p.get("ef_hashed", {})
    cfg = p.get("embed_cfg", {})
    vals = {
        "user_agent_data_brands": p.get("ua_brands"),      # FF: None
        "user_agent_data_mobile": p.get("ua_mobile"),
        "navigator_connection_downlink": p.get("conn_downlink"),
        "navigator_connection_downlink_max": p.get("conn_downlink_max"),
        "network_info_rtt": p.get("conn_rtt"),
        "network_info_save_data": p.get("conn_save_data"),
        "network_info_rtt_type": p.get("conn_type"),
        "screen_pixel_depth": scr["pd"],
        "navigator_device_memory": p.get("deviceMemory"),
        "navigator_languages": ",".join(p["languages"]),
        "window_inner_width": p["window"]["iw"], "window_inner_height": p["window"]["ih"],
        "window_outer_width": p["window"]["ow"], "window_outer_height": p["window"]["oh"],
        "browser_detection_firefox": p.get("is_firefox", True),
        "browser_detection_brave": False,
        "browser_object_checks": p.get("browser_object_checks", ""),
        "audio_codecs": p["audio_codecs"], "audio_codecs_extended_hash": p["audio_codecs_hash"],
        "video_codecs": p["video_codecs"], "video_codecs_extended_hash": p["video_codecs_hash"],
        "media_query_dark_mode": p.get("dark_mode", False),
        "headless_browser_phantom": False,          # clean
        "headless_browser_selenium": False,         # clean
        "headless_browser_nightmare_js": False,     # clean
        "document__referrer": cfg.get("referrer", ""),
        "window__ancestor_origins": cfg.get("ancestor_origins", []),
        "window__tree_index": cfg.get("tree_index", [0]),
        "window__tree_structure": cfg.get("tree_structure", "[[],[],[],[[]],[]]"),
        "window__location_href": cfg.get("location_href", ""),
        "client_config__sitedata_location_href": cfg.get("sitedata_href", ""),
        "client_config__language": cfg.get("language", "en"),
        "client_config__surl": cfg.get("surl", "https://roblox-api.arkoselabs.com"),
        "client_config__surl_hash": x64hash128(cfg.get("surl", "https://roblox-api.arkoselabs.com"), 0),
        "client_config__triggered_inline": cfg.get("triggered_inline", False),
        "mobile_sdk__is_sdk": False,
        "z87b89t5": 100302,                         # confirmed constant
        "audio_fingerprint": p["audio_fp"],         # [hw]
        "navigator_battery_charging": p.get("battery_charging", True),
        "math_fingerprint": p.get("math_fingerprint"),        # per-engine constant (capture)
        "supported_math_functions": p.get("supported_math_functions"),
        "4b4b269e68": cfg.get("enforcement_id", ""),          # session id — set at mint time
        "isKeyless": False,
        "waitForSettings": p.get("wait_for_settings", ""),
    }
    ef = {}
    for k in EF_KEY_ORDER:
        if k in EF_HASHED:
            ef[k] = hashed.get(k)                   # captured computed-detector value
        else:
            ef[k] = vals.get(k)
    return ef


def enhanced_fp_pairs(ef):
    return [{"key": k, "value": v} for k, v in ef.items()]


# ---------------------------------------------------------------------------
def build_wh(p):
    """u.w = x64hash128(sorted window own-prop names,420) | x64hash128(proto-chain names,420).
    These name-lists are a per-browser-VERSION constant captured once from a clean real browser."""
    own = p["wh_window_props"]        # list[str] already filtered of f_/pU/webpack, then .sort()
    proto = p["wh_proto_props"]       # list[str] from walking the prototype chain
    a = x64hash128("|".join(sorted(own)), 420)
    b = x64hash128("|".join(proto), 420)
    return f"{a}|{b}"


def build_jsbd(p):
    """u.js. NWD carries the webdriver verdict — MUST be 'undefined' (a generated env has no
    navigator.webdriver descriptor at all, so it never reads 'faked')."""
    A = {
        "HL": p.get("history_length", 2),
        "NCE": True,                          # navigator.cookieEnabled
        "DT": p.get("document_title", ""),    # arkose iframe title
        "NWD": "undefined",                   # <-- clean; never "faked"
        "DMTO": 1,
        "DOTO": 1,
    }
    return json.dumps(A, separators=(",", ":"))


# ---------------------------------------------------------------------------
def build_bda_plaintext(p, capi_version="4.4.5"):
    """Assemble the ordered BDA plaintext array exactly as api.js does (deob 14089-14091)."""
    fe = build_fe(p)
    fe_strs = fe_strings(fe)
    f_h = x64hash128(fe_values_joined(fe), 0)
    ef = build_enhanced_fp(p)
    arr = [
        {"key": "api_type", "value": "js"},
        {"key": "f", "value": f_h},
        {"key": "n", "value": base64.b64encode(str(int(time.time())).encode()).decode()},
        {"key": "wh", "value": build_wh(p)},
        {"key": "enhanced_fp", "value": enhanced_fp_pairs(ef)},
        {"key": "fe", "value": fe_strs},
        {"key": "ife_hash", "value": x64hash128(", ".join(fe_strs), 38)},
        {"key": "jsbd", "value": build_jsbd(p)},
        {"key": "c", "value": capi_version},
    ]
    # fb inserted after enhanced_fp only if FOS/FB/FR set — we keep them clean, so omitted.
    return arr


if __name__ == "__main__":
    import sys
    prof = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "bda_gen/profile_sample.json"))
    bda = build_bda_plaintext(prof)
    print(json.dumps(bda, indent=2)[:2000])
    print("...\n[f_h]", next(x["value"] for x in bda if x["key"] == "f"))
    print("[wh]", next(x["value"] for x in bda if x["key"] == "wh"))
    print("[ife_hash]", next(x["value"] for x in bda if x["key"] == "ife_hash"))
