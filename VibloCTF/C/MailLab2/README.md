# Mô tả

A seemingly innocuous letter is actually a communication letter between two suspects. However, the body of the message appears to have been forged. There are 4 letters edited with `*`, please help me recover it

Bài cho ta một file .eml

# Phân tích

Mở lên thấy flag nhưng bị che mất 4 kí tự

`Flag{38e96c6f6a60736a612d6b7****263f8}`

Do bài có nói đến việc email đã bị chỉnh sửa, thay đổi (forged) cho nên phải đọc file .eml này dưới dạng raw

chatlgbt làm ra idk https://chatgpt.com/share/685e1650-2d50-800d-b80e-678947977694

Chưa đọc được raw trên máy. Nhưng nói chung là khi đọc trong outlook như bình thường thì trong phần `Content-Type: text/html; charset="UTF-8" | Content-Transfer-Encoding: quoted-printable` sẽ tự động chuyển các kí tự kia về `****` nếu đọc raw sẽ thấy lúc này bốn dấu `*` chỉ là placeholder, trong bản raw thực tế bạn sẽ thấy chúng được viết dưới dạng chuỗi escape của quoted-printable

```
Flag{…b7=61=33=32=65=26=33=66=38…}
```

Với các mã `=61`, `=33`, `=32`, `=65` xen kẽ giữa các ký tự còn lại

**Giải mã các escape của quoted-printable:**

- `=61` → hex 0x61 → ký tự `'a'`
- `=33` → hex 0x33 → ký tự `'3'`
- `=32` → hex 0x32 → ký tự `'2'`
- `=65` → hex 0x65 → ký tự `'e'`

Thay `****` bằng `"a32e"`, ta có flag

`Flag{38e96c6f6a60736a612d6b7a32e263f8}`