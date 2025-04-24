Bài cho ta một file pcap, qua kiểm tra thấy phần lớn protocol được sử dụng là SMB2 và có truyền các file netlab1.7z, password.txt,...

Vào phần `export objects/SMB` sau đó export 2 file đấy ra thì biết được password.txt chứa mật khẩu của `netlab1.7z`

Mật khẩu: `SMBprotocol`

Giải nén ta được file `netlab1.db`

Dùng `DB Browser for SQLite` để xem, thấy trong các `Database Structure` có cột `flag`

Vào `Browse Data/Table: flag` thì sẽ thấy cột BillingCity chứa flag

`Flag{NetLab1_N0w_y0u_kn0w_SMB??}`