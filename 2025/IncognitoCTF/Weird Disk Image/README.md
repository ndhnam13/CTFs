Bài cho ta một file .img

Tìm 1 chuỗi nhị phân, tìm một key, decode chuỗi nhị phân + xor với key sẽ ra flag

Sử dụng FTK imager để xem nội dung của đĩa

Trong thư mục `bin` có các file .elf fake các dòng lệnh cơ bản trong linux, tại file `unusually_long_ls` nếu xem hex hoặc strings và kéo xuống cuối sẽ có một chuỗi nhị phân, đây là một nửa của bài

```
00011011 01010000 00010111 01010110 00010101 00001000 00000111 01010100 01000011 00101101 00101011 00001011 01000001 01101011 00000100 00011001 00000010 00000000 00101101 00000010 00001101 01101111 00011101 01011101 01010000 01010011 00011010 00111011 01000001 00010101
```

Strings `weird_challenge.img` và ở cuối sẽ có key

```
encryption_key
r3c0nn3ct_th3_gr1d
```

Tạo một script để thực hiện decode và xor làm việc đó

`ictf{f477r_cr4ck3d_1n_s3c0nd5}`
