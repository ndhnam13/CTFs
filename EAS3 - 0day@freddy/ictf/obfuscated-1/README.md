# Mô tả

I installed every old software known to man... The flag is the VNC password, wrapped in `ictf{}`.

# Phân tích

VNC (cụ thể là RealVNC, TightVNC…) từ lâu đã lưu mật khẩu dưới dạng **DES encryption**, key và iv được hardcode vào mã nguồn của nó, tìm trên mạng thì biết được

**Key**: `e84ad660c4721ae0`

**IV**: `0000000000000000`

Bây giờ ta chỉ cần tìm mật khẩu của người dùng bị mã hoá

Sau khi tìm trên file không được, thì t chuyển qua tìm trong registry, xuất file `NTUSER.dat` từ thư mục người dùng `/Users/rumi`

Nó ở entry `Password` trong `HKCU\Software\TightVNC\Server`

`7e9b311248b7c8a8` 

```bash
$ echo -n 7e9b311248b7c8a8 | xxd -r -p | \
openssl enc -des-cbc --nopad --nosalt -K e84ad660c4721ae0 -iv 0000000000000000 -d
Slay4U!!
```

> **ictf{Slay4U!!}**