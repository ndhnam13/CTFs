# Phân tích
Bài muốn ta tìm clock rate conversion value

Từ pinpoint1 ta biết được người dùng đang sử dụng một loại smart card, muốn biết được các thông tin của smart card đó thì có thể kiểm tra `ATR` của nó

https://en.wikipedia.org/wiki/Answer_to_reset

Sau đó lên đây tìm thông tin https://en.wikipedia.org/wiki/Answer_to_reset hoặc tự phân tích các byte đó cũng ra

ATR thường bắt đầu bằng byte 3b hoặc 3f, 3b phổ biến hơn (TS)

byte tiếp theo là `Number of Ti, presence of TA1..TD1` (T0)

Và byte thứ 3 là `Maximum clock frequency(FI), proposed bit duration(DI)` bài muốn ta tìm FI

# FLag
```
$ tshark -r FindMyClockConversion.pcap -T fields -e usb.capdata | grep 3b
801200000000470000003b7d96000080318065b0831111e583009000
8002010000005b000000d14cf524bd5e7932d89d9863137c21c933b7492130fe
8001010000005e0000005800483b220fd6b41e861378c9be8cbe59ab84ab5964
$ tshark -r FindMyClockConversion.pcap -T fields -e usb.capdata > tsouput.txt
```

Có 2 chuỗi khá giống ATR ở dòng 1 và 3, thử cả 2 trên web thì chỉ có dòng thứ nhất là ra thông tin của smart card

`3b7d96000080318065b0831111e583009000` có FI là `512`

`DawgCTF{512}`