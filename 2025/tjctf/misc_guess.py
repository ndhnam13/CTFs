from pwn import *

# Kết nối tới challenge
conn = remote('tjc.tf', 31700)

low, high = 1, 1000
for _ in range(10):
    guess = (low + high) // 2
    conn.sendline(str(guess))
    response = conn.recvline().decode().strip()
    print(f"Guess: {guess}, Response: {response}")

    if "Too high" in response:
        high = guess - 1
    elif "Too low" in response:
        low = guess + 1
    else:
        # Đoán đúng, flag xuất hiện
        flag_line = response
        print(f"Flag: {flag_line}")
        break

conn.close()

#tjctf{g0od_j0b_u_gu33sed_correct_998}