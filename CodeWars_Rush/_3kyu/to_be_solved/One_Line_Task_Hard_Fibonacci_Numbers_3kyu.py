# accepted on codewars.com, but the scores has not been achieved...
import sys
import time
from functools import lru_cache

sys.set_int_max_str_digits(1_000_000)

counter: int

k = lambda x: pow(n := 2 << x, x, n * n - n - 1) // n  # the task has not been solved..., formula is unclear.

# for i in range(12):
#     print(f'k({i}): {k(i)}')


# F(2n-1) = F(n-1)2 + F(n)2
# F(2n) = ( 2 F(n-1) + F(n) ) F(n)

@lru_cache()
def dijkstra_fib(num: int) -> int:

    # print(f'{num = }')

    global counter
    counter += 1

    if num < 3:
        return [0, 1, 1][num]

    if num % 2:
        n = num // 2 + 1
        res = dijkstra_fib(n - 1) ** 2 + dijkstra_fib(n) ** 2
    else:
        n = num // 2
        res = (2 * dijkstra_fib(n - 1) + dijkstra_fib(n)) * dijkstra_fib(n)

    return res


number = 10

# print(f'...............................................................................................................')
# for i in range(12):
#     print(f'Fib({i}) -> {dijkstra_fib(i)}')

i = 100_000_000
counter = 0

start = time.time_ns()
f = dijkstra_fib(i)
# print(f'Fib({i}) -> {f}')
finish = time.time_ns()
print(f'time elapsed1: {(finish - start) // 10 ** 6} milliseconds')
print(f'{counter = }')

# start = time.time_ns()
# f = k(i)
# print(f'Fib({i}) -> {f}')
# finish = time.time_ns()
# print(f'time elapsed2: {(finish - start) // 10 ** 6} milliseconds')
