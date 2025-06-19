def rc4_crypt(key: bytes, data: bytes) -> bytes:
    S = list(range(256))
    j = 0
    out = []

    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        out.append(byte ^ K)

    return bytes(out)


# Static key from binary
key = bytes([
    0x79, 0xE1, 0x0A, 0x5D, 0x87, 0x7D, 0x9F, 0x46,
    0x49, 0x41, 0x2E, 0x11, 0x65, 0xAC, 0xE3, 0x25
])

# Encrypted hex strings (each line from data.txt)
hex_lines = [
    "b3cc4f",
    "ecd34463f5800cb582fe7045725d733c8ad62a1d1cc08743",
    "b4d3446ffdc6",
    "b7c9427efcca0ccd",
    "aadf",
    "b6d24f33a19f48f7c3fa6e49761e5227d498211b1999c57965e826af94cc15ca66e255e1413513f9a7d2e76085252043ca55ba8d91afa48d5df69da1bac8492ef77dcc51c300d214179539a2569e4458c2c764850ff9f329223caf8f371b5c122a2c4fd5f3deae511e626e8342a67f0111dc53afc1a8d56d47bc2331c421e9bac67f95e596f6f4d89887520a88cb09a646896aee5a0a1d1c1597e34cf5fb4204b76ff91cb6b62c8bbb7c8301b6055eb6362213f6e564054c511bd144867dacbb38c0ba3def74055e8ebf78dd286d24e6487678f5deef",
    "a6d84361b0e92d948eed67463219040ca9f4152d4cd7ab3a65b53daf8e940bc15cf40eb4532f14e4aa",
    "85ee786bf3d41ef380bd43744a2168628ee735421097802164b6698484d710d36bfe14bc2c",
    "a6d84361b08d01a89eae74417017173198dd28520dd39a2c31f86ca2c6c70ad47ab45cff06370be2b2c5f425cd61",
    "ebf5442ec2ca0cb299e0352a06",
]

# Decrypt each line
decrypted_lines = []
for hex_str in hex_lines:
    ciphertext = bytes.fromhex(hex_str)
    plaintext = rc4_crypt(key, ciphertext)
    decrypted_lines.append(plaintext.decode(errors="replace"))  # replace undecodable chars

for line in decrypted_lines:
    print(line)