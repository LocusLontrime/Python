# accepted on coderun
import sys
import math


def get_max_days():  # 36.6
    k, m, day = get_pars()
    # first week:
    q = m
    counter = 0
    while True:
        if (counter + day) % 7 not in [6, 0]:
            q += k
        q -= (counter + 1)
        if q < 0:
            return counter
        counter += 1
        if (counter + day) % 7 == 1:
            break

    print(f'week past, counter: {counter}, day: {day + counter} q: {q}')

    # rough evaluating:
    b = 10 * k - 7 - 14 * counter
    d = b ** 2 + 392 * q
    w = (b + math.sqrt(d)) / 98.0
    print(f'{b, d, w = }')
    weeks = int(w)
    # now we can easily get parameters needed in this point (weeks later):
    days = 7 * weeks + counter
    print(f'weeks: {weeks}, days: {days}')
    q = q + 5 * k * weeks - ((28 + 7 * counter) * weeks + 49 * weeks * (weeks - 1) // 2)
    print(f'q: {q}')

    # Levi Gin's area:
    while True:
        if (days + day) % 7 not in [6, 0]:
            q += k
        q -= (days + 1)
        print(f'days: {days + day}, q: {q}')
        if q < 0:
            break
        days += 1
    return days  # -1???


def get_pars() -> tuple[int, int, int]:
    k, m, d = [int(_) for _ in input().split(' ')]
    return k, m, d


print(f'days gone: {get_max_days()}')



