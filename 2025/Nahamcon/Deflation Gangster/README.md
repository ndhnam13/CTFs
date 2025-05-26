`strings gangster.zip` ra b64 `DEFGZmxhZ3thZjExNTBmMDdmOTAwODcyZTE2MmUyMzBkMGVmOGY5NH0K`

Decrypt ra flag xddddddddd

`flag{af1150f07f900872e162e230d0ef8f94}`

# Phân tích

Nhưng mà thực ra gì tác giả muốn mình sử dụng một tool gọi là https://github.com/Octoberfest7/zip_smuggling 

Nói chung là cái này có tác dụng 

```
tạo các tệp zip có chứa dữ liệu bổ sung được nhúng bên trong cấu trúc tệp. Dữ liệu bổ sung này không hiển thị hoặc không được hiển thị khi tệp zip được kiểm tra hoặc giải nén, nhưng có thể được truy xuất bằng PowerShell thông qua một tệp phím tắt của Windows (tệp LNK) nằm trong tệp zip
```

Cái file .lnk khi extract ra thì nó chả có tác dụng gì hết, có lẽ bài này nhiều người không giải được do họ tải về, extract ra xong xoá file zip đi (me 2)

```
Locates an egghunter byte sequence (0x55/0x55/0x55/0x55) marking the start of the smuggled data
```

Dữ liệu ẩn được đánh dấu bằng chuỗi `0x55/0x55/0x55/0x55`
