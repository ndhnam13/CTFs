# File: Traffic-1.pcapng

Không có gì đặc biệt lắm so với các bài trước, vẫn là phân tích packet của SMB, tìm file được mở, authen qua tài khoản nào, tìm thông tin trong statistics, hierachy, conversations

# File: Traffic-2.pcapng

**The attacker used "named pipes" for communication, suggesting they may have utilized Remote Procedure Calls (RPC) for lateral movement across the network. RPC allows one program to request services from another remotely, which could grant the attacker unauthorized access or control.
What is the name of the service that communicated using this named pipe?**

Named Pipes là một phương thức giao tiếp giữa các tiến trình (IPC - Inter-Process Communication), cho phép các tiến trình khác nhau trên cùng một máy, hoặc qua mạng, giao tiếp với nhau một cách bảo mật và có cấu trúc. Chúng hoạt động giống như các file ảo mà một tiến trình có thể ghi dữ liệu vào và tiến trình khác có thể đọc từ đó, giúp trao đổi dữ liệu giữa hai bên

Trong Windows, named pipes thường được sử dụng để giao tiếp giữa các ứng dụng, dịch vụ, và thành phần hệ thống. Mỗi named pipe có một đường dẫn hoặc tên cụ thể, thường được định dạng như `\\.\PIPE\<tên dịch vụ>`

Các named pipe phổ biến trong Windows mà hacker thường sử dụng:

`\PIPE\svcctl` – **Service Control Manager (SCM)**
 Quản lý dịch vụ hệ thống từ xa, cho phép khởi động, dừng và cấu hình dịch vụ. Kẻ tấn công có thể sử dụng nó để thao túng dịch vụ nhằm duy trì quyền truy cập hoặc thực thi lệnh từ xa

`\PIPE\samr` – **Security Account Manager (SAM)**
 Cung cấp quyền truy cập cơ sở dữ liệu SAM, nơi lưu trữ thông tin xác thực người dùng. Thường được kẻ tấn công sử dụng để liệt kê tài khoản hoặc trích xuất hash mật khẩu

`\PIPE\netlogon` – **Netlogon Service**
 Dùng cho xác thực và quản lý quan hệ tin cậy miền. Kẻ tấn công có thể khai thác để thực hiện tấn công pass-the-hash hoặc truy cập miền trái phép

`\PIPE\lsarpc` – **Local Security Authority RPC**
 Cung cấp quyền truy cập các chính sách bảo mật và đặc quyền tài khoản. Kẻ tấn công có thể lợi dụng để thu thập thông tin về cấu hình bảo mật và đặc quyền người dùng.

`\PIPE\atsvc` – **AT Service / Task Scheduler**
 Hỗ trợ lập lịch tác vụ từ xa, thường bị lạm dụng để thực thi lệnh trên hệ thống từ xa vào thời gian định sẵn. Phổ biến trong việc duy trì truy cập, di chuyển ngang (lateral movement), và leo thang đặc quyền.

`\PIPE\eventlog` – **Event Log Service**
 Quản lý nhật ký sự kiện. Kẻ tấn công có thể tương tác để xóa hoặc chỉnh sửa nhật ký, nhằm che giấu hoạt động độc hại

`\PIPE\spoolss` – **Print Spooler Service**
 Quản lý hàng đợi in. Từng tồn tại lỗ hổng nghiêm trọng (như PrintNightmare), khiến nó trở thành mục tiêu cho tấn công thực thi mã từ xa và di chuyển ngang

`\PIPE\wmi` – **Windows Management Instrumentation (WMI)**
 Cung cấp giao diện truy vấn và quản lý cấu hình hệ thống. Kẻ tấn công thường sử dụng WMI để kiểm soát hệ thống từ xa hoặc thu thập thông tin

`\PIPE\browser` – **Browser Service**
 Hỗ trợ duyệt mạng và xác định bộ điều khiển miền. Kẻ tấn công có thể sử dụng để xác định các máy chủ và miền trong mạng

`\PIPE\msrpc` – **Microsoft RPC Endpoint Mapper**
 Là cổng vào cho các dịch vụ RPC. Pipe này cung cấp quyền truy cập đến nhiều dịch vụ RPC khác nhau, khiến nó trở thành mục tiêu giá trị cao để kẻ tấn công khai thác nhiều chức năng

Để filter trong wireshark có thể sử dụng `frame contains 5c:00:50:00:49:00:50:00:45`

`5c:00:50:00:49:00:50:00:45` chỉ là dạng hexadecimal của string `/PIPE` thôi

Sau đó chỉ cần tìm các mục chó chưa `/PIPE` trong những cái packet filter được

`atsvc`

**Measuring the duration of suspicious communication can reveal how long the attacker maintained unauthorized access, providing insights into the scope and persistence of the attack.
What was the duration of communication between the identified addresses 172.16.66.1 and 172.16.66.36?**

Chỉnh lại ở phần `View` cột thời gian là thời gian đã trôi qua kể tử khi bắt đầu capture và sau đó tìm thời điểm cuối cùng rồi trừ đi thời điểm đầu tiên mà 2 ip kia kết nối với nhau

`11.7247`

# File: Traffic-3.pcapng

Tương thự như traffic-1 nhưng đây là sau khi hacker đã truy cập được vào hệ thống, setup thêm người dùng, cài file độc hại để nâng quyền truy cập, persistence, ...