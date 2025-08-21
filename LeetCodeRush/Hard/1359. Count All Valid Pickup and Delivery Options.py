# accepted on leetcode.com

memo_table = None

MODULO = 10 ** 9 + 7


def count_orders(n: int) -> int:
    global memo_table
    if memo_table is None:
        memo_table = {}
        i = 0
        permuts = 1
        memo_table[1] = 1
        multiplier = 0
        while i <= 500:
            multiplier += 4 * i + 1
            permuts = (permuts * multiplier) % MODULO
            memo_table[i] = permuts
            i += 1

    return memo_table[n - 1]


print(f'{count_orders(5)}')                                                           # 36 366 98 989 98989 LL LL



