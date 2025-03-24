# Active2 sẽ là giai đoạn hacker truy cập được vào hệ thống và tiến hành điều tra file, các người dùng trong hệ thống
Tham khảo thêm:

https://attack.mitre.org/techniques/T1558/004/
# 3 user bị tấn công là dan, emily, james

# Flag1
Get-ChildItem -Path "Users/" -Recurse -File | Where-Object { $_.Name -match "\.ps1|\.bat|\.exe|\.txt|\.rdp" } > Test.txt

Kiểm tra các file script hoặc đáng nghi mà hacker có thể chạy

File lạ: Users\Public\Downloads\script.txt

File này chạy lệnh = emily, jake: Users\Administrator\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt

File chứa mật khẩu của jake: Users\patrick\Desktop\note_from_jake.txt, fwa3fe8#FEwef

File lạ: Users\dan\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt, Dùng sharphound.ps1, rubeus.exe 

https://attack.mitre.org/software/S0521/

https://github.com/SpecterOps/BloodHound-Legacy/blob/master/Collectors/SharpHound.ps1: Khá giống file ở Users\admin\Desktop\Users\dan\Desktop\SharpHound.ps1

- Tên hacker đã sử dụng .\Rubeus.exe asreproast để dump password hash của emily vào file asreproast.ouput ra đâu đó(trong user dan)

Cách này chỉ thành công nếu tài khoản của user không bật Kerberos preauthentication, ở đây emily không bật nên lấy hash thành công

Đến giờ biết được phần lớn các file dùng cho việc hack nằm ở user "dan", kiểm tra các thư mục của dan

Kiểm tra thư mục Desktop/asreproast.ouput ta có đoạn mã base64 dịch thành part1 của flag: 

`wctf{asr3pr04st3d?_`


# Flag2
Ta crack được hash của emily trong file .output vừa rồi(crack = hashcat -m 18200 emilyHash.txt rockyou.txt --force)

Mật khẩu: `youdontknowmypasswordhaha`

Xong việc ở đây, giờ ta đã biết hacker nhắm đến user emily nên sẽ kiểm tra emily, tìm kiếm một hồi tìm được file emily/important.7z, nhưng mật khẩu giải nén lại không chính xác?? Vậy ta sẽ phải đào sâu hơn vào emily. Ở trong thư mục emily có file tree.txt gợi ý rằng trong Documents có important.7z(đã biết) và README(Khi kiểm tra lại không có trong thư mục) Vậy có thể README đã bị xoá, cần kiểm tra log

Qua kiểm tra Users\emily\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt Ta biết được emily để đảm bảo không bị hack đã tự nhắc mình là phải thêm đuôi 777 vào mật khẩu cho file zip, james cũng nhờ emily giấu hộ mật khẩu của anh ấy, vậy trong file zip sẽ chứa flag2 và mật khẩu của james(Sau đó hacker đã thay đổi mật khẩu của james trong các phần sau)

Mật khẩu file important.7z: `youdontknowmypasswordhaha777`

Giải nén ta được folder important với 3 ảnh mèo

binwalk file car.jpeg ta thấy còn một file jpeg khác được giấu bên trong

Lấy nó ra = `dd if=car.jpeg of=hidden.jpg bs=1 skip=9296`

Được 1 ảnh hidden.jpg có flag part 2 và mật khẩu của James: `wd!A2@fge83S` (Sau đó đã bị thay đổi)

`sh0uldv3_3nabl3d_s0m3_k3rb3r0s_pr34uth_4nd_`

# Flag3
Trước đó emily có nhắc đến việc được james nhắc giữ kín mật khẩu của anh ấy, kiểm tra ConsoleHost_history của James ta được part 3(Đến đoạn này trong log powershell của james hacker đã thay đổi mật khẩu của patrick và emily thành `Password123!`)

`d0nt_us3_4ll3xtendedr1ghts}`

`wctf{asr3pr04st3d?_sh0uldv3_3nabl3d_s0m3_k3rb3r0s_pr34uth_4nd_d0nt_us3_4ll3xtendedr1ghts}`
