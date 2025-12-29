import binascii
import hashlib
import struct

expected = [0x7DCA862E, 0x1F1D2720]

for serial in range (0, 0xFFFFFFFF): 
	data = struct.pack("<II", serial, serial)
	md5_hash = hashlib.md5(data).digest()
	crc32_hash = binascii.crc32(md5_hash)

	if crc32_hash in expected:
		print(hex(serial))


# results = [0xf1c2471b,0xa0612028,0xfc6c5235,0x6563784a,0x02a3ff67,0x9ac82dcd]
# for i in results:
# 	serial = i
# 	data = struct.pack("<II", serial, serial)
# 	print( hex(binascii.crc32(hashlib.md5(data).digest())) )
# print(hex(serial))