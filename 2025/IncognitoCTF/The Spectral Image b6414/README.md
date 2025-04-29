Bài cho ta một file jpeg, nhưng khi kiểm tra bằng `xxd` thì biết được đây là một file .wav

Đổi lại đuôi file để nghe, nghe được nhiều tiếng bíp, thay đổi 3 lần, cường độ không thay đổi nên có thể nghĩ đến một vài tín hiệu truyền tải

Bài có nhắc đến việc sử dụng `old school transmissions`, sau một hồi tìm hiểu biết được đây là tín hiệu SSTV

Tìm một tool để decode SSTV: https://github.com/colaclanth/sstv

`sstv -d transmission.wav -o result.png`

Xem ảnh sẽ thấy flag

`ictf{cjFrX3kzX2YwX2Z0M195MDB6}`