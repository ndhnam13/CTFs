# Mô tả
I accidentally broke my message and it got all mixed up with everything else. Can you help me get it back?

Flag format: TexSAW{flag}

# Phân tích
Bài cho ta một file pcap, sau khi xem qua có thể thấy các trong protocol ICMP có các packet chỉ có một byte, khá khác thường

Filter trong wireshark `ICMP && data.len == 1`

Nhìn kĩ sẽ thấy thứ tự của phần `icmp.seq` - `seq=x/x` bị lộn xộn, giống những gì đề bài nói đến, đọc phần data theo thứ tự từ bé đến lớn thấy `TexSAW` chắc chắn là flag rồi

# Flag
Tiếp tục đọc các đoạn data 1 byte đó đến khi gặp `}`

Có thể dùng payload tshark để lấy phần data đó nhưng nó chỉ trả về cho ta kí tự dưới dạng hex vậy phải kết hợp với 1 số câu lệnh linux để biến về flag đúng, đoạn này nhờ chatgpt giúp

## Sẽ học cách viết payload tshark trong tương lai

```
tshark -r cap.pcap -Y "icmp" -T fields -e icmp.seq -e data.data | \ 
  awk 'length($2) >= 2 { printf "%d %c\n", $1, strtonum("0x" substr($2,1,2)) }' | \
  sort -n
```

`TexSAW{not_the_fake_xone}`