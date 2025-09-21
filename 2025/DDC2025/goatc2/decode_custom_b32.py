#!/usr/bin/env python3
import argparse, base64, re
from pathlib import Path

CONST = 0xA0761D6478BD642F

def rol64(x: int, r: int) -> int:
    x &= (1<<64)-1
    return ((x << r) & ((1<<64)-1)) | (x >> (64-r))

def init_b32_alphabet() -> str:
    # Start from RFC4648 A..Z + 2..7
    arr = [ord('A') + i for i in range(26)] + [ord('2') + i for i in range(6)]
    # Seed per decompiled logic (watch operator precedence/grouping)
    v6 = rol64(rol64(0xC2B2AE3D27D4EB4F, 17) ^ 0x73FCD03E1A095D1A, 35)
    S  = ((v6 ^ CONST) << 13) & ((1<<64)-1)
    tmp = (S ^ v6 ^ CONST) & ((1<<64)-1)
    v7 = ((tmp >> 7) ^ S ^ v6) & ((1<<64)-1)
    v8 = (((v7 ^ CONST) << 17) ^ v7 ^ CONST) & ((1<<64)-1)
    if v8 == 0:
        v8 = 0xD1B54A32D192ED03
    state = v8
    # Fisher-Yates with the xorshift-ish PRNG
    for i in range(31, 0, -1):
        t = ((state << 13) ^ state) & ((1<<64)-1)
        t ^= (t >> 7)
        state = (t ^ (t << 17)) & ((1<<64)-1)
        if state == 0:
            state = 0x2545F4914F6CDD1D
        j = int(state % (i + 1))
        arr[i], arr[j] = arr[j], arr[i]
    return "".join(chr(c) for c in arr)

def decode_custom_b32(b32_text: str, alphabet: str) -> bytes:
    RFC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    # Build translation map custom->RFC (accept lowercase too)
    trans_map = {a: r for a, r in zip(alphabet, RFC)}
    trans_map.update({a.lower(): r for a, r in zip(alphabet, RFC)})
    mapped = re.sub(r'[\s=]', '', b32_text).translate(str.maketrans(trans_map)).upper()
    # pad to multiple of 8
    mapped += "=" * ((8 - (len(mapped) % 8)) % 8)
    return base64.b32decode(mapped, casefold=True)

def main():
    ap = argparse.ArgumentParser(description="Derive custom Base32 alphabet, decode input b32 file, write backup.zip")
    ap.add_argument("--in", dest="infile", default="recovered.b32.txt", help="Input Base32 text file (default: recovered.b32.txt)")
    ap.add_argument("--out", dest="outfile", default="backup.zip", help="Output file path (default: backup.zip)")
    args = ap.parse_args()

    in_path = Path(args.infile)
    out_path = Path(args.outfile)

    if not in_path.exists():
        raise SystemExit(f"Input file not found: {in_path}")

    b32_text = in_path.read_text(encoding="utf-8", errors="ignore")
    alphabet = init_b32_alphabet()
    data = decode_custom_b32(b32_text, alphabet)

    out_path.write_bytes(data)
    print("Alphabet:", alphabet)
    print(f"Wrote {len(data)} bytes to {out_path}")

if __name__ == "__main__":
    main()
