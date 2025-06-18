#!/usr/bin/env python3
# solve_fORtran.py
#
# 1) brute‑force seed (0‑255) → tìm seed duy nhất cho 28 byte printable
# 2) in flag
# 3) gợi ý một key 24 ký tự hợp lệ để đưa vào ./fORtran

dword_4020 = [
    0xBF, 0xF3, 0x3B, 0x25, 0xB3, 0x2F, 0x97, 0x1A,
    0xD9, 0xBF, 0xAA, 0xA2, 0xA6, 0x55, 0xC4, 0xCA,
    0x15, 0x90, 0x93, 0x51, 0x8B, 0x34, 0x41, 0x6E,
    0x0B, 0x24, 0xF1, 0xBB
]

def decrypt(seed: int) -> str | None:
    """Trả về chuỗi 28 ký tự nếu seed hợp lệ, ngược lại None."""
    v = seed
    out = []
    for i in range(28):
        v = (v * 4919) & 0xFFFFFFFF
        v ^= 0xDEADBEEF
        c = dword_4020[i] ^ (v & 0xFF)
        if not (32 <= c <= 126):
            return None
        out.append(chr(c))
    return ''.join(out)

def build_key(seed_byte: int) -> str:
    """
    Sinh 1 key **24 printable‑ASCII** sao cho tổng ASCII ≡ seed_byte (mod 256).
    Dùng '{' (123) + 23 lần '!' (33) ⇒ tổng = 123 + 23*33 = 882 = 3·256 + 114.
    """
    return '{' + '!' * 23   # dài đúng 24 và không có khoảng trắng cuối

if __name__ == "__main__":
    for seed in range(256):
        flag = decrypt(seed)
        if flag:
            print(f"[+] Seed tìm được: {seed} (0x{seed:02X})")
            print(f"[+] Flag        : {flag}")
            print(f"[+] Ví dụ key  :", build_key(seed))
            break
