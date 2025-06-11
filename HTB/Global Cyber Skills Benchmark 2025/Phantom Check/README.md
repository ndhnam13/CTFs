# Mô tả

Talion suspects that the threat actor carried out anti-virtualization checks to avoid detection in sandboxed environments. Your task is to analyze the event logs and identify the specific techniques used for virtualization detection. Byte Doctor requires evidence of the registry checks or processes the attacker executed to perform these checks.

# Phân tích

## Q1

**Which WMI class did the attacker use to retrieve model and manufacturer information for virtualization detection?**

[WMI](https://learn.microsoft.com/en-us/windows/win32/wmisdk/wmi-start-page) được sử dụng để quản lí dữ liệu, giám sát hệ thống trong các hệ điều hành Windows-based, thường hay bị lợi dụng bởi malware để thu thập thông tin về hệ thống và ở đây là phát hiện phần mềm ảo hoá 

Filter id `4104` và tìm từ khoá `WMI` trong log powershell operational ta sẽ thấy lệnh vào 4:19:10

```powershell
Creating Scriptblock text (1 of 1):
$Model = Get-WmiObject -Class Win32_ComputerSystem | select-object -expandproperty "Model"

ScriptBlock ID: f7d9f302-0766-4979-bd48-2e152dd54b12
Path: 
```

Gọi tới WMI class `Win32_ComputerSystem`, chứa thông tin về hệ thống máy tính. Sau đó trích xuất giá trị cụ thể của thuộc tính `"Model"` từ kết quả trả về rồi lưu vào biến `$Model` để sử dụng xong

Nếu lệnh trên được chạy trên một máy bình thường thì sẽ trả về tên máy thôi. Nhưng trong trường hợp chạy trên một môi trường ảo hoá thì sẽ trả về `VMware Virtual Platform (VMware)` hoặc `Virtual Machine (Hyper-V)` 

`Win32_ComputerSystem`

## Q2

**Which WMI query did the attacker execute to retrieve the current temperature value of the machine?**

4:20:11

```powershell
Creating Scriptblock text (1 of 1):
Get-WmiObject -Query "SELECT * FROM MSAcpi_ThermalZoneTemperature" -ErrorAction SilentlyContinue

ScriptBlock ID: 5bede686-4917-4326-ab5e-ccd7fba2662c
Path: 
```

`SELECT * FROM MSAcpi_ThermalZoneTemperature`

## Q3

**The attacker loaded a PowerShell script to detect virtualization. What is the function name of the script?**

4:20:53

```powershell
Creating Scriptblock text (1 of 1):
function Check-VM
{

<# 
.SYNOPSIS 
Nishang script which detects whether it is in a known virtual machine.
 
.DESCRIPTION 
This script uses known parameters or 'fingerprints' of Hyper-V, VMWare, Virtual PC, Virtual Box,
Xen and QEMU for detecting the environment.

.EXAMPLE 
PS > Check-VM
 
.LINK 
http://www.labofapenetrationtester.com/2013/01/quick-post-check-if-your-payload-is.html
https://github.com/samratashok/nishang

.NOTES 
The script draws heavily from checkvm.rb post module from msf.
https://github.com/rapid7/metasploit-framework/blob/master/modules/post/windows/gather/checkvm.rb
#> 
    [CmdletBinding()] Param()
    $ErrorActionPreference = "SilentlyContinue"
    #Hyper-V
    $hyperv = Get-ChildItem HKLM:\SOFTWARE\Microsoft
    if (($hyperv -match "Hyper-V") -or ($hyperv -match "VirtualMachine"))
        {
            $hypervm = $true
        }

    if (!$hypervm)
        {
            $hyperv = Get-ItemProperty hklm:\HARDWARE\DESCRIPTION\System -Name SystemBiosVersion
            if ($hyperv -match "vrtual")
                {
                    $hypervm = $true
                }
        }
    
    if (!$hypervm)
        {
            $hyperv = Get-ChildItem HKLM:\HARDWARE\ACPI\FADT
            if ($hyperv -match "vrtual")
                {
                    $hypervm = $true
                }
        }
            
    if (!$hypervm)
        {
            $hyperv = Get-ChildItem HKLM:\HARDWARE\ACPI\RSDT
            if ($hyperv -match "vrtual")
                {
                    $hypervm = $true
                }
        }

    if (!$hypervm)
        {
            $hyperv = Get-ChildItem HKLM:\SYSTEM\ControlSet001\Services
            if (($hyperv -match "vmicheartbeat") -or ($hyperv -match "vmicvss") -or ($hyperv -match "vmicshutdown") -or ($hyperv -match "vmiexchange"))
                {
                    $hypervm = $true
                }
        }
   
    if ($hypervm)
        {
    
             "This is a Hyper-V machine."
    
        }

    #VMWARE

    $vmware = Get-ChildItem HKLM:\SYSTEM\ControlSet001\Services
    if (($vmware -match "vmdebug") -or ($vmware -match "vmmouse") -or ($vmware -match "VMTools") -or ($vmware -match "VMMEMCTL"))
        {
            $vmwarevm = $true
        }

    if (!$vmwarevm)
        {
            $vmware = Get-ItemProperty hklm:\HARDWARE\DESCRIPTION\System\BIOS -Name SystemManufacturer
            if ($vmware -match "vmware")
                {
                    $vmwarevm = $true
                }
        }
    
    if (!$vmwarevm)
        {
            $vmware = Get-Childitem hklm:\hardware\devicemap\scsi -recurse | gp -Name identifier
            if ($vmware -match "vmware")
                {
                    $vmwarevm = $true
                }
        }

    if (!$vmwarevm)
        {
            $vmware = Get-Process
            if (($vmware -eq "vmwareuser.exe") -or ($vmware -match "vmwaretray.exe"))
                {
                    $vmwarevm = $true
                }
        }

    if ($vmwarevm)
        {
    
             "This is a VMWare machine."
    
        }
    
    #Virtual PC

    $vpc = Get-Process
    if (($vpc -eq "vmusrvc.exe") -or ($vpc -match "vmsrvc.exe"))
        {
        $vpcvm = $true
        }

    if (!$vpcvm)
        {
            $vpc = Get-Process
            if (($vpc -eq "vmwareuser.exe") -or ($vpc -match "vmwaretray.exe"))
                {
                    $vpcvm = $true
                }
        }

    if (!$vpcvm)
        {
            $vpc = Get-ChildItem HKLM:\SYSTEM\ControlSet001\Services
            if (($vpc -match "vpc-s3") -or ($vpc -match "vpcuhub") -or ($vpc -match "msvmmouf"))
                {
                    $vpcvm = $true
                }
        }

    if ($vpcvm)
        {
    
         "This is a Virtual PC."
    
        }


    #Virtual Box

    $vb = Get-Process
    if (($vb -eq "vboxservice.exe") -or ($vb -match "vboxtray.exe"))
        {
    
        $vbvm = $true
    
        }
    if (!$vbvm)
        {
            $vb = Get-ChildItem HKLM:\HARDWARE\ACPI\FADT
            if ($vb -match "vbox_")
                {
                    $vbvm = $true
                }
        }

    if (!$vbvm)
        {
            $vb = Get-ChildItem HKLM:\HARDWARE\ACPI\RSDT
            if ($vb -match "vbox_")
                {
                    $vbvm = $true
                }
        }

    
    if (!$vbvm)
        {
            $vb = Get-Childitem hklm:\hardware\devicemap\scsi -recurse | gp -Name identifier
            if ($vb -match "vbox")
                {
                    $vbvm = $true
                }
        }



    if (!$vbvm)
        {
            $vb = Get-ItemProperty hklm:\HARDWARE\DESCRIPTION\System -Name SystemBiosVersion
            if ($vb -match "vbox")
                {
                     $vbvm = $true
                }
        }
  

    if (!$vbvm)
        {
            $vb = Get-ChildItem HKLM:\SYSTEM\ControlSet001\Services
            if (($vb -match "VBoxMouse") -or ($vb -match "VBoxGuest") -or ($vb -match "VBoxService") -or ($vb -match "VBoxSF"))
                {
                    $vbvm = $true
                }
        }

    if ($vbvm)
        {
    
         "This is a Virtual Box."
    
        }



    #Xen

    $xen = Get-Process

    if ($xen -eq "xenservice.exe")
        {
    
        $xenvm = $true
    
        }
    
    if (!$xenvm)
        {
            $xen = Get-ChildItem HKLM:\HARDWARE\ACPI\FADT
            if ($xen -match "xen")
                {
                    $xenvm = $true
                }
        }

    if (!$xenvm)
        {
            $xen = Get-ChildItem HKLM:\HARDWARE\ACPI\DSDT
            if ($xen -match "xen")
                {
                    $xenvm = $true
                }
        }
    
    if (!$xenvm)
        {
            $xen = Get-ChildItem HKLM:\HARDWARE\ACPI\RSDT
            if ($xen -match "xen")
                {
                    $xenvm = $true
                }
        }

    
    if (!$xenvm)
        {
           $xen = Get-ChildItem HKLM:\SYSTEM\ControlSet001\Services
            if (($xen -match "xenevtchn") -or ($xen -match "xennet") -or ($xen -match "xennet6") -or ($xen -match "xensvc") -or ($xen -match "xenvdb"))
                {
                    $xenvm = $true
                }
        }


    if ($xenvm)
        {
    
         "This is a Xen Machine."
    
        }


    #QEMU

    $qemu = Get-Childitem hklm:\hardware\devicemap\scsi -recurse | gp -Name identifier
    if ($qemu -match "qemu")
        {
    
            $qemuvm = $true
    
        }
    
    if (!$qemuvm)
        {
        $qemu = Get-ItemProperty hklm:HARDWARE\DESCRIPTION\System\CentralProcessor\0 -Name ProcessorNameString
        if ($qemu -match "qemu")
            {
                $qemuvm = $true
            }
        }    

    if ($qemuvm)
        {
    
         "This is a Qemu machine."
    
        }
}

ScriptBlock ID: 7c52679e-db36-49f4-87e0-675a6b23913e
Path: 
```

`Check-VM`

## Q4

**The script enumerates the registry for virtualization services. Which key is being enumerated?**

Phân tích script trên, hacker lấy trực tiếp value chứa tên của các loại dịch vụ ảo hoá từ key `HKLM:\SYSTEM\ControlSet001\Services`

`HKLM:\SYSTEM\ControlSet001\Services`

## Q5

**When identifying the presence of VirtualBox, which two processes are being checked for existing? (ServiceA.exe:ServiceB.exe)**

Vẫn phân tích script trên thấy 2 process được check

```powershell
    $vb = Get-Process
    if (($vb -eq "vboxservice.exe") -or ($vb -match "vboxtray.exe"))
```

`vboxservice.exe:vboxtray.exe`

## Q6

**The VM detection script prints any detection with the prefix 'This is a'. Which two virtualization platforms did the script detect?**

Bỏ filter `4104` đi rồi tìm `This is a` là sẽ ra 

Tìm thấy vào 4:20:57 hai dịch vụ ảo hoá được script phát hiện là `Hyper-V` và `VMWare`

```
CommandInvocation(Out-Default): "Out-Default"
ParameterBinding(Out-Default): name="InputObject"; value="This is a Hyper-V machine."
ParameterBinding(Out-Default): name="InputObject"; value="This is a VMWare machine."


Context:
        Severity = Informational
        Host Name = ConsoleHost
        Host Version = 5.1.26100.2161
        Host ID = 0fad0cf8-6cb6-4657-86f7-655ec22eed9f
        Host Application = C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe
        Engine Version = 5.1.26100.2161
        Runspace ID = 2aeeba59-d0f6-4ce7-b41c-e07625b3beec
        Pipeline ID = 43
        Command Name = 
        Command Type = Script
        Script Name = 
        Command Path = 
        Sequence Number = 146
        User = DESKTOP-M3AKJSD\User
        Connected User = 
        Shell ID = Microsoft.PowerShell


User Data:
```

`Hyper-V:Vmware`