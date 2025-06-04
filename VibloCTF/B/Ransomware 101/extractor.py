import re

def extract_txt_filenames(input_file, output_file):
    pattern = r'([\w\d]+\.txt)'  

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    matches = re.findall(pattern, content)
    unique_matches = sorted(set(matches))  

    with open(output_file, 'w', encoding='utf-8') as f:
        for match in unique_matches:
            f.write(match + '\n')

extract_txt_filenames('logs.txt', 'filenames_only.txt')