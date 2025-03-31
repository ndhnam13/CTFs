https://github.com/kimci86/bkcrack

# Phân tích
./bkcrack-1.7.1-Linux/bkcrack -L deflated.zip
Check decryption của file zip biết được git/HEAD và .git/refs/heads/main ở dạng `Stored`
và theo tài liệu của bkcrack ta có thể đoán >= 12bytes đầu của plaintext để lấy được decryption key của file zip

Known plaintext của .git/HEAD thường có: `ref: refs/heads/main` tạo một file chứa đoạn plaintext này sau đó zip nó lại

`echo "ref: refs/heads/main" > HEAD_plain`

`zip -0 known.zip HEAD_plain`

# Lấy decryption key
`./bkcrack-1.7.1-Linux/bkcrack -C deflated.zip -c .git/HEAD -P known.zip -p HEAD_plain`

keys: `f2635bca a91bec3a ec81bdf9`

3 key này chỉ hoạt động cho toàn bộ file zip nếu các file còn lại trong đó sử dụng chung bộ key này, trong trường hợp của bài thì là có

# Decrypt
`./bkcrack-1.7.1-Linux/bkcrack -C deflated.zip -k f2635bca a91bec3a ec81bdf9 -D decrypted.zip`

# Tìm flag
Kiểm tra `C:\Users\admin\Desktop\.git\logs\refs\heads`

```
nam@DESKTOP-NF3DDH9:/mnt/c/Users/admin/Desktop$ git log --oneline
5e6304a (HEAD -> main) remove flag and put a super long commit message so that it gets compressed
01c525a initial commit
```

print_flag.py đã bị thay đổi

Kiểm tra đã thay đổi cái gì: `git diff 01c525a1a206c1a6dd2f4124b19c60853e16ff3c 5e6304a711c542fb448a368be9270c7aba3ba627`

Khôi phục flag trước khi sửa

`git checkout 01c525a1a206c1a6dd2f4124b19c60853e16ff3c -- print_flag.py`

`gigem{}`