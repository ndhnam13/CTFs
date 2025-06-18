import struct

# Định nghĩa từ decompiled:
elem = [21,23,1,3,14,18,13,0,20,10,6,11,17,2,15,8,9,12,16,4,22,7,5,19]

# S1_table (little-endian 24 byte)
func1_vals = [0x47300FC1F251843E, 0x6C1AB14C445D2D6F, 0x0257CC82AC421251]
S1 = b''.join(struct.pack('<Q', v) for v in func1_vals)

# key2_table
func2_vals = [0x0912EFA6C49BD6BE, 0x6A163B0583444D46, 0x24E61FF4643EA395]
K2 = b''.join(struct.pack('<Q', v) for v in func2_vals)

# expected_table
exp_vals = [0x58C4D6920D33EF5C, 0x77250476F61923AC, 0xF5903C93901FDBD0]
E = b''.join(struct.pack('<Q', v) for v in exp_vals)

# Tính flag bytes
flag = bytearray(24)
for i in range(24):
    flag[i] = S1[elem[i]] ^ K2[i] ^ E[i]

print(flag)           # b'.;,;.{goh3m1an_rh4p50dy}'
print(flag.decode())  # ".;,;.{goh3m1an_rh4p50dy}"
