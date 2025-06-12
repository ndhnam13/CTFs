# Mô tả

I secretly installed tracking software on a virtual reality headset before selling it to a known rebel spy. Before handing it over, I made sure to record myself typing on a virtual keyboard (and my tracking software captured it all!).

Later, I recovered the spy's usage data. Im confident they typed the flag. Use the data to recover their message and help me squash this rebellion once and for all!

hints> -Single spaces represent underscores and double spaces represent braces in the flag. -The virtual keyboard appears 2 units in front of the controller, along the controllers forward z axis. -Be warned: the user's perspective may differ between sessions.

# Ý tưởng
Tạo ra một map bàn phím sẵn từ soure.txt nhưng do 2 session thì pov của người dùng vr khác nhau cho nên ta sẽ phải lấy position gần nhất sau đó map lại vào -> flag

Có message.py chatgpt gen ra nhưng đang bị lỗi chữ được chữ không

Dùng thêm thư viện `from scipy.spatial.transform import Rotation as R`
