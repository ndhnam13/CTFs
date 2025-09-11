# Mô tả

The frontend has gone down but the store is still open, can you buy the flag?

**Bài này sử dụng protocol `THRIFT` để giao tiếp với server**

```
thrift-store.chal.imaginaryctf.org:9090
```

# Phân tích

Trong `capture.pcap` khi filter `THRIFT` sẽ thấy nó gọi các hàm sau

`createBasket` : Tạo một giỏ hàng với id

`addToBasket` : Thêm hàng vào (Dựa vào item trong `getInventory`)

`getBasket`: Xem giỏ hàng  

`getInventory` : Xem item trong cửa hàng, giá tiền sẽ nằm ở `thrift.i64` trong phần data của `REPLY` từ server

`pay`: Trả tiền, tiền phải khớp với tổng tiền trong giỏ. Nếu khớp trả về receipt và nếu sai sẽ báo lỗi

Trong file capture gốc thì output của `getInventory` không đầy đủ (không có flag), ta sẽ phải tạo script mô phỏng lại protocol `THRIFT` để gọi lại `getInventory` đến server

`@ChatGBT help`

```py
#!/usr/bin/env python3
"""
Manual Thrift client (strict TBinary + TFramed) for thrift-store.
Supports single-call: createBasket, getInventory, addToBasket, getBasket, pay, price.
"""
import argparse
import socket
import struct
import sys
from typing import Any, Dict, List, Tuple, Union
import re

# ---- Protocol constants ----
CALL, REPLY, EXCEPTION, ONEWAY = 1, 2, 3, 4
TTYPE_STOP, TTYPE_BOOL, TTYPE_BYTE, TTYPE_DOUBLE, TTYPE_I16, TTYPE_I32, TTYPE_I64, TTYPE_STRING, TTYPE_STRUCT, TTYPE_MAP, TTYPE_SET, TTYPE_LIST = (
    0, 2, 3, 4, 6, 8, 10, 11, 12, 13, 14, 15
)

# ---- IO helpers ----
def send_framed_and_recv(host: str, port: int, payload: bytes, timeout: float = 5.0) -> bytes:
    """Send one framed message; read one framed reply (or empty if none)."""
    with socket.create_connection((host, port), timeout=timeout) as s:
        s.settimeout(timeout)
        s.sendall(struct.pack(">I", len(payload)) + payload)
        hdr = s.recv(4)
        if len(hdr) < 4:
            return b""
        ln = struct.unpack(">I", hdr)[0]
        data = b""
        while len(data) < ln:
            chunk = s.recv(ln - len(data))
            if not chunk:
                break
            data += chunk
        return data

def build_call(method: str, seqid: int, args_struct: bytes) -> bytes:
    """Strict TBinary CALL frame body (without the outer 4-byte transport frame)."""
    ver_type = 0x80010000 | CALL  # unsigned 32-bit
    name = method.encode()
    return (
        struct.pack(">I", ver_type) +
        struct.pack(">I", len(name)) + name +
        struct.pack(">i", seqid) +
        args_struct
    )

# ---- Write fields ----
def tstop() -> bytes: return b"\x00"
def tfield_string(fid: int, s: str) -> bytes: 
    b = s.encode(); return bytes([TTYPE_STRING]) + struct.pack(">hI", fid, len(b)) + b
def tfield_i32(fid: int, v: int) -> bytes: return bytes([TTYPE_I32]) + struct.pack(">hi", fid, int(v))
def tfield_i64(fid: int, v: int) -> bytes: return bytes([TTYPE_I64]) + struct.pack(">hq", fid, int(v))
def tfield_double(fid: int, v: float) -> bytes: return bytes([TTYPE_DOUBLE]) + struct.pack(">hd", fid, float(v))

# ---- Read & parse ----
def read_message(buf: bytes, i: int = 0):
    if i + 4 > len(buf): raise ValueError("short header")
    ver_type = struct.unpack_from(">I", buf, i)[0]; i += 4
    if (ver_type & 0xffff0000) != 0x80010000:
        raise ValueError("not strict TBinary reply")
    mtype = ver_type & 0xff
    nlen = struct.unpack_from(">I", buf, i)[0]; i += 4
    name = buf[i:i+nlen].decode(errors="ignore"); i += nlen
    seqid = struct.unpack_from(">i", buf, i)[0]; i += 4
    return mtype, name, seqid, i

def skip_field(buf: bytes, i: int, t: int) -> int:
    if t == TTYPE_STOP: return i
    if t == TTYPE_BOOL or t == TTYPE_BYTE: return i + 1
    if t == TTYPE_I16: return i + 2
    if t == TTYPE_I32: return i + 4
    if t == TTYPE_I64 or t == TTYPE_DOUBLE: return i + 8
    if t == TTYPE_STRING:
        ln = struct.unpack_from(">I", buf, i)[0]; i += 4; return i + ln
    if t == TTYPE_STRUCT:
        while True:
            if i >= len(buf): raise ValueError("EOF while skipping struct")
            st = buf[i]; i += 1
            if st == TTYPE_STOP: break
            if i + 2 > len(buf): raise ValueError("EOF in struct fid")
            i += 2
            i = skip_field(buf, i, st)
        return i
    if t == TTYPE_LIST or t == TTYPE_SET:
        et = buf[i]; i += 1
        size = struct.unpack_from(">i", buf, i)[0]; i += 4
        for _ in range(size):
            i = skip_field(buf, i, et)
        return i
    if t == TTYPE_MAP:
        kt = buf[i]; vt = buf[i+1]; i += 2
        size = struct.unpack_from(">i", buf, i)[0]; i += 4
        for _ in range(size):
            i = skip_field(buf, i, kt)
            i = skip_field(buf, i, vt)
        return i
    raise ValueError(f"unknown type to skip {t}")

def parse_struct(buf: bytes, i: int) -> Tuple[Dict[int, Tuple[str, Any]], int]:
    fields: Dict[int, Tuple[str, Any]] = {}
    while True:
        if i >= len(buf): raise ValueError("EOF in struct")
        t = buf[i]; i += 1
        if t == TTYPE_STOP: break
        if i + 2 > len(buf): raise ValueError("EOF in fid")
        fid = struct.unpack_from(">h", buf, i)[0]; i += 2

        if t == TTYPE_STRING:
            ln = struct.unpack_from(">I", buf, i)[0]; i += 4
            s = buf[i:i+ln]; i += ln
            fields[fid] = ("STRING", s)
        elif t == TTYPE_I32:
            v = struct.unpack_from(">i", buf, i)[0]; i += 4
            fields[fid] = ("I32", v)
        elif t == TTYPE_I64:
            v = struct.unpack_from(">q", buf, i)[0]; i += 8
            fields[fid] = ("I64", v)
        elif t == TTYPE_DOUBLE:
            v = struct.unpack_from(">d", buf, i)[0]; i += 8
            fields[fid] = ("DOUBLE", v)
        elif t == TTYPE_BOOL:
            v = 1 if buf[i] != 0 else 0; i += 1
            fields[fid] = ("BOOL", v)
        elif t == TTYPE_BYTE:
            v = struct.unpack_from(">b", buf, i)[0]; i += 1
            fields[fid] = ("BYTE", v)
        elif t == TTYPE_STRUCT:
            sub, i = parse_struct(buf, i)
            fields[fid] = ("STRUCT", sub)
        elif t == TTYPE_LIST:
            et = buf[i]; i += 1
            size = struct.unpack_from(">i", buf, i)[0]; i += 4
            items: List[Any] = []
            for _ in range(size):
                if et == TTYPE_STRUCT:
                    sub, i = parse_struct(buf, i)
                    items.append(sub)
                elif et == TTYPE_STRING:
                    ln = struct.unpack_from(">I", buf, i)[0]; i += 4
                    s = buf[i:i+ln]; i += ln
                    items.append(("STRING", s))
                elif et == TTYPE_I32:
                    v = struct.unpack_from(">i", buf, i)[0]; i += 4
                    items.append(("I32", v))
                elif et == TTYPE_I64:
                    v = struct.unpack_from(">q", buf, i)[0]; i += 8
                    items.append(("I64", v))
                elif et == TTYPE_DOUBLE:
                    v = struct.unpack_from(">d", buf, i)[0]; i += 8
                    items.append(("DOUBLE", v))
                elif et == TTYPE_BOOL:
                    v = 1 if buf[i] != 0 else 0; i += 1
                    items.append(("BOOL", v))
                elif et == TTYPE_BYTE:
                    v = struct.unpack_from(">b", buf, i)[0]; i += 1
                    items.append(("BYTE", v))
                else:
                    i = skip_field(buf, i, et)
            fields[fid] = ("LIST", (et, items))
        elif t == TTYPE_SET:
            et = buf[i]; i += 1
            size = struct.unpack_from(">i", buf, i)[0]; i += 4
            for _ in range(size):
                i = skip_field(buf, i, et)
            fields[fid] = ("SET", (et, []))
        elif t == TTYPE_MAP:
            kt = buf[i]; vt = buf[i+1]; i += 2
            size = struct.unpack_from(">i", buf, i)[0]; i += 4
            for _ in range(size):
                i = skip_field(buf, i, kt)
                i = skip_field(buf, i, vt)
            fields[fid] = ("MAP", (kt, vt, []))
        else:
            i = skip_field(buf, i, t)
            fields[fid] = ("SKIPPED", t)
    return fields, i

def decode_reply(buf: bytes):
    if not buf:
        return ("", "NO_REPLY")
    try:
        mtype, name, seqid, i = read_message(buf, 0)
    except Exception as e:
        return ("", f"PARSE_ERROR: {e}")
    if mtype == EXCEPTION:
        try:
            exc_fields, _ = parse_struct(buf, i)
            msg = exc_fields.get(1, ("STRING", b""))[1]
            try: msg = msg.decode()
            except: msg = repr(msg)
            return (name, f"EXCEPTION: {msg}")
        except Exception as e:
            return (name, f"EXCEPTION(parse_failed): {e}")
    try:
        result_fields, _ = parse_struct(buf, i)
        return (name, result_fields)
    except Exception as e:
        return (name, f"PARSE_ERROR(result): {e}")

def printable(b: bytes) -> str:
    return ''.join(chr(x) if 32 <= x <= 126 else '.' for x in b)

# ---- Commands ----
def cmd_create(args):
    payload = build_call("createBasket", seqid=1, args_struct=tstop())
    reply = send_framed_and_recv(args.host, args.port, payload, timeout=args.timeout)
    name, result = decode_reply(reply)
    print("[raw]", printable(reply))
    print("[decoded]", name, result)

def cmd_inventory(args):
    payload = build_call("getInventory", seqid=1, args_struct=tstop())
    reply = send_framed_and_recv(args.host, args.port, payload, timeout=args.timeout)
    name, result = decode_reply(reply)
    print("[raw]", printable(reply))
    print("[decoded]", name)
    if isinstance(result, dict):
        for k, (t, v) in result.items():
            if t == "LIST":
                et, items = v
                print(f"[items] count={len(items)} (showing up to {args.max})")
                shown = 0
                for entry in items:
                    if not isinstance(entry, dict): 
                        continue
                    slug = None; nm = None; desc = None; price = None; p_kind=None
                    for fid, (ft, fv) in entry.items():
                        if ft == "STRING":
                            if slug is None: slug = fv
                            elif nm is None: nm = fv
                            elif desc is None: desc = fv
                        elif ft in ("DOUBLE", "I64", "I32", "BYTE", "I16"):
                            price = fv; p_kind = ft
                    def D(x): 
                        return x.decode() if isinstance(x, (bytes,bytearray)) else str(x)
                    ptxt = "?" if price is None else (f"${price:.2f}" if p_kind=="DOUBLE" else f"{price} {p_kind.lower()}")
                    print("-", D(slug), "|", D(nm), "|", ptxt)
                    shown += 1
                    if shown >= args.max: break

def cmd_add(args):
    if args.qty is None or args.slug is None or args.basket is None:
        print("Missing --basket / --slug / --qty"); sys.exit(2)
    args_struct = (
        tfield_string(1, args.basket) +
        tfield_string(2, args.slug) +
        tfield_i32(3, int(args.qty)) +
        tstop()
    )
    payload = build_call("addToBasket", seqid=1, args_struct=args_struct)
    reply = send_framed_and_recv(args.host, args.port, payload, timeout=args.timeout)
    name, result = decode_reply(reply)
    print("[raw]", printable(reply))
    print("[decoded]", name, result)

def cmd_get(args):
    if args.basket is None:
        print("Missing --basket"); sys.exit(2)
    args_struct = tfield_string(1, args.basket) + tstop()
    payload = build_call("getBasket", seqid=1, args_struct=args_struct)
    reply = send_framed_and_recv(args.host, args.port, payload, timeout=args.timeout)
    name, result = decode_reply(reply)
    print("[raw]", printable(reply))
    print("[decoded]", name, result)

def cmd_pay(args):
    if args.basket is None:
        print("Missing --basket"); sys.exit(2)
    if args.dollars is None and args.cents is None:
        print("Provide either --dollars or --cents"); sys.exit(2)
    if args.dollars is not None and args.cents is not None:
        print("Use only one of --dollars / --cents"); sys.exit(2)
    if args.dollars is not None:
        args_struct = tfield_string(1, args.basket) + tfield_double(2, float(args.dollars)) + tstop()
    else:
        args_struct = tfield_string(1, args.basket) + tfield_i64(2, int(args.cents)) + tstop()
    payload = build_call("pay", seqid=1, args_struct=args_struct)
    reply = send_framed_and_recv(args.host, args.port, payload, timeout=args.timeout)
    name, result = decode_reply(reply)
    print("[raw]", printable(reply))
    print("[decoded]", name, result)


def cmd_price(args):
    target = args.slug
    target_lc = target.lower()
    payload = build_call("getInventory", seqid=1, args_struct=tstop())
    reply = send_framed_and_recv(args.host, args.port, payload, timeout=args.timeout)
    name, result = decode_reply(reply)
    if isinstance(result, str):
        print("[decoded]", name, result); return
    found = False
    slug_re = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    for k, (t, v) in result.items():
        if t != "LIST": continue
        et, items = v
        for entry in items:
            if not isinstance(entry, dict): continue
            string_fields = []
            price_val = None
            price_kind = None
            for fid, (ft, fv) in entry.items():
                if ft == "STRING":
                    try: s = fv.decode()
                    except: s = str(fv)
                    string_fields.append(s)
                elif ft in ("DOUBLE","I64","I32","I16","BYTE"):
                    price_val = fv; price_kind = ft
            # Match: if target equals ANY string (case-insensitive)
            if any(s.lower() == target_lc for s in string_fields):
                slug = next((s for s in string_fields if slug_re.match(s)), string_fields[0] if string_fields else target)
                print(f"[price] match strings={string_fields}")
                print(f"[price] slug='{slug}' kind={price_kind} value={price_val}")
                if price_kind == "DOUBLE":
                    print(f"[pay with dollars] --dollars {price_val:.2f}")
                elif price_kind in ("I64","I32","I16","BYTE"):
                    print(f"[pay with cents] --cents {price_val}")
                else:
                    print("[warn] no numeric price field found in this entry")
                found = True
                return
    if not found:
        print(f"[price] slug '{target}' not found in inventory (case-insensitive search). Try running `getInventory --max 100` and paste the [raw] block here.")


def fmt_field(ft, fv):
    if ft == "STRING":
        try: return ("STRING", fv.decode())
        except: return ("STRING", ''.join(chr(x) if 32<=x<=126 else '.' for x in fv))
    return (ft, fv)

def cmd_dump(args):
    # Dump the full structure of getInventory results, including field IDs and types
    reply = send_framed_and_recv(args.host, args.port, build_call("getInventory", 1, tstop()), timeout=args.timeout)
    name, result = decode_reply(reply)
    print("[decoded-name]", name)
    if not isinstance(result, dict):
        print("[decoded-body]", result); return
    for k, (t, v) in result.items():
        if t != "LIST": continue
        et, items = v
        print(f"[list] elements={len(items)} (showing up to {args.max})\n")
        for idx, entry in enumerate(items[:args.max]):
            if not isinstance(entry, dict):
                print(f"  [{idx}] <non-struct elem>", entry); continue
            print(f"  [{idx}] --- item struct ---")
            for fid, (ft, fv) in sorted(entry.items()):
                ftt, fvv = fmt_field(ft, fv)
                print(f"    field {fid}: {ftt} = {fvv}")
            print()

def cmd_price_scan(args):
    # For each item, guess numeric price candidates and print them next to slug strings
    reply = send_framed_and_recv(args.host, args.port, build_call("getInventory", 1, tstop()), timeout=args.timeout)
    name, result = decode_reply(reply)
    if not isinstance(result, dict):
        print("[decoded-body]", result); return
    target = args.slug.lower() if args.slug else None
    for k, (t, v) in result.items():
        if t != "LIST": continue
        et, items = v
        for entry in items:
            if not isinstance(entry, dict): continue
            strings = []
            numeric = []
            for fid, (ft, fv) in sorted(entry.items()):
                if ft == "STRING":
                    try: strings.append(fv.decode())
                    except: strings.append(''.join(chr(x) if 32<=x<=126 else '.' for x in fv))
                elif ft in ("DOUBLE","I64","I32","I16","BYTE"):
                    numeric.append((ft, fv, fid))
            if not strings: continue
            slug = strings[0]
            if (target is None) or (slug.lower()==target) or any(s.lower()==(target or "") for s in strings):
                nums = ", ".join([f"{kind}={val} (fid {fid})" for kind,val,fid in numeric]) or "<none>"
                print(f"- slug={slug} | other strings={strings[1:]} | nums: {nums}")

# Register new subcommands

# ---- CLI ----
def main():
    ap = argparse.ArgumentParser(description="Manual Thrift client (one-call).")
    ap.add_argument("--host", default="thrift-store.chal.imaginaryctf.org")
    ap.add_argument("--port", type=int, default=9090)
    ap.add_argument("--timeout", type=float, default=5.0)
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_dump = sub.add_parser("dump")
    ap_dump.add_argument("--max", type=int, default=50)

    ap_ps = sub.add_parser("price-scan")
    ap_ps.add_argument("--slug")

    sub.add_parser("createBasket")
    sub.add_parser("getInventory").add_argument("--max", type=int, default=12)

    ap_add = sub.add_parser("addToBasket")
    ap_add.add_argument("--basket", required=True)
    ap_add.add_argument("--slug", required=True)
    ap_add.add_argument("--qty", type=int, required=True)

    ap_get = sub.add_parser("getBasket")
    ap_get.add_argument("--basket", required=True)

    ap_pay = sub.add_parser("pay")
    ap_pay.add_argument("--basket", required=True)
    g = ap_pay.add_mutually_exclusive_group(required=True)
    g.add_argument("--dollars", type=float)
    g.add_argument("--cents", type=int)

    ap_price = sub.add_parser("price")
    ap_price.add_argument("--slug", required=True)

    args = ap.parse_args()

    if args.cmd == "createBasket":
        cmd_create(args)
    elif args.cmd == "getInventory":
        cmd_inventory(args)
    elif args.cmd == "addToBasket":
        cmd_add(args)
    elif args.cmd == "getBasket":
        cmd_get(args)
    elif args.cmd == "pay":
        cmd_pay(args)
    elif args.cmd == "price":
        cmd_price(args)
    elif args.cmd == "dump":
        cmd_dump(args)
    elif args.cmd == "price-scan":
        cmd_price_scan(args)

if __name__ == "__main__":
    main()
```

Sau đó bật capture trên wireshark rồi chạy `getInventory`, tôi đã lưu output vào `getInv.pcapng`

Mở lên và kiểm tra REPLY của server ta thấy có thêm item `flag` ở cuối khác với trong capture gốc, nó có giá 9999

Vậy ta thực hiện tạo giỏ, add flag vào sau đó mua với giá 9999

```
PS C:\Users\admin\Desktop> python .\thrift_manual_client.py pay --basket f4c08f9a-229a-4d5c-935d-cff4618b884a --cents 9999
[raw] ........pay..............ictf{l1k3_gRPC_bUt_l3ss_g0ogly}..
[decoded] pay {0: ('STRUCT', {1: ('STRING', b'ictf{l1k3_gRPC_bUt_l3ss_g0ogly}')})}
```

> **ictf{l1k3_gRPC_bUt_l3ss_g0ogly}**

