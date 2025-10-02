# Đáp án

## When does the suspicious process start?

Check `windows.cmdline` thấy `mmc.exe` load một file khá lạ không thường có trong windows là `family_image.obj`

Kiểm tra bằng `windows.pslist` để xem một số thông tin của process `mmc.exe`

**mmc.exe, PID: 3120**

>2024-09-05 15:58:11

## What is the size of the archive file containing the malware in bytes?

Bởi vì đề bài nhắc đến người dùng đã xoá mọi thứ liên quan đến file mã độc, dù có nhắc đến email và trong pslist có phần mềm mail `outlook` đang chạy nhưng tôi không thể dump được bằng vola

Cho nên chúng ta sẽ phải check trong strings của memdump. Trước hết tôi check một vài header HTTP như là `POST PUT HEAD GET` thì có hiện ra là người dùng tải về 1 file `family_image.zip` tiếp tục strings tên file thì sẽ thấy độ lớn

Khi strings tên của người dùng là `Binz` thì cũng tìm thấy được 1 email khả năng là cũng đính kèm cái mã độc đó

>1971433

## The user unzipped the archive containing the malware. Write down the names of the files contained in the unzipped archive and sort them alphabetically.?

Biết `family_image.zip` được tải về, vậy có thể nếu tìm strings liên quan đến file `.zip` sẽ thấy các file con ở bên trong nó

```py
strings memory.raw | grep -i "family_image" -C 8
```

>family_image.msc,family_image.obj

# How many NAT (native) modules are loaded into suspicious process in total?

```sh
vol -f .\memory.raw windows.dlllist --pid 3120 | findstr mmc.exe > list.txt
```

Có 102 module được load nhưng 4 module là của .NET không phải native

>98

## Submit the assembly address of all CLR modules in Ascending order.

```sh
D:\CTF\Tools\MemProcFS\MemProcFS.exe -device .\memory.raw -forensic 1
```

Copy file minidump từ của pid 3120 về

Mở windbg

`0:000> !DumpDomain`

để load các module .NET

Check mmc.exe ko thấy dấu hiệu malware vậy có thể là dll sideloading

>0000000004E62FD0,0000000004E630F0,0000000004E63690,0000000004E638D0,0000000004E63B10

## What is the name of the malicious module loaded?

Kiểm tra các module được load thấy một module có tên khá lạ

>Ad00bce9305554c87927205710b17699f

## Dump malicious dll using dlldump only helps you get the correct size of image but the data inside is messed up. Try to use other way to dump dll from memory and submit md5 of dll

```windbg
0:000> !SaveModule 00000000`06630000 C:\Users\admin\Desktop\Ad00bce9305554c87927205710b17699f.dll
```

>e67f5692a35b8e40049e30ad04c12b41

## What is the xor key used to obfuscate strings in the dll?

Load vào dnSpy

>a7ad965a-50b4-4846-bfb2-2282839f8d0c

## What is the IP of C2 server and port the malware connects to?

Up lên vt thấy phân loại là cobalt strike dùng 1768.py để xem 
Dùng trực tiếp lên memorydump

```sh
python D:\CTF\Tools\1768.py memory.raw
```

>149.28.22.48:8484

## What is the md5 hash of shellcode used for the final stage?

Tìm trong dnSpy thấy một class internal `Abddcbaea7acb47039a7d3800a0862e5b` thực hiện tìm string `A$+` sau đó xoá, đảo ngược rồi decode B64

```sh
strings minidump.dmp | grep "A$+" > out.txt
```

Sau khi strings ra thấy nhiều biến `B_xxx=....A$+....` khá lạ và một số `B_xxx=` xuất hiện nhiều lần nhưng có nội dung giống nhau, sau đó tôi nhờ chatgpt sort lại theo thứ tự tăng dần, lấy các chuỗi `B_xxx=` duy nhất và ghép nội dung của chúng lại với nhau (Đằng sau dấu `=`) sau đó áp dụng tương tự cái chức năng của internal class trên sẽ ra chính xác shellcode của final stage

Dùng [cyberchef](https://gchq.github.io/CyberChef/#recipe=Find_/_Replace(%7B'option':'Simple%20string','string':'A$%2B'%7D,'',true,false,true,false)Reverse('Character')From_Base64('A-Za-z0-9%2B/%3D',true,false)MD5())

>f7efce4bac431a5c703e73cce7c5f7c7