# accepted on codewars.com
from itertools import combinations


def choose_best_sum(t: int, k: int, ls: list[int]) -> int or None:
    if k > len(ls):
        return None

    towns_combs = combinations(ls, k)
    biggest_dis = 0
    for chain in towns_combs:
        if (s := sum(chain)) <= t:
            biggest_dis = max(biggest_dis, s)

    return biggest_dis if biggest_dis else None


# print(list(combinations([1, 2, 3, 4, 5], 3)))

xs = [100, 76, 56, 44, 89, 73, 68, 56, 64, 123, 2333, 144, 50, 132, 123, 34, 89]
print(choose_best_sum(230, 4, xs))  # 230
print(choose_best_sum(430, 5, xs))  # 430
print(choose_best_sum(430, 8, xs))  # None
