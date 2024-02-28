import time


MAX_N = 10 ** 7


memo_table = {}
powers_calculated = {'': 0}


def perf_happy(n: int) -> list[int]:                                                    # 36 366 98 989 LL

    happies = []

    for i in range(1, n + 1):
        if i % 100_000 == 0:
            print(f'{i = }')
        if rec_happy_checker(i, set()):
            happies.append(i)

    return happies


def rec_happy_checker(n: int, path: set[int]) -> bool:

    # print(f'{n = } | {path = }')

    if n in memo_table.keys():
        # print(f'in memo already! {"Happy!" if memo_table[n] else "Unhappy..."}')
        return memo_table[n]

    if (k := get_pow_sum(str(n))) == 1:
        # print(f'sum = 1! Happy!')
        return True

    if k in path:
        # print(f'occurred in path already...')
        return False

    memo_table[n] = rec_happy_checker(k, path | {k})
    return memo_table[n]


def get_pow_sum(n: str) -> int:

    if n not in powers_calculated.keys():
        powers_calculated[n] = get_pow_sum(n[:-1]) + int(n[-1]) ** 2

    return powers_calculated[n]

    # return sum(int(x) ** 2 for x in n)


start = time.time_ns()
happy_nums = perf_happy(10_000_000)
finish = time.time_ns()

# print(f'Happies: {happy_nums}')
print(f'Size: {len(happy_nums)}')

print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')




