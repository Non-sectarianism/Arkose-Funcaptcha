import sys
p = "/root/arkose-solver/arkose/encryption.go"
s = open(p).read()
if "ENCVARIANT" in s:
    print("already patched"); sys.exit(0)

old_key = '''	key := make([]byte, 32)
	if _, err := rand.Read(key); err != nil {
		return "", fmt.Errorf("rand key: %w", err)
	}'''
assert old_key in s, "key anchor"
new_key = '''	// The VM's envelope is confirmed identical to ours (caasgs trap: ct = plaintext
	// length, tag 16 B, iv 12 B, rsa-wrapped key 256 B, assembled iv|tag|key|ct).
	// The only unobservable choices left are the AES key size and the OAEP hash;
	// a wrong pick makes Arkose's decrypt fail, which presents as "no BDA" and the
	// worst tier (waves=10 extendedshadows) while everything else still works.
	// ENCVARIANT: oaep256-aes256 (default) | oaep1-aes256 | oaep256-aes128 | oaep1-aes128
	variant := os.Getenv("ENCVARIANT")
	keyLen := 32
	if strings.HasSuffix(variant, "aes128") {
		keyLen = 16
	}
	key := make([]byte, keyLen)
	if _, err := rand.Read(key); err != nil {
		return "", fmt.Errorf("rand key: %w", err)
	}'''
s = s.replace(old_key, new_key, 1)

old_oaep = '''	encryptedKey, err := rsa.EncryptOAEP(sha256.New(), rand.Reader, rsaPub, key, nil)
	if err != nil {
		return "", fmt.Errorf("rsa oaep: %w", err)
	}'''
assert old_oaep in s, "oaep anchor"
new_oaep = '''	oaepHash := crypto.Hash(crypto.SHA256).New()
	if strings.HasPrefix(variant, "oaep1-") {
		oaepHash = sha1.New()
	}
	encryptedKey, err := rsa.EncryptOAEP(oaepHash, rand.Reader, rsaPub, key, nil)
	if err != nil {
		return "", fmt.Errorf("rsa oaep: %w", err)
	}
	if variant != "" {
		fmt.Printf("ENCVARIANT=%s aeskey=%dB\\n", variant, keyLen)
	}'''
s = s.replace(old_oaep, new_oaep, 1)

for imp in ('"crypto"', '"crypto/sha1"', '"os"', '"strings"'):
    if "\n\t" + imp not in s:
        s = s.replace("import (", "import (\n\t" + imp, 1)
open(p, "w").write(s)
print("patched OK")
