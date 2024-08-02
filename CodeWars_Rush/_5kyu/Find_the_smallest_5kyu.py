# accepted on codewars.com
import math


def smallest(n: int) -> tuple[int, int, int]:
    n_str = f'{n}'
    size = len(n_str)

    best_num = math.inf                                                               # 36 36.6 366 98 989 98989 LL

    for j in range(size):
        dig = int(n_str[j])
        num_ = n_str[:j] + n_str[j + 1:]
        print(f'{j = } -> {num_ = }')
        for i in range(size):
            num__ = num_[:i] + n_str[j] + num_[i:]
            print(f'...{j}|{i} -> {num__ = }')
            if int(num__) < best_num:
                best_num = int(num__)
                res = best_num, j, i

    return res


print(f'res -> {smallest(1268367)}')

