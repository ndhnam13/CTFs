# Mô tả

We managed to steal this USB stick from a member of PwnTopia, but there was nothing useful on it. Can you see if you can find anything ?

**Authors: algorab, CaptWake**

# Phân tích

Bài cho ta một file disk.img nhưng không load được trong FTK imager nên sẽ sử dụng Autopsy (vì load vào được)

Kiểm tra các file trong disk.img thấy 2 file đáng ngờ là `cryptodisko` một file ELF được viết bằng GO và `cryptodisko.passwd` chứa có thể là một encryption key `PwnT0p14_s3cr3t_p4rt1t10n`. Trong autopsy cũng báo cáo rằng vol3 có dấu hiệu bị mã hoá (có thể đây là lí do không load được trong ftk imager)

```
$ ./cryptodisko -h
flag needs an argument: -h
Usage of ./cryptodisko:
  -d string
        Name of the disk to work on
  -h int
        Size of the hidden partition in bytes (default 10485760)
  -k string
        Key for the encryption/decryption
  -m string
        Specify a mode among "create" and "encrypt"
```

Vậy đoán được rằng file ELF đã dùng mật khẩu này để mã hoá ổ đĩa. Để encrypt một ổ đĩa người dùng cần đưa vào đường dẫn đến ổ đĩa, size và key

Đưa nó vào trong IDA xem sao thì thấy được 2 hàm encrypt là `main_Aes256Encode` sử dụng padding PKCS5 (`main_PKCS5Padding`)

```c
// main.Aes256Encode
// local variable allocation has failed, the output may be wrong!
void __golang main_Aes256Encode(
        _slice_uint8_0 content,
        _slice_uint8_0 encryptionKey,
        _slice_uint8_0 IV,
        _slice_uint8_0 encryptedContent,
        error_0 err)
{
  __int64 v5; // rcx
  __int64 v6; // rax
  int len; // rdx
  __int64 v8; // r9
  uint8 *array; // rax
  int v10; // rbx OVERLAPPED
  int v11; // rcx
  __int64 v12; // rax
  __int64 v13; // rcx
  __int64 v14; // rax
  __int64 v15; // rax
  __int64 v16; // rax
  runtime_slice v17; // r8
  __int64 v18; // r9
  int v19; // r10
  int v20; // r9
  __int64 v21; // r9
  int v22; // rbx
  __int64 v23; // r9
  uint8 *v24; // rax
  int v25; // rcx
  __int64 v26; // [rsp+0h] [rbp-68h]
  int cap; // [rsp+18h] [rbp-50h]
  __int64 v28; // [rsp+20h] [rbp-48h]
  __int64 v29; // [rsp+40h] [rbp-28h]
  __int64 v30; // [rsp+48h] [rbp-20h]
  __int64 b; // [rsp+50h] [rbp-18h]
  int err_8; // [rsp+90h] [rbp+28h]
  int key; // [rsp+98h] [rbp+30h]
  uint8 *_r0; // [rsp+A0h] [rbp+38h]
  __int128 iv; // [rsp+A8h] [rbp+40h]
  crypto_cipher_BlockMode v36; // 0:r8.16
  _slice_uint8_0 v37; // 0:rcx.8,8:rdi.16

  *(_QWORD *)&iv = IV.len;
  err_8 = encryptionKey.len;
  _r0 = IV.array;
  *((_QWORD *)&iv + 1) = IV.cap;
  key = encryptionKey.cap;
  main_PKCS5Padding(content, 16, *(_slice_uint8_0 *)&encryptionKey.len);
  cap = content.len;
  v28 = v5;
  v29 = v6;
  len = encryptionKey.len;
  if ( encryptionKey.len >= 32 )
  {
    encryptionKey.len = key;
  }
  else
  {
    encryptionKey.cap = key;
    v8 = 0;
    while ( v20 < 32 - encryptionKey.len )
    {
      if ( encryptionKey.cap < (unsigned __int64)++len )
      {
        v26 = v21;
        v22 = len;
        v19 = 32 - encryptionKey.len;
        runtime_growslice(
          encryptionKey.array,
          len,
          encryptionKey.cap,
          1,
          (internal_abi_Type *)&RTYPE_uint8,
          *(runtime_slice *)&encryptionKey.cap);
        encryptionKey.len = err_8;
        v23 = v26;
        len = v22;
        encryptionKey.array = v24;
        encryptionKey.cap = v25;
      }
      encryptionKey.array[len - 1] = encryptionKey.len;
      ++v18;
    }
    encryptionKey.len = encryptionKey.cap;
  }
  array = encryptionKey.array;
  v10 = len;
  v11 = encryptionKey.len;
  crypto_aes_NewCipher(
    *(_slice_uint8_0 *)(&v10 - 1),
    *(crypto_cipher_Block *)&encryptionKey.array,
    *(error_0 *)&encryptionKey.cap);
  if ( !v13 )
  {
    b = v12;
    runtime_makeslice((internal_abi_Type *)&RTYPE_uint8, cap, cap, encryptionKey.array);
    v30 = v14;
    v37.array = _r0;
    *(_OWORD *)&v37.len = iv;
    v15 = b;
    crypto_cipher_NewCBCEncrypter(*(crypto_cipher_Block *)(&v10 - 1), v37, v36);
    (*(void (__golang **)(int, __int64, int, int, __int64, int, __int64))(v16 + 32))(v10, v30, cap, cap, v29, cap, v28);
    if ( *((_QWORD *)&iv + 1) < (unsigned __int64)(iv + cap) )
      runtime_growslice(_r0, iv + cap, *((int *)&iv + 1), cap, (internal_abi_Type *)&RTYPE_uint8, v17);
    runtime_memmove();
  }
}

// main.PKCS5Padding
void __golang main_PKCS5Padding(_slice_uint8_0 cipherText, int blockSize, _slice_uint8_0 _r0)
{
  int v3; // rdi
  __int64 v4; // rax
  runtime_slice v5; // r8
  int v6; // rsi
  unsigned __int64 v7; // rcx
  uint8 *v8; // rdi
  uint8 *v9; // rax
  _BYTE b[25]; // [rsp+1h] [rbp-31h] BYREF
  __int64 v11; // [rsp+1Ah] [rbp-18h]
  uint8 *v12; // [rsp+22h] [rbp-10h]
  uint8 *oldPtr; // [rsp+3Ah] [rbp+8h]
  int cipherTexta; // [rsp+42h] [rbp+10h]
  unsigned __int64 oldCap; // [rsp+4Ah] [rbp+18h]
  _slice_uint8_0 v16; // 0:rax.8,8:rbx.8,16:rcx.8

  if ( !blockSize )
    runtime_panicdivide();
  cipherTexta = cipherText.len;
  oldPtr = cipherText.array;
  oldCap = cipherText.cap;
  v3 = blockSize - cipherText.len % blockSize;
  b[0] = v3;
  v16.array = b;
  v16.cap = 1;
  v16.len = 1;
  bytes_Repeat(v16, v3, _r0);
  v6 = cipherTexta + 1;
  v7 = oldCap;
  if ( oldCap < cipherTexta + 1 )
  {
    *(_QWORD *)&b[1] = 1;
    v11 = v4;
    runtime_growslice(oldPtr, cipherTexta + 1, oldCap, 1, (internal_abi_Type *)&RTYPE_uint8, v5);
    v8 = v9;
    v6 = cipherTexta + 1;
  }
  else
  {
    v8 = oldPtr;
  }
  v12 = v8;
  *(_QWORD *)&b[17] = v7;
  *(_QWORD *)&b[9] = v6;
  runtime_memmove();
}
```

Đưa vào nhớ chatgbt tạo script giải mã

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import sys

# === Cấu hình ===
KEY_ORIGINAL = b'PwnT0p14_s3cr3t_p4rt1t10n'  # 25 bytes
DISK_IMG = 'disk.img'
OUTPUT_FILE = 'decrypted_output.bin'

# === Pad key lên 32 bytes theo logic của chương trình Go ===
def pad_key(key: bytes, desired_length=32) -> bytes:
    if len(key) >= desired_length:
        return key[:desired_length]
    pad_value = len(key)
    return key + bytes([pad_value] * (desired_length - len(key)))

# === Đọc IV + ciphertext từ disk image ===
def read_iv_and_ciphertext(path: str):
    with open(path, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()
    return iv, ciphertext

# === Giải mã bằng AES-256-CBC ===
def decrypt_aes_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_padded = cipher.decrypt(ciphertext)
    try:
        plaintext = unpad(plaintext_padded, AES.block_size)
    except ValueError as e:
        print(f"[!] Unpadding failed: {e}")
        return plaintext_padded  # Trả về dữ liệu chưa unpad
    return plaintext

# === Main ===
def main():
    key = pad_key(KEY_ORIGINAL)
    iv, ciphertext = read_iv_and_ciphertext(DISK_IMG)
    print(f"[+] IV: {iv.hex()}")
    print(f"[+] Ciphertext size: {len(ciphertext)} bytes")

    decrypted = decrypt_aes_cbc(ciphertext, key, iv)
    
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(decrypted)
    
    print(f"[+] Done! Decrypted data saved to: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
```

```bash
$ python solve.py
[+] IV: 00000000000000000000000000000000
[+] Ciphertext size: 1074790416 bytes
[+] Done! Decrypted data saved to: decrypted_output.bin
```

```bash
$ strings decrypted_output.bin | grep N0PS
N0PS{mBr_t4bl3_h4s_n0_s3cr3t_4_U_4Nym0r3}
```



