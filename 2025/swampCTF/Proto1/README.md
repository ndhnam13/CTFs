![image](https://github.com/user-attachments/assets/a540e395-cb62-4070-9ae6-3adc387476d2)

# Phân tích
Bài cho ta một file pcap và ở mô tả có server với port nhưng mà netcat thì lại không vào được

Kiểm tra file pcap thì thấy tại protocol `UDP` có fake flag và trước khi hiện ra fake flag thì đã gửi đến server(Ở đây khả năng cao là server trong mô tả qua UDP) `..flag.txt`

Qua phân tích data của nó ta biết được:
- 2 byte đầu có thể là request để lấy flag `02`
- 2 byte tiếp theo là độ dài của string `flag.txt` ở đây là `08` 
- Còn lại là `flag.txt` khi dịch ra hex

Vậy để lấy được flag ta cần gửi cái payload này đến server qua netcat với option `-u` để gửi = UDP bởi `nc` kết nối bằng tcp là default

# Flag
Copy value của request UDP vừa thấy trong wireshark

`echo 0208666c61672e747874 | xxd -r -p > payload.txt`

Gửi `flag.txt` đến server 

`nc -u chals.swampctf.com 44254 < payload.txt > flag.txt`

`swampCTF{m070_m070_54y5_x0r_15_4_n0_n0}`
