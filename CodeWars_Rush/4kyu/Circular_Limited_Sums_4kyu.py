# accepted on codewars.com
import math
import time


def circular_limited_sums(max_n, max_fn):  # 36 366 98 989
    if max_n == 1:
        return max_fn

    memo_table = dict()

    def recursive_seeker(curr_n, prev_element, last_elem):
        # border case:
        if curr_n == 1:
            return min(max_fn - prev_element, max_fn - last_elem) + 1

        if (curr_n, prev_element, last_elem) not in memo_table:
            sum_of_paths = 0

            for i in range(0, max_fn - prev_element + 1):
                sum_of_paths += recursive_seeker(curr_n - 1, i, i if curr_n == max_n else last_elem)

            memo_table[(curr_n, prev_element, last_elem)] = sum_of_paths

        return memo_table[(curr_n, prev_element, last_elem)]

    result = recursive_seeker(max_n, 0, 0)

    # print(result)
    # print('memo table:')
    # print(memo_table)

    return result % 12345787


# print(circular_limited_sums(1, 1))
# print(circular_limited_sums(6, 5))
# print(circular_limited_sums(1, 2))
# print(circular_limited_sums(2, 2))
# print(circular_limited_sums(3, 2))
# print(circular_limited_sums(4, 2))
# print(circular_limited_sums(5, 2))
# print(circular_limited_sums(10, 5))
# print(circular_limited_sums(98, 4))


# print(circular_limited_sums(100, 10))

for i in range(1, 11):
    print(f'3^{i}: {3 ** i}, cls({i}, 2): {circular_limited_sums(i, 2)}')

for i in range(1, 11):
    print(f'cls(10, {i}): {circular_limited_sums(10, i)}, diff: {(i + 1) ** 10 - circular_limited_sums(10, i)}')

for i in range(1, 11):
    print(math.comb(10, i))









# tic = time.perf_counter()
# print(circular_limited_sums(989, 111))
# toc1 = time.perf_counter()
# print(f"Time elapsed for calculations: {toc1 - tic:0.4f} seconds")
