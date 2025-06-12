#!/usr/bin/env python3
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class RandomGenerator:
    def __init__(self, seed=None, modulus=2**32, multiplier=157, increment=1):
        if seed is None: 
            seed = time.asctime()
        if type(seed) is int: 
            self.seed = seed
        if type(seed) is str: 
            self.seed = int.from_bytes(seed.encode(), "big")
        if type(seed) is bytes: 
            self.seed = int.from_bytes(seed, "big")
        self.m = modulus
        self.a = multiplier
        self.c = increment
    
    def randint(self, bits: int):
        self.seed = (self.a * self.seed + self.c) % self.m
        result = self.seed.to_bytes(4, "big")
        while len(result) < bits // 8:
            self.seed = (self.a * self.seed + self.c) % self.m
            result += self.seed.to_bytes(4, "big")
        return int.from_bytes(result, "big") % (2 ** bits)
    
    def randbytes(self, length: int):
        return self.randint(length * 8).to_bytes(length, "big")

def find_seed_with_known_plaintext(known_plaintext, known_ciphertext, approximate_time):
    """
    Find the seed by trying to match a known plaintext->ciphertext pair
    """
    print(f"Looking for seed that produces ciphertext: {known_ciphertext.hex()}")
    print(f"When encrypting plaintext: {known_plaintext}")
    
    for time_offset in range(-300, 301):  # Try ±5 minutes
        test_time = approximate_time + time_offset
        time_str = time.asctime(time.localtime(test_time))
        
        try:
            # Create RNG with this time seed
            randgen = RandomGenerator(seed=time_str)
            
            # Skip the flag key (first key generated)
            randgen.randbytes(32)
            
            # Get the second key (used for our plaintext)
            our_key = randgen.randbytes(32)
            
            # Try to encrypt our known plaintext with this key
            cipher = AES.new(our_key, AES.MODE_ECB)
            test_ciphertext = cipher.encrypt(pad(known_plaintext, AES.block_size))
            
            if test_ciphertext == known_ciphertext:
                print(f"FOUND SEED! Time string: {time_str}")
                
                # Now decrypt the flag using the first key
                flag_randgen = RandomGenerator(seed=time_str)
                flag_key = flag_randgen.randbytes(32)
                
                return time_str, flag_key
                
        except Exception as e:
            continue
    
    print("Could not find matching seed")
    return None, None

# Quick attack - you'll need to fill in the known plaintext/ciphertext
if __name__ == "__main__":
    flag_ciphertext = b'I<B\x8f7\x1a\x9d\xba\xcb=Dz8\x97\xe9c\xb7\xaf\x15\x01\xf4\xd9\xd9\xc2\x83jm\x1a\xa2\xda\x10\xb5'
    
    print("Quick Oracle Attack")
    print("=" * 30)
    print("1. Send 'hello' to the oracle and copy the ciphertext")
    print("2. Update the variables below with the actual values")
    print()
    
    # Actual values from the oracle:
    known_plaintext = b"hello"  # What you sent to oracle
    known_ciphertext = b'\xaf\xe6\xc1\x15,\x95,\x85\x15\xfc\\g\x08\xc96\xf0'  # What the oracle returned
    approximate_time = int(time.time())  # Current time
    
    if known_ciphertext != b"UPDATE_THIS":
        time_str, flag_key = find_seed_with_known_plaintext(
            known_plaintext, known_ciphertext, approximate_time
        )
        
        if flag_key:
            # Decrypt the flag
            cipher = AES.new(flag_key, AES.MODE_ECB)
            decrypted = cipher.decrypt(flag_ciphertext)
            flag = unpad(decrypted, AES.block_size)
            print(f"FLAG: {flag.decode('ascii')}")
        else:
            print("Attack failed")
    else:
        print("Please update known_ciphertext with the actual value from the oracle")