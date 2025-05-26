# Mô tả



# Phân tích

Chạy thử

```
$ ./whats-a-base
Enter the password:
hello
Invalid password!
```

Giống bài trước, cần tìm hiểu input được so sánh với password thực sự như nào

Đưa vào IDA nó ko tự load ra hàm main zzz, đi đến hàm main thì cũng không có gì nhiều lắm, bây giờ chỉ còn cách thử check strings thì thấy một vài điều khá kì lạ

```
already borrowedassertion `left  right` failed: ) when slicing `core/src/time.rsrange end index called `Result::unwrap()` on an `Err` valueEnter the password:
src/main.rsm7xzr7muqtxsr3m8pfzf6h5ep738ez5ncftss7d1cftskz49qj4zg7n9cizgez5upbzzr7n9cjosg45wqjosg3muInvalid password!
Congratulations! flag{}
0123456789abcdef{invalid syntax}
_NoneSomemainnameVarsArgscodekindKindpeer
fullIterOnce/
varsPATHaddrDiskmodereadFilepathHOME && env args
NullNOEX
Zinit    (..)true <= dataybndrfg8ejkmcpqxot1uwisza345h769std/src/io/buffered/bufwriter.rsstd/src/os/unix/net/ancillary.rsstd/src/sys/sync/rwlock/futex.rs
```

Có một vài dữ liệu linh tinh được đưa vào giữa các từ như sau `main.rs` .... `Invali password!` với cả sau `data` .... `std/src/io` hay cái string kì lạ này là 

- `m7xzr7muqtxsr3m8pfzf6h5ep738ez5ncftss7d1cftskz49qj4zg7n9cizgez5upbzzr7n9cjosg45wqjosg3mu`
- `ybndrfg8ejkmcpqxot1uwisza345h769`

Đưa 2 cái này lên https://www.dcode.fr/cipher-identifier thì đoạn thứ nhất trả về là `z-base-32` còn đoạn thứ 2 là `base-58` nhưng mà đoạn thứ nhất tỉ lệ đoán chính xác cao hơn nên khá chắc đây là cipher text, trên [cyberchef](https://gchq.github.io/CyberChef/#recipe=From_Base32('ybndrfg8ejkmcpqxot1uwisza345h769',true)&input=bTd4enI3bXVxdHhzcjNtOHBmemY2aDVlcDczOGV6NW5jZnRzczdkMWNmdHNrejQ5cWo0emc3bjljaXpnZXo1dXBienpyN245Y2pvc2c0NXdxam9zZzNtdQ) khi chọn `From base32` thì cái alphabet default không được nhưng lúc cho đoạn thứ 2 vào alphabet sẽ ra một đoạn, đoán rằng đây là mật khẩu

`__rust_begin_short_backtrace__rust_end_short_backtraces`

# Flag

```
$ ./whats-a-base
Enter the password:
__rust_begin_short_backtrace__rust_end_short_backtraces
Congratulations! flag{50768fcb270edc499750ea64dc45ee92}
```

clm thôi thì do đề bài có nhắc đến base