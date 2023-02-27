# -*- coding: utf-8 -*-

import time
from multiprocessing import Pool


def if_prime(x):
    if x <= 1:
        return 0
    elif x <= 3:
        return x
    elif x % 2 == 0 or x % 3 == 0:
        return 0
    i = 5
    while i ** 2 <= x:
        if x % i == 0 or x % (i + 2) == 0:
            return 0
        i += 6
    return x


if __name__ == '__main__':

    start = time.time()
    answer = 0

    for i in range(1000000):
        answer += if_prime(i)
    print(f'1 процесс  {time.time() - start}')

    new_st = time.time()

    with Pool(2) as p:
        sum(p.map(if_prime, list(range(1000000))))
    print(f'2 процесса  {time.time() - new_st}')

    new_st = time.time()

    with Pool(4) as p:
        sum(p.map(if_prime, list(range(1000000))))
    print(f'4 процесса  {time.time() - new_st}')

    new_st = time.time()

    with Pool(6) as p:
        sum(p.map(if_prime, list(range(1000000))))
    print(f'6 процессов  {time.time() - new_st}')

    new_st = time.time()

    with Pool(8) as p:
        sum(p.map(if_prime, list(range(1000000))))
    print(f'8 процессов  {time.time() - new_st}')

    new_st = time.time()

    with Pool(12) as p:
        sum(p.map(if_prime, list(range(1000000))))
    print(f'12 процессов  {time.time() - new_st}')

    new_st = time.time()

    with Pool(14) as p:
        sum(p.map(if_prime, list(range(1000000))))
    print(f'14 процессов  {time.time() - new_st}')

    new_st = time.time()

    with Pool(16) as p:
        sum(p.map(if_prime, list(range(1000000))))
    print(f'16 процессов  {time.time() - new_st}')


