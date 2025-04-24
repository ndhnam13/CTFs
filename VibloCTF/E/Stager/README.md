Bài cho ta một file pcap, có khá nhiều protocol SSDP, DNS

Các protocol SSDP sẽ gửi thông điệp discover đến một máy `239.255.255.250` và sau đó máy đó hỏi DNS server địa chỉ IPv6 của `xxx3.thomdt.tk`

Nói chung là flag sẽ nằm trong phần trả lời của DNS query request trên

Lúc làm thì tôi đã `Follow UDP stream` và thấy flag ở các stream 12 13 14 16

`Flag{ae6032eeeb5cedc1555940983435335b}`