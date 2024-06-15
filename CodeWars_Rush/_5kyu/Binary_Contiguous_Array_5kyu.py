def bin_array(s: list[int]) -> int:
    precalced = [0 for _ in range(len(s) + 1)]
    deltas = {0: [0]}
    for i, el in enumerate(s):
        key = precalced[i + 1] = precalced[i] + (1 if el else -1)
        if key not in deltas.keys():
            deltas[key] = [i + 1]
        else:                                                                         # 36 366 98 989 98989 LL
            deltas[key].append(i + 1)
    print(f'{precalced = }')
    print(f'{deltas = }')

    m = max(deltas, key=(helper := lambda k: deltas[k][-1] - deltas[k][0]))
    return helper(m)


arr_ = [0, 0, 1, 1, 1, 0, 0, 0, 0, 0]  # -> 6

print(f'res: {bin_array(arr_)}')

