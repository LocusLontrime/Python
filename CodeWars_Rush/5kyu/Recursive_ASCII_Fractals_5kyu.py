# accepted on codewars.com
import time

def fractalize(seed: list, i: int) -> list:
    if '' in seed: return []
    return rec_builder(seed, i)

def rec_builder(seed: list, iteration: int) -> list:
    if iteration == 1: return seed
    previous_fractal = rec_builder(seed, iteration - 1)
    J, I = len(previous_fractal), len(previous_fractal[0])
    current_fractal = []
    for j in range(J * len(seed)):
        current_fractal.append('')
        for i in range(len(seed[0])):
            if seed[j // J][i] == '*': current_fractal[j] += previous_fractal[j % J]
            else: current_fractal[j] += '.' * I
    return current_fractal


the_core = [
    '***',
    '.*.',
]

the_large_core = [
    '****....*',
    '.*...*...',
    '..***..*.',
    '.***...*.',
    '.*...****',
    '*.*...*.*',
    '...*..*.*',
    '*.**..**.',
    '.*..**.**'
]

def show(grid: list):
    for row in grid:
        for cell in row:
            if cell == '*': print("\033[31m{}\033[0m".format(cell), end='')
            else: print(f' ', end='')
        print()


start = time.time_ns()
for ind in range(1, 5 + 1 + 1):
    f = fractalize(the_core,ind )
    print(f'f sizes: {len(f)}x{len(f[0])}')
    print(f'{show(f)}')
finish = time.time_ns()
print(f'Time elapsed: {(finish - start) // 10 ** 6} milliseconds')
