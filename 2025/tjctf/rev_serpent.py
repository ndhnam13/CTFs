import pickletools

with open('ast_dump.pickle', 'rb') as f:
    data =  pickletools.dis(f)

print(data)
