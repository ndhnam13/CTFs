import pefile
pe = pefile.PE("AntiChatGPT-pro.exe")
pe.OPTIONAL_HEADER.AddressOfEntryPoint = 0x1900
pe.write("patched.exe")
