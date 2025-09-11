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
