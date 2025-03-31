
# Phân tích
Hiện tại đang tìm hiểu(chờ tác giả post official writeup) có thể tham khảo file pdf của một người khác làm nhưng đây không phải intended solution

Nói chung ở đây ta cần các byte `02` `độ dài mật khẩu` `mật khẩu` `độ dài flag.txt` `flag.txt` để gửi đến server

`fakePayload.txt` sẽ cho ta fake flag `swampCTF{y0u_kn0w_b3773r_7h4n_7h47}`

Nếu thử thay supersecretpw thành cái fake flag đó vào `testPayload.txt` ta sẽ có được một phần của mật khẩu, fake flag có độ dài `35` sang hex là `23`

`echo 02237377616D704354467B7930755F6B6E30775F6233373733725F3768346E5F376834377D08666c61672e747874 | xxd -r -p > testPayload.txt`

Rồi gửi `testPayload` đến server thì sẽ cho ta mật khẩu nhưng đã bị mã hoá: `i_do_realKe,Fzp4RhjbBxu`

`nc -u chals.swampctf.com 44255 < testPayload.txt > encPw.txt`

Đến đoạn này nhìn khá giống bị xor, bây giờ thử mật khẩu chỉ là `swampCTF` xem

`echo 02087377616D7043544608666c61672e747874 | xxd -r -p > testPayload2.txt`

`nc -u chals.swampctf.com 44255 < testPayload2.txt > encPw2.txt`

`i_do_readE44#n@0.Q6-evT5vS-)nOk(BjF"`

Mật khẩu lại bị thay đổi, có thể là `i_do_real_.....` và sau đó sẽ tiếp tục xor từng đoạn một để ra mật khẩu

# Flag
Ở đây ông viết cái pdf đoán luôn mật khẩu là `i_do_real_encryption` và được thật 

`echo 0214695F646F5F7265616C5F656E6372797074696F6E08666c61672e747874 | xxd -r -p > payload.txt`

`nc -u chals.swampctf.com 44255 < payload.txt > flag.txt`

`swampCTF{m070_m070_54y5_x0r_15_4_n0_n0}`