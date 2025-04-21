import asyncio
import struct
import websockets
import random
import binascii

class SpaceGameClient:
    def __init__(self, server_url="wss://spacegame.io:443", player_name="Player", color=(255, 0, 0)):
        self.server_url = server_url
        self.player_name = player_name
        self.color = color  # RGB tuple
        self.player_id = None
        self.map_size = None
        self.websocket = None
        self.players = {}
        self.debug_mode = True
        self.current_sector = None  # Track our current sector
        self.target_sector = (15, 2)  # Target sector to meet the challenge creator
        
        # Message types
        self.MSG_TYPES = {
            "SIGN_UP": 0,
            "SIGN_UP_RESP": 1,
            "CONTROL": 2,
            "PLAYER_LOC": 3,
            "PING": 4,
            "PONG": 6,
            "ERROR": 7
        }
        
        # Reverse lookup for message types (for debugging)
        self.MSG_NAMES = {v: k for k, v in self.MSG_TYPES.items()}
        
        # Key codes (SDL_SCANCODE constants)
        self.KEY_CODES = {
            "RIGHT": 79,
            "LEFT": 80,
            "UP": 82,
            "DOWN": 81
        }
        
        # Currently pressed keys
        self.pressed_keys = set()

    async def connect(self):
        """Connect to the game server and sign up"""
        try:
            self.websocket = await websockets.connect(self.server_url)
            await self.send_signup()
            print(f"Connected to {self.server_url}")
            
            # Start background tasks
            asyncio.create_task(self.message_loop())
            asyncio.create_task(self.control_loop())
            
            # Start navigation to target sector
            asyncio.create_task(self.navigate_to_target())
            
            # Keep the connection open
            while True:
                await asyncio.sleep(1)
                
        except Exception as e:
            print(f"Connection error: {e}")
            if self.websocket:
                await self.websocket.close()
    
    def create_header(self, msg_type, payload_length):
        """Create the message header - using BIG endian as per docs"""
        return struct.pack(">4sHHI", 
                          b"SPGM",                 # Signature
                          msg_type,                # Message type
                          0,                       # Padding
                          payload_length)          # Payload length
    
    async def send_signup(self):
        """Send a SIGN_UP message to the server"""
        r, g, b = self.color
        name_bytes = self.player_name.encode('ascii')
        name_size = len(name_bytes)
        
        # Construct the payload - using BIG endian as per docs
        payload = struct.pack(f">BBBBHs", 
                             r, g, b,            # RGB color
                             0,                  # Padding
                             name_size,          # Name length
                             name_bytes)         # Name
        
        # Add header and send
        header = self.create_header(self.MSG_TYPES["SIGN_UP"], len(payload))
        await self.websocket.send(header + payload)
        print(f"Sent signup message for player: {self.player_name}")
    
    async def send_control(self):
        """Send a CONTROL message with currently pressed keys"""
        if not self.pressed_keys:
            return
            
        keys_list = list(self.pressed_keys)
        num_pressed = len(keys_list)
        
        # Construct the payload - using BIG endian as per docs
        payload = struct.pack(f">H{num_pressed}H", 
                             num_pressed,           # Number of pressed keys
                             *keys_list)            # Key codes
        
        # Add header and send
        header = self.create_header(self.MSG_TYPES["CONTROL"], len(payload))
        await self.websocket.send(header + payload)
    
    def parse_signup_resp(self, data):
        """Parse a SIGN_UP_RESP message - trying LITTLE endian instead of BIG"""
        try:
            # First try with LITTLE endian (opposite of docs)
            self.player_id, self.map_size = struct.unpack("<IH", data)
            print(f"Player ID: {self.player_id}, Map Size: {self.map_size}x{self.map_size} sectors (little endian)")
        except Exception as e:
            try:
                # If that fails, try with BIG endian (as docs specify)
                self.player_id, self.map_size = struct.unpack(">IH", data)
                print(f"Player ID: {self.player_id}, Map Size: {self.map_size}x{self.map_size} sectors (big endian)")
            except Exception as inner_e:
                print(f"Error parsing SIGN_UP_RESP with both endianness: {inner_e}")
                if self.debug_mode:
                    print(f"Raw data: {binascii.hexlify(data)}")
    
    def parse_player_loc(self, data):
        """Parse a PLAYER_LOC message - trying LITTLE endian instead of BIG"""
        try:
            if len(data) < 2:
                print(f"Player location data too short: {len(data)} bytes")
                return
                
            # Try with LITTLE endian first (opposite of docs)
            num_players = struct.unpack("<H", data[:2])[0]
            print(f"Received update with {num_players} players. Data length: {len(data)} bytes")
            
            if self.debug_mode and num_players > 0:
                print(f"First 50 bytes: {binascii.hexlify(data[:min(50, len(data))])}")

            # Parse player data
            offset = 2  # Skip num_players field
            creators_found = []
            
            for i in range(num_players):
                # Make sure we have at least enough data for player ID
                if offset + 4 > len(data):
                    break
                    
                # Extract player ID - LITTLE endian
                player_id = struct.unpack("<I", data[offset:offset+4])[0]
                offset += 4
                
                # Extract name (up to 17 bytes with null terminator)
                if offset + 17 > len(data):
                    break
                    
                name_bytes = data[offset:offset+17]
                name = ""
                for j in range(17):
                    if name_bytes[j] == 0:
                        break
                    name += chr(name_bytes[j])
                offset += 17
                
                # Extract color (RGB)
                if offset + 3 > len(data):
                    break
                    
                r, g, b = struct.unpack(">BBB", data[offset:offset+3])  # Keep RGB as big endian
                offset += 3
                
                # Extract sector coordinates with padding - LITTLE endian
                if offset + 8 > len(data):
                    break
                    
                try:
                    # Try LITTLE endian for sector coordinates
                    sec_x, sec_y = struct.unpack("<HxxHxx", data[offset:offset+8])
                except:
                    try:
                        # Try alternate format
                        dummy1, sec_x, dummy2, sec_y = struct.unpack("<BHBH", data[offset:offset+6])
                        offset += 6
                        continue
                    except:
                        # Last resort, just extract the values
                        sec_x = int.from_bytes(data[offset:offset+2], byteorder='little')
                        sec_y = int.from_bytes(data[offset+4:offset+6], byteorder='little')
                
                offset += 8
                
                # Extract position and velocity - LITTLE endian
                if offset + 32 > len(data):
                    break
                    
                try:
                    map_x, map_y, map_vx, map_vy = struct.unpack("<dddd", data[offset:offset+32])
                except:
                    map_x, map_y, map_vx, map_vy = 0.0, 0.0, 0.0, 0.0
                    
                offset += 32
                
                # Create player object
                player = {
                    "id": player_id,
                    "name": name,
                    "color": (r, g, b),
                    "sector": (sec_x, sec_y),
                    "position": (map_x, map_y),
                    "velocity": (map_vx, map_vy)
                }
                
                # Store player info
                self.players[player_id] = player
                
                # Print player info
                print(f"Player {player_id} ({name}): Sector ({sec_x},{sec_y}), Pos ({map_x:.1f},{map_y:.1f})")
                
                # Is this our player?
                if player_id == self.player_id:
                    self.current_sector = (sec_x, sec_y)
                    print(f"Our current sector: ({sec_x},{sec_y})")
                
                # Check if this is a player in sector (15,2) - might be the creator
                if sec_x == 15 and sec_y == 2:
                    creators_found.append(player)
                    print(f"FOUND PLAYER IN TARGET SECTOR: {name}")
                    print(f"Potential flag: {name}")
                    
                    # Check if name looks like a flag
                    if "CTF" in name or "{" in name or "}" in name:
                        print(f"FLAG FOUND: {name}")
            
            # Process any creators found
            for creator in creators_found:
                # Check surrounding bytes for flag data
                self.check_for_hidden_flag(data)
                
        except Exception as e:
            print(f"Error parsing PLAYER_LOC: {e}")
            if self.debug_mode:
                print(f"Raw data length: {len(data)}")
                #print(f"First 50 bytes: {binascii.hexlify(data[:min(50, len(data))])}")
                print(f"All bytes: {binascii.hexlify(data)}")

    
    def check_for_hidden_flag(self, data):
        """Check for hidden flag in raw data"""
        # Look for "CTF" or similar patterns
        data_str = data.decode('ascii', errors='ignore')
        
        # Look for common flag patterns
        patterns = ["flag", "CTF", "DawgCTF", "{", "}", "Flag"]
        
        for pattern in patterns:
            if pattern in data_str:
                start_idx = data_str.find(pattern)
                context = data_str[max(0, start_idx-10):min(len(data_str), start_idx+50)]
                print(f"Found pattern '{pattern}' in data: {context}")
                
                # Try to extract flag if it looks like flag format
                if pattern == "CTF" or pattern == "DawgCTF":
                    flag_start = start_idx
                    # Find the opening brace
                    brace_idx = data_str.find("{", flag_start)
                    if brace_idx > 0 and brace_idx - flag_start < 15:
                        # Find the closing brace
                        end_idx = data_str.find("}", brace_idx)
                        if end_idx > 0:
                            flag = data_str[flag_start:end_idx+1]
                            print(f"EXTRACTED FLAG: {flag}")
    
    def get_message_type_name(self, type_id):
        """Get the name of a message type from its ID"""
        return self.MSG_NAMES.get(type_id, f"UNKNOWN({type_id})")
    
    async def message_loop(self):
        """Handle incoming messages from the server"""
        try:
            while True:
                message = await self.websocket.recv()
                if len(message) < 12:  # Minimum header size
                    print("Received malformed message (too short)")
                    if self.debug_mode:
                        print(f"Message: {binascii.hexlify(message)}")
                    continue
                
                header = message[:12]
                # Headers are still BIG endian as per docs
                signature, msg_type, padding, payload_length = struct.unpack(">4sHHI", header)
                
                if signature != b"SPGM":
                    print(f"Invalid message signature: {signature}")
                    continue
                
                payload = message[12:]
                msg_type_name = self.get_message_type_name(msg_type)
                
                if self.debug_mode:
                    print(f"Received {msg_type_name} message, payload length: {len(payload)}")
                
                try:
                    if msg_type == self.MSG_TYPES["SIGN_UP_RESP"]:
                        self.parse_signup_resp(payload)
                    elif msg_type == self.MSG_TYPES["PLAYER_LOC"]:
                        self.parse_player_loc(payload)
                    elif msg_type == self.MSG_TYPES["ERROR"]:
                        print(f"Received error from server: {payload}")
                    elif msg_type == self.MSG_TYPES["PING"]:
                        # Respond with PONG
                        header = self.create_header(self.MSG_TYPES["PONG"], 0)
                        await self.websocket.send(header)
                except Exception as e:
                    print(f"Error processing {msg_type_name} message: {e}")
                    if self.debug_mode:
                        print(f"Payload (first 50 bytes): {binascii.hexlify(payload[:min(50, len(payload))])}")
                    
        except websockets.exceptions.ConnectionClosed:
            print("Connection to server closed")
        except Exception as e:
            print(f"Error in message loop: {e}")
    
    async def control_loop(self):
        """Periodically send control messages"""
        try:
            while True:
                await self.send_control()
                await asyncio.sleep(1/20)  # ~20Hz rate
        except Exception as e:
            print(f"Error in control loop: {e}")
    
    def press_key(self, key_name):
        """Press a key"""
        if key_name in self.KEY_CODES:
            self.pressed_keys.add(self.KEY_CODES[key_name])
            print(f"Pressed: {key_name}")
    
    def release_key(self, key_name):
        """Release a key"""
        if key_name in self.KEY_CODES and self.KEY_CODES[key_name] in self.pressed_keys:
            self.pressed_keys.remove(self.KEY_CODES[key_name])
            print(f"Released: {key_name}")
    
    async def navigate_to_target(self):
        """Navigate to the target sector (15,2)"""
        await asyncio.sleep(2)  # Wait for initial player data
        
        print(f"Starting navigation to target sector {self.target_sector}")
        
        while True:
            # Check if we have our current position
            if self.current_sector is None:
                print("Waiting for our position data...")
                await asyncio.sleep(1)
                continue
                
            # Check if we've reached the target
            if self.current_sector == self.target_sector:
                print(f"REACHED TARGET SECTOR {self.target_sector}!")
                print("Waiting for creator or flag...")
                # Release all keys
                for key in list(self.pressed_keys):
                    self.pressed_keys.remove(key)
                break
            
            # Plan our route
            moves = self.plan_route()
            print(f"Planned moves: {moves}")
            
            # Execute the next move
            if moves:
                next_move = moves[0]
                print(f"Moving {next_move}...")
                
                # Release all keys first
                for key in list(self.pressed_keys):
                    self.pressed_keys.remove(key)
                
                # Press the key for this move
                self.press_key(next_move)
                
                # Move for a short time
                await asyncio.sleep(1.5)
                
                # Release the key
                self.release_key(next_move)
            
            # Wait before planning next move
            await asyncio.sleep(0.5)
    
    def plan_route(self):
        """Plan a route to the target sector"""
        if not self.current_sector:
            return []
            
        moves = []
        current_x, current_y = self.current_sector
        target_x, target_y = self.target_sector
        
        # Calculate delta
        delta_x = target_x - current_x
        delta_y = target_y - current_y
        
        # Determine horizontal movement
        if delta_x > 0:
            moves.append("RIGHT")
        elif delta_x < 0:
            moves.append("LEFT")
            
        # Determine vertical movement
        if delta_y > 0:
            moves.append("DOWN")  # Y increases downward
        elif delta_y < 0:
            moves.append("UP")    # Y decreases upward
            
        return moves

# Example usage
async def main():
    # Create client with random color
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    client = SpaceGameClient(player_name="DawgHunter", color=color)
    
    # Connect and run the client
    await client.connect()

if __name__ == "__main__":
    print("Space Game Client - Modified for Challenge 2")
    print("------------------------------------------")
    print("Target: Meet creator in sector (15,2)")
    print("Strategy: Trying LITTLE endian instead of BIG endian")
    print()
    
    asyncio.run(main())