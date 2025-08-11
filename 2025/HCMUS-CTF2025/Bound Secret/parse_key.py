import os
import io
import sys
import json
import struct
import ctypes
import sqlite3
import pathlib
import binascii

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

if __name__ == "__main__":
    f = open("decrypted_key", "rb")
    key = f.read()

    data = parse_key_blob(key)
    for k, v in data.items():
        if isinstance(v, bytes):
            print(f"{k}: {v.hex()}")
        else:
            print(f"{k}: {v}")