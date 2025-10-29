Tham khảo https://github.com/GoSecure/pyrdp

Mở file `capture.pcap`, áp keylog vào, export PDUS OSI layer 7 ra file `rdp.pcap`

Kiểm tra file pcap mới xuất ra thấy `FastPath, Bitmap` nên nghĩ rằng phải làm như nào đấy để xuất cái file bitmap ra rồi xem hình ảnh màn hình lúc đang rdp vào đang lướt website gì

Tải PyRDP, chạy `python3 -m pyrdp.bin.convert --src 192.168.56.1 -s tls-lsa.log -o ./output rdp.pcap` sau khi chạy xong sẽ ra 2 file `.pyrdp`, bởi vì file của srcport `33324` có nhiều dữ liệu hơn nên ta sẽ chạy `pyrdp-player` để xem người dùng thực hiện những gì khi đang rdp

 `pyrdp-player 20251020191524_192.168.56.1_33324-192.168.56.102_3389.pyrdp`

Qua video ta thấy được đáp án của 2 câu hỏi cuối

**What is the website the victim is currently browsing. (TLD only: google.com)**

> `thedfirreport.com`

**What is the username:password combination for website `http://barrowick.htb`**

Kiểm tra phần clipboard của người dùng trong `pyrdp-player` sẽ thấy

> `candle_eyed:AshWitness_99@Tomb`