# Phân tích

```c
// bad sp value at call has been detected, the output may be wrong!
// positive sp value has been detected, the output may be wrong!
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char s[72]; // [rsp+10h] [rbp-50h] BYREF
  unsigned __int64 v5; // [rsp+58h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  printf("Please enter the secret key: ");
  fgets(s, 64, _bss_start);
  s[strcspn(s, "\n")] = 0;
  mprotect(
    (void *)((unsigned __int64)&check_flag & 0xFFFFFFFFFFFFF000LL),
    ((unsigned __int64)marker & 0xFFFFFFFFFFFFF000LL) + 4096 - ((unsigned __int64)&check_flag & 0xFFFFFFFFFFFFF000LL),
    7);
  ((void (__fastcall *)(void *, __int64 *, __int64 *))rotate_matrix)(&check_flag, matrix_length, matrix_length);
  if ( (unsigned __int8)((__int64 (__fastcall *)(char *))check_flag)(s) )
    puts("Yes");
  else
    puts("No");
  return 0;
}
```

Chương trình nó tự decode hàm check_flag bằng cái hàm rotate_matrix thì e đặt bp sau hàm rotate matrix xong dump cái disassemble của check_flag sau đó đưa lên cho chatgpt để nó đưa cái disassemble thành pseudocode

Cái check_flag sau khi decode nó sẽ check xem input có đủ 37 chữ cái ko xong rồi sẽ có mấy cái kiểu input[a] * input[b] == x giải cái này t nghĩ sẽ sử dụng

```py
#!/usr/bin/env python3
from z3 import *

# Khởi tạo một đối tượng solver
solver = Solver()

# Flag có độ dài 37 ký tự. Tạo 37 biến 8-bit (byte).
flag = [BitVec(f'flag_{i}', 8) for i in range(37)]

# Thêm ràng buộc: tất cả các ký tự phải là ký tự ASCII có thể in được
for i in range(37):
    solver.add(And(flag[i] >= 32, flag[i] <= 126))

# Chuyển đổi tất cả 149 điều kiện từ mã assembly thành các ràng buộc Z3
# --- Các điều kiện đã được trích xuất từ pseudocode ---

solver.add(flag[0] != If(flag[4] == 0x3a, 1, 0))
solver.add(flag[0] * flag[0xb] == 0x20a0)
solver.add(flag[0] + flag[0x15] == 0xba)
solver.add(flag[0] * flag[0xa] == 0x1ab8)
solver.add(flag[1] != If(flag[0x11] == 0x30, 1, 0))
solver.add(flag[1] + flag[0x21] == 0xc6)
solver.add(flag[1] * flag[0x16] == 0xfc0)
solver.add(flag[1] + flag[0xc] == 0xbc)
solver.add(flag[2] != If(flag[0x16] == 0x72, 1, 0))
solver.add(flag[2] + flag[4] == 0xb4)
solver.add(flag[2] != If(flag[0xc] == 0x2a, 1, 0))
solver.add(flag[2] != If(flag[0x12] == 0x71, 1, 0))
solver.add(flag[3] * flag[0x16] == 0x1710)
solver.add(flag[3] != If(flag[0xc] == 0x13, 1, 0))
solver.add(flag[3] + flag[0x18] == 0xe9)
solver.add(flag[3] + flag[0x13] == 0xda)
solver.add(flag[4] * flag[0xc] == 0x2e50)
solver.add(flag[4] + flag[0x1d] == 0xa5)
solver.add(flag[4] * flag[0x14] == 0x2b32)
solver.add(flag[4] * flag[5] == 0x1560)
solver.add(flag[5] != If(flag[0x18] == 0x5e, 1, 0))
solver.add(flag[5] != If(flag[1] == 0x64, 1, 0))
solver.add(flag[5] + flag[0x22] == 0x9c)
solver.add(flag[5] != If(flag[0x24] == 0x4d, 1, 0))
solver.add(flag[6] * flag[0xf] == 0x2cdc)
solver.add(flag[6] + flag[0xe] == 0xd3)
solver.add(flag[6] * flag[0x15] == 0x33a8)
solver.add(flag[6] + flag[0xa] == 0xd3)
solver.add(flag[7] * flag[8] == 0x1790)
solver.add(flag[7] + flag[0x10] == 0x64)
solver.add(flag[7] != If(flag[0] == 0x7c, 1, 0))
solver.add(flag[7] + flag[5] == 0x64)
solver.add(flag[8] != If(flag[1] == 0x20, 1, 0))
solver.add(flag[8] != If(flag[0xe] == 0x2b, 1, 0))
solver.add(flag[8] * flag[0x18] == 0x31d8)
solver.add(flag[8] + flag[0x21] == 0xe6)
solver.add(flag[9] + flag[0x15] == 0xa5)
solver.add(flag[9] * flag[0x1e] == 0x12ed)
solver.add(flag[9] * flag[0x1d] == 0xa29)
solver.add(flag[9] != If(flag[0x1b] == 0x47, 1, 0))
solver.add(flag[0xa] * flag[0xc] == 0x2698)
solver.add(flag[0xa] != If(flag[0xb] == 0x2b, 1, 0))
solver.add(flag[0xa] != If(flag[0x23] == 0x3b, 1, 0))
solver.add(flag[0xa] * flag[0x16] == 0x11d0)
solver.add(flag[0xb] + flag[7] == 0xa8)
solver.add(flag[0xb] * flag[0x13] == 0x2b0c)
solver.add(flag[0xb] != If(flag[0x17] == 0x1, 1, 0))
solver.add(flag[0xb] + flag[5] == 0xa4)
solver.add(flag[0xc] != If(flag[0x14] == 0x9, 1, 0))
solver.add(flag[0xc] * flag[9] == 0x14b8)
solver.add(flag[0xc] * flag[0x1d] == 0x14b8)
solver.add(flag[0xc] + flag[0x23] == 0xcc)
solver.add(flag[0xd] != If(flag[3] == 0x48, 1, 0))
solver.add(flag[0xd] * flag[0x10] == 0x990)
solver.add(flag[0xd] * flag[0x19] == 0x13ec)
solver.add(flag[0xd] + flag[0x1b] == 0xa7)
solver.add(flag[0xe] != If(flag[0x15] == 0x2d, 1, 0))
solver.add(flag[0xe] + flag[9] == 0x92)
solver.add(flag[0xe] * flag[0x11] == 0x251c)
solver.add(flag[0xe] + flag[0x13] == 0xbe)
solver.add(flag[0xf] + flag[6] == 0xd7)
solver.add(flag[0xf] != If(flag[0xc] == 0xb, 1, 0))
solver.add(flag[0xf] + flag[0x1f] == 0xda)
solver.add(flag[0xf] + flag[0x1d] == 0x96)
solver.add(flag[0x10] + flag[0x1f] == 0xa7)
solver.add(flag[0x10] != If(flag[0x21] == 0x42, 1, 0))
solver.add(flag[0x10] + flag[0x22] == 0x9c)
solver.add(flag[0x10] * flag[0xb] == 0x15c0)
solver.add(flag[0x11] + flag[0x24] == 0xe1)
solver.add(flag[0x11] + flag[0x12] == 0x97)
solver.add(flag[0x11] + flag[0x1d] == 0x97)
solver.add(flag[0x11] + flag[0x1e] == 0xc3)
solver.add(flag[0x12] + flag[0xe] == 0x92)
solver.add(flag[0x12] * flag[5] == 0x990)
solver.add(flag[0x12] + flag[0x1a] == 0x92)
solver.add(flag[0x12] + flag[3] == 0xae)
solver.add(flag[0x13] * flag[0x1f] == 0x2c29)
solver.add(flag[0x13] * flag[0x22] == 0x2814)
solver.add(flag[0x13] + flag[0x24] == 0xdc)
solver.add(flag[0x13] != If(flag[0x10] == 0x6f, 1, 0))
solver.add(flag[0x14] * flag[0xc] == 0x2768)
solver.add(flag[0x14] * flag[0x22] == 0x28ec)
solver.add(flag[0x14] * flag[7] == 0x13b4)
solver.add(flag[0x14] != If(flag[0x10] == 0x51, 1, 0))
solver.add(flag[0x15] != If(flag[0x24] == 0xf, 1, 0))
solver.add(flag[0x15] * flag[9] == 0x16b6)
solver.add(flag[0x15] != If(flag[0] == 0x3a, 1, 0))
solver.add(flag[0x15] * flag[0x17] == 0x341a)
solver.add(flag[0x16] * flag[0x20] == 0x14d0)
solver.add(flag[0x16] + flag[0x19] == 0x94)
solver.add(flag[0x16] != If(flag[1] == 0x64, 1, 0))
solver.add(flag[0x16] + flag[0x1a] == 0x8f)
solver.add(flag[0x17] + flag[0x22] == 0xe1)
solver.add(flag[0x17] != If(flag[0xb] == 0x1, 1, 0))
solver.add(flag[0x17] != If(flag[0x20] == 0x1a, 1, 0))
solver.add(flag[0x17] + flag[0x14] == 0xd6)
solver.add(flag[0x18] * flag[0x14] == 0x29ae)
solver.add(flag[0x18] * flag[0x19] == 0x2af8)
solver.add(flag[0x18] != If(flag[0x21] == 0x1c, 1, 0))
solver.add(flag[0x18] != If(flag[0x1a] == 0x31, 1, 0))
solver.add(flag[0x19] != If(flag[3] == 0x1f, 1, 0))
solver.add(flag[0x19] * flag[7] == 0x1450)
solver.add(flag[0x19] + flag[0xd] == 0x97)
solver.add(flag[0x19] + flag[0x17] == 0xd9)
solver.add(flag[0x1a] * flag[0x20] == 0x2931)
solver.add(flag[0x1a] != If(flag[0x21] == 0x2d, 1, 0))
solver.add(flag[0x1a] * flag[4] == 0x2a4e)
solver.add(flag[0x1a] + flag[3] == 0xda)
solver.add(flag[0x1b] != If(flag[0x17] == 0x1, 1, 0))
solver.add(flag[0x1b] + flag[0x13] == 0xd3)
solver.add(flag[0x1b] + flag[0xe] == 0xd3)
solver.add(flag[0x1b] != If(flag[0x21] == 0x6, 1, 0))
solver.add(flag[0x1c] * flag[0x15] == 0x2e50)
solver.add(flag[0x1c] + flag[0x11] == 0xcc)
solver.add(flag[0x1c] != If(flag[6] == 0x1c, 1, 0))
solver.add(flag[0x1c] * flag[0xf] == 0x2838)
solver.add(flag[0x1d] != If(flag[0x13] == 0x6c, 1, 0))
solver.add(flag[0x1d] != If(flag[0x17] == 0x46, 1, 0))
solver.add(flag[0x1d] != If(flag[0x1c] == 0x5b, 1, 0))
solver.add(flag[0x1d] * flag[0x15] == 0x16b6)
solver.add(flag[0x1e] + flag[0x1d] == 0x92)
solver.add(flag[0x1e] * flag[0xf] == 0x24bd)
solver.add(flag[0x1e] + flag[0xb] == 0xd3)
solver.add(flag[0x1e] * flag[0xa] == 0x2341)
solver.add(flag[0x1f] * flag[9] == 0x17b5)
solver.add(flag[0x1f] + flag[0xe] == 0xd6)
solver.add(flag[0x1f] * flag[0x12] == 0x17b5)
solver.add(flag[0x1f] + flag[0x11] == 0xdb)
solver.add(flag[0x20] * flag[0x10] == 0x14d0)
solver.add(flag[0x20] * flag[8] == 0x324c)
solver.add(flag[0x20] * flag[0x11] == 0x2b5c)
solver.add(flag[0x20] != If(flag[1] == 0x3b, 1, 0))
solver.add(flag[0x21] * flag[0xa] == 0x2a4e)
solver.add(flag[0x21] != If(flag[0x23] == 0x16, 1, 0))
solver.add(flag[0x21] != If(flag[0xc] == 0x1a, 1, 0))
solver.add(flag[0x21] * flag[0x11] == 0x2c88)
solver.add(flag[0x22] != If(flag[0x12] == 0x5f, 1, 0))
solver.add(flag[0x22] != If(flag[3] == 0x17, 1, 0))
solver.add(flag[0x22] + flag[5] == 0x9c)
solver.add(flag[0x22] != If(flag[0x1e] == 0x33, 1, 0))
solver.add(flag[0x23] != If(flag[9] == 0x57, 1, 0))
solver.add(flag[0x23] + flag[6] == 0xd8)
solver.add(flag[0x23] != If(flag[0xa] == 0x3b, 1, 0))
solver.add(flag[0x23] != If(flag[7] == 0x50, 1, 0))
solver.add(flag[0x24] != If(flag[0xa] == 0x22, 1, 0))
solver.add(flag[0x24] != If(flag[0x1f] == 0xa, 1, 0))
solver.add(flag[0x24] * flag[0x1e] == 0x2e63)
solver.add(flag[0x24] != If(flag[0x15] == 0xf, 1, 0))

# Kiểm tra xem có lời giải nào không
if solver.check() == sat:
    # Lấy mô hình lời giải
    model = solver.model()
    
    # Xây dựng lại chuỗi flag từ các giá trị đã giải
    result = ""
    for i in range(37):
        result += chr(model[flag[i]].as_long())
        
    print("✅ Flag đã được tìm thấy!")
    print(f"   {result}")
else:
    print("❌ Không tìm thấy lời giải. Có thể có lỗi trong quá trình phân tích.")
```

>**HTB{r0t4t3_th3_c0d3_ar0und_th3_world}**