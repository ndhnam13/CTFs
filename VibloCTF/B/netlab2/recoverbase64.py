#!/usr/bin/env python3

import re
import os

def extract_base64():
    print("Starting extraction process...")
    input_file = 'susdnsquery.txt'
    
    # Check if input file exists
    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return
    
    # Read the DNS queries
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Extract the first part of each query (before the "-.")
    pattern = r'([A-Za-z0-9+/={}\[\]]+)-\.'
    matches = re.findall(pattern, content)
    
    print(f"Found {len(matches)} matching chunks")
    
    if not matches:
        print("Error: No valid data chunks found!")
        return
    
    # Process each chunk
    processed_chunks = []
    for chunk in matches:
        # Reverse character substitutions
        processed = chunk.replace("{", "/").replace("}", "+")
        processed_chunks.append(processed)
    
    # Combine the chunks into a single base64 string
    combined_base64 = ''.join(processed_chunks)
    print(f"Combined base64 length: {len(combined_base64)}")
    
    # Save base64 to a file for inspection
    with open("base64Goc.txt", 'w') as f:
        f.write(combined_base64)
    
    print("Base64 data saved to 'base64Goc.txt'")

if __name__ == "__main__":
    extract_base64()
