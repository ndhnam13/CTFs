Đọc file binary -> dùng hex.hex.css. để exfil file

Decode bằng B32 với custom alphabet

Tìm thấy hàm initb32alphabet, dựng lại thuật toán của nó -> giải ra alphabet custom: `AKU6EVFQDSP4ITJ3Y5RXZ2HCGOWLNMB7`

Filter traffic có `dns contains 'css'` dùng tshark lấy dữ liệu file bị mã hoá b32 `tshark -r dnscss.pcapng -Y 'dns && ip.addr==1.1.1.1' -T fields -e dns.qry.name | uniq > qnames.txt`

Decode ra backup.zip

Unzip flag trong ảnh