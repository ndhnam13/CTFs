# Mô tả
Chúng tôi đang điều tra một vụ vi phạm dữ liệu. Trong thời gian sự cố xảy ra, có một USB lạ đã được cắm vào máy chủ của chúng tôi. Hãy giúp chúng tôi tìm tên phân vùng của USB đó.

 Related Resource: Wrap flag in format Flag{...}/Bọc tên USB bạn tìm thấy trong định dạng Flag{...}

# Phân tích
Bài cho ta một loạt các hive registry, vì mô tả cso nói đến việc có một usb lạ bị cắm vào nên ta có thể tập trung vào hive `SYSTEM` các hive còn lại không liên quan tới flag của ta

Để tìm được các thiết bị removable media trong registry thì rất đơn giả thôi, ta có rất nhiều nơi trong `SYSTEM`
- MountedDevices: Ánh xạ giữa thiết bị và ký tự ổ đĩa (không lưu tên thiết bị cụ thể)
- ControlSet(CurenControlSet)\Enum\USB: Chứa thông tin thiết bị USB nói chung.
- ControlSet(CurenControlSet)\Enum\USBSTOR: Dành cho các thiết bị lưu trữ USB (USB mass storage)
- ControlSet(CurenControlSet)\Enum\WpdBusEnumRoot: Chứa thông tin về các thiết bị nhận diện là WPD (Windows Portable Device), chẳng hạn như điện thoại, máy nghe nhạc hoặc USB giả dạng thiết bị WPD

# Flag
Flag được cố tình giấu trong nhánh ít người kiểm tra (WpdBusEnumRoot), đánh lừa những ai chỉ xem USBSTOR, USB với MountedDevices zzzz

Tên của USB lạ này sẽ nằm tại `ControlSet(CurenControlSet)\Enum\WpdBusEnumRoot\UMB` trong data của value `FriendlyName`

Flag{5usP3cted_USB_d3T3c73d}
