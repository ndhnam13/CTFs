#!/usr/bin/env python3

import sys

class ICMPPayloadDecoder:
    def __init__(self, xor_key_hex):
        self.xor_key = bytes.fromhex(xor_key_hex.replace(' ', '').replace('\n', ''))
        if len(self.xor_key) != 8:
            raise ValueError("XOR key must be exactly 8 bytes")
        self.fragments = {}

    def decode_fragment_payload(self, payload_hex):
        payload = bytes.fromhex(payload_hex.strip())

        if len(payload) < 8:
            raise ValueError("Payload too short - need at least 8 bytes for fragment header")

        try:
            seq_info = payload[:8].decode('ascii')
            current_frag = int(seq_info[:4])
            total_frags = int(seq_info[4:8])
        except Exception as e:
            raise ValueError(f"Failed to parse fragment header: {e}")

        encrypted_data = payload[8:]  # có thể rỗng hoặc chỉ 1 byte
        self.fragments[current_frag] = encrypted_data

        print(f"Fragment {current_frag}/{total_frags} added ({len(encrypted_data)} bytes)")

        if len(self.fragments) == total_frags:
            return self.assemble_and_decrypt(total_frags)
        return None

    def assemble_and_decrypt(self, total_frags):
        assembled = b''
        for i in range(1, total_frags + 1):
            if i not in self.fragments:
                raise ValueError(f"Missing fragment {i}")
            assembled += self.fragments[i]

        decrypted = self.xor_decrypt(assembled).rstrip(b'\x00')
        try:
            return decrypted.decode('utf-8', errors='replace')
        except:
            return decrypted.hex()

    def xor_decrypt(self, data):
        return bytes([b ^ self.xor_key[i % 8] for i, b in enumerate(data)])

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 icmp_type8_payload_decoder.py <xor_key_hex>")
        sys.exit(1)

    xor_key_hex = sys.argv[1]
    decoder = ICMPPayloadDecoder(xor_key_hex)

    print("ICMP Type 8 Payload Decoder - Interactive Mode")
    print("=" * 50)
    print(f"Using XOR key: {xor_key_hex}")
    print("\nEnter payloads to decode (or 'quit' to exit):\n")

    while True:
        line = input("Payload (hex): ").strip()
        if line.lower() in ['quit', 'exit', 'q']:
            break
        if not line:
            continue
        try:
            result = decoder.decode_fragment_payload(line)
            if result:
                print("\n" + "=" * 40)
                print("Decoded result:")
                print(result)
                print("=" * 40)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()