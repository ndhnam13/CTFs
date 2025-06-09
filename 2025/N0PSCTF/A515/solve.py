data = open("BLUE.png", 'rb').read()

header = b""
chunks = []
footer = b""
is_first_idat = True

for i in range(len(data)-4):
    if data[i:i+4] == b"IDAT":
        if is_first_idat:
            is_first_idat = False
            header = header[:-4]
        size = int.from_bytes(data[i-4:i], byteorder="big")
        chunk = data[i-4:i+4+size+4]
        chunks.append(chunk)
    if data[i:i+4] == b"IEND":
        footer = data[i-4:]
    if is_first_idat:
        header += bytes([data[i]])

chunks_order = [11, 12, 10, 14, 16, 15, 17, 18, 8, 13, 9]
#chunks_order = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

for i in range(len(chunks)):
    if not i in chunks_order:
        with open(f"out{i}.png", "wb") as out:
            out.write(header)
            for index in chunks_order:
                out.write(chunks[index])
            out.write(chunks[i])
            out.write(footer)