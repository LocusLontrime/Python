def dio():
    x = 1
    while 1:
        print(f'x: {x}')
        for y in range(1, x):
            for z in range(1, y):
                if x * x == y * y + 12752041 * z * z:
                    return "Found it"
        x = x + 1


print(f'res: {dio()}')




