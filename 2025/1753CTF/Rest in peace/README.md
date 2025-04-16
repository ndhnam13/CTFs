# Mô tả
One of our agents never returned from his mission. We've found that he died captured by enemies. All that we got left are these backup files. Not sure how to get to them, but I think he used one of his family member names to secure it.

# Phân tích
Bài cho ta một thư mục `rest-in-peace_backup`, xem một lúc thì thấy nếu mà tìm kiếm tên các file trong thư mục `data index keys locks snapshot` trên google ta sẽ thấy đây là các file của phần mềm `restic` dùng để backup

https://restic.readthedocs.io/en/v0.16.0/manual_rest.html

Dùng `restic2john` để lấy hash, bởi vì hashcat không có chế độ dành cho restic nên ta sẽ dùng `john` để crack mật khẩu

Mô tả đề cập đến `Not sure how to get to them, but I think he used one of his family member names to secure it`, vậy thay vì dùng wordlist dài sẽ chỉ cần tìm wordlist chứa tên thôi

https://raw.githubusercontent.com/huntergregal/wordlists/refs/heads/master/names.txt

Sau khi có mật khẩu dùng `restic` để recover file và tìm flag

# Flag
`restic2john rest-in-peace_backup > hash.txt`

`john hash.txt --wordlist=names.txt`

Mật khẩu là `Christopher`

```
$ restic snapshots -r .
enter password for repository:
repository 5c2fc885 opened (version 2, compression level auto)
created new cache in /home/nam/.cache/restic
ID        Time                 Host        Tags        Paths  Size
------------------------------------------------------------------
cd3921b4  2025-04-12 00:27:29  AgentAlpha              /flag  16 B
------------------------------------------------------------------
1 snapshots
```

Thử recover xem sao

```
$ restic recover -r . cd3921b4
enter password for repository:
repository 5c2fc885 opened (version 2, compression level auto)
load index files
[0:00] 100.00%  4 / 4 index files loaded
load 4 trees
[0:00] 100.00%  4 / 4 trees loaded
load snapshots
done

found 3 unreferenced roots
saved new snapshot 9aba141b
```

```
$ restic snapshots -r .
enter password for repository:
repository 5c2fc885 opened (version 2, compression level auto)
ID        Time                 Host             Tags        Paths     Size
--------------------------------------------------------------------------
cd3921b4  2025-04-12 00:27:29  AgentAlpha                   /flag     16 B
9aba141b  2025-04-16 13:04:31  DESKTOP-NF3DDH9  recovered   /recover
--------------------------------------------------------------------------
2 snapshots
```

Bây giờ nếu muốn xem nội dung của `9aba141b` cần restore đến 1 đường dẫn
```
$ restic restore -r . 9aba141b --target=.
enter password for repository:
repository 5c2fc885 opened (version 2, compression level auto)
[0:00] 100.00%  5 / 5 index files loaded
restoring snapshot 9aba141b of [/recover] at 2025-04-16 13:04:31.005034958 +0700 +07 by nam@DESKTOP-NF3DDH9 to .
Summary: Restored 15 files/dirs (103 B) in 0:00
```

Xuất hiện thêm 3 thư mục `4cf74ce5  a0811fc2  ac3313e0`

```
$ ls *
config

4cf74ce5:
flag1.txt  flag3.txt  flag4.txt  flag5.txt

a0811fc2:
flag1.txt  flag2.txt  flag3.txt  flag4.txt  flag5.txt

ac3313e0:
flag1.txt  flag4.txt  flag5.txt
```

Có thể thấy chỉ có một thư mục chứa đầy đủ 5 phần của flag, kết hợp 5 file lại sẽ ra flag
```
a0811fc2:
flag1.txt  flag2.txt  flag3.txt  flag4.txt  flag5.txt
```

`1753c{faked_my_own_death_to_save_the_flag}`
