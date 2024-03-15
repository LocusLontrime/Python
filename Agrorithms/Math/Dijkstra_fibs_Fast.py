import math


def dijkstra_fib(num: int) -> int:
    memo_table = {}
    counter = 0

    def _dijkstra_fib(num_: int) -> int:
        # print(f'{num_ = }')
        nonlocal counter
        counter += 1

        if num_ < 3:
            return [0, 1, 1][num_]

        if num_ not in memo_table.keys():
            if num_ % 2:
                n = num_ // 2 + 1
                memo_table[num_] = _dijkstra_fib(n - 1) ** 2 + _dijkstra_fib(n) ** 2
            else:
                n = num_ // 2
                memo_table[num_] = (2 * _dijkstra_fib(n - 1) + _dijkstra_fib(n)) * _dijkstra_fib(n)

        return memo_table[num_]

    res = _dijkstra_fib(num)
    # print(f'...calculated FIB({num}) = {res}')
    print(f"...fib's length: {int(math.log10(res))}")
    print(f'...memo table size: {len(memo_table)}')
    print(f'...counter: {counter}')
    return res


fib = dijkstra_fib(1_000_000)
# print(f'{fib}')
