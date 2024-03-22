# accepted on codewars.com


def will_it_balance(stick, terrain):
    return terrain.index(1) <= sum(i * mi for i, mi in enumerate(stick)) / sum(stick) <= len(stick) - 1 - terrain[::-1].index(1)


_arr = [9, 1, 11, 98, 11, 1]
arr_ = [0, 0, 1, 1, 1, 0]                                                             # 36 366 98 989 98989 LL                                             


print(f'res: {will_it_balance(_arr, arr_)}')
