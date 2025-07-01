from base64 import b64decode
from Crypto.Cipher import AES

# AES key giống như mã Java đã phân tích
AES_KEY = b'vuvtuYXvHYvW"#vu'  # 16 bytes

def decrypt_base64_aes(base64_str):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    encrypted_bytes = b64decode(base64_str)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)

    # Remove potential padding (PKCS7)
    pad_len = decrypted_bytes[-1]
    if all(b == pad_len for b in decrypted_bytes[-pad_len:]):
        decrypted_bytes = decrypted_bytes[:-pad_len]

    return decrypted_bytes.decode(errors='ignore')

def main():
    with open("data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                plaintext = decrypt_base64_aes(line)
                print("[+] Decrypted:", plaintext)
            except Exception as e:
                print("[-] Failed to decrypt:", line)
                print("    Reason:", e)

if __name__ == "__main__":
    main()
