# Tìm hiểu(Sử dụng bloodhound): biết domain admin là jessica
Tham khảo: https://github.com/SpecterOps/BloodHound

Sử dụng BloodHound để soi `explore/cypher/All Domain Admins`, ta thấy được người dùng jessica cũng là 1 domain admin

![image](https://github.com/user-attachments/assets/d8d2a4c3-3ef2-45c5-b28e-189f56640942)

![image](https://github.com/user-attachments/assets/5be1077f-a399-4c97-bc65-32424ce120f8)

Trong thư mục của jake có `ntds.dit`, `sam.hive`, `system.hive` đủ 3 điều kiện để sử dụng `impacket-secretdump -ntds ntds.dit -sam sam.hive -system system.hive LOCAL` để lấy ntlm hash của jessica

Format mật khẩu là `wctf{bl00dh0und_is_c00l_cityxxx}` xxx là 3 số ngẫu nhiên

Có thể lấy danh sách các thành phố ở https://github.com/FinNLP/cities-list/blob/master/list.txt

Sau đó dùng `pwFormat.py` tạo wordlist custom 

wctf{bl00dh0und_is_c00l_city + 3 số ngẫu nhiên và "}" sẽ được thêm vào khi sử dụng hashcat

`hashcat -a 6 -m 1000 jessicahash cities_wordlist.txt "?d?d?d}"`

Mật khẩu và cũng chính là flag

`wctf{bl00dh0und_is_c00l_votuporanga985}`
