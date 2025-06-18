# Mô tả

deoxy ribo nucleic acid deoxy meaning without oxygen ribo meaning the 5-carbon sugar backbone nucleic meaning of the nucleus acid meaning proton donor

Bài cho ta một file **.pyc** và một file **vm.dna** có nội dung là các cái nucleotit trong dna

# Phân tích

## Decompile file pyc

Dùng tool online hoặc nhờ chatgbt được đoạn này

```py
import marshal
import sys
s = []
m = {}
nm = {'A': 0, 'T': 1, 'G': 2, 'C': 3}
unlucky = [b'\x8coooooooooooonooolooo,ooo\x9cSooo\x06o\x12o\x1bo\x0bnvo\x13o\x0bmSo\x1bo\x0blvo\x13o\x0bnSo\x1bo\x0bkvo\x13o\x0blSo\x1bo\x0bmvo\x13o\x0bkSo\x13o\x0eo\x0bo<oFj!\xb5n;\xb5n.\xb5n(\xb5n,\xc6n\xb5m\x01\x02\xc6n\xb5l\x1b\x02\x1f\xc6o\x1deooo\x95fS\x1a\x01\x03\x1a\x0c\x04\x16Q\xb5h\x1a\x01\x03\x1a\x0c\x04\x16booo\x9ccoookmcncncncngn', b'\x96uuuuuuuuuuuuruuu}uuu6uuu\x86\x11uuu\x11t\x08u\x11w\x08t\x11v\x08w\x11q\x11p\xf1u\tu1u\xf6t\x08v\tu\tt\tw\x13v1u(n\x08q\x01u\x01t\x01w\xd5v\xd4u\xf6t\xf6t1u(e)w\x08p\x08s\tv\tspulu\x01w\tq\tpluluMuvuIu\x04i\x04g\tv\x14w\x11u&u\\s;\xafq426!\xafq!642\xafq6!24\x16tuuuuuuuuuuuwuuusuuu&uuu\x86ouuu\x1cu\tu(|\x08t\tt\x01u\x01t\xd5w\xd4u\xf6t\xe6w\x04w&u\\u\xdcv\xafv\x06\x00\x18\xafw\x1b\x18\xafs\x03\x14\x19\x00\x10\x06\xdcw\xafw[E\xaft\x16\xdcu\x07xuuu\x8f|I\x00\x1b\x19\x00\x16\x1e\x0cK\xafr\x00\x1b\x19\x00\x16\x1e\x0cnuuu\x86wuuuou\x8fh\x00\x1b\x19\x00\x16\x1e\x0c*G[I\x19\x1a\x16\x14\x19\x06K[I\x11\x1c\x16\x01\x16\x1a\x18\x05K\xdcq\xaf|\x10\x1b\x00\x18\x10\x07\x14\x01\x10\xafs\x06\x1a\x07\x01\x10\x11\x07}uuu\xafq\x1e\x10\x0c\x06\xdcr\xafw\x06D\xafw\x06G\xafw\x06F\xafv\x01\x18\x05\xaft\x06\xaft\x1c\x07yuuu\x07xuuu\x07xuuu\x07{uuu\x07zuuucuuu\x86guuuqwqtqt{t{tmtotw\x8a}w', b"\x8aiiiiiiiiiiiihiiiniiijiii\x9a/iii\x1di\rh\xeah\xe0i\xe1i\xc9h\x1di\rk\xeah\xc9k\rj\rm\xedi\x1dj\xc9m\xc8i\xc8k\xc8hhi.i\xeei\x0fh\rl\ro\xeda\ro\x1dl\xeaj\x14i\x15i\x1dj\xeah\x08j\ri:i@n'\xb3o\x1b\x08\x07\r\x06\x04\xb3`\x0f\x1c\x07\n\x1d\x06\x06\x05\x1a\nkiiiiiiiiiiikiiikiii:iii\x9aaiii\x15i\x15h(i:i@h'\xc0i\xc0k\xb3h\x11\xb3h\x10\x1bliii\x1bliii\x93`U\x1c\x07\x05\x1c\n\x02\x10W\xb3n\x1c\x07\x05\x1c\n\x02\x10Miii\x9akiiiai\x93r\x1c\x07\x05\x1c\n\x02\x106ZGU\x05\x06\n\x08\x05\x1aWGU\x05\x08\x04\x0b\r\x08W\niiiiiiiiiiiiiiiijiiiiiii\x9aCiii\x0ci3h\ri3k\xeei\xeeh\x0fk\rh\rk\xeda3j\xeei\x0fh\rj\rm\xeda3m\xeeimi3l:i@l\x93s\x1c\x07\x05\x1c\n\x02\x106ZGU\x05\x06\n\x08\x05\x1aWG\x1c\x07\x05\x1c\n\x02\x10\nkiiiiiiiiiiimiiiliiiziii\x9a-iii\x1di\xeai\xc9h\x15h\xc8hhi\x1dk\rh\xeah\x14k\xe1h\xc9j\x15k\xc8hhi\x1dm\rk\xeah-i4e\x14j\x15h\x15k\x15jpipi\x15i\rh\x15jpiUi\x18z\ri:i@j'\xb3m(*.=\x80miii\xc0l\xb3l\x1a\x1c\x19\x0c\x1b\xb3a66\x00\x07\x00\x1d66\xb3m\x05\x00\x1a\x1d\xb3n\x1a\x01\x1c\x0f\x0f\x05\x0c\xb3l\x1b\x08\x07\x0e\x0c\xc0m\xb3m\x1a\x0c\x05\x0f\xb3n\x04\x08\x19\x19\x00\x07\x0e\xb3m\x02\x0c\x10\x1a\xb3h\x00\xc0k\xb3`66\n\x05\x08\x1a\x1a66\xb3h\x1b\x1bliii\x1b`iii\x1bciiiOiii\x9aeiiiehahcheh\x7fhm\x96\x93J\x1c\x07\x05\x1c\n\x02\x106ZGU\x05\x06\n\x08\x05\x1aWG\x1c\x07\x05\x1c\n\x02\x10G66\x00\x07\x00\x1d66\nkiiiiiiiiiiiliiiliiiziii\x9a;iii\x1di\rh\xeah\x14k\x1di\rk\xeah\x14j`i\x15k\xc9h\rm\xc8h\x14m\x1dk\xeei\x0fh\rl\ro\xeda\x15j\xc9j\x15m\xc8h\xc9m\xc8i\ri\rn\xeckpi-i\xeah\xeah\x1bA\x1dl\xeai\xc9o\xe1i\xc8h:i\x18`@a'\x1bkiii\xb3n\x01\x08\x1a\x01\x05\x00\x0b=\x80Iiii\nhiiiiiiiiiiikiiimiiiZiii\x9auiii\xe8i\x15i4`\x14h\x15h\x1di\xe1i\xeah\x02k?ihi\x18k\ri:i@h'\xc0h\xb3j\x06\x1b\r\xc0k\xb3kGY\x1bniii\xc0h\xb3j\x02\x0c\x10\x1bliii\x1b`iii\x1bciii[iii\x9amiiik\xe9si\x93P\x1c\x07\x05\x1c\n\x02\x106ZGU\x05\x06\n\x08\x05\x1aWG\x1c\x07\x05\x1c\n\x02\x10G66\x0e\x0c\x1d\x00\x1d\x0c\x0466GU\x05\x06\n\x08\x05\x1aWGU\x0e\x0c\x07\x0c\x11\x19\x1bW\x80hiii\xc0n\xb3c66\x00\x04\x19\x06\x1b\x1d66\xb3`\x1b\x08\x07\r\x0b\x10\x1d\x0c\x1a\xb3j\x08\x05\x05\xb3o\x1a\x01\x08[\\_\xb3o\r\x00\x0e\x0c\x1a\x1d\x1bziii\xb3b66\x0e\x0c\x1d\x00\x1d\x0c\x0466\xc0l\x1bpiii\x1bBiii\xb3m\x01\x05\x00\x0b\xb3m\x1b\x05\x00\x0b\xb3h\x0b\xc0h\x1bwiii\x1bCiii\x1b`iii\x1bciiiDiii\x9agiiiahahkhchAhehk\x94\x93O\x1c\x07\x05\x1c\n\x02\x106ZGU\x05\x06\n\x08\x05\x1aWG\x1c\x07\x05\x1c\n\x02\x10G66\x0e\x0c\x1d\x00\x1d\x0c\x0466\xc0o\xb3a66\x07\x08\x04\x0c66\xb3c66\x04\x06\r\x1c\x05\x0c66\xb3e66\x18\x1c\x08\x05\x07\x08\x04\x0c66\x1b}iii\x1b\\iii\xb3d66\n\x05\x08\x1a\x1a\n\x0c\x05\x0566\x1bliii\xc0h\x1bviii\x1bSiii\x1b`iii\x1bciiiLiii\x9aoiiiaigh}n\x1bciii\xc0o\x1bYiii\xb3m\x1a\x0c\x0c\r\xb3o\x1b\x0c\r\x1c\n\x0c\xb3k\x07\x04\xb3o\x1f\x08\x05\x1c\x0c\x1a\xb3m\r\x00\n\x1d\xc0h\x1bciii\x1bliii\x1b+iii\x1b`iii\x1bciiiHiii\x9aaiiiakwh}hey", b'\x82aaaaaaaaaaaacaaagaaa"aaa\x92]aaa&a\x05`\x05c\xe5a\x05c\x15a\xe2b\x1ca&a\x05b\x05e\xe5a\x05e\x15`\x1da\x05d\xece\x1c`\x15c\x05g\x15`\x15b\xe2`\xfaa\x05f\xfcb\xe2``a\x05a2aHi/\x02aaaaaaaaaaaaaaaabaaaaaaa\x92Iaaa\x04a;`\x05a;c\xe6a\x07`\x05`\x05c\xe5i;b\xe6a\x07`\x05b\x05e\xe5i;e\xe6aea;d2aHd\x9bt\x14\x0f\r\x14\x02\n\x18>UO]\r\x0e\x02\x00\r\x12_O,,\x02eaaaaaaaaaaaeaaagaaaraaa\x92saaa\x15a\xe2a\xc1`\x1da\x1d`\x1dc\x1db\xc0e2aH`/\xc8c\xbbd\x12\x14\x11\x04\x13\xbbf>>\x0f\x04\x16>>\xc8e\xbbb\x02\r\x12\xbbe\x0f\x00\x0c\x04\xbbd\x03\x00\x12\x04\x12\xbbb\x05\x02\x15\xc8`\xbbh>>\x02\r\x00\x12\x12>>\xc8a\x9bh]\x14\x0f\r\x14\x02\n\x18_\xbbf\x14\x0f\r\x14\x02\n\x18Zaaa\x92caaas`\x9b|\x14\x0f\r\x14\x02\n\x18>UO]\r\x0e\x02\x00\r\x12_O,,O>>\x0f\x04\x16>>\x02`aaaaaaaaaaafaaadaaa~aaa\x92\x05aaa\x15a\xe2a\x0b`\x1d`\x08a\x1dc\xc5`\xef`\x1cb\x15c\x1db\xc1b\xc0a\xe2`\x1ce\x1de\x05a\x05a\x05`\xe4bxa\x1de\x05c\x05a\x05`\xe4bxava\x1ce\x15e\x15d\x1db\xc1g\xc0a\xe2`\xe2`%a<k=c\x1cd\x1cg\x1de\x1ddxa\x1db\x1dg]a\x10D\x1db2aHb/\x88caaa\x88`aaa\xc8f\x13gaaa\xbbi>>\x02\x00\r\r>>\xbbe\r\x08\x12\x15\xbbg\x17\x00\r\x14\x04\x12\xbbh\x04\x0f\x14\x0c\x04\x13\x00\x15\x04\xbbg\x12\x0e\x13\x15\x04\x05\xbbe\n\x04\x18\x12\xc8f\x13haaa\xbbe\x00\x13\x06\x12\xbbg\n\x16\x00\x13\x06\x12\xbbi\x08\x0f\x12\x15\x00\x0f\x02\x04\xbbe\x17\x00\r\x12\xbb`\x08\xbb`\n\x13laaa\x13naaa\x13qaaa\x13paaa_aaa\x92maaas`m`}`y`o`e`\x9b\x7f\x14\x0f\r\x14\x02\n\x18>UO]\r\x0e\x02\x00\r\x12_O,,O>>\x02\x00\r\r>>\xc8g\xbbi>>\x0f\x00\x0c\x04>>\xbbk>>\x0c\x0e\x05\x14\r\x04>>\xbbm>>\x10\x14\x00\r\x0f\x00\x0c\x04>>\x13faaa\x13yaaa\xbbl>>\x02\r\x00\x12\x12\x02\x04\r\r>>\x13naaa\x13naaa\x13laaa\x13qaaa\x13paaa[aaa\x92gaaaiam`ub\xbbc,,\x02aaaaaaaaaaaaaaaa`aaa!aaa\x92maaa\x04a;`\x05a;c\x05`2aHc\x9bt\x14\x0f\r\x14\x02\n\x18>UO]\r\x0e\x02\x00\r\x12_O,%/\xc8b\x13Iaaa\x13Haaa\x13Kaaa\x13naaa\x13naaa\x13naaa\x13qaaa\x13paaa\'aaa\x92eaaaiae`\xbbc,%\xc8`\xbbh\x0c\x04\x15\x00\x02\r\x00\x12\x12\x9b@\x06\r\x0e\x03\x00\r\x12IH:F\x0f\x14\x02\r\x04\x0e\x15\x08\x05\x04>\x0c\x00\x11F<A\\A,%I\x9b`H\xc8e\xbbe\x15\x18\x11\x04\xbbe\x05\x08\x02\x15\xbbe\x04\x19\x04\x02\xbbc\x0f\x0c\xc8c\x13Laaa\x13Saaa\x13naaa\x13naaa\x13qaaa\x13paaaVaaa\x92gaaaqbumyb']
trans = lambda s: sum((nm[c] << 2 * i for i, c in enumerate(s)))
if len(sys.argv)!= 2:
    print(f'Usage: {sys.argv[0]} <dna_file>')
    sys.exit(1)
code = open(sys.argv[1]).read()
flag = input('> ').encode()
if len(flag)!= 56:
    exit('WRONG!')
if flag[:6]!= b'.;,;.{':
    exit('WRONG!')
if flag[(-1)]!= 125:
    exit('WRONG!')
flag = flag[6:(-1)]
for i in range(len(flag)):
    m[640 + i] = flag[i]
pc = 0
while pc < len(code):
    pri, pro = map(trans, [code[pc:pc + 2], code[pc + 2:pc + 12]])

    @pri
    case 0:
        s.append(pro)
        pc += 12
    else:  # inserted
        case 1:
            if not s:
                raise Exception('Stack underflow')
            s.pop()
            pc += 2
        else:  # inserted
            case 2:
                if pro not in m:
                    raise Exception(f'Uninitialized memory access at {pro}')
                s.append(m[pro])
                pc += 12
            else:  # inserted
                case 3:
                    if not s:
                        raise Exception('Stack underflow')
                    m[pro] = s.pop()
                    pc += 12
                else:  # inserted
                    case 4:
                        if len(s) < 2:
                            raise Exception('Stack underflow')
                        a, b = (s.pop(), s.pop())
                        s.append(a + b)
                        pc += 2
                    else:  # inserted
                        case 5:
                            if len(s) < 2:
                                raise Exception('Stack underflow')
                            a, b = (s.pop(), s.pop())
                            s.append(b - a)
                            pc += 2
                        else:  # inserted
                            case 6:
                                if len(s) < 2:
                                    raise Exception('Stack underflow')
                                a, b = (s.pop(), s.pop())
                                s.append(a * b)
                                pc += 2
                            else:  # inserted
                                case 7:
                                    if len(s) < 2:
                                        raise Exception('Stack underflow')
                                    a, b = (s.pop(), s.pop())
                                    if a == 0:
                                        raise Exception('Division by zero')
                                    s.append(b % a)
                                    pc += 2
                                else:  # inserted
                                    case 8:
                                        if len(s) < 2:
                                            raise Exception('Stack underflow')
                                        a, b = (s.pop(), s.pop())
                                        s.append(1 if a == b else 0)
                                        pc += 2
                                    else:  # inserted
                                        case 9:
                                            pc = pro
                                        else:  # inserted
                                            case 10:
                                                if not s:
                                                    raise Exception('Stack underflow')
                                                if s.pop() == 1:
                                                    pc = pro
                                                else:  # inserted
                                                    pc += 12
                                            else:  # inserted
                                                case 11:
                                                    if not s:
                                                        raise Exception('Stack underflow')
                                                    if s.pop()!= 1:
                                                        pc = pro
                                                    else:  # inserted
                                                        pc += 12
                                                else:  # inserted
                                                    case 12:
                                                        if not s:
                                                            raise Exception('Stack underflow')
                                                        print(chr(s.pop()), end='')
                                                        pc += 2
                                                    else:  # inserted
                                                        case 13:
                                                            if not s:
                                                                raise Exception('Stack underflow')
                                                            key = s.pop()

                                                            def f():
                                                                return
                                                            f.__code__ = marshal.loads(bytes([b ^ key for b in unlucky.pop(0)]))
                                                            f()
                                                            pc += 2
                                                        else:  # inserted
                                                            case 14:
                                                                if len(s) < 2:
                                                                    raise Exception('Stack underflow')
                                                                a, b = (s.pop(), s.pop())
                                                                if a not in nm or b not in nm:
                                                                    raise Exception('Invalid')
                                                                nm[a], nm[b] = (nm[b], nm[a])
                                                                pc += 2
                                                            else:  # inserted
                                                                case 15:
                                                                    break
```

## Marshal

Module `marshal` thường được dùng để:

- Lưu trữ **code object** (ví dụ: từ hàm, module, script) thành dạng `.pyc`
- **Ghi/đọc dữ liệu nhị phân** giữa các lần chạy

**Marshal objects** là một cách để **biến các object Python thành chuỗi byte**, và ngược lại - tức là để ghi và đọc các object dưới dạng nhị phân

Để ý thấy  mỗi phần tử trong danh sách **`unlucky`** chính là một “marshal object”, nhưng đã bị **XOR với một byte key** trước khi nạp lại:

```python
key = s.pop()
def f():
 return
f.__code__ = marshal.loads(bytes([b ^ key for b in unlucky.pop(0)]))
f()
```

**`marshal.loads(...)`** chỉ chấp nhận chuỗi `bytes` ghi đúng định dạng marshal (đầu tiên là một vài byte “magic” mô tả kiểu, rồi tới nội dung đối tượng)

Ở đây, chuỗi `bytes([...])` được tạo ra bằng cách lấy phần tử đầu của `unlucky`, xor từng byte với `key`, rồi mới đưa vào `marshal.loads`. Nếu bỏ lớp XOR đi, dòng lệnh đó sẽ nạp ra một `code object` hợp lệ và gán cho `f.__code__`

Nói cách khác, mỗi entry của `unlucky` = code object đã serialize bằng `marshal.dumps` rồi xor

**Lưu ý: Do cái này được code bằng python 3.10 cho nên khi thực hiện decode cũng phải dùng python 3.10**

Để tìm ra xor key thì ta cần bruteforce mỗi byte với một key từ 0->256

## Flag checker

```py
m[640 + i] = flag[i]
```

Địa chỉ bắt đầu chuỗi flag được load vào bộ nhớ nên sẽ lấy base address là 640

Đọc file main.py thấy ngoài opcode 13 và 14 là nạp động một đoạn mã từ mảng `unlucky` khi chạy chương trình, ngoài ra còn opcode 3 là `load memory` và opcode 8 là để so sánh các giá trị vừa được nạp vào với flag chính xác rồi trả về 0 (sai) hoặc 1 (đúng)

Sau đó nhờ chatgpt tạo hộ 1 script để sửa lại file pyc ở trên cho chạy được sau đó load vm.dna và in ra các địa chỉ được nạp vào, giá trị được kiểm tra là gì

```py
#!/usr/bin/env python3
import sys
import sympy as sp

# ====== Cấu hình ======
# Đường dẫn file dna, hoặc truyền qua argv
DNA_PATH = 'vm.dna'
# Số byte flag (không tính prefix/suffix). 
# Bạn cần sửa cho đúng 56 - .;,;.{} = 49
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
```

**Output**

```
Encounter break opcode tại pc=15218, dừng decode.
Decoded 2160 instructions.
1370: memory[4096] = (((((((((((((((((((((((((((((((((((((((((((((((((flag[14]) * (15) + (flag[28]) * (21)) + (flag[33]) * (22)) + (flag[1]) * (27)) + (flag[27]) * (28)) + (flag[35]) * (31)) + (flag[46]) * (41)) + (flag[15]) * (55)) + (flag[41]) * (68)) + (flag[43]) * (71)) + (flag[42]) * (75)) + (flag[5]) * (91)) + (flag[29]) * (97)) + (flag[36]) * (101)) + (flag[23]) * (104)) + (flag[0]) * (106)) + (flag[8]) * (106)) + (flag[4]) * (108)) + (flag[11]) * (115)) + (flag[26]) * (118)) + (flag[32]) * (118)) + (flag[9]) * (127)) + (flag[17]) * (131)) + (flag[6]) * (131)) + (flag[3]) * (138)) + (flag[7]) * (138)) + (flag[2]) * (140)) + (flag[40]) * (146)) + (flag[18]) * (147)) + (flag[30]) * (151)) + (flag[13]) * (152)) + (flag[38]) * (155)) + (flag[10]) * (161)) + (flag[48]) * (161)) + (flag[45]) * (173)) + (flag[12]) * (177)) + (flag[19]) * (183)) + (flag[24]) * (188)) + (flag[25]) * (196)) + (flag[21]) * (197)) + (flag[22]) * (200)) + (flag[34]) * (212)) + (flag[31]) * (217)) + (flag[44]) * (218)) + (flag[47]) * (220)) + (flag[37]) * (227)) + (flag[16]) * (230)) + (flag[20]) * (235)) + (flag[39]) * (237))
2752: memory[4100] = (((((((((((((((((((((((((((((((((((((((((((((((((flag[13]) + (flag[34]) * (3)) + (flag[24]) * (9)) + (flag[32]) * (11)) + (flag[36]) * (14)) + (flag[46]) * (22)) + (flag[20]) * (25)) + (flag[33]) * (28)) + (flag[43]) * (29)) + (flag[25]) * (53)) + (flag[0]) * (56)) + (flag[31]) * (57)) + (flag[48]) * (61)) + (flag[8]) * (63)) + (flag[4]) * (66)) + (flag[41]) * (66)) + (flag[11]) * (69)) + (flag[37]) * (70)) + (flag[17]) * (97)) + (flag[39]) * (102)) + (flag[28]) * (104)) + (flag[29]) * (104)) + (flag[23]) * (105)) + (flag[44]) * (107)) + (flag[6]) * (113)) + (flag[26]) * (115)) + (flag[16]) * (118)) + (flag[42]) * (133)) + (flag[5]) * (136)) + (flag[21]) * (141)) + (flag[35]) * (146)) + (flag[14]) * (147)) + (flag[2]) * (152)) + (flag[30]) * (153)) + (flag[38]) * (154)) + (flag[45]) * (155)) + (flag[27]) * (162)) + (flag[15]) * (169)) + (flag[40]) * (169)) + (flag[19]) * (175)) + (flag[12]) * (191)) + (flag[18]) * (193)) + (flag[3]) * (225)) + (flag[47]) * (231)) + (flag[9]) * (233)) + (flag[22]) * (234)) + (flag[7]) * (243)) + (flag[1]) * (249)) + (flag[10]) * (254))
4134: memory[4104] = (((((((((((((((((((((((((((((((((((((((((((((((((flag[21]) + (flag[27]) * (10)) + (flag[9]) * (10)) + (flag[12]) * (15)) + (flag[28]) * (18)) + (flag[44]) * (27)) + (flag[39]) * (34)) + (flag[40]) * (46)) + (flag[20]) * (54)) + (flag[24]) * (62)) + (flag[41]) * (64)) + (flag[2]) * (66)) + (flag[19]) * (69)) + (flag[3]) * (72)) + (flag[16]) * (77)) + (flag[25]) * (99)) + (flag[1]) * (104)) + (flag[18]) * (106)) + (flag[29]) * (117)) + (flag[22]) * (122)) + (flag[35]) * (127)) + (flag[5]) * (134)) + (flag[17]) * (137)) + (flag[4]) * (140)) + (flag[6]) * (140)) + (flag[37]) * (145)) + (flag[0]) * (149)) + (flag[33]) * (150)) + (flag[48]) * (150)) + (flag[26]) * (155)) + (flag[46]) * (156)) + (flag[47]) * (156)) + (flag[11]) * (162)) + (flag[45]) * (163)) + (flag[30]) * (164)) + (flag[7]) * (174)) + (flag[43]) * (182)) + (flag[15]) * (183)) + (flag[42]) * (189)) + (flag[38]) * (190)) + (flag[14]) * (191)) + (flag[36]) * (193)) + (flag[23]) * (195)) + (flag[10]) * (209)) + (flag[31]) * (216)) + (flag[13]) * (223)) + (flag[32]) * (231)) + (flag[8]) * (236)) + (flag[34]) * (255))
5516: memory[4108] = (((((((((((((((((((((((((((((((((((((((((((((((((flag[5]) + (flag[24]) * (4)) + (flag[46]) * (5)) + (flag[37]) * (7)) + (flag[9]) * (10)) + (flag[38]) * (11)) + (flag[3]) * (13)) + (flag[21]) * (16)) + (flag[40]) * (26)) + (flag[22]) * (28)) + (flag[11]) * (30)) + (flag[25]) * (32)) + (flag[17]) * (43)) + (flag[16]) * (60)) + (flag[45]) * (65)) + (flag[0]) * (67)) + (flag[39]) * (68)) + (flag[12]) * (74)) + (flag[35]) * (75)) + (flag[23]) * (80)) + (flag[26]) * (83)) + (flag[48]) * (84)) + (flag[20]) * (85)) + (flag[30]) * (92)) + (flag[47]) * (101)) + (flag[31]) * (105)) + (flag[1]) * (113)) + (flag[6]) * (115)) + (flag[44]) * (116)) + (flag[36]) * (122)) + (flag[42]) * (122)) + (flag[41]) * (140)) + (flag[8]) * (151)) + (flag[27]) * (156)) + (flag[19]) * (162)) + (flag[15]) * (170)) + (flag[28]) * (173)) + (flag[4]) * (173)) + (flag[14]) * (175)) + (flag[34]) * (180)) + (flag[10]) * (188)) + (flag[18]) * (188)) + (flag[2]) * (188)) + (flag[7]) * (188)) + (flag[43]) * (201)) + (flag[33]) * (218)) + (flag[29]) * (222)) + (flag[13]) * (224)) + (flag[32]) * (251))
6898: memory[4112] = (((((((((((((((((((((((((((((((((((((((((((((((((flag[38]) * (7) + (flag[23]) * (9)) + (flag[26]) * (12)) + (flag[15]) * (16)) + (flag[39]) * (21)) + (flag[18]) * (25)) + (flag[42]) * (25)) + (flag[12]) * (27)) + (flag[10]) * (31)) + (flag[37]) * (39)) + (flag[43]) * (47)) + (flag[44]) * (58)) + (flag[36]) * (62)) + (flag[2]) * (67)) + (flag[14]) * (68)) + (flag[6]) * (69)) + (flag[21]) * (72)) + (flag[3]) * (72)) + (flag[45]) * (72)) + (flag[11]) * (81)) + (flag[22]) * (83)) + (flag[41]) * (83)) + (flag[9]) * (86)) + (flag[25]) * (87)) + (flag[19]) * (94)) + (flag[0]) * (105)) + (flag[31]) * (114)) + (flag[48]) * (127)) + (flag[34]) * (131)) + (flag[20]) * (132)) + (flag[17]) * (133)) + (flag[40]) * (135)) + (flag[32]) * (138)) + (flag[27]) * (149)) + (flag[24]) * (154)) + (flag[35]) * (175)) + (flag[5]) * (183)) + (flag[4]) * (186)) + (flag[16]) * (188)) + (flag[30]) * (199)) + (flag[33]) * (200)) + (flag[13]) * (207)) + (flag[8]) * (212)) + (flag[1]) * (219)) + (flag[29]) * (225)) + (flag[47]) * (230)) + (flag[46]) * (235)) + (flag[7]) * (249)) + (flag[28]) * (255))
8280: memory[4116] = ((((((((((((((((((((((((((((((((((((((((((((((((flag[23]) * (7) + (flag[44]) * (13)) + (flag[10]) * (17)) + (flag[45]) * (21)) + (flag[11]) * (23)) + (flag[42]) * (24)) + (flag[48]) * (24)) + (flag[16]) * (33)) + (flag[32]) * (37)) + (flag[40]) * (45)) + (flag[29]) * (50)) + (flag[4]) * (51)) + (flag[14]) * (54)) + (flag[3]) * (56)) + (flag[28]) * (61)) + (flag[46]) * (64)) + (flag[22]) * (77)) + (flag[17]) * (78)) + (flag[33]) * (103)) + (flag[39]) * (114)) + (flag[5]) * (114)) + (flag[47]) * (115)) + (flag[7]) * (115)) + (flag[6]) * (132)) + (flag[26]) * (134)) + (flag[12]) * (145)) + (flag[27]) * (145)) + (flag[38]) * (147)) + (flag[13]) * (148)) + (flag[43]) * (150)) + (flag[15]) * (152)) + (flag[34]) * (162)) + (flag[35]) * (172)) + (flag[2]) * (176)) + (flag[8]) * (180)) + (flag[18]) * (191)) + (flag[1]) * (192)) + (flag[20]) * (193)) + (flag[24]) * (196)) + (flag[41]) * (196)) + (flag[0]) * (198)) + (flag[25]) * (202)) + (flag[19]) * (203)) + (flag[21]) * (236)) + (flag[9]) * (236)) + (flag[30]) * (244)) + (flag[36]) * (246)) + (flag[37]) * (250))
9662: memory[4120] = (((((((((((((((((((((((((((((((((((((((((((((((((flag[17]) + (flag[6]) * (2)) + (flag[10]) * (7)) + (flag[3]) * (12)) + (flag[30]) * (13)) + (flag[0]) * (29)) + (flag[15]) * (31)) + (flag[22]) * (40)) + (flag[36]) * (42)) + (flag[1]) * (45)) + (flag[33]) * (53)) + (flag[24]) * (59)) + (flag[27]) * (67)) + (flag[41]) * (69)) + (flag[11]) * (70)) + (flag[31]) * (72)) + (flag[42]) * (90)) + (flag[9]) * (91)) + (flag[29]) * (95)) + (flag[25]) * (97)) + (flag[48]) * (111)) + (flag[37]) * (113)) + (flag[38]) * (117)) + (flag[19]) * (118)) + (flag[34]) * (122)) + (flag[46]) * (122)) + (flag[43]) * (135)) + (flag[16]) * (139)) + (flag[45]) * (156)) + (flag[12]) * (163)) + (flag[14]) * (166)) + (flag[5]) * (166)) + (flag[23]) * (169)) + (flag[47]) * (181)) + (flag[13]) * (182)) + (flag[40]) * (182)) + (flag[32]) * (186)) + (flag[4]) * (189)) + (flag[44]) * (192)) + (flag[28]) * (195)) + (flag[8]) * (204)) + (flag[20]) * (218)) + (flag[26]) * (224)) + (flag[18]) * (229)) + (flag[21]) * (229)) + (flag[35]) * (229)) + (flag[2]) * (240)) + (flag[39]) * (246)) + (flag[7]) * (253))
11044: memory[4124] = (((((((((((((((((((((((((((((((((((((((((((((((((flag[48]) * (2) + (flag[36]) * (4)) + (flag[7]) * (11)) + (flag[43]) * (12)) + (flag[37]) * (22)) + (flag[19]) * (24)) + (flag[31]) * (24)) + (flag[16]) * (26)) + (flag[44]) * (27)) + (flag[46]) * (42)) + (flag[22]) * (48)) + (flag[42]) * (53)) + (flag[4]) * (59)) + (flag[23]) * (64)) + (flag[5]) * (64)) + (flag[33]) * (67)) + (flag[21]) * (68)) + (flag[12]) * (76)) + (flag[13]) * (80)) + (flag[29]) * (82)) + (flag[38]) * (82)) + (flag[11]) * (87)) + (flag[8]) * (105)) + (flag[27]) * (106)) + (flag[3]) * (106)) + (flag[0]) * (114)) + (flag[1]) * (134)) + (flag[45]) * (134)) + (flag[20]) * (140)) + (flag[26]) * (141)) + (flag[30]) * (151)) + (flag[40]) * (152)) + (flag[47]) * (163)) + (flag[18]) * (170)) + (flag[2]) * (171)) + (flag[41]) * (195)) + (flag[17]) * (196)) + (flag[35]) * (197)) + (flag[14]) * (204)) + (flag[34]) * (216)) + (flag[10]) * (221)) + (flag[28]) * (221)) + (flag[6]) * (227)) + (flag[32]) * (233)) + (flag[39]) * (235)) + (flag[24]) * (238)) + (flag[25]) * (238)) + (flag[15]) * (240)) + (flag[9]) * (240))
12426: memory[4128] = (((((((((((((((((((((((((((((((((((((((((((((((((flag[12]) * (7) + (flag[28]) * (8)) + (flag[27]) * (12)) + (flag[9]) * (14)) + (flag[10]) * (15)) + (flag[6]) * (19)) + (flag[20]) * (21)) + (flag[36]) * (24)) + (flag[34]) * (27)) + (flag[18]) * (35)) + (flag[21]) * (40)) + (flag[4]) * (42)) + (flag[46]) * (56)) + (flag[13]) * (57)) + (flag[8]) * (58)) + (flag[1]) * (63)) + (flag[3]) * (64)) + (flag[29]) * (77)) + (flag[48]) * (81)) + (flag[17]) * (97)) + (flag[26]) * (99)) + (flag[32]) * (101)) + (flag[35]) * (109)) + (flag[37]) * (109)) + (flag[23]) * (111)) + (flag[25]) * (116)) + (flag[15]) * (119)) + (flag[24]) * (119)) + (flag[30]) * (120)) + (flag[0]) * (127)) + (flag[41]) * (138)) + (flag[47]) * (146)) + (flag[42]) * (154)) + (flag[14]) * (158)) + (flag[44]) * (159)) + (flag[19]) * (167)) + (flag[43]) * (174)) + (flag[11]) * (176)) + (flag[7]) * (182)) + (flag[45]) * (184)) + (flag[31]) * (201)) + (flag[33]) * (218)) + (flag[2]) * (220)) + (flag[40]) * (230)) + (flag[16]) * (231)) + (flag[38]) * (234)) + (flag[5]) * (237)) + (flag[22]) * (238)) + (flag[39]) * (245))
13808: memory[4132] = (((((((((((((((((((((((((((((((((((((((((((((((((flag[40]) * (16) + (flag[34]) * (17)) + (flag[31]) * (38)) + (flag[48]) * (39)) + (flag[18]) * (43)) + (flag[7]) * (46)) + (flag[19]) * (50)) + (flag[33]) * (51)) + (flag[27]) * (57)) + (flag[3]) * (59)) + (flag[41]) * (60)) + (flag[21]) * (70)) + (flag[45]) * (70)) + (flag[47]) * (71)) + (flag[25]) * (75)) + (flag[14]) * (95)) + (flag[9]) * (95)) + (flag[8]) * (101)) + (flag[39]) * (110)) + (flag[38]) * (111)) + (flag[24]) * (118)) + (flag[28]) * (120)) + (flag[29]) * (120)) + (flag[16]) * (121)) + (flag[23]) * (122)) + (flag[37]) * (122)) + (flag[42]) * (130)) + (flag[13]) * (134)) + (flag[20]) * (135)) + (flag[26]) * (138)) + (flag[35]) * (142)) + (flag[22]) * (144)) + (flag[43]) * (147)) + (flag[15]) * (152)) + (flag[11]) * (171)) + (flag[2]) * (175)) + (flag[44]) * (180)) + (flag[1]) * (185)) + (flag[36]) * (190)) + (flag[30]) * (198)) + (flag[46]) * (200)) + (flag[32]) * (202)) + (flag[4]) * (219)) + (flag[5]) * (231)) + (flag[17]) * (232)) + (flag[10]) * (237)) + (flag[12]) * (242)) + (flag[6]) * (246)) + (flag[0]) * (253))
15190: memory[4136] = (((((((((((((((((((((((((((((((((((((((((((((((((flag[4]) * (8) + (flag[26]) * (17)) + (flag[0]) * (31)) + (flag[41]) * (41)) + (flag[47]) * (41)) + (flag[45]) * (43)) + (flag[39]) * (48)) + (flag[48]) * (50)) + (flag[1]) * (56)) + (flag[25]) * (70)) + (flag[12]) * (72)) + (flag[27]) * (86)) + (flag[32]) * (87)) + (flag[19]) * (91)) + (flag[20]) * (99)) + (flag[17]) * (103)) + (flag[35]) * (109)) + (flag[13]) * (113)) + (flag[46]) * (115)) + (flag[9]) * (117)) + (flag[42]) * (118)) + (flag[15]) * (135)) + (flag[8]) * (136)) + (flag[43]) * (139)) + (flag[29]) * (143)) + (flag[23]) * (144)) + (flag[33]) * (152)) + (flag[14]) * (153)) + (flag[36]) * (154)) + (flag[7]) * (157)) + (flag[28]) * (161)) + (flag[5]) * (162)) + (flag[40]) * (174)) + (flag[3]) * (186)) + (flag[11]) * (188)) + (flag[38]) * (193)) + (flag[2]) * (216)) + (flag[16]) * (218)) + (flag[18]) * (228)) + (flag[37]) * (231)) + (flag[21]) * (234)) + (flag[31]) * (234)) + (flag[24]) * (235)) + (flag[30]) * (241)) + (flag[44]) * (244)) + (flag[34]) * (247)) + (flag[22]) * (249)) + (flag[6]) * (252)) + (flag[10]) * (254))
Hit break opcode.
Done.
```

Đến đây thấy rằng các địa chỉ bộ nhớ được đặt thành các hàng của vector tạo thành một ma trận sau đó chúng được so sánh với các giá trị chứa trong bytecode => matrix multiplication

Để giải cái ma trận này và lấy được nội dung của flag ta sẽ dùng thư viện **z3** và method **Solver()** trong python

```python
from z3 import *

s = Solver()
flag = [Int(f'{i}') for i in range(49)]
# Các giá trị được so sánh với input nhập vào
target = [
    692012, 611030, 658676, 556679, 588728, 628470, 659130, 623012, 590356, 670831,
    734960, 694096, 673431, 676517, 638313, 730305, 651347, 612947, 614037, 722768,
    662232, 608720, 598699, 626932, 659018, 554138, 627484, 620929, 655810, 598103,
    664749, 772833, 710796, 669747, 576742, 715958, 682073, 687276, 806029, 660519,
    728567, 689664, 746796, 597800, 629625, 585142, 678960, 665322, 710793
]

# Ma trận 49x49 
coefficients = [
    # m[4096]:
    [106, 27, 140, 138, 108, 91, 131, 138, 106, 127, 161, 115, 177, 152, 15, 55, 230, 131, 147, 183, 235, 197, 200, 104, 188, 196, 118, 28, 21, 97, 151, 217, 118, 22, 212, 31, 101, 227, 155, 237, 146, 68, 75, 71, 218, 173, 41, 220, 161],

    # m[4100]:
    [56, 249, 152, 225, 66, 136, 113, 243, 63, 233, 254, 69, 191, 1, 147, 169, 118, 97, 193, 175, 25, 141, 234, 105, 9, 53, 115, 162, 104, 104, 153, 57, 11, 28, 3, 146, 14, 70, 154, 102, 169, 66, 133, 29, 107, 155, 22, 231, 61],

    # m[4104]:
    [149, 104, 66, 72, 140, 134, 140, 174, 236, 10, 209, 162, 15, 223, 191, 183, 77, 137, 106, 69, 54, 1, 122, 195, 62, 99, 155, 10, 18, 117, 164, 216, 231, 150, 255, 127, 193, 145, 190, 34, 46, 64, 189, 182, 27, 163, 156, 156, 150],

    # m[4108]:
    [67, 113, 188, 13, 173, 1, 115, 188, 151, 10, 188, 30, 74, 224, 175, 170, 60, 43, 188, 162, 85, 16, 28, 80, 4, 32, 83, 156, 173, 222, 92, 105, 251, 218, 180, 75, 122, 7, 11, 68, 26, 140, 122, 201, 116, 65, 5, 101, 84],  

    # m[4112]:
    [105, 219, 67, 72, 186, 183, 69, 249, 212, 86, 31, 81, 27, 207, 68, 16, 188, 133, 25, 94, 132, 72, 83, 9, 154, 87, 12, 149, 255, 225, 199, 114, 138, 200, 131, 175, 62, 39, 7, 21, 135, 83, 25, 47, 58, 72, 235, 230, 127], 

    # m[4116]:
    [198, 192, 176, 56, 51, 114, 132, 115, 180, 236, 17, 23, 145, 148, 54, 152, 33, 78, 191, 203, 193, 236, 77, 7, 196, 202, 134, 145, 61, 50, 244, 0, 37, 103, 162, 172, 246, 250, 147, 114, 45, 196, 24, 150, 13, 21, 64, 115, 24],

    # m[4120]:
    [29, 45, 240, 12, 189, 166, 2, 253, 204, 91, 7, 70, 163, 182, 166, 31, 139, 1, 229, 118, 218, 229, 40, 169, 59, 97, 224, 67, 195, 95, 13, 72, 186, 53, 122, 229, 42, 113, 117, 246, 182, 69, 90, 135, 192, 156, 122, 181, 111],

    # m[4124]:
    [114, 134, 171, 106, 59, 64, 227, 11, 105, 240, 221, 87, 76, 80, 204, 240, 26, 196, 170, 24, 140, 68, 48, 64, 238, 238, 141, 106, 221, 82, 151, 24, 233, 67, 216, 197, 4, 22, 82, 235, 152, 195, 53, 12, 27, 134, 42, 163, 2],

    # m[4128]:
    [127, 63, 220, 64, 42, 237, 19, 182, 58, 14, 15, 176, 7, 57, 158, 119, 231, 97, 35, 167, 21, 40, 238, 111, 119, 116, 99, 12, 8, 77, 120, 201, 101, 218, 27, 109, 24, 109, 234, 245, 230, 138, 154, 174, 159, 184, 56, 146, 81],

    # m[4132]:
    [253, 185, 175, 59, 219, 231, 246, 46, 101, 95, 237, 171, 242, 134, 95, 152, 121, 232, 43, 50, 135, 70, 144, 122, 118, 75, 138, 57, 120, 120, 198, 38, 202, 51, 17, 142, 190, 122, 111, 110, 16, 60, 130, 147, 180, 70, 200, 71, 39],

    # m[4136]:
    [31, 56, 216, 186, 8, 162, 252, 157, 136, 117, 254, 188, 72, 113, 153, 135, 218, 103, 228, 91, 99, 234, 249, 144, 235, 70, 17, 86, 161, 143, 241, 234, 87, 152, 247, 109, 154, 231, 193, 48, 174, 41, 118, 139, 244, 43, 115, 41, 50],

    # m[4140]:
    [60, 107, 224, 167, 53, 64, 187, 212, 249, 64, 32, 237, 18, 155, 194, 215, 15, 1, 30, 239, 163, 225, 161, 87, 228, 113, 71, 153, 183, 62, 146, 54, 231, 201, 56, 252, 112, 130, 208, 205, 11, 255, 91, 7, 114, 91, 175, 246, 37],

    # m[4144]:
    [135, 96, 194, 108, 97, 191, 20, 140, 113, 63, 145, 97, 221, 100, 89, 38, 8, 31, 47, 68, 225, 54, 124, 140, 215, 189, 167, 210, 93, 149, 172, 5, 14, 207, 186, 124, 188, 247, 161, 238, 215, 226, 48, 26, 185, 170, 84, 253, 92],

    # m[4148]:
    [221, 229, 12, 122, 30, 173, 171, 188, 64, 199, 16, 209, 221, 139, 5, 249, 240, 118, 37, 126, 252, 253, 95, 92, 73, 241, 156, 69, 44, 229, 224, 8, 58, 35, 146, 47, 177, 142, 100, 156, 37, 0, 97, 227, 100, 53, 12, 220, 212],

    # m[4152]:
    [95, 87, 172, 60, 150, 10, 71, 141, 50, 204, 201, 212, 248, 235, 115, 76, 56, 32, 82, 169, 83, 206, 175, 83, 223, 100, 244, 34, 127, 24, 76, 136, 128, 226, 146, 187, 51, 232, 236, 53, 60, 38, 54, 51, 0, 228, 114, 34, 185],

    # m[4156]:
    [251, 59, 207, 64, 175, 77, 94, 243, 222, 81, 138, 176, 175, 83, 74, 160, 243, 128, 222, 56, 7, 160, 112, 141, 64, 237, 21, 110, 83, 217, 222, 54, 194, 201, 227, 149, 242, 10, 78, 254, 196, 130, 232, 115, 62, 159, 164, 30, 72],

    # m[4160]:
    [110, 186, 42, 142, 162, 231, 238, 121, 109, 214, 64, 222, 178, 67, 114, 193, 78, 90, 39, 35, 181, 182, 99, 7, 177, 20, 131, 106, 249, 101, 153, 43, 237, 17, 54, 97, 173, 63, 193, 115, 17, 192, 11, 252, 75, 7, 214, 163, 137],

    # m[4164]:
    [157, 175, 119, 133, 215, 235, 223, 6, 195, 165, 156, 63, 72, 2, 193, 184, 39, 231, 155, 98, 79, 183, 185, 146, 62, 84, 216, 246, 91, 217, 82, 93, 52, 161, 74, 13, 36, 50, 34, 86, 102, 38, 21, 122, 67, 28, 186, 24, 191],

    # m[4168]:
    [166, 92, 195, 65, 177, 193, 150, 153, 235, 164, 177, 52, 39, 143, 24, 85, 197, 41, 84, 78, 36, 18, 232, 243, 57, 110, 145, 18, 75, 55, 164, 81, 116, 21, 122, 122, 181, 171, 57, 20, 63, 147, 66, 226, 188, 141, 104, 194, 81],

    # m[4172]:
    [250, 180, 121, 157, 28, 204, 8, 242, 114, 156, 5, 240, 115, 129, 142, 194, 160, 36, 136, 193, 181, 241, 63, 253, 254, 211, 57, 35, 89, 66, 63, 73, 59, 171, 217, 209, 126, 155, 247, 43, 150, 99, 153, 215, 132, 103, 16, 86, 242],

    # m[4176]:
    [176, 180, 114, 217, 233, 76, 158, 79, 35, 127, 167, 46, 119, 222, 128, 169, 191, 253, 120, 190, 123, 236, 110, 163, 65, 94, 22, 31, 35, 231, 16, 174, 168, 106, 95, 93, 160, 29, 179, 53, 183, 7, 60, 162, 189, 74, 110, 106, 103],

    # m[4180]:
    [248, 69, 173, 169, 88, 169, 73, 188, 107, 110, 150, 138, 26, 123, 0, 127, 113, 245, 44, 14, 67, 52, 165, 224, 252, 82, 28, 110, 54, 122, 1, 30, 183, 104, 206, 46, 8, 207, 183, 138, 182, 117, 156, 110, 128, 157, 171, 7, 91],

    # m[4184]:
    [8, 156, 69, 25, 236, 68, 60, 213, 4, 172, 95, 27, 5, 124, 203, 55, 111, 229, 133, 98, 107, 120, 40, 156, 95, 115, 180, 208, 106, 59, 47, 57, 104, 29, 53, 166, 204, 120, 186, 112, 86, 85, 154, 77, 166, 211, 120, 219, 118],

    # m[4188]:
    [226, 143, 174, 202, 237, 226, 42, 101, 79, 81, 213, 110, 180, 81, 38, 104, 24, 89, 112, 177, 161, 121, 81, 34, 81, 196, 75, 3, 110, 134, 218, 104, 242, 130, 140, 38, 49, 75, 139, 62, 110, 172, 106, 86, 142, 77, 167, 105, 105],

    # m[4192]:
    [80, 17, 66, 212, 94, 125, 6, 41, 160, 157, 182, 200, 154, 66, 212, 231, 77, 42, 249, 125, 129, 208, 128, 20, 192, 243, 33, 162, 17, 164, 94, 246, 186, 143, 50, 185, 248, 186, 123, 60, 80, 66, 62, 33, 247, 129, 8, 239, 31],

    # m[4196]:
    [81, 139, 25, 57, 233, 229, 185, 96, 173, 22, 47, 37, 104, 128, 20, 133, 176, 50, 37, 250, 84, 13, 246, 72, 102, 23, 30, 204, 231, 98, 17, 106, 39, 1, 7, 253, 94, 230, 87, 32, 191, 23, 167, 150, 140, 55, 80, 67, 119],   

    # m[4200]:
    [105, 196, 90, 196, 124, 253, 35, 0, 91, 143, 122, 176, 71, 215, 5, 108, 122, 252, 188, 219, 200, 159, 159, 241, 232, 83, 79, 17, 194, 208, 15, 62, 67, 80, 123, 29, 47, 168, 234, 68, 56, 24, 46, 45, 89, 46, 132, 221, 86],

    # m[4204]:
    [69, 12, 13, 225, 71, 76, 254, 169, 78, 135, 82, 5, 193, 231, 141, 149, 251, 25, 132, 26, 57, 222, 26, 210, 42, 138, 145, 47, 201, 59, 135, 71, 160, 129, 127, 45, 47, 151, 54, 241, 57, 219, 71, 248, 77, 91, 44, 145, 176],

    # m[4208]:
    [240, 164, 45, 125, 101, 228, 50, 221, 161, 175, 235, 92, 65, 229, 128, 14, 254, 144, 9, 147, 4, 6, 152, 66, 147, 157, 193, 85, 253, 174, 112, 181, 86, 158, 90, 42, 94, 244, 58, 125, 199, 111, 8, 89, 37, 218, 9, 200, 50],

    # m[4212]:
    [178, 247, 234, 21, 251, 76, 5, 175, 105, 22, 51, 139, 244, 146, 22, 202, 54, 65, 76, 43, 205, 86, 158, 124, 71, 178, 67, 2, 64, 121, 13, 76, 108, 29, 193, 114, 48, 103, 219, 111, 131, 122, 124, 167, 83, 217, 11, 110, 232],

    # m[4216]:
    [131, 235, 213, 78, 227, 127, 52, 163, 62, 234, 203, 174, 73, 12, 61, 208, 167, 214, 4, 132, 152, 31, 115, 211, 189, 158, 201, 87, 121, 228, 246, 15, 236, 9, 96, 222, 112, 108, 104, 139, 89, 56, 48, 132, 111, 20, 7, 72, 174],

    # m[4220]:
    [235, 34, 250, 173, 179, 188, 218, 123, 30, 226, 40, 228, 207, 17, 141, 21, 172, 128, 23, 26, 117, 175, 128, 202, 44, 239, 161, 166, 253, 191, 107, 183, 138, 127, 213, 50, 133, 75, 184, 199, 199, 255, 67, 180, 159, 152, 232, 84, 239],

    # m[4224]:
    [155, 61, 154, 162, 51, 85, 204, 216, 23, 125, 151, 251, 116, 139, 196, 231, 180, 54, 24, 111, 13, 90, 158, 61, 118, 133, 150, 228, 195, 38, 121, 224, 156, 179, 162, 0, 241, 91, 38, 162, 115, 63, 188, 196, 70, 239, 131, 241, 164],

    # m[4228]:
    [158, 107, 181, 167, 146, 147, 68, 213, 184, 252, 52, 167, 10, 23, 35, 2, 182, 150, 103, 196, 58, 132, 146, 243, 222, 104, 27, 63, 212, 76, 195, 92, 188, 107, 92, 96, 145, 141, 177, 108, 174, 23, 17, 229, 178, 64, 209, 44, 190],

    # m[4232]:
    [223, 69, 65, 108, 111, 229, 104, 201, 105, 188, 81, 192, 56, 53, 82, 83, 241, 15, 97, 166, 194, 23, 241, 86, 72, 141, 116, 86, 21, 68, 54, 237, 96, 66, 240, 11, 53, 119, 39, 63, 139, 180, 19, 202, 23, 15, 195, 123, 52],

    # m[4236]:
    [157, 177, 129, 30, 248, 141, 245, 255, 19, 91, 249, 52, 3, 211, 225, 82, 142, 212, 72, 223, 175, 219, 22, 211, 250, 121, 209, 45, 70, 128, 208, 70, 128, 124, 6, 247, 52, 156, 1, 137, 79, 174, 69, 170, 98, 230, 213, 102, 33],

    # m[4240]:
    [44, 246, 209, 236, 70, 70, 180, 71, 155, 207, 228, 14, 137, 43, 94, 45, 53, 176, 121, 255, 206, 56, 61, 140, 191, 87, 197, 142, 155, 55, 67, 19, 139, 155, 21, 106, 88, 239, 224, 208, 203, 45, 212, 62, 173, 174, 58, 227, 54],

    # m[4244]:
    [6, 179, 3, 126, 149, 167, 108, 150, 33, 219, 198, 233, 251, 168, 115, 36, 55, 160, 235, 16, 76, 142, 228, 123, 184, 221, 116, 74, 85, 147, 59, 113, 61, 166, 245, 23, 172, 132, 10, 24, 199, 47, 199, 66, 203, 197, 253, 129, 193],

    # m[4248]:
    [113, 238, 10, 19, 231, 203, 51, 138, 219, 210, 176, 236, 182, 147, 23, 25, 251, 52, 161, 213, 230, 194, 61, 229, 224, 19, 243, 233, 43, 26, 77, 198, 245, 153, 232, 122, 253, 150, 121, 206, 176, 248, 177, 99, 98, 198, 130, 57, 179],

    # m[4252]:
    [156, 111, 253, 204, 184, 159, 220, 72, 176, 156, 79, 160, 40, 201, 95, 63, 240, 9, 140, 44, 36, 92, 17, 251, 178, 81, 226, 91, 66, 50, 241, 73, 84, 24, 64, 187, 27, 52, 61, 241, 181, 155, 135, 47, 113, 191, 232, 207, 56],

    # m[4256]:
    [58, 179, 252, 193, 242, 85, 168, 251, 47, 196, 147, 166, 223, 251, 42, 55, 28, 185, 38, 23, 230, 239, 105, 238, 217, 197, 238, 107, 178, 212, 27, 95, 77, 134, 159, 61, 229, 7, 85, 96, 87, 232, 125, 89, 44, 152, 66, 61, 223],

    # m[4260]:
    [181, 77, 50, 127, 215, 247, 134, 13, 30, 98, 64, 199, 77, 161, 210, 128, 124, 91, 239, 20, 186, 222, 151, 186, 92, 172, 13, 223, 215, 65, 161, 108, 172, 64, 40, 117, 189, 227, 135, 81, 174, 204, 183, 45, 61, 83, 195, 51, 183],

    # m[4264]:
    [203, 42, 52, 215, 162, 208, 149, 221, 184, 64, 219, 6, 155, 196, 206, 240, 226, 168, 94, 189, 28, 146, 209, 84, 250, 204, 204, 246, 112, 223, 29, 30, 69, 244, 100, 37, 250, 20, 255, 174, 193, 91, 65, 126, 75, 7, 114, 141, 55],

    # m[4268]:
    [232, 108, 24, 251, 61, 153, 121, 90, 58, 27, 45, 142, 3, 88, 54, 29, 122, 145, 160, 70, 146, 125, 187, 40, 78, 91, 155, 111, 153, 33, 106, 232, 210, 198, 47, 122, 223, 154, 4, 155, 60, 81, 255, 225, 22, 92, 56, 93, 170],

    # m[4272]:
    [52, 165, 34, 229, 99, 90, 18, 232, 42, 19, 180, 144, 219, 231, 114, 6, 186, 245, 172, 151, 112, 252, 168, 232, 127, 113, 221, 83, 250, 60, 74, 88, 163, 23, 47, 120, 226, 13, 10, 34, 60, 26, 255, 3, 165, 0, 57, 96, 116],

    # m[4276]:
    [77, 227, 18, 191, 216, 169, 246, 185, 113, 45, 118, 0, 8, 144, 142, 29, 145, 171, 42, 224, 138, 39, 154, 53, 119, 154, 232, 47, 128, 43, 175, 200, 50, 100, 215, 98, 202, 98, 137, 17, 66, 64, 21, 208, 5, 31, 0, 192, 34],

    # m m[4280]:
    [0, 106, 198, 153, 63, 224, 94, 25, 27, 181, 44, 170, 243, 237, 126, 249, 108, 196, 100, 241, 164, 136, 38, 103, 123, 131, 35, 83, 182, 252, 16, 54, 209, 223, 2, 62, 199, 158, 39, 122, 118, 145, 30, 65, 212, 199, 70, 205, 216],

    # m[4284]:
    [97, 227, 167, 124, 20, 193, 221, 116, 101, 164, 158, 33, 116, 181, 150, 215, 123, 248, 30, 214, 155, 77, 105, 188, 139, 162, 95, 118, 219, 66, 246, 136, 92, 197, 7, 199, 216, 112, 29, 200, 22, 80, 64, 7, 203, 100, 80, 26, 1],

    # m[4288]:
    [10, 177, 31, 35, 108, 132, 53, 119, 122, 72, 51, 62, 160, 167, 251, 191, 245, 142, 79, 235, 184, 142, 194, 218, 240, 66, 226, 179, 125, 18, 246, 234, 25, 56, 4, 240, 215, 214, 42, 143, 32, 87, 5, 215, 62, 231, 179, 186, 219]
]

for i in range(49):
    e = sum(coefficients[i][j] * flag[j] for j in range(49))
    s.add(e == target[i])

if s.check() == sat:
    m = s.model()
    raw = [m[b].as_long() for b in flag]
    [print(chr(x), end='') for x in raw]
```

`.;,;.{we_ought_to_start_storing_our_data_as_dna_instead}`
