package arkose

import (
	"strings"
	"os"
	"crypto/sha1"
	"crypto/aes"
	"crypto/cipher"
	"crypto/md5"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
)

func Encrypt(content string, pubkeyB64 string) (string, error) {
	// The VM's envelope is confirmed identical to ours (caasgs trap: ct = plaintext
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
	}
	iv := make([]byte, 12)
	if _, err := rand.Read(iv); err != nil {
		return "", fmt.Errorf("rand iv: %w", err)
	}

	block, err := aes.NewCipher(key)
	if err != nil {
		return "", fmt.Errorf("aes cipher: %w", err)
	}

	aesgcm, err := cipher.NewGCMWithNonceSize(block, 12)
	if err != nil {
		return "", fmt.Errorf("gcm: %w", err)
	}
	sealed := aesgcm.Seal(nil, iv, []byte(content), nil)

	if len(sealed) < 16 {
		return "", errors.New("gcm sealed too short")
	}
	ciphertext := sealed[:len(sealed)-16]
	tag := sealed[len(sealed)-16:]

	pubDER, err := base64.StdEncoding.DecodeString(pubkeyB64)
	if err != nil {
		return "", fmt.Errorf("pubkey b64: %w", err)
	}
	pubKeyIfc, err := x509.ParsePKIXPublicKey(pubDER)
	if err != nil {
		return "", fmt.Errorf("parse SPKI: %w", err)
	}
	rsaPub, ok := pubKeyIfc.(*rsa.PublicKey)
	if !ok {
		return "", errors.New("pubkey not RSA")
	}
	oaepHash := sha256.New()
	if strings.HasPrefix(variant, "oaep1-") {
		oaepHash = sha1.New()
	}
	encryptedKey, err := rsa.EncryptOAEP(oaepHash, rand.Reader, rsaPub, key, nil)
	if err != nil {
		return "", fmt.Errorf("rsa oaep: %w", err)
	}
	if variant != "" {
		fmt.Printf("ENCVARIANT=%s aeskey=%dB\n", variant, keyLen)
	}

	b64 := base64.StdEncoding.EncodeToString
	return b64(iv) + b64(tag) + b64(encryptedKey) + b64(ciphertext), nil
}

func genKeyGo(userAgent, xArkValue, sValueHex string) ([]byte, error) {
	transformed, err := hex.DecodeString(sValueHex)
	if err != nil {
		return nil, err
	}
	u := append([]byte(userAgent+xArkValue), transformed...)

	s := make([][]byte, 3)
	h := md5.Sum(u)
	s[0] = h[:]
	f := make([]byte, 0, 48)
	f = append(f, s[0]...)
	for l := 1; l < 3; l++ {
		combined := append(append([]byte{}, s[l-1]...), u...)
		h := md5.Sum(combined)
		s[l] = h[:]
		f = append(f, s[l]...)
	}
	return f[:32], nil
}

func EncryptAES(data, userAgent, xArkValue string) (string, error) {
	sBytes := make([]byte, 8)
	if _, err := rand.Read(sBytes); err != nil {
		return "", err
	}
	sHex := hex.EncodeToString(sBytes)

	iv := make([]byte, 16)
	if _, err := rand.Read(iv); err != nil {
		return "", err
	}

	key, err := genKeyGo(userAgent, xArkValue, sHex)
	if err != nil {
		return "", err
	}

	block, err := aes.NewCipher(key)
	if err != nil {
		return "", err
	}

	padded := pkcs7Pad([]byte(data), 16)
	ct := make([]byte, len(padded))
	mode := cipher.NewCBCEncrypter(block, iv)
	mode.CryptBlocks(ct, padded)

	type payload struct {
		Ct string `json:"ct"`
		S  string `json:"s"`
		Iv string `json:"iv"`
	}
	buf, err := json.Marshal(payload{
		Ct: base64.StdEncoding.EncodeToString(ct),
		S:  sHex,
		Iv: hex.EncodeToString(iv),
	})
	if err != nil {
		return "", err
	}
	return string(buf), nil
}

func pkcs7Pad(data []byte, blockSize int) []byte {
	pad := blockSize - (len(data) % blockSize)
	if pad == 0 {
		pad = blockSize
	}
	out := make([]byte, len(data)+pad)
	copy(out, data)
	for i := len(data); i < len(out); i++ {
		out[i] = byte(pad)
	}
	return out
}
