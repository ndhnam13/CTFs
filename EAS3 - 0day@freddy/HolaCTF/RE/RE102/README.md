Chạy thử

```
$ ./RE102
SecureSoft Enterprise License Management System v4.7.2
Copyright (c) 2024 SecureSoft Technologies Inc.
Initializing secure authentication protocols...

Warning: Debugger environment detected
Loading security module 1/5...
Loading security module 2/5...
Loading security module 3/5...
Loading security module 4/5...
Loading security module 5/5...
Warning: System integrity compromised
Database connections: 0
Network status: Offline
Encryption level: 531 bits
Security policy violations detected (2). Entering safe mode.
Trial access granted: HOLACTF{trial_version_expires_soon}
```

Đưa file vào DiE thì chỉ hiện `Operating System: UNIX...` khả năng cao đã bị packed. Kiểm tra thêm section header bằng `readelf -S` thì báo là không có section header vậy chắc chắn rằng file này bị packed

Nhìn qua strings thì thấy

```
$Info: This file is packed with the XXX executable packer http://xxx.sf.net $
$Id: XXX 4.22 Copyright (C) 1996-2024 the XXX Team. All Rights Reserved. $
```

Và 1 vài string `FAKE` (1 cái ở đầu 2 cái ở cuối), tìm cái string trên google thì khá là tương đồng với string trong một file bị packed bởi **UPX**

Thử tạo một file ELF print hello world xong rồi dùng UPX để pack xem như nào

```
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
$Id: UPX 4.24 Copyright (C) 1996-2024 the UPX Team. All Rights Reserved. $
```

Và thay vì cái string `FAKE` như trên kia thì lại là `UPX!` cũng ở cùng vị trí

Vậy thử thay thế các string `FAKE` thành `UPX!` trong file RE102 xem như nào, đưa vào DiE và thấy nhận dạng được file bị packed bởi UPX thành công

Unpack và xem hàm main

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  unsigned int v3; // eax
  const char *v4; // rax
  char s2[8]; // [rsp+14h] [rbp-1Ch] BYREF
  int v7; // [rsp+1Ch] [rbp-14h]
  int v8; // [rsp+20h] [rbp-10h]
  int j; // [rsp+24h] [rbp-Ch]
  int i; // [rsp+28h] [rbp-8h]
  int v11; // [rsp+2Ch] [rbp-4h]

  signal(5, handle_security_violation);
  v3 = time(0);
  srand(v3);
  puts("SecureSoft Enterprise License Management System v4.7.2");
  puts("Copyright (c) 2024 SecureSoft Technologies Inc.");
  puts("Initializing secure authentication protocols...\n");
  initialize_logging_system();
  v11 = 0;
  v8 = verify_database_connection();
  v7 = validate_license_server();
  perform_system_maintenance();
  if ( (unsigned int)check_debugger_presence() )
  {
    ++v11;
    puts("Warning: Debugger environment detected");
  }
  configure_user_settings();
  for ( i = 0; i <= 4; ++i )
  {
    usleep(0xC350u);
    printf("Loading security module %d/5...\n", i + 1);
  }
  if ( (unsigned int)validate_system_integrity() )
  {
    ++v11;
    puts("Warning: System integrity compromised");
  }
  if ( (unsigned int)measure_execution_timing() )
  {
    ++v11;
    puts("Warning: Abnormal execution timing detected");
  }
  printf("Database connections: %d\n", g_database_connections);
  if ( g_network_status )
    v4 = "Online";
  else
    v4 = "Offline";
  printf("Network status: %s\n", v4);
  printf("Encryption level: %d bits\n", g_encryption_level % 512 + 128);
  if ( (unsigned int)scan_parent_process() )
  {
    ++v11;
    puts("Warning: Suspicious parent process detected");
  }
  if ( v11 <= 0 )
  {
    puts("System integrity verified. Proceeding with license validation...");
    if ( argc == 2 )
    {
      printf("Validating license key: %s\n", argv[1]);
      strcpy(s2, "reverse");
      if ( !strcmp(argv[1], s2) )
      {
        puts("License key accepted. Connecting to activation servers...");
        for ( j = 0; j <= 2; ++j )
        {
          usleep(0x30D40u);
          printf("Authenticating with server %d...\n", j + 1);
        }
        if ( (unsigned int)activate_premium_subscription() )
        {
          puts("All systems operational. Welcome to SecureSoft Enterprise!");
          return 0;
        }
        else
        {
          puts("Server authentication failed. Switching to educational mode.");
          launch_educational_version();
          return 1;
        }
      }
      else
      {
        puts("Invalid license key provided. Starting demo session.");
        start_demo_session();
        return 1;
      }
    }
    else
    {
      printf("Usage: %s <license_key>\n", *argv);
      puts("Contact support@securesoft.com for license activation.");
      return 1;
    }
  }
  else
  {
    printf("Security policy violations detected (%d). Entering safe mode.\n", v11);
    printf("Trial access granted: %s\n", trial_subscription);
    return 0;
  }
}
```

Dùng các hàm này để kiểm tra, không phù hợp sẽ tăng `v11` và in ra fake flag và exit

```
check_debugger_presence()
validate_system_integrity()
measure_execution_timing()
scan_parent_process()
```

```c
__int64 check_debugger_presence()
{
  unsigned int v1; // [rsp+8h] [rbp-8h]
  int i; // [rsp+Ch] [rbp-4h]

  v1 = 0;
  if ( ptrace(PTRACE_TRACEME, 0, 1, 0) == -1 )
  {
    v1 = 1;
    g_database_connections = 1;
  }
  for ( i = 0; i <= 99; ++i )
    v1 ^= 3 * i % 7;
  return v1;
}
```

`check_debugger_presence()` sẽ luôn trả về giá trị dương dù có debugger hay không, vậy nên chạy bình thường cũng không được

Nếu vượt qua tất cả các check thì sẽ thực hiện hàm `activate_premium_subscription()`

```c
__int64 activate_premium_subscription()
{
  _BYTE v1[16]; // [rsp+0h] [rbp-70h] BYREF
  _BYTE v2[16]; // [rsp+10h] [rbp-60h] BYREF
  _BYTE v3[72]; // [rsp+20h] [rbp-50h] BYREF
  int v4; // [rsp+68h] [rbp-8h]
  int v5; // [rsp+6Ch] [rbp-4h]

  initialize_network_protocols(&database_connection_string, v2, 16);
  initialize_network_protocols(&api_authentication_token, v1, 16);
  v5 = process_encrypted_subscription(&premium_subscription_data, 32, v2, v1, v3);
  if ( v5 <= 0 )
    return 0;
  v4 = (unsigned __int8)v3[v5 - 1];
  v3[v5 - v4] = 0;
  puts("Premium subscription activated! Access granted.");
  return 1;
}
```

```c
__int64 __fastcall initialize_network_protocols(__int64 a1, __int64 a2, int a3)
{
  __int64 result; // rax
  unsigned int i; // [rsp+20h] [rbp-4h]

  for ( i = 0; ; ++i )
  {
    result = i;
    if ( (int)i >= a3 )
      break;
    *(_BYTE *)((int)i + a2) = *(_BYTE *)((int)i + a1) ^ 0x5A;
  }
  return result;
}
```

```c
__int64 __fastcall process_encrypted_subscription(__int64 a1, unsigned int a2, __int64 a3, __int64 *a4, __int64 a5)
{
  __int64 v5; // rdx
  __int64 *v6; // rax
  __int64 v7; // rdx
  _BYTE v11[16]; // [rsp+30h] [rbp-E0h] BYREF
  __int64 v12; // [rsp+40h] [rbp-D0h]
  __int64 v13; // [rsp+48h] [rbp-C8h]
  _BYTE v14[180]; // [rsp+50h] [rbp-C0h] BYREF
  int v15; // [rsp+104h] [rbp-Ch]
  int j; // [rsp+108h] [rbp-8h]
  int i; // [rsp+10Ch] [rbp-4h]

  v15 = (int)a2 / 16;
  generate_round_keys(a3, v14);
  v5 = a4[1];
  v12 = *a4;
  v13 = v5;
  for ( i = 0; i < v15; ++i )
  {
    decrypt_data_block(16 * i + a1, v14, v11);
    for ( j = 0; j <= 15; ++j )
      *(_BYTE *)(16 * i + j + a5) = *((_BYTE *)&v12 + j) ^ v11[j];
    v6 = (__int64 *)(16 * i + a1);
    v7 = v6[1];
    v12 = *v6;
    v13 = v7;
  }
  return a2;
}
```

Nói chung là `initialize_network_protocols()` sẽ XOR 2 biến là `database_connection_string` và `api_authentication_token` với `0x5A` làm key và IV sau đó `process_encrypted_subscription()` sẽ giải mã AES-128-CBC `premium_subscription_data`

Giờ ta chỉ cần lấy nhưng cái này ra sau đó giải mã là được

```
database_connection_string: 1723093F39283F2E113F236B68696E6F
api_authentication_token: 6b68696e6f6c6d62636a6b68696e6f6c
```

Kết quả sau khi XOR 0x5A

- Key: `MySecretKey12345` (`4d795365637265744b65793132333435`)
- IV: `1234567890123456` (`31323334353637383930313233343536`)

```
premium_subscription_data: 8f2c45917a6b12883de79455c28147937629f418ad52356987b14375289c64a8
```

Ciphertext (hex): `8f2c45917a6b12883de79455c28147937629f418ad52356987b14375289c64a8`

Sau đó giải mã AES_128_CBC

Flag ở dạng `HOLACTF{hex}`

`HOLACTF{1b0b403ac790763ba5218d13801aa4e801c5947d4d25705006e5c603b08807f2}`