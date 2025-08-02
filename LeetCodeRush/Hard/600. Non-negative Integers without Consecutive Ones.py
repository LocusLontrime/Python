# Given a positive integer n, return the number of the integers in the range[0, n] whose binary representations do not contain consecutive ones.
import math

# Example 1:
# Input: n = 5
# Output: 5
# Explanation: Here are the non - negative integers <= 5 with their corresponding binary representations:
# 0: 0
# 1: 1
# 2: 10
# 3: 11
# 4: 100
# 5: 101
# Among them, only integer 3 disobeys the rule(two consecutive ones) and the other 5 satisfy the rule.

# Example 2:
# Input: n = 1
# Output: 2

# Example 3:
# Input: n = 2
# Output: 3

# Constraints: 1 <= n <= 10**9


MAX_N = 10 ** 9


def find_integers(n: int) -> int:
    k = int(math.log2(MAX_N)) + 1
    print(f'{k = }')
    consecutives = [0] * k
    # filling in the consecutives array:
    for i in range(2, k):
        consecutives[i] = consecutives[i - 1] + consecutives[i - 2] + 2 ** (i - 2)
    print(f'{consecutives = }')
    bin_n = bin(n)[2:]
    ones = [0] + [len(bin_n) - i - 1 for i in range(len(bin_n)) if bin_n[i] == '1']
    print(f'{bin_n = }')
    print(f'{ones = }')

    # the core cycle:
    res = 0
    flag = False
    for i in range(1, len(ones)):
        if not flag:
            if ones[i - 1] - ones[i] == 1:
                flag = True
                res += 1
            res += consecutives[ones[i]]
        else:
            res += 2 ** (ones[i])

    print(f'{res = }')

    # returns res:
    return n + 1 - res


test_ex = 991

test_ex_1 = 5  # 5
test_ex_2 = 2  # 3
test_ex_err = 13  # 8
test_ex_err_2 = 100  # 34


print(f'test ex res -> {find_integers(test_ex)}')                                     # 36 366 98 989 98989 LL
print(f'test ex 1 res -> {find_integers(test_ex_1)}')
print(f'test ex 2 res -> {find_integers(test_ex_2)}')
print(f'test ex err res -> {find_integers(test_ex_err)}')
print(f'test ex err 2 res -> {find_integers(test_ex_err_2)}')
