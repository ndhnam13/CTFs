#!/usr/bin/env python3
import sys
import base64
from Crypto.Cipher import AES

def pad_b64(s: str) -> str:
    """Bổ sung “=” để độ dài chuỗi chia hết cho 4."""
    return s + '=' * ((4 - len(s) % 4) % 4)

def modif_bytes_string(instr_b64: str) -> bytes:
    """
    Tương đương C# Convert.FromBase64String + Array.Reverse,
    nhưng có pad thêm '=' nếu cần.
    """
    data = base64.b64decode(pad_b64(instr_b64))
    return data[::-1]

def decrypt_command(cmd_str: str) -> str:
    """
    Giải mã chuỗi sau khi đã bóc prefix "Orange"/"Tangerine".
    Áp dụng chính xác logic của Program.Decrypt().
    """
    # Phân tách prefix
    if cmd_str.startswith('Orange'):
        body = cmd_str[6:]
        use_cbc = True
    elif cmd_str.startswith('Tangerine'):
        body = cmd_str[9:]
        use_cbc = False
    else:
        raise ValueError("Chưa nhận dạng được prefix Orange/Tangerine")

    # Cắt key (44 ký tự), phần giữa, và IV (chúng ta lấy 24 ký tự cuối)
    instr1 = body[:44]
    iv_b64 = body[-24:]           # 24 ký tự base64 (16 bytes sau decode)
    instr2 = body[44:len(body)-24]

    # Lấy byte[]
    key_bytes = modif_bytes_string(instr1)
    iv_bytes  = base64.b64decode(pad_b64(iv_b64))
    ct_bytes  = modif_bytes_string(instr2)

    # Khởi tạo AES
    if use_cbc:
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv_bytes)
        padded = cipher.decrypt(ct_bytes)
        plaintext = padded.rstrip(b'\x00')
    else:
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        padded = cipher.decrypt(ct_bytes)
        pad_len = padded[-1]
        plaintext = padded[:-pad_len]

    return plaintext.decode('utf-8', errors='replace')

def main():
    if len(sys.argv) > 1:
        lines = open(sys.argv[1], 'r', encoding='utf-8').read().splitlines()
    else:
        lines = sys.stdin.read().splitlines()

    for idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line: continue
        try:
            cmd = decrypt_command(line)
            print(f"[{idx:02d}] {cmd}")
        except Exception as e:
            print(f"[{idx:02d}] Lỗi giải mã: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
