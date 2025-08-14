# accepted on leetcode.com -> 5d dp...

intr_base = 120
extr_base = 40

intr_lose = 30
extr_gain = 20

bases = [0, intr_base, extr_base]

happiness_matrix = (
    (0, 0, 0),
    (0, - 2 * intr_lose, extr_gain - intr_lose),
    (0, - intr_lose + extr_gain, 2 * extr_gain)
)

rec_counter: int

# bitmasks on 3-nary numerical system?..


def get_max_grid_happiness(m: int, n: int, introverts_count: int, extroverts_count: int) -> int:
    global rec_counter
    rec_counter = 0
    # let us use some dp technic:
    # for the every step of new room appending the main parameters will be:
    # row, column, introverts remained, extroverts remained, previous row saved through its bitmask ->
    memo_table = {}
    return dp(0, 0, m, n, introverts_count, extroverts_count, tuple(0 for _ in range(n)), memo_table)


def dp(j: int, i: int, m: int, n: int, intr_rem: int, extr_rem: int, prev_row: tuple[int, ...], memo_table: dict) -> int:
    global rec_counter
    rec_counter += 1
    print(f'{rec_counter} -> {j, i, intr_rem, extr_rem, prev_row = }')
    # border cases:
    if j == m:
        # we reached the last cell:
        return 0
    if intr_rem == 0 and extr_rem == 0:
        # we used all the people given:
        return 0
    # the core algo:
    if (j, i, intr_rem, extr_rem, prev_row) not in memo_table.keys():
        res = 0
        # new coords:
        j_, i_ = next_ji(j, i, n)
        # 1. blank room:
        res = max(res, dp(j_, i_, m, n, intr_rem, extr_rem, prev_row[1:] + (0,), memo_table))
        # 2. new introvert:
        if intr_rem > 0:
            delta = intr_base
            delta += happiness_matrix[1][prev_row[-1] if i > 0 else 0]
            delta += happiness_matrix[1][prev_row[-n]]
            res = max(res, dp(j_, i_, m, n, intr_rem - 1, extr_rem, prev_row[1:] + (1,), memo_table) + delta)
        # 3. new extrovert:
        if extr_rem > 0:
            delta = extr_base
            delta += happiness_matrix[2][prev_row[-1] if i > 0 else 0]
            delta += happiness_matrix[2][prev_row[-n]]
            res = max(res, dp(j_, i_, m, n, intr_rem, extr_rem - 1, prev_row[1:] + (2,), memo_table) + delta)
        memo_table[(j, i, intr_rem, extr_rem, prev_row)] = res
    return memo_table[(j, i, intr_rem, extr_rem, prev_row)]


def next_ji(j: int, i: int, n: int):
    return (j + 1, 0) if i == n - 1 else (j, i + 1)


test_ex = 2, 3, 1, 2  # res -> 240
test_ex_1 = 3, 1, 2, 1  # 260
test_ex_2 = 2, 2, 4, 0  # 240
test_ex_3 = 3, 4, 4, 3  # 680

print(f'test ex res -> {get_max_grid_happiness(*test_ex)}')                           # 36 366 98 989 98989 LL
print(f'test ex 1 res -> {get_max_grid_happiness(*test_ex_1)}')
print(f'test ex 2 res -> {get_max_grid_happiness(*test_ex_2)}')
print(f'test ex 3 res -> {get_max_grid_happiness(*test_ex_3)}')
print(f'huge test res -> {get_max_grid_happiness(5, 5, 6, 6)}')

print(f'{(1, 98) + (98989,)}')
for row_ in happiness_matrix:
    print(f'{row_}')


class Solution:

    a = 98
    b = 989
    c = 98989

    k = a * b * c


print(f'{Solution.k = }')



