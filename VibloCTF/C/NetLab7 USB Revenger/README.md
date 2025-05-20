Phân tích file pcap thấy usb hid data (Dữ liệu human iteraction devices) như là chuột, bàn phím

Biết vậy, extract dữ liệu từ trường usbhid.data ra khỏi pcap

```bash
tshark -r netlab7.pcap -T fields -e usbhid.data > usb.txt
```

Sau đó dùng tool để chuyển đổi hiddata ra chữ hoặc chuyển động chuột, ở đây tôi sử dụng keyboard_decode.py của https://github.com/Nissen96/USB-HID-decoders/tree/main

```bash
python keyboard_decode.py usb.txt
```

Flag: `Flag{SuCh_4_b0r1n9_ch4LL_1n_3veRy_CTFs}`