from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import sys

# === Cấu hình ===
KEY_ORIGINAL = b'PwnT0p14_s3cr3t_p4rt1t10n'  # 25 bytes
DISK_IMG = 'disk.img'
OUTPUT_FILE = 'decrypted_output.bin'

# === Pad key lên 32 bytes theo logic của chương trình Go ===
def pad_key(key: bytes, desired_length=32) -> bytes:
    if len(key) >= desired_length:
        return key[:desired_length]
    pad_value = len(key)
    return key + bytes([pad_value] * (desired_length - len(key)))

# === Đọc IV + ciphertext từ disk image ===
def read_iv_and_ciphertext(path: str):
    with open(path, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()
    return iv, ciphertext

# === Giải mã bằng AES-256-CBC ===
def decrypt_aes_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_padded = cipher.decrypt(ciphertext)
    try:
        plaintext = unpad(plaintext_padded, AES.block_size)
    except ValueError as e:
        print(f"[!] Unpadding failed: {e}")
        return plaintext_padded  # Trả về dữ liệu chưa unpad
    return plaintext

# === Main ===
def main():
    key = pad_key(KEY_ORIGINAL)
    iv, ciphertext = read_iv_and_ciphertext(DISK_IMG)
    print(f"[+] IV: {iv.hex()}")
    print(f"[+] Ciphertext size: {len(ciphertext)} bytes")

    decrypted = decrypt_aes_cbc(ciphertext, key, iv)
    
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(decrypted)
    
    print(f"[+] Done! Decrypted data saved to: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
