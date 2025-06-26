# Mô tả

A true cosmopolitan should speak many languages. And I do... but everywhere I go, people seem to understand different things...

Could you help me find a consensus they can all agree on? Someone might even give you a flag for it.

# Phân tích



Bài cho 1 file `variants` lúc đầu chạy thử nhưng mà không có gì

```bash
$ file variants
variants: DOS/MBR boot sector; partition 1 : ID=0x7f, active, start-CHS (0x0,0,1), end-CHS (0x3ff,255,63), startsector 0, 4294967295 sectors

$ binwalk variants

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Microsoft executable, portable (PE)
104367        0x197AF         Copyright string: "Copyright 2024 Justine Alexandra Roberts Tunney"
104560        0x19870         Copyright string: "copyright notice and this permission notice appear in all copies."
105227        0x19B0B         Copyright string: "Copyright (C) 1997, 1998, 2000 by Lucent Technologies"
105307        0x19B5B         Copyright string: "Copyright 2005-2014 Rich Felker, et. al."
163840        0x28000         ELF, 64-bit LSB executable, version 1 (FreeBSD)
218903        0x35717         Unix path: /usr/bin/ape
219119        0x357EF         Copyright string: "Copyright 2022 ARM Limited"
219260        0x3587C         Copyright string: "Copyright (C) 1997, 1998, 2000 by Lucent Technologies"
219340        0x358CC         Copyright string: "Copyright 2005-2014 Rich Felker, et. al."
226488        0x374B8         gzip compressed data, maximum compression, from Unix, last modified: 1970-01-01 00:00:00 (null date)
```

Binwalk có ra một đoạn `usr/bin/ape`, thử trên linux thì `ape` không tồn tại nhưng mà khi lên mạng tìm thì thấy có một repo github về file [APE](https://github.com/jart/cosmopolitan/blob/master/ape/specification.md)

Actually Portable Executable (APE) là một định dạng tập tin thực thi kiểu polyglot kết hợp giữa file PE của Windows với một đoạn shell script kiểu UNIX Sixth Edition, không sử dụng shebang (`#!`). Tạo ra một file binary có thể chạy được trên các hệ điều hành và kiến trúc khác nhau

Về signature thì file APE có nhiều kiểu khác nhau nhưng phổ biến nhất là

### (1) APE MZ Magic

- ASCII: `MZqFpD='`
- Hex: 4d 5a 71 46 70 44 3d 27

Xem hexdump của file `variants`

```bash
$ xxd variants | head
00000000: 4d5a 7146 7044 3d27 0a00 0010 00f8 0000  MZqFpD='........
```

Đúng là có signature của APE, thử bật chế độ debug trong bash xem nó chạy như nào

```bash
$ bash -x ./variants
+ MZqFpD='
@JT'
+ PINE='This is all stupid'
++ command -v ./variants
+ o=./variants
+ type ape
++ sysctl -n hw.machine_arch
++ read arch
++ '[' -n '' ']'
++ sysctl -n hw.machine
++ read arch
++ '[' -n '' ']'
++ uname -m
+ m=x86_64
+ '[' x86_64 = x86_64 ']'
+ t=/home/nam/./variants
+ '[' x '!=' x--assimilate ']'
+ mkdir -p /home/nam/.
+ cp -f ./variants /home/nam/./variants.522
+ mv -f /home/nam/./variants.522 /home/nam/./variants
+ o=/home/nam/./variants
+ exec
+ printf '\177ELF\2\1\1\11\0\0\0\0\0\0\0\0\2\0>\0\1\0\0\0\345$@\0\0\0\0\0\200\6\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\100\0\70\0\5\0\0\0\0\0\0\0'
+ exec
+ '[' -d /Applications ']'
+ '[' x = x--assimilate ']'
+ exec /home/nam/./variants
```

Khi chạy, `variants` sẽ kiểm tra kiến trúc hệ thống, sao chép chính nó vào thư mục home của người dùng `home/nam/`, sau đó thực hiện một số thao tác chuẩn bị (như ghi header ELF vào output) và cuối cùng dùng `exec` để thay thế tiến trình hiện tại bằng chính tập tin đó, lúc này hệ điều hành sẽ nhận diện phần nhị phân và thực thi phần ELF

Copy file elf từ `/home/nam` về, đổi tên để kiểm tra

```bash
┌──(nam㉿DESKTOP-NF3DDH9)-[/mnt/c/Users/admin/Desktop/variants]
└─$ file elf
elf: ELF 64-bit LSB executable, x86-64, version 1 (FreeBSD), for OpenBSD, statically linked, no section header

┌──(nam㉿DESKTOP-NF3DDH9)-[/mnt/c/Users/admin/Desktop/variants]
└─$ xxd elf | head
00000000: 7f45 4c46 0201 0109 0000 0000 0000 0000  .ELF............
```

Đây là file elf chuẩn
