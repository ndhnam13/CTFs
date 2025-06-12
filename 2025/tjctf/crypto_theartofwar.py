from Crypto.Util.number import long_to_bytes

def load_data(filename):
    data = {}
    with open(filename, 'r') as f:
        current_key = None
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ' = ' in line:
                key, value = line.split(' = ')
                data[key] = int(value)
    return data

def crt(n, a):
    sum = 0
    prod = 1
    for ni in n:
        prod *= ni

    for ni, ai in zip(n, a):
        p = prod // ni
        sum += ai * pow(p, -1, ni) * p
    return sum % prod

def nth_root(x, n):
    high = 1
    while high ** n <= x:
        high *= 2
    low = high // 2
    while low < high:
        mid = (low + high) // 2
        if mid**n < x:
            low = mid + 1
        else:
            high = mid
    return low

def main():
    try:
        data = load_data('output.txt')
        e = data['e']
        
        # Collect all n and c values
        ns = []
        cs = []
        for i in range(e + 1):  # n0 to n{e-1}
            n_key = f'n{i}'
            c_key = f'c{i}'
            if n_key in data and c_key in data:
                ns.append(data[n_key])
                cs.append(data[c_key])
        
        if len(ns) < e:
            print(f"Error: Need at least {e} pairs, but only found {len(ns)}")
            return

        x = crt(ns, cs)
        m = nth_root(x, e)

        if pow(m, e) == x:
            flag = long_to_bytes(m)
            print("Flag found:", flag.decode())
        else:
            print("Warning: Couldn't find exact root. Possible issues:")
            print("- Not enough ciphertext-modulus pairs")
            print("- Message too large for the attack")
            print("Best guess:", long_to_bytes(m).decode())

    except Exception as e:
        print("Error:", e)
        print("Please ensure:")
        print("1. output.txt is in the same directory")
        print("2. The file contains properly formatted n and c pairs")
        print("3. You have pycryptodome installed (pip install pycryptodome)")

if __name__ == "__main__":
    main()