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

# Flag4
Đưa vào DiE biết được đây là 1 file C# vậy chỉ cần đưa vào dotPeek để tìm hiểu

![image](https://github.com/user-attachments/assets/e12a664e-2d8d-401f-8791-128584efe924)
