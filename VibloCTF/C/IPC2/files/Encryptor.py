from PIL import Image
from hashlib import sha256
import random

img = Image.open("IPC_Flag.png")
newimg = Image.new(img.mode, img.size)
pix = newimg.load()
password = open("password.txt", "r").read().encode()
key = bytes(sha256(password).hexdigest().encode())
random.seed(key)

for y in range(img.size[1]):
    for x in range(img.size[0]):
        r, g, b = img.getpixel((x, y))
        if y in range(686, 730) and x in range(450, 1480):
            r ^= random.randint(0,255)
            b ^= random.randint(0,255)
            g ^= random.randint(0,255)
            pix[x, y] = r, g, b
        else:
            pix[x, y] = r, g, b
newimg.save("IPC_FlagENC.png")
            
