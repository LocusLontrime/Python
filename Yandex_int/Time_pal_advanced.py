import random

MODULO = 10 ** 9 + 7
import time


def time_palindrome(n: str, m: str) -> int:
    # n_, m_ = int(n), int(m)  # n, m = input().split(' ')
    # n_, m_ = n_ - 1, m_ - 1
    n_str, m_str = subtract_one(n), subtract_one(m)
    steps = min(len(n_str), len(m_str))
    min_str, max_str = (m_str, n_str) if len(n_str) > len(m_str) or len(n_str) == len(m_str) and n_str > m_str else (n_str, m_str)
    min_rev_str = min_str[::-1]
    palindromes = (int(min_str) + 1) % MODULO  # 0 included
    # pre-calculation:
    min_, max_ = '', ''
    pre_calc = [0 for _ in range(steps)]
    for step_ in range(steps):
        min_ = min_rev_str[step_] + min_
        max_ = max_str[step_] + max_
        if max_ > min_:
            pre_calc[step_] = 1
    pre_calc[-1] = 0
    # palindromes quantity calculation:
    product_ = 0
    for step_ in range(steps):
        multiplier = 10
        dig_ = int(max_str[steps - 1 - step_])
        _dig = int(min_str[step_])
        d_ = pre_calc[steps - step_ - 1 - 1]
        dl, dr = (multiplier - dig_ - 1 if multiplier - 1 > dig_ else 0) * product_, (_dig - dig_ - d_ if _dig - dig_ - d_ > 0 else 0)
        palindromes -= (dl + dr)
        # print(f'{step_ + 1}th step -> _dig, dig_, d_, product_, dl, dr, delta, pre_estimation: {_dig, dig_, d_, product_, dl, dr, dl + dr, palindromes}')
        product_ = (product_ * 10 + _dig) % MODULO
    return palindromes % MODULO


def subtract_one(num: str) -> str:
    if num == '1':
        return '0'
    i = 0
    while num[len(num) - 1 - i] == '0':
        i += 1
    res = num[:len(num) - 1 - i] + f'{int(num[len(num) - 1 - i]) - 1}' + f'9' * i
    if res[0] == '0':
        res = res[1:]
    return res


def i_am_brute(n: int, m: int):
    n_, m_ = n - 1, m - 1
    min_, max_ = min(n_, m_), max(n_, m_)
    length = len(str(max_))
    counter_pals = 0
    power_of_ten = 10
    l_ = 1
    for num in range(min_ + 1):
        if num == power_of_ten:
            power_of_ten *= 10
            l_ += 1
        if int(str_ := str(num)[::-1] + '0' * (length - l_)) <= max_:
            counter_pals += 1
            # print(f'')
            # print(f'num: {num}, num[::-1]: {int(str_)}')
    return counter_pals


# 75819; f'{random.randint(1, 10 ** 1_000)}', f'{random.randint(1, 10 ** 1_000)}'  #
# while True:  # 752913, 293581; 5 * 10 ** 1_001 + 9 * 10 ** 1_000 - 6 * 10 ** 771, 1 * 10 ** 1_001 + 7 * 10 ** 1_000 - 8 * 10 ** 991
n__, m__ = f'1234567809' * 10_000, f'9876543201' * 10_000  # 752977529752913651365752913655291365136575297529136513657529136575291365, 292929358129358122935812992935812935829293581293581229358129912293581299  # random.randint(100_000 + 1, 999_999), random.randint(100_000 + 1, 999_999)  # 1269, 5196, 752913, 293581; 57, 91; 899, 651
# print(f'n__, m__: {n__, m__}')
# print(f'pals: {i_am_brute(24, 60)}')
# print(f'pals: {i_am_brute(12, 1234)}')
# print(f'pals: {i_am_brute(723, 581)}')
# time_palindrome(723 + 1, 581 + 1)
# time_palindrome(24, 60)
# time_palindrome(12, 1234)
start = time.time_ns()
# res1 = i_am_brute(int(n__), int(m__))
res2 = time_palindrome(n__, m__)
finish = time.time_ns()
print(f'RES: {res2}')
# print(f'pals: {res1}')
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')
# if res1 - res2 > 1:
# print(f'n__, m__: {n__, m__}')
# print(f'res1, res2: {res1, res2}')
# print(f'res1 - res2: {res1 - res2}')

# s = f'98'
# print(f'{subtract_one(s)}')


def i_am_brute_():
    # teams...
    n = int(input())
    arr = list(map(int, input().split(' ')))

    if len(arr) % 2 != 0:
        return -1

    li, ri = 0, len(arr) - 1

    numset = set()
    while li < ri:
        numset.add(arr[li] + arr[ri])
        if len(numset) > 1:
            return -1
        li += 1
        ri -= 1

    return numset.pop()


# print(i_am_brute_())
