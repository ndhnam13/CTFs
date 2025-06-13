import numpy as np
from scipy.spatial.transform import Rotation as R
import re # Import the regular expressions module

def get_data_from_logs():
    """
    Reads the log data from source.txt and unknown.txt files.
    """
    with open("source.txt", "r") as source_file:
        source_content = source_file.read()
    with open("unknown.txt", "r") as unknown_file:
        unknown_content = unknown_file.read()
    return source_content, unknown_content

def parse_log_data(log_content):
    """
    Parses the log string into controller data and keystroke events using
    regular expressions for robust parsing.
    """
    controller_data = []
    keystrokes = []
    # This regex captures the timestamp, position tuple, and orientation tuple
    controller_pattern = re.compile(r"([\d\.]+),RightController,\((.+?)\),\((.+?)\),")

    for line in log_content.strip().split('\n'):
        match = controller_pattern.match(line)
        if match:
            try:
                timestamp = float(match.group(1))
                pos_str = match.group(2)
                orient_str = match.group(3)
                pos = np.fromstring(pos_str, sep=',')
                orient = np.fromstring(orient_str, sep=',')
                if pos.shape == (3,) and orient.shape == (4,):
                    controller_data.append({'ts': timestamp, 'pos': pos, 'orient': orient})
            except (ValueError, IndexError):
                continue
        elif "Keystroke" in line:
            parts = line.split(',')
            if len(parts) == 3:
                key = parts[1].strip()
                timestamp = float(parts[2].strip())
                keystrokes.append({'ts': timestamp, 'key': key})

    return controller_data, keystrokes

def calculate_3d_positions(controller_data, keystrokes, forward_direction):
    """
    Calculates the 3D world position of each keystroke, handling known and
    unknown data correctly.
    """
    all_key_presses = []
    
    for stroke in keystrokes:
        key_ts = stroke['ts']
        key_char = stroke['key']
        
        last_data = None
        for data in controller_data:
            if data['ts'] < key_ts:
                last_data = data
            else:
                break
        
        if last_data:
            pos = last_data['pos']
            rot = R.from_quat(last_data['orient'])
            forward_vec = rot.apply(forward_direction)
            key_pos = pos + 2 * forward_vec
            all_key_presses.append({'key': key_char, 'pos': key_pos})

    # Create the averaged keyboard map from the source data
    temp_positions_for_avg = {}
    for press in all_key_presses:
        key_char = press['key']
        if key_char != 'Unknown':
            if key_char not in temp_positions_for_avg:
                temp_positions_for_avg[key_char] = []
            temp_positions_for_avg[key_char].append(press['pos'])
            
    avg_key_positions = {k: np.mean(v, axis=0) for k, v in temp_positions_for_avg.items()}

    # Create the ordered list of all positions. This is crucial for the spy's data.
    ordered_positions = [press['pos'] for press in all_key_presses]

    return avg_key_positions, ordered_positions

def find_rigid_transform(A, B):
    """
    Finds the optimal rigid transformation (Rotation, translation) between two 
    sets of 3D points A and B using the Kabsch algorithm.
    """
    assert A.shape == B.shape
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    H = (A - centroid_A).T @ (B - centroid_B)
    U, S, Vt = np.linalg.svd(H)
    R_matrix = Vt.T @ U.T

    if np.linalg.det(R_matrix) < 0:
       Vt[2,:] *= -1
       R_matrix = Vt.T @ U.T
       
    t_vector = centroid_B.T - R_matrix @ centroid_A.T
    
    A_transformed = (R_matrix @ A.T).T + t_vector
    rmsd = np.sqrt(np.mean(np.sum((A_transformed - B)**2, axis=1)))
    
    return R_matrix, t_vector, rmsd

def find_closest_key(pos, keyboard_map):
    """Finds the nearest character in the keyboard_map to a given 3D position."""
    min_dist = float('inf')
    best_key = '?'
    for key, key_pos in keyboard_map.items():
        dist = np.linalg.norm(pos - key_pos)
        if dist < min_dist:
            min_dist = dist
            best_key = key
    return best_key

def format_flag(char_list):
    """Formats the decoded character list into the final flag string based on hints."""
    s = "".join(char_list)
    s = s.replace("Space_ButtonSpace_Button", "BRACE")
    s = s.replace("Space_Button", "_")
    s = s.replace("BRACE", "{", 1)
    s = s.replace("BRACE", "}", 1)
    return s

def solve():
    """Main solver function to orchestrate the decoding process."""
    source_log, unknown_log = get_data_from_logs()

    # Parse both log files
    source_controller, source_keystrokes = parse_log_data(source_log)
    spy_controller, spy_keystrokes = parse_log_data(unknown_log)

    # Set the correct forward direction
    forward_direction = np.array([0, 0, 1])

    # Calculate positions for both datasets
    my_keyboard_map, _ = calculate_3d_positions(source_controller, source_keystrokes, forward_direction)
    _, spy_positions = calculate_3d_positions(spy_controller, spy_keystrokes, forward_direction)

    # Define the target to search for
    target_plaintext = 'tjctf'
    target_points = np.array([my_keyboard_map[char] for char in target_plaintext])
    
    best_match = {'rmsd': float('inf')}

    # Find the best alignment
    for i in range(len(spy_positions) - len(target_plaintext) + 1):
        spy_window = np.array(spy_positions[i : i + len(target_plaintext)])
        if spy_window.shape != target_points.shape:
            continue
        R_matrix, t_vector, rmsd = find_rigid_transform(spy_window, target_points)
        
        if rmsd < best_match['rmsd']:
            best_match = {'rmsd': rmsd, 'R': R_matrix, 't': t_vector, 'start_index': i}

    # Apply the best transformation
    best_R = best_match['R']
    best_t = best_match['t']
    transformed_spy_positions = (best_R @ np.array(spy_positions).T).T + best_t

    # Decode the full message
    decoded_chars = [find_closest_key(pos, my_keyboard_map) for pos in transformed_spy_positions]

    # Format and return the flag
    flag = format_flag(decoded_chars)
    
    return flag

# --- Execute the Solver and Print the Result ---
final_flag = solve()

print(f"Correct Flag: {final_flag}")
