import wave

def extract_lsb(wav_file):
    with wave.open(wav_file, mode='rb') as wav:
        frames = wav.readframes(wav.getnframes())

    bits = []
    for byte in frames:
        bits.append(byte & 1)

    chars = []
    for b in range(0, len(bits), 8):
        byte = bits[b:b+8]
        if len(byte) == 8:
            value = 0
            for bit in byte:
                value = (value << 1) | bit
            chars.append(value)

    extracted = bytes(chars)
    return extracted

if __name__ == "__main__":
    wav_file = "h4ck3r_h1n7.wav"
    output = extract_lsb(wav_file)

    try:
        text = output.decode('utf-8')
        print("[+] Extracted Text:")
        print(text)
    except UnicodeDecodeError:
        print("[+] Extracted Raw Bytes (not UTF-8):")
        print(output)