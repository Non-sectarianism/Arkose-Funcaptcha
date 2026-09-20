package arkose

import (
	"fmt"
	"os"
	"strings"
	"time"

	"math/rand"

	"github.com/google/uuid"
)

// ARK_FIREFOX=1 makes the BDA present as Windows Firefox 152 instead of Chrome.
// Values captured from a real Camoufox (Firefox) session — see Funcaptcha/bda_capture.
// Bounded experiment: flips the browser-family "tells"; WebGL params left as-is.
func arkFirefox() bool { return os.Getenv("ARK_FIREFOX") == "1" }

// Firefox Windows feature set for f58835f (vs chromeWindowsFeatures).
var firefoxWindowsFeatures = BrowserFeatures{
	PermissionStatus:  true,  // FF has PermissionStatus
	EyeDropper:        false, // Chrome-only
	AudioData:         false, // WebCodecs AudioData - not in FF stable BDA path
	WritableStream:    true,  // FF has it
	CSSStyleRule:      true,
	NavigatorUA:       false, // FF has no navigator.userAgentData
	BarcodeDetector:   false,
	DisplayNames:      true, // Intl.DisplayNames
	ContactsManager:   false,
	SVGDiscardElement: false,
	USB:               false, // FF has no WebUSB
	MediaDevices:      true,
	PlaybackQuality:   true, // getVideoPlaybackQuality
}

// buildFEFirefox: the fe[] array with Firefox plugin order + Win32.
func buildFEFirefox(preset *Config, device DeviceProfile, identity *DeviceIdentity) ([]string, string) {
	screenW, screenH := device.ScreenWidth, device.ScreenHeight
	availW, availH := device.AvailWidth, device.AvailHeight
	fe := []string{
		"DNT:unknown",
		"L:" + identity.LanguageTag,
		fmt.Sprintf("D:%d", device.ColorDepth),
		fmt.Sprintf("PR:%s", formatDPR(device.DevicePixelRatio)),
		fmt.Sprintf("S:%d,%d", screenW, screenH),
		fmt.Sprintf("AS:%d,%d", availW, availH),
		fmt.Sprintf("TO:%d", identity.TZOffset),
		"SS:true",
		"LS:true",
		"IDB:true",
		"B:false",
		"ODB:false",
		"CPUC:unknown",
		"PK:Win32",
		fmt.Sprintf("CFP:%d", identity.CFP),
		"FR:false",
		"FOS:false",
		"FB:false",
		"JSF:" + identity.FontList,
		// Firefox enumerates the 5 PDF plugins in this order (real capture)
		"P:PDF Viewer,Chrome PDF Viewer,Chromium PDF Viewer,Microsoft Edge PDF Viewer,WebKit built-in PDF",
		"T:0,false,false",
		fmt.Sprintf("H:%d", device.HardwareConcurrency),
		"SWF:false",
	}
	return fe, ComputeF(fe)
}

// buildEnhancedFPFirefox: near-copy of buildEnhancedFP with Firefox-family deltas.
func buildEnhancedFPFirefox(preset *Config, identity *DeviceIdentity, device DeviceProfile, buildID string) []Item {
	gpu := device.WebGL()
	chrome := pickChromeVersion() // still used for webgl version strings (left as-is)

	ancestorOrigins := preset.WindowAncestorOrigins
	if ancestorOrigins == nil {
		ancestorOrigins = []string{}
	}
	treeIndex := preset.WindowTreeIndex
	if treeIndex == nil {
		treeIndex = []int{}
	}
	treeStructures := []string{
		"[[[],[]],[[]],[],[]]",
		"[[],[],[],[[]],[]]",
		"[[],[],[],[[]],[[]],[],[]]",
	}
	treeStructure := preset.WindowTreeStructure
	if treeStructure == "" {
		treeStructure = treeStructures[rand.Intn(len(treeStructures))]
	}
	surl := preset.Surl
	c8480Hex := md5Hex(surl)
	nowMs := time.Now().UnixMilli()
	innerW, innerH := device.Inner()

	webglFields := buildWebGLFieldsInternal(gpu, chrome)
	webglHash := ComputeWebGLHash(webglFields)
	rttType := ComputeRTTType(ComputeWebGLExtensionsHash(WebGLExtensions), webglHash)

	return append(append([]Item{}, webglFields...), []Item{
		{Key: "webgl_hash_webgl", Value: webglHash},
		// Firefox: NO navigator.userAgentData
		{Key: "user_agent_data_brands", Value: nil},
		{Key: "user_agent_data_mobile", Value: nil},
		{Key: "navigator_connection_downlink", Value: device.Downlink},
		{Key: "navigator_connection_downlink_max", Value: identity.NavConnectionDownlink_Max},
		{Key: "network_info_rtt", Value: device.RTT},
		{Key: "network_info_save_data", Value: device.SaveData},
		{Key: "network_info_rtt_type", Value: rttType},
		{Key: "screen_pixel_depth", Value: device.ColorDepth},
		// Firefox: navigator.deviceMemory is undefined -> null
		{Key: "navigator_device_memory", Value: nil},
		{Key: "navigator_languages", Value: identity.Languages},
		{Key: "window_inner_width", Value: innerW},
		{Key: "window_inner_height", Value: innerH},
		{Key: "window_outer_width", Value: device.OuterWidth},
		{Key: "window_outer_height", Value: device.OuterHeight},
		{Key: "browser_detection_firefox", Value: true},
		{Key: "browser_detection_brave", Value: false},
		{Key: "9f41a2c", Value: false},
		{Key: "5c273b3", Value: false},
		{Key: "ce4046e", Value: false},
		{Key: "f58835f", Value: ComputeF58835f(firefoxWindowsFeatures)},
		// Firefox: no window.chrome / opr / etc.
		{Key: "browser_object_checks", Value: ComputeBrowserObjectChecks([]string{})},
		{Key: "29s83ih9", Value: md5Str("false") + "⁣"},
		// Firefox canPlayType strings (real capture)
		{Key: "audio_codecs", Value: `{"ogg":"probably","mp3":"maybe","wav":"probably","m4a":"maybe","aac":"maybe"}`},
		{Key: "audio_codecs_extended_hash", Value: AudioCodecsExtendedHash()},
		{Key: "video_codecs", Value: `{"ogg":"","h264":"probably","webm":"probably","mpeg4v":"","mpeg4a":"probably","theora":""}`},
		{Key: "video_codecs_extended_hash", Value: VideoCodecsExtendedHash()},
		{Key: "media_query_dark_mode", Value: false},
		{Key: "f9bf2db", Value: `{"pc":"no-preference","ah":"hover","ap":"fine","p":"fine","h":"hover","u":"fast","prm":"no-preference","prt":"no-preference","s":"enabled","fc":"none"}`},
		{Key: "headless_browser_phantom", Value: false},
		{Key: "headless_browser_selenium", Value: false},
		{Key: "headless_browser_nightmare_js", Value: false},
		{Key: "862f2c1", Value: 4},
		{Key: "1l2l5234ar2", Value: fmt.Sprintf("%d⁣", nowMs)},
		{Key: "document__referrer", Value: firstNonEmpty(preset.DocumentReferrer, defaultDocumentReferrer)},
		{Key: "window__ancestor_origins", Value: ancestorOrigins},
		{Key: "window__tree_index", Value: treeIndex},
		{Key: "window__tree_structure", Value: treeStructure},
		{Key: "window__location_href", Value: preset.WindowLocationHref},
		{Key: "client_config__sitedata_location_href", Value: preset.SitedataLocationHref},
		{Key: "client_config__language", Value: strings.ToLower(preset.Language)},
		{Key: "client_config__surl", Value: surl},
		{Key: "c8480e29a", Value: c8480Hex + "⁢"},
		{Key: "client_config__triggered_inline", Value: false},
		{Key: "mobile_sdk__is_sdk", Value: false},
		{Key: "z87b89t5", Value: nil},
		{Key: "audio_fingerprint", Value: PickAudioFingerprint()},
		// Firefox removed the Battery API -> null
		{Key: "navigator_battery_charging", Value: nil},
		{Key: "7541c2s", Value: identity.Hash7541c2s},
		{Key: "1f220c9", Value: identity.Hash1f220c9},
		{Key: "math_fingerprint", Value: identity.MathFingerprint},
		{Key: "supported_math_functions", Value: identity.SupportedMathFuncs},
		{Key: "3f76dd27", Value: "landscape-primary"},
		{Key: "5dd48ca0", Value: 5},
		{Key: "4b4b269e68", Value: uuid.New().String()},
		{Key: "6a62b2a558", Value: firstNonEmpty(buildID, preset.EnforcementHash, defaultEnforcementHash)},
		{Key: "is_keyless", Value: false},
		{Key: "client_config__wait_for_settings", Value: false},
		{Key: "c2d2015", Value: identity.Hashc2d2015},
		{Key: "43f2d94", Value: []interface{}{}},
		{Key: "20c15922", Value: true},
		{Key: "4f59ca8", Value: nil},
		{Key: "3ea7194", Value: HDRInfo{Supported: true, Formats: []string{"HDR10", "HLG"}, IsHDR: false}},
		{Key: "05d3d24", Value: identity.Hash05d3d24},
		{Key: "speech_default_voice", Value: identity.SpeechDefaultVoice},
		{Key: "speech_voices_hash", Value: identity.SpeechVoicesHash},
		{Key: "83eb055", Value: identity.Hash83eb055},
		{Key: "4ca87df3d1", Value: "Ow=="},
		{Key: "867e25e5d4", Value: "Ow=="},
		{Key: "d4a306884c", Value: "Ow=="},
	}...)
}
