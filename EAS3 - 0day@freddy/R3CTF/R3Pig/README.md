# Mô tả

R3GIRL opened the resulting text, for the first time, a human being read a message from the r3kapig world. There was a warning repeated three times:

**"Do not answer! Do not answer!! Do not answer!!!"**

The message revealed a huge secret, and the fate of the entire human race was now tied to her fingers!

# Phân tích

Follow tcp stream sẽ thấy số pi được lặp lại 3 lần và kết thúc bằng `EOF`, lúc đầu khi nhìn đề bài thì nghĩ rằng việc bị lặp lại 3 lần sẽ có liên quan nên kiểm tra các packet sau mỗi một chuỗi số pi nhưng kết quả lại không có gì

Trong các packet tcp cũng không có urgent value. Vậy dữ liệu mật thực sự được chuyển đi như nào ?

Cứ sau mỗi khi server `192.168.0.24:1337` gửi 1 chữ số của pi cho server thì server sẽ trả lại 1 tcp ack để xác nhận chuyển thành công (Không quan trọng trong phân tích bài này), vậy thì filter wireshark của ta sẽ như này để chỉ tập trung vào phần dữ liệu được chuyển đi

``` 
tcp && ip.src == 192.168.0.24 && data
```

Nếu để ý kĩ thời gian trong mục `frame.time_delta_displayed` của các packet (trừ packet đầu tiên ra) thì đều thuộc khoảng 2 giá trị là ~0,2 hoặc ~0,1. Vậy bây giờ sẽ thử xuất các giá trị đó ra sau đó tạo script để đưa chúng về 2 giá trị 0 và 1. Sau khi thử 2 trường hợp thì biết được chuyển `0,2 = 0` và `0,1 = 1` sẽ cho ta flag

**Lấy các giá trị thời gian ra file (Không lấy packet số 7 do nó có giá trị = 0)**

 ```bash
 tshark -r pig.pcapng -Y "tcp && ip.src == 192.168.0.24 && data" -T fields -e frame.time_delta_displayed > raw.txt
 ```

Xong vào file raw.txt xoá dòng `0.000000` ở đầu đi

```py
def convert_value(val):
    try:
        f = float(val)
        if 0.09 <= f <= 0.11:
            return '1'
        elif 0.015 <= f <= 0.03:
            return '0'
        else:
            return '?'  # Unknown / ambiguous
    except ValueError:
        return '?'  # Not a float

def main():
    with open("raw.txt", "r") as infile:
        lines = infile.readlines()

    results = [convert_value(line.strip()) for line in lines if line.strip()]
    
    # Join results into a binary string
    binary_string = ''.join(results)

    # Optionally group bits into bytes
    byte_grouped = ' '.join([binary_string[i:i+8] for i in range(0, len(binary_string), 8)])

    # Write result
    with open("converted.txt", "w") as outfile:
        outfile.write(byte_grouped + '\n')

    print("✅ Done. Output saved to converted.txt")

if __name__ == "__main__":
    main()
```

Sau đó đưa giá trị trong `converted.txt` lên mấy trang web [decode binary](https://gchq.github.io/CyberChef/#recipe=From_Binary('Space',8)Remove_null_bytes()&input=MDEwMDExMDEgMDExMTEwMDEgMDAxMDAwMDAgMDExMDAwMTEgMDExMTAwMTAgMDExMDAwMDEgMDExMTEwMTAgMDExMTEwMDEgMDAxMDAwMDAgMDExMDAwMDEgMDExMTAwMTAgMDExMDExMDEgMDExMTEwMDEgMDAxMDAwMDAgMDExMDEwMTEgMDExMDExMTAgMDExMDExMTEgMDExMTAxMTEgMDExMTAwMTEgMDAxMDAwMDAgMDExMTAxMDAgMDExMDEwMDAgMDExMDAxMDEgMDAxMDAwMDAgMDExMTAwMDAgMDExMDEwMDEgMDExMDAxMTEgMDExMTAwMTEgMDAxMDAxMTEgMDAxMDAwMDAgMDExMTAwMTEgMDExMDAxMDEgMDExMDAwMTEgMDExMTAwMTAgMDExMDAxMDEgMDExMTAxMDAgMDAxMDAwMDEgMDAxMDAwMDAgMDExMTAwMTAgMDAxMTAwMTEgMDExMDAwMTEgMDExMTAxMDAgMDExMDAxMTAgMDExMTEwMTEgMDExMTAxMDAgMDExMDEwMDAgMDAxMTAwMTEgMDAxMDExMDEgMDExMTAxMDAgMDExMDEwMDAgMDExMTAwMTAgMDAxMTAwMTEgMDAxMTAwMTEgMDAxMDExMDEgMDExMDAwMTAgMDAxMTAwMDAgMDExMDAxMDAgMDExMTEwMDEgMDAxMDExMDEgMDExMTAwMDAgMDExMTAwMTAgMDAxMTAwMDAgMDExMDAwMTAgMDExMDExMDAgMDExMDAxMDEgMDExMDExMDEgMDAxMDExMDEgMDExMDEwMDAgMDAxMTAxMDAgMDExMDAxMDAgMDAxMDExMDEgMDExMDExMTAgMDAxMTAwMDAgMDAxMDExMDEgMDExMTAwMTEgMDExMDExMTEgMDExMDExMDAgMDExMTAxMDEgMDExMTAxMDAgMDExMDEwMDEgMDExMDExMTEgMDExMDExMTAgMDExMTExMDEgMDAxMDAwMDAgMDEwMDAxMDAgMDExMDExMTEgMDAxMDAwMDAgMDExMDExMTAgMDExMDExMTEgMDExMTAxMDAgMDAxMDAwMDAgMDExMDAwMDEgMDExMDExMTAgMDExMTAwMTEgMDExMTAxMTEgMDExMDAxMDEgMDExMTAwMTAgMDAxMDAwMDEgMDAxMDAwMDAgMDEwMDAxMDAgMDExMDExMTEgMDAxMDAwMDAgMDExMDExMTAgMDExMDExMTEgMDExMTAxMDAgMDAxMDAwMDAgMDExMDAwMDEgMDExMDExMTAgMDExMTAwMTEgMDExMTAxMTEgMDExMDAxMDEgMDExMTAwMTAgMDAxMDAwMDEgMDAxMDAwMDEgMDAxMDAwMDAgMDEwMDAxMDAgMDExMDExMTEgMDAxMDAwMDAgMDExMDExMTAgMDExMDExMTEgMDExMTAxMDAgMDAxMDAwMDAgMDExMDAwMDEgMDExMDExMTAgMDExMTAwMTEgMDExMTAxMTEgMDExMDAxMDEgMDExMTAwMTAgMDAxMDAwMDEgMDAxMDAwMDEgMDAxMDAwMDEgMDEwMDExMDEgMDExMTEwMDEgMDAxMDAwMDAgMDExMDAwMTEgMDExMTAwMTAgMDExMDAwMDEgMDExMTEwMTAgMDExMTEwMDEgMDAxMDAwMDAgMDExMDAwMDEgMDExMTAwMTAgMDExMDExMDEgMD8xMTEwMDEgMDAxMDAwMDAgMDExMDEwMTEgMDExMDExMTAgMDExMDExMTEgMDExMTAxMTEgMDExMTAwMTEgMDAxMDAwMDAgMDExMTAxMDAgMDExMDEwMDAgMDExMDAxMDEgMDAxMDAwMDAgMDExMTAwMDAgMDExMDEwMDEgMDExMDAxMTEgMDExMTAwMTEgMDAxMDAxMTEgMDAxMDAwMDAgMDExMTAwMTEgMDExMDAxMDEgMDExMDAwMTEgMDExMTAwMTAgMDExMDAxMDEgMDExMTAxMDAgMDAxMDAwMDEgMDAxMDAwMDAgMDExMTAwMTAgMDAxMTAwMTEgMDExMDAwMTEgMDExMTAxMDAgMDExMDAxMTAgMDExMTEwMTEgMDExMTAxMDAgMDExMDEwMDAgMDAxMTAwMTEgMDAxMDExMDEgMDExMTAxMDAgMDExMDEwMDAgMDExMTAwMTAgMDAxMTAwMTEgMDAxMTAwMTEgMDAxMDExMDEgMDExMDAwMTAgMDAxMTAwMDAgMDExMDAxMDAgMDE) trên mạng hoặc tự thêm phần decode vào trong script

```
My crazy army knows the pigs' secret! r3ctf{th3-thr33-b0dy-pr0blem-h4d-n0-solution} Do not answer! Do not answer!! Do not answer!!!My crazy arm knows the pigs' secret! r3ctf{th3-thr33-b0d
```



# Flag

`r3ctf{th3-thr33-b0dy-pr0blem-h4d-n0-solution}`