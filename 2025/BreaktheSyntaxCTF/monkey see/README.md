# Phân tích 
Bài cho ta một file pcap lưu lại protocol USB và USBMS, sau một hồi kiểm tra biết được đây đang lưu lại các keystroke gõ phím

https://github.com/Nissen96/USB-HID-decoders/tree/main

https://www.usb.org/sites/default/files/hid1_11.pdf để đọc thêm về USB HID

Dùng các script tại đây để parse các data đó ra, với bài tiếp theo là `monkey paint` thì sẽ parse data của chột thay vì bàn phím

# Flag
`./extract_hid_data.sh monkey-see.pcapng` lấy hid data và lưu vào file `usbdata-1.9.1.txt`

```
python keyboard_decode.py usbdata-1.9.1.txt --offset1 | grep BtSCTF{
# --offset: Index of modifier byte in case of added prefix bytes (default: 0) Nếu để default thì sẽ hiện cả <Ctrl+...> lấy offset 1 để bỏ phím thừa
```

BtSCTF{m0nk3y_tYpE!!1!!oneone!}