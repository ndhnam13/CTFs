from PIL import Image
from hashlib import sha256
import random

# 1. Tính key
password = open("password.txt", "rb").read()
key = bytes(sha256(password).hexdigest().encode())

# 2. Chuyển key thành int và seed
seed_int = int.from_bytes(key, byteorder='big')
random.seed(seed_int)

# 3. Mở ảnh encrypted
enc = Image.open("IPC_FlagENC.png")
dec = Image.new(enc.mode, enc.size)
pix_enc = enc.load()
pix_dec = dec.load()

# 4. Vùng bị xáo
x0, x1 = 450, 1480
y0, y1 = 686, 730

for y in range(enc.height):
    for x in range(enc.width):
        r, g, b = pix_enc[x, y]
        if x0 <= x < x1 and y0 <= y < y1:
            r ^= random.randint(0, 255)
            b ^= random.randint(0, 255)
            g ^= random.randint(0, 255)
        pix_dec[x, y] = (r, g, b)

dec.save("IPC_Flag_DEC.png")
print("Recovered saved as IPC_Flag_DEC.png")
