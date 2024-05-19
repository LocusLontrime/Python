# longest increasing subsequence


rec_counter: int


def lis(arr: list[int]) -> list[int]:
    global rec_counter
    rec_counter = 0
    n = len(arr)
    print(f'{n = }')
    res = rec_seeker(n, arr, dp := [0 for _ in range(n + 1)], indices := [None for _ in range(n + 1)])
    print(f'{res = }')
    print(f'{dp = }')
    print(f'{indices = }')
    lis_ = []
    i_ = n
    while indices[i_] is not None:                                                    # 36 366 98 989 98989 LL
        i_ = indices[i_]
        lis_ += [arr[i_]]
    return lis_[::-1]


def rec_seeker(i: int, arr: list[int], dp: list[int], indices: list[int | None]) -> int:
    global rec_counter
    rec_counter += 1
    # print(f'{i = }')
    res = 0
    best_ind = None
    if dp[i] == 0:
        for i_ in range(i):
            if i == len(arr) or arr[i] > arr[i_]:  # condition of increasing
                if (r := rec_seeker(i_, arr, dp, indices) + 1) > res:
                    res = r
                    best_ind = i_
        dp[i] = res
        indices[i] = best_ind
    return dp[i]


arr_ = [5, 2, 7, 3, 6, 1, 2, 1, 7, 5, 4, 3, 5, 1, 0, 1, 7, 8, 18, 7, 2, 98, 11, 1, 89, 989]

arr_x = [98, 98, 98]

print(f'res: {lis(arr_)}')
print(f'{rec_counter = }')
