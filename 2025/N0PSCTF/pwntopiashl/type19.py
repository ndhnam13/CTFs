#!/usr/bin/env python3
"""
ICMP Type 19 Code 42 Payload Decoder
Decodes XOR-encrypted payloads using provided key
"""

import sys
import binascii

def decode_payload(payload_hex, xor_key_hex):
    """
    Decode XOR-encrypted payload using 8-byte repeating key
    
    Args:
        payload_hex: Hex string of encrypted payload
        xor_key_hex: Hex string of 8-byte XOR key
    
    Returns:
        Decoded payload as string
    """
    # Convert hex strings to bytes
    try:
        payload = bytes.fromhex(payload_hex.replace(' ', '').replace('\n', ''))
        xor_key = bytes.fromhex(xor_key_hex.replace(' ', '').replace('\n', ''))
    except ValueError as e:
        raise ValueError(f"Invalid hex input: {e}")
    
    if len(xor_key) != 8:
        raise ValueError(f"XOR key must be 8 bytes, got {len(xor_key)} bytes")
    
    # XOR decode with repeating 8-byte key
    decoded = bytearray()
    for i, byte in enumerate(payload):
        key_byte = xor_key[i % 8]  # Use modulo for repeating key
        decoded.append(byte ^ key_byte)
    
    # Convert to string, handling null bytes and non-printable characters
    try:
        # Remove trailing null bytes
        decoded = decoded.rstrip(b'\x00')
        result = decoded.decode('utf-8', errors='replace')
        return result
    except:
        # If decoding fails, return as hex
        return decoded.hex()

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 icmp_decoder.py <payload_hex> <xor_key_hex>")
        print("Example: python3 icmp_decoder.py 'deadbeef...' 'da0adee0d03e04ea'")
        sys.exit(1)
    
    payload_hex = sys.argv[1]
    xor_key_hex = sys.argv[2]
    
    try:
        decoded = decode_payload(payload_hex, xor_key_hex)
        print("Decoded payload:")
        print(decoded)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def interactive_decode():
    """Interactive mode for decoding multiple payloads"""
    print("ICMP Type 19 Payload Decoder - Interactive Mode")
    print("=" * 50)
    
    # Get XOR key once
    while True:
        xor_key_hex = input("Enter 8-byte XOR key (hex): ").strip()
        try:
            xor_key = bytes.fromhex(xor_key_hex.replace(' ', ''))
            if len(xor_key) == 8:
                break
            else:
                print(f"Key must be 8 bytes, got {len(xor_key)} bytes")
        except ValueError:
            print("Invalid hex format")
    
    print(f"Using XOR key: {xor_key.hex()}")
    print("\nEnter payloads to decode (or 'quit' to exit):")
    
    while True:
        payload_hex = input("\nPayload (hex): ").strip()
        
        if payload_hex.lower() in ['quit', 'exit', 'q']:
            break
            
        if not payload_hex:
            continue
            
        try:
            decoded = decode_payload(payload_hex, xor_key_hex)
            print(f"Decoded: {decoded}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        interactive_decode()
    else:
        main()