# accepted on codewars.com
import math


def pow_root_pandigit(val: int, n: int, k: int):
    num = math.ceil(pow(val, 1 / n))
    if num ** n == val:
        num += 1
    print(f'{num = }')
    print(f'powered_num: {num ** n}')
    res = []                                                                          # 36 366 98 989 98989 LL
    while (powered_num := num ** n) <= 987654321:
        # checks for pandigitness:
        if is_pandigit(num) and is_pandigit(powered_num):
            res += [[num, powered_num]]
            if len(res) == k:
                break
        # next step:
        num += 1
    return res


def is_pandigit(n: int) -> bool:
    num_str = str(n)
    set_ = set(num_str)
    return '0' not in set_ and len(num_str) == len(set_)


print(f'res: {pow_root_pandigit(600000000, 2, 5)}')  # -> [25941, 672935481]
print(f'res: {pow_root_pandigit(1750, 3, 5)}')
print(f'res: {pow_root_pandigit(1728, 3, 4)}')
