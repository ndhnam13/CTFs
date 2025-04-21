import asyncio
import struct
import websockets
import binascii

async def extract_flag():
    server_url = "wss://spacegame.io:443"
    
    try:
        # Connect to the server
        websocket = await websockets.connect(server_url)
        print(f"Connected to {server_url}")
        
        # Send SIGN_UP message
        await send_signup(websocket)
        
        # Process server responses
        flag_parts = []
        raw_data = bytearray()
        
        while True:
            message = await websocket.recv()
            
            if len(message) < 12:  # Minimum header size
                continue
                
            header = message[:12]
            signature, msg_type, padding, payload_length = struct.unpack(">4sHHI", header)
            
            if signature != b"SPGM":
                continue
                
            payload = message[12:]
            
            # Store raw data for manual inspection
            raw_data.extend(payload)
            
            # Check for PLAYER_LOC messages (type 3)
            if msg_type == 3:  # PLAYER_LOC
                print(f"\nReceived PLAYER_LOC message, payload length: {len(payload)}")
                print(f"Raw payload: {binascii.hexlify(payload)}")
                
                # Try to find all text in the payload
                for i in range(len(payload) - 4):
                    if is_printable_ascii(payload[i:i+4]):
                        potential_text = extract_text(payload, i)
                        if len(potential_text) > 3:
                            print(f"Found text at offset {i}: {potential_text}")
                            if "CTF" in potential_text or "flag" in potential_text.lower():
                                flag_parts.append(potential_text)
                
                # Search for the flag format specifically
                flag = extract_flag_from_payload(payload)
                if flag:
                    print(f"\nFound flag: {flag}")
                    return flag
            
            # After processing a few messages, try to assemble the flag
            if len(flag_parts) > 0:
                assembled_flag = assemble_flag(flag_parts)
                if assembled_flag:
                    print(f"\nAssembled flag: {assembled_flag}")
                    return assembled_flag
                
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Try to extract flag from all raw data if we haven't found it yet
        print("\nAttempting to extract flag from all raw data...")
        for i in range(len(raw_data) - 7):
            if raw_data[i:i+7] == b'DawgCTF' or raw_data[i:i+7] == b'dawgCTF':
                potential_flag = extract_text(raw_data, i)
                if '}' in potential_flag:
                    potential_flag = potential_flag[:potential_flag.index('}')+1]
                    print(f"Found potential complete flag: {potential_flag}")
                    return potential_flag

async def send_signup(websocket):
    """Send a SIGN_UP message to the server"""
    # Header: "SPGM" signature, type 0 (SIGN_UP), padding 0, payload length
    color = (255, 0, 0)  # Red color
    player_name = "FlagExtractor"
    name_bytes = player_name.encode('ascii')
    name_size = len(name_bytes)
    
    # Construct the payload
    payload = struct.pack(f">BBBBHs", 
                         color[0], color[1], color[2],  # RGB color
                         0,                            # Padding
                         name_size,                    # Name length
                         name_bytes)                   # Name
    
    # Construct the header
    header = struct.pack(">4sHHI", 
                        b"SPGM",                     # Signature
                        0,                           # Type (SIGN_UP)
                        0,                           # Padding
                        len(payload))                # Payload length
    
    # Send the message
    await websocket.send(header + payload)
    print(f"Sent signup message for player: {player_name}")

def is_printable_ascii(data):
    """Check if the data contains printable ASCII characters"""
    try:
        for byte in data:
            if byte < 32 or byte > 126:
                return False
        return True
    except:
        return False

def extract_text(data, start_pos):
    """Extract text starting at the given position until non-printable character"""
    result = ""
    i = start_pos
    
    while i < len(data) and 32 <= data[i] <= 126:
        result += chr(data[i])
        i += 1
        
    return result

def extract_flag_from_payload(payload):
    """Try to extract the flag from the payload"""
    # Convert to bytes if it's not already
    if not isinstance(payload, (bytes, bytearray)):
        return None
    
    # Look for flag pattern DawgCTF{...}
    flag = None
    payload_str = payload.decode('ascii', errors='ignore')
    
    # Check for flag format
    if "DawgCTF{" in payload_str:
        start = payload_str.find("DawgCTF{")
        if start >= 0:
            end = payload_str.find("}", start)
            if end >= 0:
                flag = payload_str[start:end+1]
    
    return flag

def assemble_flag(flag_parts):
    """Try to assemble complete flag from parts"""
    # Join all parts and search for the flag pattern
    joined = "".join(flag_parts)
    
    if "DawgCTF{" in joined:
        start = joined.find("DawgCTF{")
        if start >= 0:
            # Find the closing brace
            end = joined.find("}", start)
            if end >= 0:
                return joined[start:end+1]
    
    # If we have "DawgCTF{" but no closing brace, try to piece together a flag
    for part in flag_parts:
        if "DawgCTF{" in part:
            start_part = part
            
            # Find complement parts
            for other in flag_parts:
                if other != part and "}" in other:
                    # Try to combine the parts
                    start_idx = start_part.find("DawgCTF{")
                    end_idx = other.find("}") + 1
                    
                    # Simple case: just join them
                    potential_flag = start_part[start_idx:] + other[:end_idx]
                    if potential_flag.count("{") == 1 and potential_flag.count("}") == 1:
                        return potential_flag
    
    return None

if __name__ == "__main__":
    print("Space Game Flag Extractor")
    print("-------------------------")
    flag = asyncio.run(extract_flag())
    
    if flag:
        print(f"\nExtracted flag: {flag}")
    else:
        print("\nCould not extract the complete flag automatically.")