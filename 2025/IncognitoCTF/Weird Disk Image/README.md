Bài cho ta một file .img

Tìm 1 chuỗi nhị phân, tìm một key, decode chuỗi nhị phân + xor với key sẽ ra flag

Sử dụng FTK imager để xem nội dung của đĩa

Trong thư mục `bin` có các file .elf fake các dòng lệnh cơ bản trong linux, tại file `unusually_long_ls` nếu xem hex hoặc strings và kéo xuống cuối sẽ có một chuỗi nhị phân, đây là một nửa của bài

Strings `weird_challenge.img` và ở cuối sẽ có key

```
encryption_key
r3c0nn3ct_th3_gr1d
```

Tạo một script để thực hiện decode và xor làm việc đó

`ictf{f477r_crtck3d_1n_s3c0ld5}`