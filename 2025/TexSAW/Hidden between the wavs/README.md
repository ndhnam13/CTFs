# Mô tả
We've found the burglary suspect's voice notes. But oh no! One of them has been zipped up with a password. After throwing hashcat at it for a whole week, it's clear he covered his tracks by using a super secure password. But this format was made long before Bernstein freed us all... so perhaps you can find a back way in?

flag format: TexSAW{This_is_the_flag}

# Phân tích
Ta có một file zip yêu cầu mật khẩu rất dài, không thể bruteforce được

`But this format was made long before Bernstein freed us all...` ý nói đến Daniel J. Bernstein(tạo ra ChaCha20, Curve25519, Ed25519) đã giải phóng chúng ta khỏi cái gì đó, có thể nghĩ đến một phương pháp mã hoá zip là zipcrypto

Thử dùng bkcrack kiểm tra thì biết được file zip được mã hoá = zipcrypto và file `aaaac.wav` nén dưới dạng store

Vậy ta có thể dùng known plaintext attack 

sau khi có file `aaaac.wav` `exiftool` ra flag

# Flag
Theo https://en.wikipedia.org/wiki/WAV
```
[Master RIFF chunk]
   FileTypeBlocID  (4 bytes) : Identifier « RIFF »  (0x52, 0x49, 0x46, 0x46)
   FileSize        (4 bytes) : Overall file size minus 8 bytes
   FileFormatID    (4 bytes) : Format = « WAVE »  (0x57, 0x41, 0x56, 0x45)

[Chunk describing the data format]
   FormatBlocID    (4 bytes) : Identifier « fmt␣ »  (0x66, 0x6D, 0x74, 0x20)
   BlocSize        (4 bytes) : Chunk size minus 8 bytes, which is 16 bytes here  (0x10)
   AudioFormat     (2 bytes) : Audio format (1: PCM integer, 3: IEEE 754 float)
   NbrChannels     (2 bytes) : Number of channels
   Frequency       (4 bytes) : Sample rate (in hertz)
   BytePerSec      (4 bytes) : Number of bytes to read per second (Frequency * BytePerBloc).
   BytePerBloc     (2 bytes) : Number of bytes per block (NbrChannels * BitsPerSample / 8).
   BitsPerSample   (2 bytes) : Number of bits per sample

[Chunk containing the sampled data]
   DataBlocID      (4 bytes) : Identifier « data »  (0x64, 0x61, 0x74, 0x61)
   DataSize        (4 bytes) : SampledData size
   SampledData
```
Chỉ cần 12byte là đủ, nhưng có thể lấy 16byte đầu để crack nhanh hơn vì ta biết được độ lớn của file `aaaac.wav` là 192566

`FileSize(4 bytes) : Overall file size minus 8 bytes` 192566-8=192558 đổi ra hex là `2F02E` nhưng mới chỉ có 2,5 byte lấy dạng `signed 2's complement` ta có `0002F02E` nhưng đây đang ở big edian vậy ta phải chuyển về little edian `File size byte yêu cầu độ lớn ở dạng little edian` là:   `2EF00200`

`echo 524946462EF0020057415645666d7420 | xxd -r -p > plain`

Thêm một file zip chứa `plain`: `zip -0 known.zip plain`

Bắt đầu crack

`./bkcrack -C secret_note.zip -c aaaac.wav -P known.zip -p plain`

Được key: `f93bbe2a 0da8b6e7 2ae51dac`

Crack = 3 key:

`./bkcrack -C secret_note.zip -c aaaac.wav -k f93bbe2a 0da8b6e7 2ae51dac -d decrypted.wav`

`exiftool decrypted.wav` ra flag

`TexSAW{Th3_s1l3nce_SH4ll_l3ad_TH3_W4y}`