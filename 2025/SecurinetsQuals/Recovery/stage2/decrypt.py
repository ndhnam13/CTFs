# Decrypt sillyflag.bin using the discovered XOR+LCG scheme.
# We'll try two strategies:
# 1) Exact filename-based keystream (using 'sillyflag.png').
# 2) Fallback: known-plaintext using PNG magic to recover the initial keystream byte.


from pathlib import Path

BIN_PATH = Path("sillyflag_encrypted.png")
OUT_PATH_NAME = Path("sillyflag_from_name.png")
OUT_PATH_KNOWN = Path("sillyflag.png")

png_magic = b"\x89PNG\r\n\x1a\n"

data = BIN_PATH.read_bytes()

# --- Strategy 1: exact filename-based keystream ---
CONST_BYTES = b"evilsecretcodeforevilsecretencryption"

def make_stream_from_name(name: str, n: int) -> bytes:
    # Reproduce sub_401460 exactly
    v3 = 0
    name_bytes = name.encode('utf-8', errors='ignore')
    for i, b in enumerate(name_bytes):
        v3 ^= (b & 0xFF) << (8 * (i & 3))
    for i, b in enumerate(CONST_BYTES[:37]):
        v3 ^= (b & 0xFF) << (8 * (i & 3))
    out = bytearray(n)
    # In the original code, it increments pointer then writes *(result-1) = v3
    # after updating v3. That corresponds to: v3 = LCG(v3); out[i] = lowbyte(v3).
    for i in range(n):
        v3 = (1664525 * v3 + 1013904223) & 0xFFFFFFFF
        out[i] = v3 & 0xFF
    return bytes(out)

def xor_with(data: bytes, ks: bytes) -> bytes:
    return bytes(d ^ k for d, k in zip(data, ks))

# Try with the provided original name only (as user stated)
ks_name = make_stream_from_name("sillyflag.png", len(data))
plain_try = xor_with(data, ks_name)
ok_name = plain_try.startswith(png_magic)

if ok_name:
    OUT_PATH_NAME.write_bytes(plain_try)

# --- Strategy 2: known-plaintext (PNG magic) ---
# For the LCG modulo 2^32, the low byte recurrence is:
# b_{n+1} = (13*b_n + 95) mod 256
# Keystream[i] = b_{i+1}. Therefore, if we know plaintext[0],
# b1 = ciphertext[0] ^ plaintext[0], and keystream[0] = b1.
A = 13
C = 95
b1 = data[0] ^ png_magic[0]
ks = bytearray(len(data))
b = b1
for i in range(len(data)):
    ks[i] = b
    b = (A * b + C) & 0xFF

plain_known = xor_with(data, ks)
ok_known = plain_known.startswith(png_magic)
if ok_known:
    OUT_PATH_KNOWN.write_bytes(plain_known)

print("Input size:", len(data), "bytes")
print("Strategy 1 (name-based) PNG header match:", ok_name, "->", str(OUT_PATH_NAME) if ok_name else "-")
print("Strategy 2 (known-plaintext) PNG header match:", ok_known, "->", str(OUT_PATH_KNOWN) if ok_known else "-")

# If we decrypted successfully, also report the first few bytes for sanity.
def hexdump_prefix(b: bytes, n=32):
    return " ".join(f"{x:02X}" for x in b[:n])

print("Decrypted (name-based) prefix:", hexdump_prefix(plain_try) if ok_name else "(not valid)")
print("Decrypted (known-plaintext) prefix:", hexdump_prefix(plain_known) if ok_known else "(not valid)")


