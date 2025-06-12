from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random, itertools, binascii

def det_bytes():
    r = random.Random(42)
    k1 = r.randbytes(8)
    choices = list(r.randbytes(6))
    return k1, choices[:4]

pt   = b"example"
pt_p = pad(pt, 16)
ct1, ct_flag = bytes.fromhex("7125383e330c692c75e0ee0886ec7779"), \
               bytes.fromhex("9ecba853742db726fb39e748a0c5cfd06b682c8f15be13bc8ba2b2304897eca2")

k1, CH = det_bytes(); k3 = k1
# báº£ng tra trung gian
tbl = {}
for idx in itertools.product(range(4), repeat=8):
    k2 = bytes(CH[i] for i in idx)
    c1 = AES.new(k1+k2, AES.MODE_ECB).encrypt(pt_p)
    tbl[c1] = k2

for idx in itertools.product(range(4), repeat=8):
    k4 = bytes(CH[i] for i in idx)
    c1p = AES.new(k4+k3, AES.MODE_ECB).decrypt(ct1)
    if c1p in tbl:
        k2 = tbl[c1p]
        flag = unpad(
            AES.new(k1+k2,AES.MODE_ECB).decrypt(
                AES.new(k4+k3,AES.MODE_ECB).decrypt(ct_flag)
            ),
            16
        )
        print(flag.decode())
        break