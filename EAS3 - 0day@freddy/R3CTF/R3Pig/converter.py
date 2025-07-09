def convert_value(val):
    try:
        f = float(val)
        if 0.09 <= f <= 0.11:
            return '1'
        elif 0.015 <= f <= 0.03:
            return '0'
        else:
            return '?'  # Unknown / ambiguous
    except ValueError:
        return '?'  # Not a float

def main():
    with open("raw.txt", "r") as infile:
        lines = infile.readlines()

    results = [convert_value(line.strip()) for line in lines if line.strip()]
    
    # Join results into a binary string
    binary_string = ''.join(results)

    # Optionally group bits into bytes
    byte_grouped = ' '.join([binary_string[i:i+8] for i in range(0, len(binary_string), 8)])

    # Write result
    with open("converted.txt", "w") as outfile:
        outfile.write(byte_grouped + '\n')

    print("✅ Done. Output saved to converted.txt")

if __name__ == "__main__":
    main()
