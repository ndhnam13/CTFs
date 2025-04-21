# Phân tích
Thằng tạo ra cái này không có tạo client nên mình phải tự code

Qua tìm hiểu document thì ta có thể tự dựng 1 client để kết nối đến server `wss://spacegame.io:443`

Nói chung là khi kết nối thành công đến server sử dụng `SIGN_UP` thì sẽ nhận được `SIGN_UP_RESP` - Nếu đăng nhập không thành công thì sẽ là `Invalid signatre, incomplete player data,...`. Với cả `PLAYER_LOC`, cả 2 sẽ được gửi với rate là `~20 Hz` - Nếu gửi các tín hiệu điều khiển (Cần sử dụng nhiều trong part2 khi điều khiển tàu đến vị trí 15,2)

`PLAYER_LOC` Đây là vị trí của người chơi tại ô đó (Không phải mình) và tên player sẽ là flag luôn (Chỉ là một nửa nhưng có thể tìm thấy toàn bộ nếu lấy toàn bộ byte), phần còn lại nếu xem trong document có đề cập đến

```
name_part: The first up to 17 characters of the name + null terminator. If name > 17 characters, extra character are stored after ENTIRE player array
```

Nhìn chung cả 2 part sẽ  chỉ cần đăng nhập thành công, di chuyển đến một vị trí (part1 không cần, part2 là (15,2)) sau đó nhật `PLAYER_LOC` và giải mã ra thôi (Part2 sẽ phải điều chỉnh 1 chút `Hint part2: The documentation lies a little bit. If you are getting weird values, try switching endianess.`, vậy là chỉ cần chỉnh về little edian bởi trong document sử dụng big edian)

# Flag
Nhờ Claude viết cả 2 cái script xddd, chạy đến vị trí đúng thì sẽ tự động lấy toàn bộ chuỗi byte server gửi xong decode ra flag (Phải tự bỏ phần linh tinh ở giữa đi)

### Part1
`DawgCTF{FL4GS_1N_SP4444C3!!!!}`
### Part2
`DawgCTF{NO_ON3_C4N_H43R_YOU_SCRE4M}`
