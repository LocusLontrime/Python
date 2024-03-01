# accepted on https://informatics.msk.ru/mod/statements/view.php?id=1461&chapterid=1815#1
from collections import defaultdict as d


def charmness(n: int):

    p_factors = prime_factors(n)

    # print(f'Prime factors of {n}: {p_factors}')

    return min(p_factors.values())


def prime_factors(n: int):
    i = 2
    p_factors = d(int)

    while i * i <= n:
        while n % i == 0:
            p_factors[i] += 1
            n = n // i
        i = i + 1

    if n > 1:
        p_factors[n] += 1

    return p_factors


k = int(input())

print(charmness(k))  # f'Charmness of {k} trees forest: '
