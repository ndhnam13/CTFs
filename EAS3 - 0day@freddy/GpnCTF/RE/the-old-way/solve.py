import sympy as sp

# New FLAG values from the user
flag_values = [
    0x11fa5, 0x23e98, 0x35d06, 0x47b80, 0x59768, 0x6b5b0, 0x7c7e9, 0x8e3e0,
    0x9fe13, 0xb188c, 0xc2f67, 0xd49a0, 0xe565e, 0xf69ec, 0x10763d, 0x119fc0,
    0x129613, 0x1401d8, 0x14b987, 0x15ea00, 0x170bef, 0x17ee50, 0x1951b0, 0x1a1ae0,
    0x1b55da, 0x1c62cc, 0x1d1390, 0x1eb6c0, 0x1f345e, 0x205e18, 0x2178f5, 0x227980,
    0x243bf7, 0x24c68c, 0x2579f7, 0x26f760, 0x2871a4, 0x29a8a4, 0x29cc2b, 0x29efa0
]

# Number of unknowns
n = 40

# Define symbolic variables x0..x39
x = sp.symbols(f'x0:{n}', integer=True)

# Build equations: sum_{v3 != v4} x[v3] * (v4 + v3 + v4*v3 + 1) = flag_values[v4]
equations = []
for v4 in range(n):
    expr = 0
    for v3 in range(n):
        if v3 == v4:
            continue
        v1 = v4 + v3 + v4 * v3 + 1
        expr += x[v3] * v1
    equations.append(expr - flag_values[v4])

# Solve the linear system
solution = sp.linsolve(equations, x)

# Extract the solution and convert to characters if unique
if len(solution) == 1:
    sol = list(solution)[0]
    try:
        flag = ''.join(chr(int(val)) for val in sol)
    except Exception as e:
        flag = None
else:
    sol = None
    flag = None

print(sol)
print(flag)
