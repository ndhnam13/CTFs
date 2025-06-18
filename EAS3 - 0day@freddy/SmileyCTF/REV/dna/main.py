#!/usr/bin/env python3
import sys
import sympy as sp

# ====== Cấu hình ======
# Đường dẫn file dna, hoặc truyền qua argv
DNA_PATH = 'vm.dna'
# Số byte flag (không tính prefix/suffix). 
# 56 - .;,;.{} = 49
n_vars = 49

# Base address memory gốc (như snippet bạn dùng m[640+i])
BASE_ADDR = 640

# ====== Hàm trans và decode ======
# mapping ban đầu
mapping = {'A': 0, 'T': 1, 'G': 2, 'C': 3}

def trans(s: str) -> int:
    val = 0
    for i, c in enumerate(s):
        if c not in mapping:
            raise ValueError(f"Không phải nucleotide: {c}")
        val |= (mapping[c] << (2 * i))
    return val

def decode_instructions(data: str):
    instructions = []
    pc = 0
    L = len(data)
    while pc < L:
        if pc + 2 > L:
            break
        seg_op = data[pc:pc+2]
        opcode = trans(seg_op)
        # Xác định độ dài lệnh
        if opcode in {1,4,5,6,7,8,12,13,14,15}:
            step = 2
        else:
            step = 12
        if step == 12:
            if pc + 12 > L:
                print(f"Warning: thiếu operand tại pc={pc}, dừng decode.")
                break
            seg_operand = data[pc+2:pc+12]
            operand = trans(seg_operand)
            instructions.append({'pc': pc, 'opcode': opcode, 'operand': operand})
        else:
            instructions.append({'pc': pc, 'opcode': opcode, 'operand': None})
        if opcode == 15:
            print(f"Encounter break opcode tại pc={pc}, dừng decode.")
            break
        pc += step
    return instructions

# ====== Hàm format nested sum ======
def nested_sum_str(expr, flag_syms):
    # Flatten expression thành tổng các term
    expr = sp.expand(expr)
    terms = sp.Add.make_args(expr) if isinstance(expr, sp.Add) else (expr,)
    term_strs = []
    for t in terms:
        # Nếu Mul giữa 1 symbol flag và 1 constant
        if isinstance(t, sp.Mul):
            syms = [f for f in t.args if f in flag_syms]
            consts = [c for c in t.args if c not in flag_syms]
            if len(syms)==1 and len(consts)==1 and consts[0].is_integer:
                idx = flag_syms.index(syms[0])
                term_strs.append(f"(flag[{idx}]) * ({int(consts[0])})")
            else:
                term_strs.append(str(t))
        else:
            # t có thể là symbol flag hoặc constant
            if t in flag_syms:
                idx = flag_syms.index(t)
                term_strs.append(f"(flag[{idx}])")
            elif t.is_Number:
                term_strs.append(f"({int(t)})")
            else:
                term_strs.append(str(t))
    if not term_strs:
        return "0"
    s = term_strs[0]
    for ts in term_strs[1:]:
        s = f"({s} + {ts})"
    return s

# ====== Main ======
def main():
    # đọc dna
    try:
        with open(DNA_PATH, 'r') as f:
            data = ''.join(line.strip() for line in f)
    except FileNotFoundError:
        print(f"Không tìm thấy {DNA_PATH}, hãy đặt đúng đường dẫn hoặc chỉnh DNA_PATH.")
        sys.exit(1)

    instructions = decode_instructions(data)
    print(f"Decoded {len(instructions)} instructions.")

    # Tạo symbol flag
    flag_syms = list(sp.symbols(f'f0:{n_vars}', integer=True))
    # Khởi memory
    m = {BASE_ADDR + i: flag_syms[i] for i in range(n_vars)}
    stack = []

    # Simulate linear (chú ý: nếu VM có jump, bạn cần handle path đúng)
    # Ở đây giả sử bạn đã chọn path đúng, hoặc VM chạy tuần tự cần in store biểu thức.
    for idx, inst in enumerate(instructions):
        pc = inst['pc']
        op = inst['opcode']
        operand = inst['operand']
        if op == 0:  # push immediate
            stack.append(sp.Integer(operand))
        elif op == 1:  # pop
            if not stack:
                raise Exception("Underflow")
            stack.pop()
        elif op == 2:  # load memory
            if operand not in m:
                raise Exception(f"Uninitialized memory access tại {operand}")
            stack.append(m[operand])
        elif op == 3:  # store memory
            if not stack:
                raise Exception("Underflow")
            expr = stack.pop()
            m[operand] = expr
            # In nested sum
            expr_str = nested_sum_str(expr, flag_syms)
            print(f"{pc}: memory[{operand}] = {expr_str}")
        elif op == 4:  # add
            if len(stack) < 2: raise Exception("Underflow")
            a = stack.pop(); b = stack.pop()
            stack.append(a + b)
        elif op == 5:  # sub
            if len(stack) < 2: raise Exception("Underflow")
            a = stack.pop(); b = stack.pop()
            stack.append(b - a)
        elif op == 6:  # mul
            if len(stack) < 2: raise Exception("Underflow")
            a = stack.pop(); b = stack.pop()
            stack.append(a * b)
        elif op == 7:  # mod
            if len(stack) < 2: raise Exception("Underflow")
            a = stack.pop(); b = stack.pop()
            stack.append(b % a)
        elif op == 8:  # compare equal
            if len(stack) < 2: raise Exception("Underflow")
            a = stack.pop(); b = stack.pop()
            cond = sp.Eq(b, a)
            stack.append(sp.Piecewise((1, cond), (0, True)))
        elif op == 9:  # jump
            # Nếu muốn handle jump, bạn cần quản lý pc manually. Ở đây ta bỏ qua.
            pass
        elif op == 10:  # jump if pop == 1
            if not stack: raise Exception("Underflow")
            cond = stack.pop()
            # cần xử lý nếu symbolic: thêm constraint hoặc chọn path. Ở đây bỏ.
            pass
        elif op == 11:  # jump if pop != 1
            if not stack: raise Exception("Underflow")
            cond = stack.pop()
            pass
        elif op == 12:  # output char
            if not stack: raise Exception("Underflow")
            stack.pop()
        elif op == 13:  # dynamic code load
            # bỏ qua hoặc handle nếu cần
            pass
        elif op == 14:  # swap mapping nucleotide (nếu decode dynamic), thường không dùng ở đây
            pass
        elif op == 15:
            print("Hit break opcode.")
            break
        else:
            raise Exception(f"Unknown opcode {op} tại pc={pc}")

    print("Done.")

if __name__ == '__main__':
    main()
