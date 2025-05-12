# Phân tích
Bài cho ta file `Sus data` khi kiểm tra bằng xxd thì biết file thực ra là một png nhưng đã bị hỏng

https://en.wikipedia.org/wiki/PNG

http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html

Dựa vào đây cộng với file signature trên wiki, kết hợp với việc sử dụng `pngcheck -v(--verbose)` để check tình trạng sau mỗi lần sửa

Nói chung là các chunk của một file png sẽ bao gồm:
- 4byte lenght: `00 00 00 01`
- 4byte chunk type: `49 44 48 52` dịch ra là IDHR
- Chunk data có độ dài tuỳ chỉnh
- 4byte CRC: CRC là một CRC-32 theo thứ tự byte mạng (network byte order), được tính trên chunk type và chunk data, nhưng không bao gồm length

Ví dụ có

```
00 00 00 04    # Length = 4 bytes
67 41 4D 41    # Chunk Type = 'gAMA'
00 00 B1 8F    # Chunk Data
0B FC 61 05    # CRC
```

Thì sẽ được tính là `67 41 4D 41 00 00 B1 8F`

## Lần 1
```
Sus data  this is neither a PNG or JNG image nor a MNG stream
ERROR: Sus data
```

Lần thứ nhất ta sẽ phải sửa lại header thành PNG

`89 50 4E 47 0D 0A 1A 0A`

## Lần 2
```
File: Sus data (321007 bytes)
  chunk RHDR at offset 0x0000c, length 10:  first chunk must be IHDR
ERRORS DETECTED in Sus data
```

Sửa lại chunk IDHR 

`49`

## Lần 3
```
File: Sus data (321007 bytes)
  chunk IHDR at offset 0x0000c, length 10:  invalid length
ERRORS DETECTED in Sus data
```

Sửa lenght của chunk IDHR, lenght phải là 13 (Luôn luôn dài 13byte theo định dạng của png) 

`0D`

## Lần 4
```
File: Sus data (321007 bytes)
  chunk IHDR at offset 0x0000c, length 13
    500 x 500 image, 24-bit RGB, non-interlaced
  chunk sRGB at offset 0x00025, length 26:  invalid length
ERRORS DETECTED in Sus data
```

Sửa lenght của chunk sRGB bắt buộc là 1

`01`

## Lần 5
```
File: Sus data (321007 bytes)
  chunk IHDR at offset 0x0000c, length 13
    500 x 500 image, 24-bit RGB, non-interlaced
  chunk sRGB at offset 0x00025, length 1
    rendering intent = perceptual
  chunk MAMA at offset 0x00032, length 4:  illegal (unless recently approved) unknown, public chunk
ERRORS DETECTED in Sus data
```

Tìm chunk MAMA trong libpng thì không tồn tại nhưng lại có gAMA, thử đổi về nó thì thành công

`67`

## Lần 6
```
File: Sus data (321007 bytes)
  chunk IHDR at offset 0x0000c, length 13
    500 x 500 image, 24-bit RGB, non-interlaced
  chunk sRGB at offset 0x00025, length 1
    rendering intent = perceptual
  chunk gAMA at offset 0x00032, length 4: 0.45455
  CRC error in chunk gAMA (computed 0bfc6105, expected 0bbc6105)
ERRORS DETECTED in Sus data
```

Báo khá rõ ràng là CRC error chỉ cần đổi từ `BC` thành `FC` để đúng với CRC được computed

`FC`

## Lần 7 (Cuối cùng)
```
File: Sus data (321007 bytes)
  chunk IHDR at offset 0x0000c, length 13
    500 x 500 image, 24-bit RGB, non-interlaced
  chunk sRGB at offset 0x00025, length 1
    rendering intent = perceptual
  chunk gAMA at offset 0x00032, length 4: 0.45455
  chunk pHYs at offset 0x00042, length 9: 3779x3779 pixels/meter (96 dpi)
  chunk IDAT at offset 0x00057, length 65445
    zlib: deflated, 32K window, fast compression
    zlib: inflate error = -3 (data error)
ERRORS DETECTED in Sus data
```

Lỗi zlib, khá chắc chắn là do ở trong IDAT hoặc IEND nên kiểm tra 2 phần này luôn thì phát hiện thấy chunk IEND bị thiếu 4 byte cuối, có thể check hex của một file png bình thường thì ta biết 4 byte này là `AE 42 60 82`

Thêm 4 byte vào sau IEND rồi chạy lại pngcheck thì vẫn báo lỗi như trên, vậy là vấn đề đang nằm trong IDAT, nếu thử tìm 4 byte trên trong IDAT thì sẽ thấy nó có xuất hiện một lần, vậy vấn đề ở đây chính là 4 byte sau IEND đã bị di chuyển vào trong IDAT, cuối cùng ta chỉ cần xoá 4 byte đấy trong IDAT là sẽ sửa `Sus data` thành công

```
File: Sus data (321007 bytes)
  chunk IHDR at offset 0x0000c, length 13
    500 x 500 image, 24-bit RGB, non-interlaced
  chunk sRGB at offset 0x00025, length 1
    rendering intent = perceptual
  chunk gAMA at offset 0x00032, length 4: 0.45455
  chunk pHYs at offset 0x00042, length 9: 3779x3779 pixels/meter (96 dpi)
  chunk IDAT at offset 0x00057, length 65445
    zlib: deflated, 32K window, fast compression
  chunk IDAT at offset 0x10008, length 65524
  chunk IDAT at offset 0x20008, length 65524
  chunk IDAT at offset 0x30008, length 65524
  chunk IDAT at offset 0x40008, length 58835
  chunk IEND at offset 0x4e5e7, length 0
No errors detected in Sus data (10 chunks, 57.2% compression).
```

# Flag
Mở ảnh lên thì thấy flag

![image](solved.png)

`BtSCTF{Hecker_Picasso_3175624}`