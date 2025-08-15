# accepted on leetcode.com -> 5d dp...
import functools
import time

intr_base = 120
extr_base = 40

intr_lose = 30
extr_gain = 20

bases = [0, intr_base, extr_base]

intr_extr_d = ((0, 0), (-1, 0), (0, -1))

happiness_matrix = (
    (0, 0, 0),
    (0, - 2 * intr_lose, extr_gain - intr_lose),
    (0, - intr_lose + extr_gain, 2 * extr_gain)
)

rec_counter: int

RED = "\033[31m{}"
PURPLE = "\033[35m{}"
END = "\033[0m{}"

colours = [END, RED, PURPLE]
person = [f'none', f'intr', f'extr']

# bitmasks on 3-nary numerical system?..


def get_max_grid_happiness(m: int, n: int, introverts_count: int, extroverts_count: int) -> int:
    global rec_counter
    rec_counter = 0
    # let us use some dp technic:
    # for the every step of new room appending the main parameters will be:
    # row, column, introverts remained, extroverts remained, previous row saved through its bitmask ->
    memo_table = {}
    path = {}
    start = time.time_ns()
    r = dp(0, 0, introverts_count, extroverts_count, prev_row := tuple(0 for _ in range(n)), m, n, memo_table, path)
    finish = time.time_ns()

    # path recovering:
    node = (0, 0, introverts_count, extroverts_count, prev_row)
    grid = [[0 for _ in range(n)] for _ in range(m)]
    while True:
        who, next_node = path[node]
        grid[node[0]][node[1]] = who
        if next_node[2] == next_node[3] == 0 or next_node[0] == m:
            break
        node = next_node

    print_grid(grid)

    print(f'time elapsed -> {(finish - start) // (10 ** 6)} milliseconds')
    print(f'{rec_counter} iterations done')
    return r


def dp(j: int, i: int, intr_rem: int, extr_rem: int, prev_row: tuple[int, ...], m: int, n: int, memo_table: dict, path: dict) -> int:
    global rec_counter
    rec_counter += 1
    # print(f'{rec_counter} -> {j, i, intr_rem, extr_rem, prev_row = }')
    # border cases:
    if j == m:
        # we reached the last cell:
        return 0
    if intr_rem == 0 and extr_rem == 0:
        # we used all the people given:
        return 0
    # the core algo:
    node = (j, i, intr_rem, extr_rem, prev_row)
    res = 0
    if (j, i, intr_rem, extr_rem, prev_row) not in memo_table.keys():
        # new coords:
        j_, i_ = next_ji(j, i, n)
        # 1. blank room:
        node_ = (j_, i_, intr_rem, extr_rem, prev_row[1:] + (0,))
        r0 = dp(*node_, m, n, memo_table, path)
        path[node] = 0, node_
        # 2. new introvert:
        if intr_rem > 0:
            node_ = (j_, i_, intr_rem - 1, extr_rem, prev_row[1:] + (1,))
            delta = intr_base
            delta += happiness_matrix[1][prev_row[-1] if i > 0 else 0]
            delta += happiness_matrix[1][prev_row[-n]]
            r1 = dp(*node_, m, n, memo_table, path) + delta
            if r1 > r0:
                path[node] = 1, node_
                r0 = r1
        # 3. new extrovert:
        if extr_rem > 0:
            node_ = (j_, i_, intr_rem, extr_rem - 1, prev_row[1:] + (2,))
            delta = extr_base
            delta += happiness_matrix[2][prev_row[-1] if i > 0 else 0]
            delta += happiness_matrix[2][prev_row[-n]]
            r2 = dp(*node_, m, n, memo_table, path) + delta
            if r2 > r0:
                path[node] = 2, node_
                r0 = r2
        memo_table[(j, i, intr_rem, extr_rem, prev_row)] = r0
    return memo_table[(j, i, intr_rem, extr_rem, prev_row)]


def next_ji(j: int, i: int, n: int):
    return (j + 1, 0) if i == n - 1 else (j, i + 1)


def colour_(char, colour, flag=False):
    s = "\033[1m" if flag else ''
    return f"{(s + colour).format(char)}{END.format('')}"


def print_grid(grid: list[list[int]]):
    print(f'Solution demonstrating: ')
    for row in grid:
        for cell in row:
            print(f'[{colour_(person[cell], colours[cell])}] ', end='')
        print()


test_ex = 2, 3, 1, 2  # res -> 240
test_ex_1 = 3, 1, 2, 1  # 260
test_ex_2 = 2, 2, 4, 0  # 240
test_ex_3 = 3, 4, 4, 3  # 680

print(f'test ex res -> {get_max_grid_happiness(*test_ex)}')                           # 36 366 98 989 98989 LL
print(f'test ex 1 res -> {get_max_grid_happiness(*test_ex_1)}')
print(f'test ex 2 res -> {get_max_grid_happiness(*test_ex_2)}')
print(f'test ex 3 res -> {get_max_grid_happiness(*test_ex_3)}')
print(f'huge test res -> {get_max_grid_happiness(5, 5, 6, 6)}')
# print(f'hyper huge test res -> {get_max_grid_happiness(6, 6, 7, 7)}')
# (f'mega hyper huge test res -> {get_max_grid_happiness(7, 7, 8, 8)}')
# print(f'extr res -> {get_max_grid_happiness(4, 4, 8, 2)}')


print(f'{(1, 98) + (98989,)}')
for row_ in happiness_matrix:
    print(f'{row_}')


class Solution:

    a = 98
    b = 989
    c = 98989

    k = a * b * c


print(f'{Solution.k = }')



