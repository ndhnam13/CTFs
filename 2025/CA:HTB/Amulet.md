# Mô tả
Garrick and Thorin’s visit to Stonehelm took an unexpected turn when Thorin’s old rival, Bron Ironfist, challenged him to a forging contest. In the end Thorin won the contest with a beautifully engineered clockwork amulet but the victory was marred by an intrusion. Saboteurs stole the amulet and left behind some tracks. Because of that it was possible to retrieve the malicious artifact that was used to start the attack. Can you analyze it and reconstruct what happened? Note: make sure that domain korp.htb resolves to your docker instance IP and also consider the assigned port to interact with the service.

# Phân tích
Bài này khá đơn giản thôi, file `artifact.ps1` chỉ chạy nếu người dùng hiện tại là máy của ai đó - Chắc chắn không phải của mình nên chỉ cần loại bỏ điều kiện đó và tải file từ `http://korp.htb/a541a` về

File `a541a.ps1` đơn giả chỉ decode base64 

``` ps
$a35 = "4854427b37683052314e5f4834355f346c573459355f3833336e5f344e5f39723334375f314e56336e3730727d"
($a35-split"(..)"|?{$_}|%{[char][convert]::ToInt16($_,16)}) -join ""
```

![image](https://github.com/user-attachments/assets/533f1123-e9ec-4cd9-9f81-e1635c97bd47)

Dù là dễ nhất trong mảng for nhưng mà đã mất khá nhiều thời gian để setup máy kết nối đến `http://korp.htb/a541a`

`Note: make sure that domain korp.htb resolves to your docker instance IP and also consider the assigned port to interact with the service.`

Muốn `domain resolve to your docker instance IP` thì phải thêm  `83.136.250.155 korp.htb` vào cuối file `C:\Windows\System32\drivers\etc\hosts` nếu trên linux thì chỉ là `/etc/hosts`

Nguyên day1 phải chỉnh để kết nối được, không hiểu sao đã resolve đến IP rồi thì port lại không hoạt động?, muốn chắc chắn hơn phải dùng `nmap -sV korp.htb` để xem port có mở hay không, nếu không mở được thì phải reset `docker instance` trên htb

`HTB{7h0R1N_H45_4lW4Y5_833n_4N_9r347_1NV3n70r}`
