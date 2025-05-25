# Mô tả

You are a cybersecurity analyst working in the Security Operations Center (SOC) of BookWorld, an expansive online bookstore renowned for its vast selection of literature. BookWorld prides itself on providing a seamless and secure shopping experience for book enthusiasts around the globe. Recently, you've been tasked with reinforcing the company's cybersecurity posture, monitoring network traffic, and ensuring that the digital environment remains safe from threats.
Late one evening, an automated alert is triggered by an unusual spike in database queries and server resource usage, indicating potential malicious activity. This anomaly raises concerns about the integrity of BookWorld's customer data and internal systems, prompting an immediate and thorough investigation.
As the lead analyst in this case, you are required to analyze the network traffic to uncover the nature of the suspicious activity. Your objectives include identifying the attack vector, assessing the scope of any potential data breach, and determining if the attacker gained further access to BookWorld's internal systems.

Category:

[Network Forensics](https://cyberdefenders.org/blueteam-ctf-challenges/?categories=network-forensics)

Tactics:

[Initial Access](https://cyberdefenders.org/blueteam-ctf-challenges/?tactics=initial-access)[Persistence](https://cyberdefenders.org/blueteam-ctf-challenges/?tactics=persistence)[Command and Control](https://cyberdefenders.org/blueteam-ctf-challenges/?tactics=command-and-control)

Tools:

[Wireshark](https://cyberdefenders.org/blueteam-ctf-challenges/?tools=wireshark)[Network Miner](https://cyberdefenders.org/blueteam-ctf-challenges/?tools=network-miner)

# Flag 1

## Mô tả

By knowing the attacker's IP, we can analyze all logs and actions related to that IP and determine the extent of the attack, the duration of the attack, and the techniques used. Can you provide the attacker's IP?

## Phân tích

Mô tả nói đến việc có spike nhiều request đến server thì muốn tìm được IP của hacker ta chỉ cần vào mục `Statistics/conversations` của trong wireshark và sort địa chỉ IP gửi nhiều packet nhất tới server

## FLag

`111.224.250.131`

# Flag 2

## Mô tả

If the geographical origin of an IP address is known to be from a region that has no business or expected traffic with our network, this can be an indicator of a targeted attack. Can you determine the origin city of the attacker?

## Flag

Lên google tìm `IP to location` rồi paste cái IP vừa rồi vào là ra thành phố

`Shijiazhuang`

# Flag 3

## Mô tả

Identifying the exploited script allows security teams to understand exactly which vulnerability was used in the attack. This knowledge is critical for finding the appropriate patch or workaround to close the security gap and prevent future exploitation. Can you provide the vulnerable PHP script name?

## Phân tích

Vì bài muốn biết được file php bị lợi dùng thi trong wireshark ta có thể sort `ip.src == 111.224.250.131 && http` để xem request mà hacker đã gửi, tìm kiếm được một hồi thì có thể thấy có rất nhiều request GET lạ kiểu `/search.php?search=book and 1=1; -- -` đây là dấu hiện của SQL injection, và tất nhiên biết được file php bị lợi dụng là `search.php`

## Flag

`search.php`

# Flag 4

## Mô tả

Establishing the timeline of an attack, starting from the initial exploitation attempt, what is the complete request URI of the first SQLi attempt by the attacker?

## Flag

Tìm đến request GET có URL dài hơn bình thường đầu tiên

Lưu ý: Các request đang ở dưới dạng URL encoded, nên nếu muốn đưa về bình thường thì sẽ phải decode cái URL đó

`/search.php?search=book and 1=1; -- -` 

# Flag 5

## Mô tả

Can you provide the complete request URI that was used to read the web server's available databases?

## Phân tích

Có rất nhiều request, muốn tìm được cái request mà đọc toàn bộ database của server thì có thể tham khảo đến một vài keyword như là `INFORMATION_SCHEMA` cái này sẽ cho ta thông tin về tất cả các tables, views, columns, procedures trong database

Để tìm được thì trước hết ta phải xuất các URI ra để decode rồi check

```bash
$ tshark -r WebInvestigation.pcap -Y 'ip.src == 111.224.250.131 && http.request.uri contains "search.php"' -T fields -e http.request.full_uri | grep INFORMATION_SCHEMA
http://bookworldstore.com/search.php?search=book%27%20UNION%20ALL%20SELECT%20NULL%2CCONCAT%280x7178766271%2CJSON_ARRAYAGG%28CONCAT_WS%280x7a76676a636b%2Cschema_name%29%29%2C0x7176706a71%29%20FROM%20INFORMATION_SCHEMA.SCHEMATA--%20-
http://bookworldstore.com/search.php?search=book%27%20UNION%20ALL%20SELECT%20NULL%2CCONCAT%280x7178766271%2CJSON_ARRAYAGG%28CONCAT_WS%280x7a76676a636b%2Ctable_name%29%29%2C0x7176706a71%29%20FROM%20INFORMATION_SCHEMA.TABLES%20WHERE%20table_schema%20IN%20%280x626f6f6b776f726c645f6462%29--%20-
http://bookworldstore.com/search.php?search=book%27%20UNION%20ALL%20SELECT%20NULL%2CCONCAT%280x7178766271%2CJSON_ARRAYAGG%28CONCAT_WS%280x7a76676a636b%2Ccolumn_name%2Ccolumn_type%29%29%2C0x7176706a71%29%20FROM%20INFORMATION_SCHEMA.COLUMNS%20WHERE%20table_name%3D0x61646d696e%20AND%20table_schema%3D0x626f6f6b776f726c645f6462--%20-
http://bookworldstore.com/search.php?search=book%27%20UNION%20ALL%20SELECT%20NULL%2CCONCAT%280x7178766271%2CJSON_ARRAYAGG%28CONCAT_WS%280x7a76676a636b%2Ccolumn_name%2Ccolumn_type%29%29%2C0x7176706a71%29%20FROM%20INFORMATION_SCHEMA.COLUMNS%20WHERE%20table_name%3D0x637573746f6d657273%20AND%20table_schema%3D0x626f6f6b776f726c645f6462--%20-
http://bookworldstore.com/search.php?search=book%27%20UNION%20ALL%20SELECT%20NULL%2CCONCAT%280x7178766271%2CJSON_ARRAYAGG%28CONCAT_WS%280x7a76676a636b%2Ccolumn_name%2Ccolumn_type%29%29%2C0x7176706a71%29%20FROM%20INFORMATION_SCHEMA.COLUMNS%20WHERE%20table_name%3D0x626f6f6b73%20AND%20table_schema%3D0x626f6f6b776f726c645f6462--%20-
```

[Decode](https://www.urldecoder.org/) ta được

```sql
http://bookworldstore.com/search.php?search=book' UNION ALL SELECT NULL,CONCAT(0x7178766271,JSON_ARRAYAGG(CONCAT_WS(0x7a76676a636b,schema_name)),0x7176706a71) FROM INFORMATION_SCHEMA.SCHEMATA-- -
http://bookworldstore.com/search.php?search=book' UNION ALL SELECT NULL,CONCAT(0x7178766271,JSON_ARRAYAGG(CONCAT_WS(0x7a76676a636b,table_name)),0x7176706a71) FROM INFORMATION_SCHEMA.TABLES WHERE table_schema IN (0x626f6f6b776f726c645f6462)-- -
http://bookworldstore.com/search.php?search=book' UNION ALL SELECT NULL,CONCAT(0x7178766271,JSON_ARRAYAGG(CONCAT_WS(0x7a76676a636b,column_name,column_type)),0x7176706a71) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name=0x61646d696e AND table_schema=0x626f6f6b776f726c645f6462-- -
http://bookworldstore.com/search.php?search=book' UNION ALL SELECT NULL,CONCAT(0x7178766271,JSON_ARRAYAGG(CONCAT_WS(0x7a76676a636b,column_name,column_type)),0x7176706a71) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name=0x637573746f6d657273 AND table_schema=0x626f6f6b776f726c645f6462-- -
http://bookworldstore.com/search.php?search=book' UNION ALL SELECT NULL,CONCAT(0x7178766271,JSON_ARRAYAGG(CONCAT_WS(0x7a76676a636b,column_name,column_type)),0x7176706a71) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name=0x626f6f6b73 AND table_schema=0x626f6f6b776f726c645f6462-- -
```

Có thể thấy rằng chỉ có URI đầu tiên là xem toàn bộ database, các URI còn lại chỉ để xem tables, columns

## Flag

```sql
/search.php?search=book' UNION ALL SELECT NULL,CONCAT(0x7178766271,JSON_ARRAYAGG(CONCAT_WS(0x7a76676a636b,schema_name)),0x7176706a71) FROM INFORMATION_SCHEMA.SCHEMATA-- -
```

# Flag 6

## Mô tả

Assessing the impact of the breach and data access is crucial, including the potential harm to the organization's reputation. What's the table name containing the website users data?

## Phân tích

Vây là hacker đã có thể xem được các nội dung trong database, nếu muốn tiếp tục xem dữ liệu người dùng thì vẫn phải qua request sử dụng search.php thôi nên lần này ta sẽ lưu toàn bộ các URI request từ hacker sử dụng search.php để tìm ra table chứa dữ liệu người dùng

```bash
$ tshark -r WebInvestigation.pcap -Y 'ip.src == 111.224.250.131 && http.request.uri contains "search.php"' -T fields -e http.request.full_uri > sqli_payloads.txt
```

Decode và sau một lúc tìm kiếm thì sẽ thấy

## Flag

`customers`

# Flag 7

## Mô tả

The website directories hidden from the public could serve as an unauthorized access point or contain sensitive functionalities not intended for public access. Can you provide the name of the directory discovered by the attacker?

## Phân tích

Nhìn trong wireshark thì sẽ thấy được khá rõ ràng hacker đã làm gì tiếp theo

Xen giữa những lệnh SQL injection thì ta thấy hacker còn làm một vài request đến các trang khác trong `bookworldstore.com` tiêu biểu là lệnh GET đến /admin(packet 88648) và sau cái packet đó một lúc thì hacker đã truy cập được các thư mục như /admin/uploads

## Flag

`/admin/`

# Flag 8

## Mô tả

Knowing which credentials were used allows us to determine the extent of account compromise. What are the credentials used by the attacker for logging in?

## Phân tích

Ở đây hacker muốn đã đăng nhập vào bằng người dùng nào và tk:mk là gì thì cần kiểm tra các request POST

Kiểm tra các request POST đến /admin/login.php thì thấy hacker đã thử 1 vài tk:mk, ta sẽ lấy cái request POST cuối cùng, bởi vì sau đó thì hacker đã đăng nhập thành công

## Flag

`admin:admin123!`

# Flag 9

## Mô tả

We need to determine if the attacker gained further access or control of our web server. What's the name of the malicious script uploaded by the attacker?

## Phân tích

Ở đây ta lại phân tích request POST tiếp, thấy có một request POST đến /admin/index.php gửi file lên server đây chính là file độc mà mô tả nói đến

## Flag

`NVri2vhp.php`