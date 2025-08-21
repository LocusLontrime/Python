# accepted on leetcode.com


def max_score(nums: list[int]) -> int:
    # array's length:
    n = len(nums)
    # pre-computations:
    gcd_matrix = [[gcd(nums[j], nums[i]) for i in range(j)] for j in range(n)]
    print(f'gcd matrix -> ')
    for row in gcd_matrix:
        print(f'{row}')
    # let us use dp with bitmasks for recursive tree limiting:
    bitmask = 0
    memo_table = {}
    return dp(bitmask, n, gcd_matrix, memo_table)


def gcd(x: int, y: int) -> int:
    while x and y:
        x = x % y
        (y, x) = (x, y)
    return max(y, x)


def dp(bitmask: int, n: int, gcd_matrix: list[list[int]], memo_table: dict) -> int:
    # base case:
    if bitmask == (1 << n) - 1:
        return 0
    # the core algo:
    # if we have not encountered this bitmasks -> let's calc dp score and append it to memo_table:
    if bitmask not in memo_table.keys():
        res = 0
        # cycling over all the possible (x, y) pairs:
        for j in range(n):
            if not (bitmask & (1 << j)):
                for i in range(j):
                    if not (bitmask & (1 << i)):
                        # gets gcd from pre-computed matrix:
                        gcd_xy = gcd_matrix[j][i]
                        # calcs new bitmask:
                        bitmask_ = bitmask | (1 << j) | (1 << i)
                        # defines index of op:
                        ind = bitmask_.bit_count() // 2
                        # delta scores:
                        delta = ind * gcd_xy
                        # res obtaining:
                        res = max(res, dp(bitmask_, n, gcd_matrix, memo_table) + delta)
        memo_table[bitmask] = res
    return memo_table[bitmask]


test_ex = [1, 2, 3, 4, 5, 6]  # res = 14
test_ex_1 = [1, 2]  # 1
test_ex_2 = [3, 4, 6, 8]  # 11

print(f'test ex res -> {max_score(test_ex)}')                                         # 36 366 98 989 98989 LL LL
print(f'test ex 1 res -> {max_score(test_ex_1)}')
print(f'test ex 2 res -> {max_score(test_ex_2)}')

# print(f'{gcd(72, 27) = }')
# print(f'{gcd(8, 8) = }')
# print(f'{gcd(1, 1) = }')
# print(f'{gcd(1, 0) = }')
# print(f'{gcd(72, 72) = }')
# print(f'{gcd(13, 13) = }')
