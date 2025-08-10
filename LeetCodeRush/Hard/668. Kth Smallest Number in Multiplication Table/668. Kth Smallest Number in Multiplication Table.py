# accepted on leetcode.com

# __import__("atexit").register(lambda: open("display_runtime.txt", "w").write("0")) -> cheating!

# division -> prolonged runtime... (slightly optimized) seemed the best one possible...
def find_kth_number(m: int, n: int, k: int) -> int:
    max_k = m * n
    # binary search:
    li, ri = 0, max_k
    while li <= ri:
        # middle point:
        mi = (li + ri) // 2
        nums_no_larger_than_mi = find_nums_no_larger_than_mi(m, n, mi)  # n * (mi // n) + sum(mi // i for i in range(mi // n + 1, m + 1))
        if k <= nums_no_larger_than_mi:
            ri = mi - 1
        else:
            li = mi + 1
    return li


def find_nums_no_larger_than_mi(m: int, n: int, mi: int):
    nums_no_larger_than_mi = n * (q := mi // n)
    delta = 0
    for i in range(m, q, -1):
        while (delta + 1) * i <= mi:
            delta += 1
        nums_no_larger_than_mi += delta
    return nums_no_larger_than_mi


test_ex = 3, 3, 5
test_ex_1 = 10, 10, 6
test_ex_2 = 38, 40, 955

print(f'test ex res -> {find_kth_number(*test_ex)}')                                  # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {find_kth_number(*test_ex_1)}')
print(f'test ex 2 res -> {find_kth_number(*test_ex_2)}')

