MODULO = 10 ** 9 + 7
import time


def time_palindrome(n: str, m: str) -> int:  # diff version
    n_str, m_str = subtract_one(n), subtract_one(m)  # n, m = input().split(' ')
    steps = min(len(n_str), len(m_str))
    min_str, max_str = (m_str, n_str) if len(n_str) > len(m_str) or len(n_str) == len(m_str) and n_str > m_str else (n_str, m_str)
    palindromes = (int(min_str) + 1) % MODULO  # 0 included
    # pre-calculation:
    pre_calc = [0 for _ in range(steps)]
    for step_, (max_dig, min_dig) in enumerate(zip(max_str, min_str[::-1])):
        if max_dig > min_dig or (max_dig > min_dig and pre_calc[step_ - 1] == 1):
            pre_calc[step_] = 1
    # palindromes quantity calculation:
    product_ = 0
    for step_, (dig_, _dig, d_) in enumerate(zip(max_str[:steps][::-1], min_str, pre_calc[:-1][::-1] + [0])):
        dig_, _dig = int(dig_), int(_dig)
        palindromes -= (9 - dig_ if 9 > dig_ else 0) * product_ + (_dig - dig_ - d_ if _dig - dig_ - d_ > 0 else 0)
        product_ = (product_ * 10 + _dig) % MODULO
    return palindromes % MODULO


def subtract_one(num: str) -> str:
    i = 0
    while num[len(num) - 1 - i] == '0':
        i += 1
    res = num[:len(num) - 1 - i] + f'{int(num[len(num) - 1 - i]) - 1}' + f'9' * i
    if res[0] == '0' and len(res) > 1:
        res = res[1:]
    return res


def i_am_brute(n: int, m: int):  # time palindromes easy version
    min_, max_ = min(n - 1, m - 1), max(n - 1, m - 1)
    counter_pals, power_of_ten, l_ = 0, 10, 1
    for num in range(min_ + 1):
        if num == power_of_ten:
            power_of_ten *= 10
            l_ += 1
        if int(str(num)[::-1] + '0' * (len(str(max_)) - l_)) <= max_:
            counter_pals += 1
    return counter_pals


# print(f'')
# 75819; f'{random.randint(1, 10 ** 1_000)}', f'{random.randint(1, 10 ** 1_000)}'  #
# while True:  24, 60; 12, 1234; 723, 581
n__, m__ = f'1234567809' * 10_000, f'9876543201' * 10_000  # 752977529752913651365752913655291365136575297529136513657529136575291365, 292929358129358122935812992935812935829293581293581229358129912293581299  # random.randint(100_000 + 1, 999_999), random.randint(100_000 + 1, 999_999)  # 1269, 5196, 752913, 293581; 57, 91; 899, 651
# print(f'n__, m__: {n__, m__}')
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

# print(f'{subtract_one(f"98")}')


def pairs():
    # teams...
    n = int(input())
    arr = list(map(int, input().split(' ')))
    if len(arr) % 2 != 0:
        # early break if we have an odd number of items...
        return -1
    # the core:
    li, ri = 0, len(arr) - 1
    numset = set()
    while li < ri:
        numset.add(arr[li] + arr[ri])
        if len(numset) > 1:
            return -1
        li += 1
        ri -= 1
    return numset.pop()


k = 12
print(f'1s: {k.bit_count()}')

