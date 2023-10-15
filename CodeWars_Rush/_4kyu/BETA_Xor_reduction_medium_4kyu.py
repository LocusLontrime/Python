# accepted on codewars.com
# Given two integers, m and n, return the cumulative xor of all
# positive integers between them, inclusive.
import math


# O(1)
def fast_xor(m, n):
    def xor(k):
        return [0, k, 1, k + 1][(k + 1) % 4]
    return xor(m - 1) ^ xor(n)


# O(log2(n))
def xor_reduction(m: int, n: int) -> int:
    def find_max_pow_of_2(num: int) -> int:
        p = int(math.log2(num))
        return p if 2 ** p == num else p + 1

    def find_min_pow_of_2(num: int) -> int:
        return int(math.log2(num))

    min_pow_of_2 = find_max_pow_of_2(m)
    max_pow_of_2 = find_min_pow_of_2(n)

    print(f'min_pow_of_2: {min_pow_of_2}, max_pow_of_2: {max_pow_of_2}')

    def get_right_part(max_pow: int, right_border: int):

        if 2 ** max_pow == right_border:
            return '0'

        res_binary_str = ''
        rem = right_border - 2 ** max_pow + 1

        print(f'max_pow: {max_pow}, rem: {rem}')

        for power in range(max_pow, 0 - 1, -1):
            if power == max_pow:
                res_binary_str += '1' if rem % 2 == 1 else '0'
            elif power == 0:
                res_binary_str += '1' if (rem + 1) % 4 in [0, 3] else '0'
            else:
                if (q := (rem // (p := 2 ** power))) % 2 == 0:
                    print(f'q: {q}, p: {p}')
                    res_binary_str += '0'
                else:
                    print(f'q: {q}, p: {p}')
                    res_binary_str += '1' if (k := rem % p) % 2 == 1 else '0'
                    print(f'k: {k}')

        return res_binary_str

    def get_left_part(min_pow: int, left_border: int):

        if 2 ** min_pow == left_border:
            return '0'

        res_binary_str = ''
        rem = 2 ** min_pow - left_border

        print(f'min_pow: {min_pow}, rem: {rem}')

        for power in range(min_pow - 1, 0 - 1, -1):
            if power == min_pow:
                res_binary_str += '1' if rem % 2 == 1 else '0'
            elif power == 0:
                res_binary_str += '1' if rem % 4 in [1, 2] else '0'
            else:
                if (q := (rem // (p := 2 ** power))) % 2 == 1:
                    print(f'q: {q}, p: {p}')
                    res_binary_str += '0'
                else:
                    print(f'q: {q}, p: {p}')
                    res_binary_str += '1' if (k := rem % p) % 2 == 1 else '0'
                    print(f'k: {k}')

        print(f'left bin: {res_binary_str}')

        return res_binary_str

    bin_num_right = int(get_right_part(max_pow_of_2, n), 2)
    bin_num_left = int(get_left_part(min_pow_of_2, m), 2)

    print(f'bin_num_right: {bin_num_right}, bin_num_left: {bin_num_left}')

    return bin_num_left ^ (1 if min_pow_of_2 <= 1 < max_pow_of_2 else 0) ^ bin_num_right


def bruteforce_xor(m, n):
    res = 0
    for i in range(m, n + 1):
        res ^= i

    return res


# print(bruteforce_xor(8, 27))
# print(bruteforce_xor(8, 26))
# print(bruteforce_xor(1024, 2048 - 1))
# print(bruteforce_xor(3, 10))
# #
# # print(xor_reduction(8, 98))
# # print(xor_reduction(8, 26))
# print(xor_reduction(3, 10))
# print(xor_reduction(2, 5))


for m in range(0, 15):
    for n in range(m, 15):
        print(f'm, n: {m, n}, xor: {bruteforce_xor(m, n)}, fast_xor: {fast_xor(m, n)}')


print(fast_xor(11 ** 1000, 9 ** 9999))




