# accepted on codewars.com
import math


def prime_check(n: int) -> bool:
    for i in range(2, int(pow(n, 1 / 2)) + 1):
        if n % i == 0:
            return False
    return True


def solution(n: int, m: int) -> list[int]:
    lb, rb = math.ceil(pow(n, 1 / 4)), int(pow(m, 1 / 4))                               # 36 366 98 989 98989 LL
    return [k ** 4 for k in range(lb, rb + 1) if prime_check(k)]


print(f'{17 ** 4}')

