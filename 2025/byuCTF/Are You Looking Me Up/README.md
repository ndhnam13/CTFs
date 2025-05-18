# Mô tả

The network has a DNS server that's been receiving a lot of traffic. You've been handed a set of raw network logs. Your job? Hunt down the DNS server that has received the most DNS requests.

Use the log file found [here](https://byu.box.com/s/2rong02xtfx7sfo52nos3ra2waifogv2)

Analyze the logs and find the impostor.

Flag format: `byuctf{IP1}`

# Flag

```
$ awk -F',' '$17 == "udp" && $22 == 53 { print $20 }' logs.txt | sort | uniq -c | sort -nr | head
 127660 172.16.0.1
  41112 172.16.96.1
   3614 8.8.8.8
    215 172.16.16.1
    206 172.16.64.1
    130 172.18.0.1
     17 216.239.38.106
     16 216.239.36.106
     15 216.239.34.106
     15 172.16.4.1
```

Bài muốn ta tìm địa chỉ của dns server nhận được nhiều request nhất nên có thể dùng `uniq -c` để đếm

