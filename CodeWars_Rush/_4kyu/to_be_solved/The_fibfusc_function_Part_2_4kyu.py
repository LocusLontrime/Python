# accepted on codewars.com
def fibfusc(n, num_digits=None):
    flag = False if num_digits is None else True
    if flag:
        MODULO = 10 ** num_digits
    bin_n = bin(n)[2:]
    x, y = (1, 0) if bin_n[0] == '0' else (0, 1)
    # print(f'initial res: {x, y}')
    # print(f'bin_n: {bin_n}')
    for i in range(1, len(bin_n)):
        # print(f'ind: {i}, bin dig: {bin_n[i]}')
        if bin_n[i] == '1':
            if flag:
                x, y = (-y * (2 * x + 3 * y)) % MODULO, ((x + 2 * y) * (x + 4 * y)) % MODULO
            else:
                x, y = -y * (2 * x + 3 * y), (x + 2 * y) * (x + 4 * y)
        else:
            if flag:
                x, y = ((x + y) * (x - y)) % MODULO, (y * (2 * x + 3 * y)) % MODULO
            else:
                x, y = (x + y) * (x - y), y * (2 * x + 3 * y)
        # print(f'...x, y: {x, y}')
    return (x - MODULO) if flag else x, y

num = 101
# print(f'bin({num}): {bin(num)}')
print(f'res: {fibfusc(num)}')
# print(f'res rec: {fib_fusc_rec(num)}')

