import time
from collections import defaultdict as d


def convert(n: int, base: int) -> str:
    res = ''
    n_ = n
    while n_ > 0:
        res += f'{n_ % base}'
        n_ //= base
    return res[::-1]


num = 5 * 216 ** 3031 + 4 * 36 ** 3042 - 3 * 6 ** 3053 - 3064
# print(f'num: {num}')

start = time.time_ns()
res_ = convert(num, 6)
print(f'converted: {res_}')
print(f'sum_: {sum(map(int, res_))}')
n_ex = 3064
print(f'converted({n_ex, 6}): {convert(n_ex, 6)}')


# counts all pairs with sum divisible by modulo
def pairs(arr: list[int] or map, modulo: int):
    occurred = d(int)
    counter = 0
    for i, el in enumerate(arr):
        mod_el = el % modulo
        counter += occurred[(modulo - mod_el) % modulo]
        occurred[mod_el] += 1
    return counter


def get_arr(file_name: str):
    arr_ = []
    with open(file_name, 'r') as f:
        arr_ = map(int, f.readlines()[1:])
        f.close()
    return arr_


array = [10, 13, 57, 68, 63, 39, 34, 68, 66, 53, 66]
array_a = get_arr('27A.txt')
print(f'array_a: ')
# for el_ in array_a:
#     print(f'{el_}')
array_b = get_arr('27B.txt')
print(f'occurred EX: {pairs(array, modulo=131)}')
print(f'occurred A: {pairs(array_a, modulo=131)}')
print(f'occurred B: {pairs(array_b, modulo=131)}')

finish = time.time_ns()
print(f'time elapsed str: {(finish - start) // 10 ** 6} milliseconds')