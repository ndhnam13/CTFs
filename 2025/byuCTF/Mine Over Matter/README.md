# Mô tả
Your SOC has flagged unusual outbound traffic on a segment of your network. After capturing logs from the router during the anomaly, they handed it over to you—the network analyst.

Somewhere in this mess, two compromised hosts are secretly mining cryptocurrency and draining resources. Analyze the traffic, identify the two rogue IP addresses running miners, and report them to the Incident Response team before your network becomes a crypto farm.

Flag format: byuctf{IP1,IP2} (it doesn't matter what order the IPs are in)

### Sử dụng file log.txt ở bài trước

# Phân tích

Bài muốn ta tìm địa chỉ của 2 máy crypto miner, với crypto miner thì ta chỉ cần tìm những địa chỉ có lưu lượng mạng nhiều bất thường thôi, vậy ta sẽ phải tìm 2 địa chỉ có lưu lượng trên tcp nhiều nhất là sẽ ra

# Flag
```
$ awk -F',' '$17 == "tcp" { print $19 }' logs.txt | sort | uniq -c | sort -nr | head
  88374 172.16.0.10
  76841 172.16.0.5
  42252 172.16.96.109
  36801 172.16.96.57
  16557 172.16.16.3
   3318 172.16.96.2
    894 172.16.0.70
    311 172.16.96.56
    273 172.16.64.55
    169 172.16.96.5
```

`byuctf{172.16.0.10,172.16.0.5}`