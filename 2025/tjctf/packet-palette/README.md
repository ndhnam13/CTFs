# Phân tích

Lấy data trong tcp packet của pcap -> ghép lại file png -> flag

Mở pcap thấy 23 packet TCP, mô tả bảo là sử dụng 1 custom USBIP thấy 2 packet đầu và cuối có string USBIP:DEVICE_READY và USBIP:DONE, vậy là đã chuyển dữ liệu gì đó

Nhìn vào packet tcp thứ 2 trong string thấy "PNG" và magic byte 8950 => dữ liệu được chuyển đi là một ảnh png, đoán được ảnh này chứa flag

Bởi vì protocol USBIP được đưa vào trong data của các packet TCP nên để xuất ảnh này ra cần tách header của USBIP ra và chỉ lấy phần data để lấy được ảnh hoàn chỉnh

Trong packet 2:

`00deadbeef001234567890ab08004500022800010000400650b90a0a0a010a0a0a027a697a69000003e800000001501820000c0700005553424900000015000001f4`(header USPIP, kết thúc bằng 4 byte 000001f4) + `8950……` (data được USBIP chuyển đi)

Biết vậy rồi thì lấy ra và ghép vào rồi ra flag

```bash
#!/bin/bash

tshark -r chall.pcapng -T fields -e data | grep -o '0001f4.*' | sed 's/0001f4//' > png.txt

xxd -r -p png.txt > real.png
```



`tjctf{usb1p_f13g_1ns1d3_3_pr0t0c0l}`

