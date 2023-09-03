import time


def i_am_broot(arr: list[int]):
    # quadratic one:
    distinct_arrays = []
    for j in range(length := len(arr)):
        for i in range(j + 1, length):
            cl = len(set(slice_ := arr[j: i + 1]))
            if cl == i - j + 1:
                distinct_arrays.append(slice_)
    return distinct_arrays


def distinct_nums_subarrays(arr: list[int]):
    distinct_arrays = []
    lp, rp = 0, 0
    sau = set()
    indices = []
    # two-pointers core:
    while lp < len(arr) - 1:
        # print(f'lp, rp: {lp, rp}')
        if rp < len(arr):
            sau.add(arr[rp])
            indices.append(rp)
            if len(sau) == rp - lp + 1:
                # print(f'sau: {sau}')
                distinct_arrays.append(indices[:])
                # print(f'distinct_arrays: {distinct_arrays}')
                rp += 1
                continue
        # indices reboot:
        lp += 1
        rp = lp
        sau = set()
        indices = []
    return sorted(distinct_arrays, key=lambda a: len(a))


arr_ = [1, 1, 7, 1, 11, 98, 2, 7, 99, 98, 989, 989, 1, 98989]
arr_x = [i for i in range(1, 1_000 + 1)]

start = time.time_ns()
# res = i_am_broot(arr_x)
res = distinct_nums_subarrays(arr_x)
finish = time.time_ns()
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')

# print(f'subarrays: ')
# for row in res:
#     print(f'{row}')

# a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# print(f'a[:]: {a[:]}')
# print(f'a[::]: {a[::]}')
