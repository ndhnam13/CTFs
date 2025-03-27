import base64

def rc4(key: bytes, data: bytes) -> bytes:
    """RC4 decryption implementation."""
    S = list(range(256))
    j = 0
    out = bytearray()
    
    # Key-scheduling algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    # Pseudo-random generation algorithm (PRGA)
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(byte ^ S[(S[i] + S[j]) % 256])
    
    return bytes(out)

# The RC4 key (Replace with the actual key used for encryption)
key = bytes([
    168, 115, 174, 213, 168, 222, 72, 36, 91, 209, 242, 128, 69, 99, 195, 164,
    238, 182, 67, 92, 7, 121, 164, 86, 121, 10, 93, 4, 140, 111, 248, 44,
    30, 94, 48, 54, 45, 100, 184, 54, 28, 82, 201, 188, 203, 150, 123, 163,
    229, 138, 177, 51, 164, 232, 86, 154, 179, 143, 144, 22, 134, 12, 40, 243,
    55, 2, 73, 103, 99, 243, 236, 119, 9, 120, 247, 25, 132, 137, 67, 66,
    111, 240, 108, 86, 85, 63, 44, 49, 241, 6, 3, 170, 131, 150, 53, 49,
    126, 72, 60, 36, 144, 248, 55, 10, 241, 208, 163, 217, 49, 154, 206, 227,
    25, 99, 18, 144, 134, 169, 237, 100, 117, 22, 11, 150, 157, 230, 173, 38,
    72, 99, 129, 30, 220, 112, 226, 56, 16, 114, 133, 22, 96, 1, 90, 72,
    162, 38, 143, 186, 35, 142, 128, 234, 196, 239, 134, 178, 205, 229, 121, 225,
    246, 232, 205, 236, 254, 152, 145, 98, 126, 29, 217, 74, 177, 142, 19, 190,
    182, 151, 233, 157, 76, 74, 104, 155, 79, 115, 5, 18, 204, 65, 254, 204,
    118, 71, 92, 33, 58, 112, 206, 151, 103, 179, 24, 164, 219, 98, 81, 6,
    241, 100, 228, 190, 96, 140, 128, 1, 161, 246, 236, 25, 62, 100, 87, 145,
    185, 45, 61, 143, 52, 8, 227, 32, 233, 37, 183, 101, 89, 24, 125, 203,
    227, 9, 146, 156, 208, 206, 194, 134, 194, 23, 233, 100, 38, 158, 58, 159
])

# Example encrypted data (Replace with actual encrypted base64 string)
encrypted_base64 = "VGiPTdHXQGP876EbMX2FJhm3ZazpvA8aO8jT1uC8xPhDZq/Np5oZQnHUpKxc36FHBznusaFRsSPtnJzlC4qyGNxcWMCIs1qdVzygFbDj0se4vntsvpU9rKvQPLcPERIjLB36+ws5PVmzVsnuxNmgUPegSj+VPrRfrcHkaE0VL2hOwFIfT8iFNsaVDmnmTwc4DwNxqVqvTfOSr5YCFzLYZhlGMKbBYwhRks/IUuS31pSyoY02zA2T/8MtRORCihusuiBB6lfwkOSDyvxAAS2eTNoqirpJX4oJpFo3HRzFiGt7Tf/hYDvgs4HhXNNUHiBTgR/ckAwJHX0PoBDbTYvxQCtWNytjzQFjF8ir6ihZqFEEUibY3Enkx73tO7zgG5MDXHNRxF6dk7NdM6hcR3RNywIGvr09k/HumgOhs6MgvrHuNauqVWR5t0N52Pf21A6gTNGVtkRfBdnH/vMwOY7egIIxRNR7BlDnaeBlOfmE4aPu5C7BjLhQkwQUcC2mtMa0Sy7vtm+oqIn5po/BFqKsfdreOrYrX3XZ+98F1KC+RVKLPH9pBKd0kH9jHbAMY19YPKl5dok4ls491gXmpv+tb9aPq6PAPkHtAj0ftml7fg=="
encrypted_data = base64.b64decode(encrypted_base64)

# Decrypt the data
decrypted_data = rc4(key, encrypted_data)
decrypted_text = decrypted_data.decode(errors='ignore')  # Use UTF-8 or other encoding

print("Decrypted Text:", decrypted_text)