#!/usr/bin/env python3
import re, sys, json, zlib, base64, hashlib, string
from Crypto.Cipher import AES

DATA_TXT  = "data.txt"
CONFIG    = "config.json"

# Find key
with open(CONFIG, 'r') as f:
    cfg = json.load(f)
AES_KEY = cfg.get("AES_KEY")
if not AES_KEY:
    print("AES_KEY not found in config.js"); sys.exit(1)

chunks = {}
JOBID = None

# hex and b64 diff
hex_re = re.compile(r'^[0-9a-fA-F]+$')
b64_re = re.compile(r'^[A-Za-z0-9+/=]+$')

def normalize_line(line):
    """
    Custom decoding
    ICMP: hex str → bytes → Base64-decode → raw
    HTTP: Base64 str → raw
    """
    icmp_hex, http_b64 = line.rstrip("\n").split("\t")
    if icmp_hex:
        # data.data (icmp)
        if not hex_re.match(icmp_hex):
            raise ValueError(f"ICMP chunk not hex: {icmp_hex[:30]}")
        b64bytes = bytes.fromhex(icmp_hex)
        raw = base64.b64decode(b64bytes)
        return raw

    if http_b64:
        # urlencoded-form.value (b64)
        if not b64_re.match(http_b64):
            raise ValueError(f"HTTP chunk not Base64: {http_b64[:30]}")
        raw = base64.b64decode(http_b64)
        return raw

    return None

def extract_fields(raw):
    parts = raw.split(b"|!|")
    # REGISTER (Ignored)
    if len(parts) == 4 and parts[2] == b"REGISTER":
        return None, None, None
    # DONE
    if len(parts) == 3 and parts[2] == b"DONE":
        jobid = parts[0].decode()
        idx   = int(parts[1])
        return jobid, idx, "DONE"
    # DATA
    if len(parts) == 3:
        jobid   = parts[0].decode()
        idx     = int(parts[1])
        hexchunk= parts[2].decode().strip()
        return jobid, idx, hexchunk

    return None, None, None

# Read file
with open(DATA_TXT, 'r') as f:
    for line in f:
        raw = normalize_line(line)
        if not raw:
            continue
        jobid, idx, chunk = extract_fields(raw)
        if not jobid:
            # REGISTER or unknown format
            continue
        JOBID = jobid
        if chunk == "DONE":
            break
        # Save chunks
        chunks[idx] = chunk

if not chunks:
    print("No chunks"); sys.exit(1)

# Check for missing idx
for idx in list(chunks):
    clean = ''.join(c for c in chunks[idx] if c in string.hexdigits)
    chunks[idx] = clean

max_idx = max(chunks)
missing = set(range(max_idx+1)) - set(chunks)
if missing:
    print(f"Missing indexes: {sorted(missing)}"); sys.exit(1)

# Recover ciphertext
hexdata = "".join(chunks[i] for i in range(max_idx+1))
total_bytes = len(hexdata)//2
if total_bytes % AES.block_size != 0:
    print(f"Ciphertext len: {total_bytes} byte, note divisible by {AES.block_size}"); sys.exit(1)

blob = bytes.fromhex(hexdata)
iv, ct = blob[:16], blob[16:]

# AES-CBC decrypt
key = hashlib.sha256(AES_KEY.encode()).digest()
aes = AES.new(key, AES.MODE_CBC, iv)
padded = aes.decrypt(ct)

# zlib decompress
try:
    data = zlib.decompress(padded)
    print("Decompressed")
except zlib.error:
    data = padded
    print("Decompress failed")

# Write file
outfn = f"{JOBID}-restored.zip"
with open(outfn, 'wb') as f:
    f.write(data)

print(f"Saved to {outfn}")