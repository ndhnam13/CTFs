import copy
import random
import numpy as np

class RubiksCube:
    def __init__(self):
        self.faces = {
            'U': [['⬜'] * 3 for _ in range(3)],
            'L': [['🟧'] * 3 for _ in range(3)],
            'F': [['🟩'] * 3 for _ in range(3)],
            'R': [['🟥'] * 3 for _ in range(3)],
            'B': [['🟦'] * 3 for _ in range(3)],
            'D': [['🟨'] * 3 for _ in range(3)]
        }

    def _rotate_face_clockwise(self, face_name):
        face = self.faces[face_name]
        new_face = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                new_face[i][j] = face[2-j][i]
        self.faces[face_name] = new_face

    def _rotate_face_counter_clockwise(self, face_name):
        face = self.faces[face_name]
        new_face = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                new_face[i][j] = face[j][2-i]
        self.faces[face_name] = new_face

    def display(self):
        for i in range(3):
            print("      " + " ".join(self.faces['U'][i]))
        for i in range(3):
            print(" ".join(self.faces['L'][i]) + "  " +
                  " ".join(self.faces['F'][i]) + "  " +
                  " ".join(self.faces['R'][i]) + "  " +
                  " ".join(self.faces['B'][i]))
        for i in range(3):
            print("      " + " ".join(self.faces['D'][i]))
        print("-" * 30)

    def get_flat_cube_encoded(self):
        return "".join([chr(ord(i) % 94 + 33) for i in str(list(np.array(self.faces).flatten())) if ord(i)>256])
    
    def get_cube(self):
        return self.faces
    
    def set_cube(self, cube_state):
        self.faces = copy.deepcopy(cube_state)
    
    # Original moves from your code
    def U(self):
        self._rotate_face_clockwise('U')
        temp_row = copy.deepcopy(self.faces['F'][0])
        self.faces['F'][0] = self.faces['R'][0]
        self.faces['R'][0] = self.faces['B'][0]
        self.faces['B'][0] = self.faces['L'][0]
        self.faces['L'][0] = temp_row

    def L(self):
        self._rotate_face_clockwise('L')
        temp_col = [self.faces['U'][i][0] for i in range(3)]
        for i in range(3): self.faces['U'][i][0] = self.faces['B'][2-i][2]
        for i in range(3): self.faces['B'][2-i][2] = self.faces['D'][i][0]
        for i in range(3): self.faces['D'][i][0] = self.faces['F'][i][0]
        for i in range(3): self.faces['F'][i][0] = temp_col[i]

    def F(self):
        self._rotate_face_clockwise('F')
        temp_strip = copy.deepcopy(self.faces['U'][2])
        for i in range(3): self.faces['U'][2][i] = self.faces['L'][2-i][2]
        for i in range(3): self.faces['L'][i][2] = self.faces['D'][0][i]
        for i in range(3): self.faces['D'][0][2-i] = self.faces['R'][i][0]
        for i in range(3): self.faces['R'][i][0] = temp_strip[i]

    def D_prime(self):
        self._rotate_face_counter_clockwise('D')
        temp_row = copy.deepcopy(self.faces['F'][2])
        self.faces['F'][2] = self.faces['R'][2]
        self.faces['R'][2] = self.faces['B'][2]
        self.faces['B'][2] = self.faces['L'][2]
        self.faces['L'][2] = temp_row

    def R_prime(self):
        self._rotate_face_counter_clockwise('R')
        temp_col = [self.faces['U'][i][2] for i in range(3)]
        for i in range(3): self.faces['U'][i][2] = self.faces['B'][2-i][0]
        for i in range(3): self.faces['B'][2-i][0] = self.faces['D'][i][2]
        for i in range(3): self.faces['D'][i][2] = self.faces['F'][i][2]
        for i in range(3): self.faces['F'][i][2] = temp_col[i]

    def B_prime(self):
        self._rotate_face_counter_clockwise('B')
        temp_strip = copy.deepcopy(self.faces['U'][0])
        for i in range(3): self.faces['U'][0][i] = self.faces['L'][i][0]
        for i in range(3): self.faces['L'][i][0] = self.faces['D'][2][2-i]
        for i in range(3): self.faces['D'][2][i] = self.faces['R'][i][2]
        for i in range(3): self.faces['R'][i][2] = temp_strip[2-i]

    # Missing moves - implementing the clockwise versions
    def U_prime(self):
        self._rotate_face_counter_clockwise('U')
        temp_row = copy.deepcopy(self.faces['F'][0])
        self.faces['F'][0] = self.faces['L'][0]
        self.faces['L'][0] = self.faces['B'][0]
        self.faces['B'][0] = self.faces['R'][0]
        self.faces['R'][0] = temp_row

    def L_prime(self):
        self._rotate_face_counter_clockwise('L')
        temp_col = [self.faces['U'][i][0] for i in range(3)]
        for i in range(3): self.faces['U'][i][0] = self.faces['F'][i][0]
        for i in range(3): self.faces['F'][i][0] = self.faces['D'][i][0]
        for i in range(3): self.faces['D'][i][0] = self.faces['B'][2-i][2]
        for i in range(3): self.faces['B'][2-i][2] = temp_col[i]

    def F_prime(self):
        self._rotate_face_counter_clockwise('F')
        temp_strip = copy.deepcopy(self.faces['U'][2])
        for i in range(3): self.faces['U'][2][i] = self.faces['R'][i][0]
        for i in range(3): self.faces['R'][i][0] = self.faces['D'][0][2-i]
        for i in range(3): self.faces['D'][0][i] = self.faces['L'][i][2]
        for i in range(3): self.faces['L'][2-i][2] = temp_strip[i]

    def D(self):
        self._rotate_face_clockwise('D')
        temp_row = copy.deepcopy(self.faces['F'][2])
        self.faces['F'][2] = self.faces['L'][2]
        self.faces['L'][2] = self.faces['B'][2]
        self.faces['B'][2] = self.faces['R'][2]
        self.faces['R'][2] = temp_row

    def R(self):
        self._rotate_face_clockwise('R')
        temp_col = [self.faces['U'][i][2] for i in range(3)]
        for i in range(3): self.faces['U'][i][2] = self.faces['F'][i][2]
        for i in range(3): self.faces['F'][i][2] = self.faces['D'][i][2]
        for i in range(3): self.faces['D'][i][2] = self.faces['B'][2-i][0]
        for i in range(3): self.faces['B'][2-i][0] = temp_col[i]

    def B(self):
        self._rotate_face_clockwise('B')
        temp_strip = copy.deepcopy(self.faces['U'][0])
        for i in range(3): self.faces['U'][0][2-i] = self.faces['R'][i][2]
        for i in range(3): self.faces['R'][i][2] = self.faces['D'][2][i]
        for i in range(3): self.faces['D'][2][2-i] = self.faces['L'][i][0]
        for i in range(3): self.faces['L'][i][0] = temp_strip[i]

    def apply_moves(self, moves_string):
        moves = moves_string.split()
        for move in moves:
            if move == "U": self.U()
            elif move == "U'": self.U_prime()
            elif move == "D": self.D()
            elif move == "D'": self.D_prime()
            elif move == "L": self.L()
            elif move == "L'": self.L_prime()
            elif move == "R": self.R()
            elif move == "R'": self.R_prime()
            elif move == "F": self.F()
            elif move == "F'": self.F_prime()
            elif move == "B": self.B()
            elif move == "B'": self.B_prime()
            else:
                print(f"Warning: Unknown move '{move}' ignored.")

def solve_scrambled_cube():
    # Load the scrambled cube state
    scrambled_state = {'U': [['🟨', '🟩', '🟧'], ['🟥', '⬜', '🟦'], ['⬜', '🟧', '🟩']], 'L': [['🟦', '🟩', '🟥'], ['⬜', '🟧', '🟧'], ['🟦', '⬜', '🟩']], 'F': [['🟧', '⬜', '🟨'], ['🟦', '🟩', '🟨'], ['🟦', '🟨', '🟩']], 'R': [['⬜', '🟥', '🟦'], ['🟧', '🟥', '🟥'], ['🟧', '🟨', '⬜']], 'B': [['🟧', '⬜', '🟥'], ['🟨', '🟦', '🟥'], ['🟨', '🟩', '🟥']], 'D': [['🟩', '🟦', '⬜'], ['🟦', '🟨', '🟩'], ['🟥', '🟧', '🟨']]}
    
    # Create cube and set to scrambled state
    cube = RubiksCube()
    cube.set_cube(scrambled_state)
    
    print("Scrambled cube state:")
    cube.display()
    
    # To solve, we need to reverse the scrambling process
    # The cube was scrambled with random.seed(42) for 20 iterations of 50 moves each
    
    # Recreate the exact scrambling sequence
    moves = ["U", "L", "F", "B'", "D'", "R'"]
    random.seed(42)
    
    # Generate the same random sequence that was used
    all_moves = []
    for _ in range(20):
        order = [random.randint(0, len(moves)-1) for _ in range(50)]
        for i in range(len(order)):
            all_moves.append(moves[order[i]])
    
    print(f"Total moves applied: {len(all_moves)}")
    
    # To solve, we need to apply the inverse moves in reverse order
    inverse_moves = {
        "U": "U'", "U'": "U",
        "L": "L'", "L'": "L", 
        "F": "F'", "F'": "F",
        "B": "B'", "B'": "B",
        "D": "D'", "D'": "D",
        "R": "R'", "R'": "R"
    }
    
    # Apply inverse moves in reverse order
    solution_moves = []
    for move in reversed(all_moves):
        inverse_move = inverse_moves[move]
        solution_moves.append(inverse_move)
        cube.apply_moves(inverse_move)
    
    print("Solved cube state:")
    cube.display()
    
    # Get the flag
    flag = "tjctf{" + cube.get_flat_cube_encoded() + "}"
    print(f"Flag: {flag}")
    
    return flag, solution_moves

# Run the solver
if __name__ == "__main__":
    flag, moves = solve_scrambled_cube()
    print(f"\nSolution sequence length: {len(moves)} moves")
