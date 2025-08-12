# ELF Crack Me 1 - Time to learn x86 ASM & gdb

Load vào DiE biết được file ELF này được viết bằng C

Đưa vào IDA xem pseudocode của hàm main()

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  void *v4; // [esp+2Ch] [ebp-8h]

  v4 = malloc(0x18u);
  memset(v4, 0, 0x18u);
  strcpy((char *)v4, "FLAG-4092");
  strcat((char *)v4, "849uio2jf");
  puts("Loading...");
  strcat((char *)v4, "klsj4kl");
  puts("Where is the flag?");
  return 0;
}
```

Chương trình chỉ in ra màn hình `Loading` và `Where is the flag?`. Trước đó cấp cho mảng `v4` 18 byte hexa sau đó copy `FLAG-4092` vào rồi `strcat` thêm 2 đoạn nữa => Đây là flag

`FLAG-4092849uio2jfklsj4kl`

# See No Evil - Part 1

Bài cho ta một file exe, chạy thử trước

```
PS C:\Users\admin\Desktop> .\411c114b12e0342ee45e5efe9778154c.exe
                 _   _     _ _
     /\         | | (_)   | | |
    /  \   _ __ | |_ _  __| | |__   __ _
   / /\ \ | '_ \| __| |/ _` | '_ \ / _` |
  / ____ \| | | | |_| | (_| | |_) | (_| |
 /_/    \_\_| |_|\__|_|\__,_|_.__/ \__, |
                                    __/ |
                                   |___/

       ... Debug me if you can ...
[*] Level 1... Your flag is at 0x000001E2A37DA700
[*] Level 2... Your flag is at 0x000001E2A37DA700
[*] Level 3... Your flag is at 0x000001E2A37DAC40
[*] Level 4... Your flag is at 0x000001E2A37DAC40
[*] Level 5... Your flag is at 0x000001E2A37DA700
```

Vậy là bài muốn ta debug, load vào x64dbg thì khi debug sẽ bị dừng đột ngột, do có chữ `Antidbg` nên sẽ thử load vào IDA tìm các vị trí có các hàm anti debug như là `IsDebuggerPresent` không, khi kiểm tra thì thấy có 2 vị trí, nên sẽ đặt breakpoint tại 2 chộ đó và thay đổi giá trị của RAX để không bị exit khi debug

```
__int64 __fastcall sub_140005760(int a1)
{
  _QWORD *v2; // [rsp+20h] [rbp-18h]
  __int64 v3; // [rsp+28h] [rbp-10h]

  v3 = sub_140002490((char *)&unk_140041EB8 + 8 * a1 - 8, 8);
  v2 = (_QWORD *)sub_140001240(v3, *(&off_140040D30 + a1 - 1), 40);
  printf("Your flag is at 0x%016IX\n", *v2);
  sub_1400011E0(v2);
  return sub_1400011E0(v3);
}
```

Vậy giá trị của flag1 nằm trong `v2`, ta sẽ đặt thêm breakpoint tại đó

Sau khi vá 2 hàm anti debug rồi chạy đến hàm `sub_140005760` rồi chạy thêm 1 lúc sẽ thấy giá trị của flag được đưa vào RAX

`FLAG-JDGIkhGvlCcoojXduitQuZKpGv`

# See No Evil - Part 2

Nếu patch 2 cái anti debug kia thì sau khi chạy qua part1 sẽ bị 1 vòng lặp vô hạn với string `Heap Corruption Detected`, đây có thể là 1 cách antidebug, vào trong IDA tìm string kia

```
void __fastcall __noreturn StartAddress(LPVOID lpThreadParameter)
{
  __int64 v1; // rdx
  __int64 v2; // rcx
  __int64 v3; // r8

  while ( 1 )
  {
    if ( *(_QWORD *)((char *)GetProcessHeap() + 116) )
    {
      OutputDebugStringA("Heap Corruption Detected.");
      MEMORY[0](v2, v1, v3);
    }
    unk_140041EC0 = 0x481257362EFB5820LL;
    SetEvent(hEvent);
  }
}
```

Đây là 1 vòng lặp vô tận, rất giống những gì bị gặp lúc trước, có lẽ được đặt ra để kiểm tra xem các giá trị của `IsDebuggerPresent` có bị thay đổi không. Đặt breakpoint đầu hàm `StartAddress`, chạy rồi vá các hàm anti debug kia

Khi chạy đến đây sẽ thấy trước vòng lặp while có 2 lệnh `xor eax, eax` và `cmp eax, 0x1` vậy ta chỉ cần đi đến đó rồi chỉnh giá trị của eax = 1 thì có thể thoát khỏi vòng lặp vô hạn

Sau đó làm như part1 sẽ có flag

# Can you see through the star

File exe được viết bằng C#

```C#
// Decompiled with JetBrains decompiler
// Type: crackmeform.Form1
// Assembly: crackmeform, Version=1.0.5208.21486, Culture=neutral, PublicKeyToken=null
// MVID: 7CD8305B-BB14-486C-AEFC-5386527E8042
// Assembly location: C:\Users\admin\Desktop\ff5749e901595df1b04c3055d64df615.exe

using System;
using System.Drawing;
using System.Runtime.ExceptionServices;
using System.Runtime.InteropServices;
using System.Windows.Forms;

#nullable disable
namespace crackmeform
{
  public class Form1 : Form
  {
    private Button button1;
    private MaskedTextBox maskedTextBox1;
    private System.ComponentModel.Container components;

    public Form1()
    {
      // ISSUE: fault handler
      try
      {
        this.InitializeComponent();
      }
      __fault
      {
        base.Dispose(true);
      }
    }

    private void \u007EForm1() => this.components?.Dispose();

    private void InitializeComponent()
    {
      this.button1 = new Button();
      this.maskedTextBox1 = new MaskedTextBox();
      this.SuspendLayout();
      this.button1.Location = new Point(12, 49);
      this.button1.Name = "button1";
      this.button1.Size = new Size(260, 23);
      this.button1.TabIndex = 0;
      this.button1.Text = "Generate Flag";
      this.button1.UseVisualStyleBackColor = true;
      this.button1.Click += new EventHandler(this.button1_Click);
      this.maskedTextBox1.Location = new Point(13, 13);
      this.maskedTextBox1.Name = "maskedTextBox1";
      this.maskedTextBox1.PasswordChar = '*';
      this.maskedTextBox1.ReadOnly = true;
      this.maskedTextBox1.Size = new Size(259, 20);
      this.maskedTextBox1.TabIndex = 1;
      this.AutoScaleDimensions = new SizeF(6f, 13f);
      this.AutoScaleMode = AutoScaleMode.Font;
      this.BackColor = SystemColors.ActiveCaptionText;
      this.ClientSize = new Size(284, 88);
      this.Controls.Add((Control) this.maskedTextBox1);
      this.Controls.Add((Control) this.button1);
      this.Name = nameof (Form1);
      this.StartPosition = FormStartPosition.CenterScreen;
      this.Text = "CrackMe";
      this.ResumeLayout(false);
      this.PerformLayout();
    }

    private void button1_Click(object sender, EventArgs e)
    {
      this.maskedTextBox1.Text = "FLAG-" + this.maskedTextBox1.Name + "vc" + this.button1.Name;
    }

    [HandleProcessCorruptedStateExceptions]
    protected override void Dispose([MarshalAs(UnmanagedType.U1)] bool _param1)
    {
      if (_param1)
      {
        try
        {
          this.\u007EForm1();
        }
        finally
        {
          base.Dispose(true);
        }
      }
      else
        base.Dispose(false);
    }
  }
}
```

Có thể thấy hàm `button1_Click` gán 

```C#
this.maskedTextBox1.Text = "FLAG-" + this.maskedTextBox1.Name + "vc" + this.button1.Name;
```

Trong hàm `InitializeComponent()`:

```C#
maskedTextBox1.Name = "maskedTextBox1";
button1.Name = "button1";
```

Vậy ta có flag `FLAG-maskedTextBox1vcbutton1`

# Windows x86 Reversing is cool!

Bài cho ta 1 file exe 32bit

Chạy thử

```
PS C:\Users\admin\Desktop> .\1231fa8523f32a9118993946bccfb9ec203.exe
Key:1
Wrong Key!
```

Đưa vào ida tìm hàm kiểm tra key

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4[7]; // [esp+1h] [ebp-423h] BYREF
  char Str[1024]; // [esp+8h] [ebp-41Ch] BYREF
  size_t v6; // [esp+408h] [ebp-1Ch]
  int *p_argc; // [esp+414h] [ebp-10h]

  p_argc = &argc;
  __main();
  qmemcpy(v4, &unk_403059, sizeof(v4));
  v6 = 0;
  printf("Key:");
  scanf("%1023s", Str);
  if ( strlen(Str) != 6 )
  {
    printf("Wrong Key!");
    ExitProcess(1u);
  }
  while ( v6 < strlen(v4) )
  {
    Str[v6] ^= 211u;
    if ( Str[v6] != v4[v6] )
    {
      printf("Wrong Key!");
      ExitProcess(2u);
    }
    ++v6;
  }
  show_flag(Str);
  return 0;
}
```

Vậy là key nhập vào phải dài 6 byte sau đó được XOR với 211 và so sánh với tứng byte của `v4`, nếu đúng thì sẽ showflag

Vào x64dbg ta sẽ đặt breakpoint tại `qmemcpy(v4, &unk_403059, sizeof(v4));` để xem giá trị của `v4`

6byte đó là `97 E0 EB A0 B8 E1` dịch ra là `D38sk2`

```
PS C:\Users\admin\Desktop> .\1231fa8523f32a9118993946bccfb9ec203.exe
Key:D38sk2
FLAG-PIIXtM36MtKJ8347qh72r7C3
```

`FLAG-PIIXtM36MtKJ8347qh72r7C3`

# Crack Me 1

Chạy thử thì chỉ hiện 1 message box thôi, đưa vào ida thấy các hàm sau

```c
void __cdecl sub_401348(char *Destination, size_t Size)
{
  __time32_t v2; // eax
  size_t v3; // esi
  char *Source; // [esp+28h] [ebp-50h]
  size_t v5; // [esp+2Ch] [ebp-4Ch]
  char v6[61]; // [esp+3Bh] [ebp-3Dh] BYREF

  v2 = time(0);
  srand(v2);
  Source = (char *)malloc(Size);
  memset(Source, 0, Size);
  strcpy(v6, "abcdefghijklmnopqrstuvwxyz0123456789");
  if ( Size != 5 )
  {
    v3 = 0;
    v5 = 0;
    do
    {
      Source[v3] = v6[rand() % (strlen(v6) - 1)];
      v3 = ++v5;
    }
    while ( v5 < Size - 5 );
  }
  strcpy(Destination, Source);
  strcat(Destination, ".dll");
  free(Source);
}

BOOL __cdecl sub_4014B0(unsigned __int16 a1, char *Source)
{
  void *v2; // ebx
  HGLOBAL Resource; // esi
  const void *v4; // edi
  HANDLE FileA; // ebx
  HRSRC hResInfo; // [esp+2Ch] [ebp-2Ch]
  HRSRC hResInfoa; // [esp+2Ch] [ebp-2Ch]
  DWORD NumberOfBytesWritten; // [esp+3Ch] [ebp-1Ch] BYREF

  v2 = malloc(0x100u);
  memset(v2, 0, 0x100u);
  hResInfo = FindResourceA(0, (LPCSTR)a1, (LPCSTR)0xA);
  Resource = LoadResource(0, hResInfo);
  v4 = LockResource(Resource);
  hResInfoa = (HRSRC)SizeofResource(0, hResInfo);
  sub_40141C((char *)v2, Source);
  NumberOfBytesWritten = 0;
  FileA = CreateFileA((LPCSTR)v2, 0x40000000u, 0, 0, 2u, 0x80u, 0);
  WriteFile(FileA, v4, (DWORD)hResInfoa, &NumberOfBytesWritten, 0);
  CloseHandle(FileA);
  return FreeResource(Resource);
}
```

Vậy là chương trình sẽ tạo một file với tên ngẫu nhiên sau đó tạo file .dll và đưa vào một thư mục, lười debug nên sẽ bật `promon` lên xem file dll được drop ở `C:\Users\<name>\AppData\Roaming\`

Đưa file dll vào IDA kiểm tra, thấy hàm sau được export

```c
int DisplayMessage()
{
  void *v0; // ebx
  _BYTE *v1; // edx
  int i; // esi
  _BYTE *v4; // [esp+1Ch] [ebp-9Ch]
  _BYTE v5[148]; // [esp+24h] [ebp-94h] BYREF

  v0 = malloc(0x100u);
  memset(v0, 0, 0x100u);
  v1 = v5;
  qmemcpy(v5, "\\", 0x7Cu);
  for ( i = 0; i != 31; ++i )
  {
    v4 = v1;
    sprintf((char *const)v0, "%s%c", (const char *)v0, (char)(*(_DWORD *)&v1[4 * i] - 22));
    v1 = v4;
  }
  return MessageBoxA(0, (LPCSTR)v0, "Secret Messge", 64u);
}
```

Khá đơn giản, bởi vì đây là dll 32bit nên ta sẽ dùng x32dbg và rundll32.exe để nhảy vào hàm này `"C:\Windows\SysWOW64\rundll32.exe" C:\Users\admin\AppData\Roaming\bisk1f2os5.dll,DisplayMessage` sau đó chạy thì `MessageBoxA` sẽ hiển thị flag

`FLAG-hqoj2a5xkey9h6rmf44dc612v7`