import os
import io
import sys
import json
import struct
import ctypes
import sqlite3
import pathlib
import binascii

from Crypto.Cipher import AES

f = open("decrypted_key", "rb")
key_blob = f.read()

def parse_key_blob(blob_data: bytes) -> dict:
    buffer = io.BytesIO(blob_data)
    result = {}

    header_len = struct.unpack('<I', buffer.read(4))[0]
    result['header'] = buffer.read(header_len)
    content_len = struct.unpack('<I', buffer.read(4))[0]
    assert header_len + content_len + 8 == len(blob_data)

    flag = buffer.read(1)[0]
    result['flag'] = flag

    if flag in (1, 2):
        # [flag|iv|ciphertext|tag] => [1|12|32|16] bytes
        result['iv'] = buffer.read(12)
        result['ciphertext'] = buffer.read(32)
        result['tag'] = buffer.read(16)
    elif flag == 3:
        # [flag|encrypted_aes_key|iv|ciphertext|tag] => [1|32|12|32|16] bytes
        result['encrypted_aes_key'] = buffer.read(32)
        result['iv'] = buffer.read(12)
        result['ciphertext'] = buffer.read(32)
        result['tag'] = buffer.read(16)
    else:
        raise ValueError(f"Unsupported flag: {flag}")

    return result

def derive_v20_master_key(parsed_data: dict) -> bytes:
    if parsed_data['flag'] == 3:
        xor_key = bytes.fromhex("CCF8A1CEC56605B8517552BA1A2D061C03A29E90274FB2FCF59BA4B75C392390")
        decrypted_aes_key = bytes.fromhex("7db0346181bb695b4d6d627729d3bf6e0cddcb4968dd8d32ae221f9504d9bf92")
        xored_aes_key = bytearray(a ^ b for a, b in zip(decrypted_aes_key, xor_key))
        cipher = AES.new(xored_aes_key, AES.MODE_GCM, nonce=parsed_data['iv'])

    return cipher.decrypt_and_verify(parsed_data['ciphertext'], parsed_data['tag'])
    
enc_key = parse_key_blob(key_blob)
v20_master_key = derive_v20_master_key(enc_key)
print(f"---------- V20 MASTER KEY ----------\n{v20_master_key.hex()}")

def decrypt_cookie_v20(encrypted_value):
        cookie_iv = encrypted_value[3:3+12]
        encrypted_cookie = encrypted_value[3+12:-16]
        cookie_tag = encrypted_value[-16:]
        cookie_cipher = AES.new(v20_master_key, AES.MODE_GCM, nonce=cookie_iv)
        decrypted_cookie = cookie_cipher.decrypt_and_verify(encrypted_cookie, cookie_tag)
        return decrypted_cookie[32:].decode('utf-8')

cookie_db_path = "Cookies"
abs_cookie_db_path = pathlib.Path(cookie_db_path).resolve()
con = sqlite3.connect(abs_cookie_db_path.as_uri() + "?mode=ro", uri=True)
cur = con.cursor()
r = cur.execute("SELECT host_key, name, CAST(encrypted_value AS BLOB) from cookies;")
cookies = cur.fetchall()
cookies_v20 = [c for c in cookies if c[2][:3] == b"v20"]
con.close()

print("\n---------- DECRYPTED DATA ----------\n")
for c in cookies_v20:
        print(c[0], c[1], decrypt_cookie_v20(c[2]))