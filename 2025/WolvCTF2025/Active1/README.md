# Phần 1 của chuỗi bài active là domain access
Trong gia đoạn này của cuộc tấn công, hacker sẽ thường truy cập vào hệ thống qua fishing hoặc các lỗ hổng của web như injection,bruteforce,...


# Flag1
Trong thư mục user ta thấy có user mssql_service nên khả năng cao hacker đã tận dụng lỗ hổng nào đó để truy cập vào đây

Kiểm tra Users\mssql_service\MSSQL13.SQLEXPRESS\MSSQL\Log\ERRORLOG có thể thấy hacker đã thử bruteforce tên tài khoản trên SQL server, các tên người dùng cũng có thể ghép lại thành flag1

Sau đó hacker đã đăng nhập thành công vào mssql với tk:mk sa:Password123

`wctf{d0nt_3n4bl3`

# Flag2
Với flag2 thì khá may mắn, khi đang tìm các file ".txt" trong thư mục user lại lòi ra file Users\Public\Documents\winPEASOutput.txt

https://github.com/peass-ng/PEASS-ng/blob/master/winPEAS/winPEASexe/README.md

winPEA:Windows Privilege Escalation Awesome Script là một script sử dụng để tìm kiếm các phương pháp dẫn đến leo thang đặc quyền trên máy chủ windows

Trong đây ta thấy hacker đã sử dụng một lệnh được mã hoá bằng base64 để reverse shell kết nối đến 192.169.187.128:1433 qua xp_cmdshell trong sql server

Ở đây cũng được dấu flag2 = base64 luôn

Sau đó hacker đã có truy cập đến domain controller box 

`_xP_cmdsh311_w1th_d3fault_cr3ds_0r_`

# Flag3
Sau khi đọc phần wiki của WinPEASx64 và tiếp tục tìm kiếm trong winPEASOutput.txt, ta thấy winPEAS64.exe đã tìm được Autologon creds của user Dan với mật khẩu là "DansSuperCoolPassw0rd!!", hacker đã sử dụng những thông tin trên để truy cập vào các domain account

Và ở phần AltDefaultUserName là mã hex của flag3

`enabl3_4ut0log0n_0k??!?}`

`wctf{d0nt_3n4bl3_xP_cmdsh311_w1th_d3fault_cr3ds_0r_enabl3_4ut0log0n_0k??!?}`
