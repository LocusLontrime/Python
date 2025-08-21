# accepted on leetcode.com


def minimum_boxes(n: int) -> int:
    # l * (l + 1) * (l + 2) = 6 * n
    h = int(pow(6 * n, 1 / 3))
    if h * (h + 1) * (h + 2) > 6 * n:
        h -= 1
    print(f'{h = }')
    q = h * (h + 1) // 2
    print(f'{q = }')
    rem_n = n - h * (h + 1) * (h + 2) // 6
    print(f'{rem_n = }')
    h1 = int(pow(2 * rem_n, 1 / 2))
    if h1 * (h1 + 1) > 2 * rem_n:
        h1 -= 1
    print(f'{h1 = }')
    return q + h1 + (0 if h1 * (h1 + 1) // 2 == rem_n else 1)


test_ex = 10
test_ex_1 = 3
test_ex_2 = 4
test_ex_err = 15

print(f'test ex res -> {minimum_boxes(test_ex)}')                                     # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {minimum_boxes(test_ex_1)}')
print(f'test ex 2 res -> {minimum_boxes(test_ex_2)}')
print(f'test ex err res -> {minimum_boxes(test_ex_err)}')

