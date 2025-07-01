# Mô tả

Byte Doctor suspects the attacker used a process injection technique to run malicious code within a legitimate process, leaving minimal traces on the file system. The logs reveal Win32 API calls that hint at a specific injection method used in the attack.

Your task is to analyze these logs using a tool called API Monitor to uncover the injection technique and identify which legitimate process was targeted.

# HDSH

- Use IDA (Free) to open `inject.exe.i64`

Use [API Monitor](http://www.rohitab.com/apimonitor) to open `.apmx64` files:

- Navigate to "Files" and click on "Open" to view captured data from the file: "DC.apmx86" or "WKSTN1.apmx64"

- After opening the file, the "Monitoring Process" window will populate with a list of processes. Expand the view by clicking the '+' symbol to reveal the modules and threads associated with each process.

- The API calls can be observed in the "Summary" window. To focus our analysis on a specific module, click on the different DLLs loaded by the processes.

# Phân tích

## [1/7] What process injection technique is being used? Hint: `T***** L**** S******`

Vào phần export trong IDA thấy `TlsCallback_0	0000000140001000`, tìm trên google biết được đây là kỹ thuật **Thread Local Storage**   , thực thi lệnh trước khi chương trình vào entry point

`Thread Local Storage`

## [2/7] Which Win32 API was used to take snapshots of all processes and threads on the system?

Vào file `apmx64` trong module `inject.exe` thấy rằng để tìm và lấy snapshot của các tiến trình, luồng trên hệ thống nó đã dùng API `CreateToolhelp32Snapshot`

## [3/7] Which process is the attacker's binary attempting to locate for payload injection?

Sau đó thì thực hiện các API `lstrcmpiA` với `Notepad.exe` và tìm qua từng tiến trình một đang chạy trên máy cho đến khi gặp `lstrcmpiA ( "Notepad.exe", "Notepad.exe" )` sẽ trả về true

`Notepad.exe`

## [4/7] What is the process ID of the identified process?

Sau khi tìm thấy tiến trình mục tiêu, injector gọi `OpenProcess` để lấy handle của `Notepad.exe`. `OpenProcess` sẽ có yêu cầu đưa vào Process ID vậy ta chỉ cần xem các tham số được đưa vào `OpenProcess` trong api monitor

```c
HANDLE OpenProcess(
  [in] DWORD dwDesiredAccess,
  [in] BOOL  bInheritHandle,
  [in] DWORD dwProcessId
);
```

```c
OpenProcess ( PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION | PROCESS_VM_OPERATION | PROCESS_VM_READ | PROCESS_VM_WRITE, FALSE, 16224 )
```

`16224`

## [5/7] What is the size of the shellcode?

Để biết độ lớn của shellcode cần inject vào ta có thể xem hai API `WriteProcessMemory` hoặc `VirtualAllocEx` để biết Injector đã khởi tạo bao nhiêu dung lượng bộ nhớ sau khi có được handle của tiến trình. Khả năng cao là để đưa shellcode vào và thực hiện

```c
LPVOID VirtualAllocEx(
  [in]           HANDLE hProcess,
  [in, optional] LPVOID lpAddress,
  [in]           SIZE_T dwSize,
  [in]           DWORD  flAllocationType,
  [in]           DWORD  flProtect
);

BOOL WriteProcessMemory(
  [in]  HANDLE  hProcess,
  [in]  LPVOID  lpBaseAddress,
  [in]  LPCVOID lpBuffer,
  [in]  SIZE_T  nSize,
  [out] SIZE_T  *lpNumberOfBytesWritten
);
```

```c
WriteProcessMemory ( 0x0000000000000268, 0x00000206583d0000, 0x00007ff746571000, 511, NULL )
VirtualAllocEx ( 0x0000000000000268, NULL, 511, MEM_COMMIT, PAGE_EXECUTE_READ )
```

`511`

## [6/7] Which Win32 API was used to execute the injected payload in the identified process?

Sau khi viết được shellcode vào 1 vùng nhớ tren tiến trình đích rồi thì injector sẽ cần phải thực thi cái payload đó. Một trong các cách phổ biến đó là tạo thêm một luồng thực thi trên tiến trình đích qua API `CreateRemoteThread`

```c
HANDLE CreateRemoteThread(
  [in]  HANDLE                 hProcess,
  [in]  LPSECURITY_ATTRIBUTES  lpThreadAttributes,
  [in]  SIZE_T                 dwStackSize,
  [in]  LPTHREAD_START_ROUTINE lpStartAddress,
  [in]  LPVOID                 lpParameter,
  [in]  DWORD                  dwCreationFlags,
  [out] LPDWORD                lpThreadId
);
```

```c
CreateRemoteThread ( 0x0000000000000268, NULL, 0, 0x00000206583d0000, NULL, 0, NULL )
```

`CreateRemoteThread`

## [7/7] The injection method used by the attacker executes before the main() function is called. Which Win32 API is responsible for terminating the program before main() runs?

Sau đó thì để giết chương trình thì chỉ cần exit thôi, trong windows API cũng có hàm để thực hiện việc đó

`ExitProcess`