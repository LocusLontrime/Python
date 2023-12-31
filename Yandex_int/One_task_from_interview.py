def f(a: list[int], x: int):
    # check for wrong cases:
    if a is None or not a:
        print(f'err1')
        return -1
    if not isinstance(a, list) or not isinstance(x, int):
        print(f'err2')
        return -1
    # what about every element of a???
    if not isinstance(a[0], int):
        print(f'err3')
        return -1
    # augmented bin search:
    res = -1
    li, ri = 0, len(a) - 1
    while li <= ri:
        pivot = (ri + li) // 2
        if a[pivot] == x:
            res = x
            break
        elif (pe := a[pivot]) > x:
            ri = pivot - 1
        else:
            res = pe
            li = pivot + 1
    return res


# examples:
for x_ in [0, 1, 2, 4, 5, 7, 12, 16, 17, 97, 98, 99]:
    print(f'f({x_}) -> {f([1, 3, 4, 5, 6, 8, 12, 13, 15, 17, 98], x_)}')
