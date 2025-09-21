#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trích tất cả Unicode grapheme cluster duy nhất từ một file nhị phân
và in ra mỗi grapheme một dòng.
"""

import sys
import regex  # pip install regex

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} dump.bin [output.txt]", file=sys.stderr)
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None

    with open(in_file, "rb") as f:
        raw = f.read()

    # Giải mã UTF-8, bỏ byte lỗi
    text = raw.decode("utf-8", errors="ignore")

    seen = set()
    unique_graphemes = []

    # regex \X: 1 Unicode grapheme cluster
    for g in regex.findall(r"\X", text):
        if g not in seen:
            seen.add(g)
            unique_graphemes.append(g)

    if out_file:
        with open(out_file, "w", encoding="utf-8") as f:
            for g in unique_graphemes:
                f.write(g + "\n")
        print(f"[+] Wrote {len(unique_graphemes)} unique graphemes to {out_file}")
    else:
        for g in unique_graphemes:
            print(g)

if __name__ == "__main__":
    main()
