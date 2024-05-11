# accepted on codewars.com
from functools import reduce


def convergence(n: int):
    _n, steps = 1, 0
    elems = {_n}
    while n not in elems:
        if _n > n:
            n, steps = next_elem(n), steps + 1
        elems.add(_n := next_elem(_n))
        print(f'{n = }')
    return steps


def next_elem(n: int) -> int:
    return n + (n if n < 10 else reduce(lambda x, y: x * y if y > 0 else x, [int(k) for k in str(n)], 1))


# res = convergence(5000)  # res -> 283
res = convergence(19528)  # res -> 462
print(f'{res = }')
