import collections
import sys
import time


sys.setrecursionlimit(100_000)


rec_counter: int


def make_cocktail(ingr: dict[int], flav: int, bittersw: int) -> list[str]:
    # <--- good luck!
    pass


def can_fit(ingrs: dict[int], sum_: int):
    ...


def rec_seeker_j(i: int, j: int, sum_: int, ingrs: list[int], memo_table: dict[tuple[int, int, int], tuple[bool, list[int]]]) -> bool:
    # finds a subsequence with the given sum with j items max ...

    global rec_counter

    # print(f'{rec_counter} -> {i, j, sum_, (j, sum_) in memo_table.keys() = }')

    rec_counter += 1

    # border cases
    if i < 0 or j < 0 or sum_ < 0:
        return False

    if sum_ == 0:
        memo_table[(i, j, sum_)] = True, []
        return True

    # body of rec:
    if (i, j, sum_) not in memo_table.keys():

        if rec_seeker_j(i - 1, j - 1, sum_ - ingrs[i], ingrs, memo_table):
            memo_table[i, j, sum_] = True, memo_table[(i - 1, j - 1, sum_ - ingrs[i])][1] + [ingrs[i]]

        elif rec_seeker_j(i - 1, j, sum_, ingrs, memo_table):
            memo_table[i, j, sum_] = True, memo_table[(i - 1, j, sum_)][1]

        else:
            memo_table[i, j, sum_] = False, [-1]

            # returning value:
    return memo_table[(i, j, sum_)][0]


def rec_seeker(i: int, sum_: int, ingrs: list[int], memo_table: dict[tuple[int, int], tuple[bool, list[int]]]) -> bool:
    # finds a subsequence with the given sum...

    global rec_counter

    # print(f'{rec_counter} -> {i, j, sum_, (j, sum_) in memo_table.keys() = }')

    rec_counter += 1

    # border cases
    if i < 0 or sum_ < 0:
        return False

    if sum_ == 0:
        memo_table[(i, sum_)] = True, []
        return True

    # body of rec:
    if (i, sum_) not in memo_table.keys():

        if rec_seeker(i - 1, sum_ - ingrs[i], ingrs, memo_table):
            memo_table[i, sum_] = True, memo_table[(i - 1, sum_ - ingrs[i])][1] + [ingrs[i]]

        elif rec_seeker(i - 1, sum_, ingrs, memo_table):
            memo_table[i, sum_] = True, memo_table[(i - 1, sum_)][1]

        else:
            memo_table[i, sum_] = False, [-1]

            # returning value:
    return memo_table[(i, sum_)][0]


ingrs_ = {
    "Mormodica": -6,
    "Liquor": -4,
    "Vodka": -2,
    "Mint": 1,
    "Orange": 2,
    "Pineapple": 3,
    "Watermelon": 4,
    "Sugar": 6
}

arr_ = [_ for _ in range(100)]  # [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 5, 6, 8, 9, 15, 16, 17, 22, 23, 25, 27, 29, 85, 87, 89, 92, 95, 97, 98, 111, 189, 222, 366, 368, 487, 657, 768, 881, 888, 899, 927, 988, 989, 98989]

rec_counter = 0

start = time.time_ns()
memo_table_ = {}
sum_given = 299  # 999 + 998 + 997 + 889 + 887 + 777 + 729 + 666 + 189 + 179 + 98 + 89 + 9 + 3 + 2 + 1  # 999 + 998 + 997
j_ = 5  # len(arr_)
print(f'res: {rec_seeker_j(len(arr_) - 1, j_, sum_given, arr_, memo_table_)}')
finish = time.time_ns()

print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
print(f'{rec_counter = }')
print(f'{len(memo_table_) = }')
print(f'seq: {memo_table_[(len(arr_) - 1, j_, sum_given)][1]}')

# print(f'Memo table: ')
# for k, v in memo_table_.items():
#     print(f'{k} -> {v}')





# 36 366 98 989 98989 LL
