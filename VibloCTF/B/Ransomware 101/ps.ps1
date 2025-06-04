
$FilePath = 'C:\flag.txt'

$AesKey = New-Object System.Security.Cryptography.AesManaged
$AesKey.KeySize = 256
$AesKey.BlockSize = 128
$AesKey.GenerateKey()
$AesKey.GenerateIV()

$B64Key = [System.Convert]::ToBase64String($AesKey.Key)
$B64IV = [System.Convert]::ToBase64String($AesKey.IV)

$FileContent = [System.IO.File]::ReadAllBytes($FilePath)

$EncryptFile = $AesKey.CreateEncryptor($AesKey.Key, $AesKey.IV)
$Encrypted = $EncryptFile.TransformFinalBlock($FileContent, 0, $FileContent.Length)

$B64Encrypted = [System.Convert]::ToBase64String($Encrypted)

[System.IO.File]::WriteAllText($FilePath, $B64Encrypted)

Write-Output $B64Key
Write-Output $B64IV

$TempDir = Join-Path ([System.IO.Path]::GetTempPath()) 'encrypt'

if (!(Test-Path $TempDir)) {
    New-Item -ItemType Directory -Path $TempDir
}

$Dir1 = $TempDir
$Dir2 = $FilePath

if (!(Test-Path $Dir1)) {
    New-Item -ItemType Directory -Path $Dir1
}

$ReadFile = Get-Content -Path $Dir2 -Raw

$counter = 1

foreach ($character in $ReadFile.ToCharArray()) {
    $replaced = $character -replace '[\\/:""*?<>|]', '_'
    $FileName = $counter * 111111
    $NewPath = "$FileName$replaced.txt"
    $FilePath = Join-Path $Dir1 $NewPath
    New-Item -ItemType File -Path $FilePath -Force
    Set-Content -Path $FilePath -Value 'tmq'
    
    $counter++
}