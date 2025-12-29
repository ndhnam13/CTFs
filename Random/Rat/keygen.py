import hashlib
import struct

key_sent = 0x783a1ced66ea6b638d4b2429f3895ad1cce4b0c0314032470643c1b75d0f154d
key_recv = 0x7067c8be6dcbd867a90007581cfcd6d63f145f40dc6456446036864cf95dc74a

vsn = [0xf1c2471b,
0xa0612028,
0xfc6c6235,
0x6563784a,
0x02a3ff67,
0x9aaa28cd]

a = key_sent.to_bytes(32, 'big')
b = key_recv.to_bytes(32, 'big')

if a < b:
    pHints = a + b
else:
    pHints = b + a

first_round = hashlib.sha256(pHints).digest()

for i in vsn:
    buf = first_round + struct.pack("<I", i)
    key = hashlib.sha256(buf).digest()
    print(key.hex())