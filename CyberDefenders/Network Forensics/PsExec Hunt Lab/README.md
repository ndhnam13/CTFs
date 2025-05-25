# Mô tả

An alert from the Intrusion Detection System (IDS) flagged suspicious lateral movement activity involving PsExec. This indicates potential unauthorized access and movement across the network. As a SOC Analyst, your task is to investigate the provided PCAP file to trace the attacker’s activities. Identify their entry point, the machines targeted, the extent of the breach, and any critical indicators that reveal their tactics and objectives within the compromised environment.

# Phân tích

## Flag 1

To effectively trace the attacker's activities within our network, can you identify the IP address of the machine from which the attacker initially gained access?

Mở file pcap lên rồi sau đó check hierachy thì thấy có rất nhiều protocol SMB2 thì đoán được đây là tấn công qua SMB2, rồi sau đó xem Conversations thì thấy địa chỉ IP 10.0.0.130 gửi nhiều packet nhất, đây chính là máy mà hacker đã truy cập được vào đầu tiên và cũng sử dụng nó để di chuyển giữa các người dùng trong mạng SMB2

`10.0.0.130`

## Flag 2

To fully understand the extent of the breach, can you determine the machine's hostname to which the attacker first pivoted?

Trong SMB thì khi mình gửi một request setup một session kết nối đến máy khác qua SMB thì server(Máy đích) sẽ trả lời bằng một `NTLMSSP_CHALLENGE` yêu cầu client đưa NTLM hash của mình cho server để kiểm tra. Vậy để tìm ra được hacker đã truy cập vào máy nào tiếp theo chỉ cần filter `ntlmssp` rồi tìm packet có info challenge đầu tiên và vào check phần target name

`Sales-PC`

## Flag 3

Knowing the username of the account the attacker used for authentication will give us insights into the extent of the breach. What is the username utilized by the attacker for authentication?

Sẽ tìm được tên người dùng sau khi challenge thành công, ở đây tên người dùng ở packet 132 ngay đằng sau challenge(131)

`ssales`

## Flag 4

After figuring out how the attacker moved within our network, we need to know what they did on the target machine. What's the name of the service executable the attacker set up on the target?

`psexesvc` Giải thích ở flag sau

## Flag 5

We need to know how the attacker installed the service on the compromised machine to understand the attacker's lateral movement tactics. This can help identify other affected systems. Which network share was used by PsExec to install the service on the target machine?

Nếu muốn biết mạng SMB nào đã được sử dụng để tải các dịch vụ độc hại trên các máy khác thì phải là một máy có quyền cao như admin chẳng hạn

Tại packet 134 hacker có gửi request tree đến `ADMIN$` và sau đó là các request Create File `PSEXESVC.exe` đây chính là mạng SMB được sử dụng để cài dịch vụ độc hại

`ADMIN$`

## Flag 6

We must identify the network share used to communicate between the two machines. Which network share did PsExec use for communication?

Để biết mạng SMB nào được sử dụng để giao tiếp giữa 2 máy trên thì trong file pcap có thể kiểm tra các protocol SMB có info `stdin`, `stdout`, `stderr` để viết input và output thì khi check mục `SMB2 header` phần `smb2.tid` sẽ ra SMB share được sử dụng là `IPC$`

`IPC$`

## Flag 7

Now that we have a clearer picture of the attacker's activities on the compromised machine, it's important to identify any further lateral movement. What is the hostname of the second machine the attacker targeted to pivot within our network?

Sau khi đã setup được kết nối đến người dùng `ADMIN$`, và `IPC$` để trao đổi thì ta sẽ thấy tiếp theo là một chuỗi các read/write request rất dài đây là lúc mà hacker cài các dịch vụ độc hại, để tìm được flag có thể bỏ qua đoạn này sau đó thấy địa chỉ IP của hacker thiết lập các session setup requests đến 2 user là `jdoe` và `IEUser` của máy `Marketing-PC`

`Marketing-PC`