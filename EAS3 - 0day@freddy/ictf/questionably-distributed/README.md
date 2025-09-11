# Mô tả

Distributed computing is the new tech on the horizon, so I decided to distribute the computer itself. Enjoy this horrendous simulation of a CPU running locally over TCP. This is not a steg chall.

# Phân tích

Chạy thử file exe thì nó tạo thêm 3 cửa sổ trống không

Sau khi load vào x64dbg xem entrypoint rồi đối chiếu sang IDA thì tìm được hàm khởi tạo và hàm `main()`

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int v4; // eax
  int v5; // eax
  int v6; // eax
  char Str[8]; // [rsp+20h] [rbp-60h] BYREF
  __int64 v8; // [rsp+28h] [rbp-58h]
  __int64 v9; // [rsp+30h] [rbp-50h]
  __int64 v10; // [rsp+38h] [rbp-48h]
  __int64 v11; // [rsp+40h] [rbp-40h]
  __int64 v12; // [rsp+48h] [rbp-38h]
  __int64 v13; // [rsp+50h] [rbp-30h]
  __int64 v14; // [rsp+58h] [rbp-28h]
  __int64 v15; // [rsp+60h] [rbp-20h]
  __int64 v16; // [rsp+68h] [rbp-18h]
  __int64 v17; // [rsp+70h] [rbp-10h]
  __int64 v18; // [rsp+78h] [rbp-8h]
  __int64 v19; // [rsp+80h] [rbp+0h]
  __int64 v20; // [rsp+88h] [rbp+8h]
  __int64 v21; // [rsp+90h] [rbp+10h]
  __int64 v22; // [rsp+98h] [rbp+18h]
  __int64 v23; // [rsp+A0h] [rbp+20h]
  __int64 v24; // [rsp+A8h] [rbp+28h]
  __int64 v25; // [rsp+B0h] [rbp+30h]
  __int64 v26; // [rsp+B8h] [rbp+38h]
  __int64 v27; // [rsp+C0h] [rbp+40h]
  __int64 v28; // [rsp+C8h] [rbp+48h]
  __int64 v29; // [rsp+D0h] [rbp+50h]
  __int64 v30; // [rsp+D8h] [rbp+58h]
  __int64 v31; // [rsp+E0h] [rbp+60h]
  __int64 v32; // [rsp+E8h] [rbp+68h]
  __int64 v33; // [rsp+F0h] [rbp+70h]
  __int64 v34; // [rsp+F8h] [rbp+78h]
  __int64 v35; // [rsp+100h] [rbp+80h]
  __int64 v36; // [rsp+108h] [rbp+88h]
  __int64 v37; // [rsp+110h] [rbp+90h]
  __int64 v38; // [rsp+118h] [rbp+98h]
  struct WSAData Command; // [rsp+120h] [rbp+A0h] BYREF
  int v40; // [rsp+2B8h] [rbp+238h] BYREF
  int v41; // [rsp+2BCh] [rbp+23Ch] BYREF
  struct sockaddr name; // [rsp+2C0h] [rbp+240h] BYREF
  SOCKET port_5555; // [rsp+2D0h] [rbp+250h]
  SOCKET port_6666; // [rsp+2D8h] [rbp+258h]
  _DWORD v45[4]; // [rsp+2F0h] [rbp+270h]
  int m; // [rsp+300h] [rbp+280h]
  int k; // [rsp+304h] [rbp+284h]
  int j; // [rsp+308h] [rbp+288h]
  int i; // [rsp+30Ch] [rbp+28Ch]

  sub_7FF621682A30();
  v45[0] = 5555;
  v45[1] = 6666;
  v45[2] = 7777;
  if ( argc == 1 )
  {
    for ( i = 0; i <= 2; ++i )
    {
      custom_sprintf((__int64)&Command, "start chal.exe %d\n", v45[i]);
      system((const char *)&Command);
    }
    Sleep(500u);
    for ( j = 0; j <= 2; ++j )                  // Create socket clients
    {
      WSAStartup(0x101u, &Command);
      *(&port_5555 + j) = socket(2, 1, 6);
      if ( *(&port_5555 + j) == -1 )
        return 1;
      name.sa_family = 2;
      *(_DWORD *)&name.sa_data[2] = inet_addr("127.0.0.1");
      *(_WORD *)name.sa_data = htons(v45[j]);
      v45[3] = connect(*(&port_5555 + j), &name, 16);
    }
    *(_QWORD *)Str = 0;
    v8 = 0;
    v9 = 0;
    v10 = 0;
    v11 = 0;
    v12 = 0;
    v13 = 0;
    v14 = 0;
    v15 = 0;
    v16 = 0;
    v17 = 0;
    v18 = 0;
    v19 = 0;
    v20 = 0;
    v21 = 0;
    v22 = 0;
    v23 = 0;
    v24 = 0;
    v25 = 0;
    v26 = 0;
    v27 = 0;
    v28 = 0;
    v29 = 0;
    v30 = 0;
    v31 = 0;
    v32 = 0;
    v33 = 0;
    v34 = 0;
    v35 = 0;
    v36 = 0;
    v37 = 0;
    v38 = 0;
    memset(&Command, 0, 256);
    for ( k = 0; k <= 27; ++k )
    {                                           // Matrix 28x28
      for ( m = 0; m <= 27; ++m )
      {
        custom_sprintf((__int64)Str, "%d %d", k, m);
        v4 = strlen(Str);
        send(port_5555, Str, v4 + 1, 0);
        recv(port_5555, (char *)&Command, 256, 0);
        custom_sscanf(&Command, "%d", (unsigned int)&v41);
        custom_sprintf((__int64)Str, "%d %d ^", v41, 66);
        v5 = strlen(Str);
        send(port_6666, Str, v5 + 1, 0);
        recv(port_6666, (char *)&Command, 256, 0);
        custom_sscanf(&Command, "%d", (unsigned int)&v41);
        custom_sprintf((__int64)Str, "%d %d +", v41, 15);
        v6 = strlen(Str);
        send(port_6666, Str, v6 + 1, 0);
        recv(port_6666, (char *)&Command, 256, 0);
        custom_sscanf(&Command, "%d", (unsigned int)&v41);
      }
    }
    return 0;
  }
  if ( argc != 2 )
    return -1;
  v40 = 0;
  custom_sscanf(argv[1], "%d", (unsigned int)&v40);
  if ( v40 == 7777 )
  {
    worker_cmp_server(7777);
  }
  else
  {
    if ( v40 > 7777 )
      return -1;
    if ( v40 == 5555 )
    {
      worker_matrix_lookup_server(5555);
    }
    else
    {
      if ( v40 != 6666 )
        return -1;
      worker_arithmetic_server(0x1A0Au);
    }
  }
  return 0;
}
```

1. Nếu không có tham số
   - Spawn 3 process con
   - Tạo 3 socket client kết nối đến `127.0.0.1:5555`, `:6666`, `:7777`
   - Với mỗi ô `(k, m)` trong ma trận 28x28:
     - Gửi `(k, m)` cho **port 5555**
        Nhận về giá trị `val`
     - Gửi `(val, 66, ^)` cho **port 6666**
        Nhận về `val2 = val ^ 66`
     - Gửi `(val2, 15, +)` cho **port 6666** lần nữa
        Nhận về `val3 = val2 + 15`
     - Lặp lại cho toàn bộ 28×28 = 784 lần

```
Tổng quan 3 worker

5555 → tra cứu ma trận 28×28

6666 → thực hiện phép toán +, -, ^(xor)

7777 → so sánh >, <, =
```

2. Nếu có tham số (5555, 6666, 7777)
   - Chạy 1 trong 3 process con với port trên

Kiểm tra hàm xử lí port 5555

```c
     v69 = recv(s, buf, 256, 0);
      custom_sscanf((__int64)buf, "%d %d", &v36, &v35);
      custom_sprintf((__int64)Str, "%d", byte_7FF621690020[28 * v36 + v35]);
      v2 = strlen(Str);
      v69 = send(s, Str, v2 + 1, 0);
```

Hàm này thực hiện chờ client gửi một chuỗi (VD `1 1`) sau đó gửi lại cho client byte tại vị trí đó trong ma trận 28x28 từ `byte_7FF621690020` 

Để lấy flag thì ta sẽ xuất các byte trong `byte_7FF621690020` ra rồi xor 66 và +15 như xử lí không arguments. Flag sẽ nằm trong đường chéo chính. Script sau sẽ lấy từ file txt (đang ở dưới dạng hex), chuyển về decimal sau đó xor 66 và +15 rồi chuyển sang ascii sau đó ghép các kí tự trong đường chéo chính `a[i][i]` vào

```py
# make_matrix.py
import re
from pathlib import Path
from typing import List

W, H = 28, 28
XOR_K = 66
ADD_K = 15

def load_hex_bytes(path: str) -> List[int]:
    """
    Đọc file chứa các byte hex (ví dụ: '64 42 9F ...') và trả về list int 0..255.
    Hỗ trợ cả các biến thể có hậu tố 'h' hay '0x' (nếu có).
    """
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    # Bóc tất cả chuỗi hexdigits (cho phép có hậu tố 'h' kiểu disasm)
    tokens = re.findall(r'(?:0x)?([0-9A-Fa-f]{1,2})h?', text)
    vals = [int(tok, 16) for tok in tokens]
    if len(vals) != W * H:
        raise ValueError(f"Expected {W*H} bytes, got {len(vals)}")
    return vals

def reshape(vals: List[int], w: int, h: int) -> List[List[int]]:
    return [vals[r*w:(r+1)*w] for r in range(h)]

def transform_char(v: int) -> int:
    # Mô phỏng (char)(((int)v ^ 66) + 15) – wrap về 8-bit như khi gán vào char
    return (((v ^ XOR_K) + ADD_K) & 0xFF)

def main():
    src = "matrix.txt"   # đổi đường dẫn nếu cần
    vals = load_hex_bytes(src)
    mat_before = reshape(vals, W, H)  # ma trận decimal “trước”

    # Áp dụng phép biến đổi cho từng phần tử
    mat_after = [[transform_char(v) for v in row] for row in mat_before]

    # In chuỗi đường chéo chính (giống printf("%c", buf[i][i]) trong C)
    diagonal_bytes = [mat_after[i][i] for i in range(H)]
    diagonal_text = "".join(chr(b) for b in diagonal_bytes)
    print("Diagonal as text:")
    print(diagonal_text)
    
if __name__ == "__main__":
    main()
```

Vì sao lấy đường chéo thì đoán vậy xd

```
PS C:\Users\admin\Desktop> python .\solve.py
Diagonal as text:
51ngl3_4PP_mul71pl3_53rv1c35
```

> **ictf{51ngl3_4PP_mul71pl3_53rv1c35}**