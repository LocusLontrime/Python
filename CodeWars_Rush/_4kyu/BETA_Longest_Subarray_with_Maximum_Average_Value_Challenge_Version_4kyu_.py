# accepted
import random
import time


def solve(nums: list[int], k: int) -> tuple:
    # print(f'{nums = }')
    result = ()
    if not nums or len(nums) < k:
        return result
    # Defining precision for the binary search result (defined by nums' elements quantity...):
    precision = 10 ** -len(str(len(nums)))  # 1e-5
    print(f'{precision = }')
    n = len(nums)
    # Setting the lower and upper bounds of binary search to the min and max of nums
    left, right = min(nums), max(nums)
    # print(f'{left, right = }')
    # Binary search routine to find maximum average
    while True:
        mid = (left + right) / 2
        # print(f'{mid = }')
        # If the current mid-value can be an average, update the lower bound
        if r := can_be_average(nums, mid, k):
            # print(f'...{r = }')
            left = mid
            result = r
        # Otherwise, update the upper bound
        else:
            right = mid
        if right - left < precision:
            break
    # The result is the left bound after the binary search loop ends
    return result


def can_be_average(nums: list[int], v: float, k: int) -> tuple:
    # Initialize the sum of the first k elements adjusted by subtracting v
    current_sum = sum(nums[:k]) - k * v
    # If the current average is already >= 0, return True
    res = ()
    ind, max_len = 0, 0
    if current_sum >= 0:
        max_len = k
        res = 0, k
    prev_sum = min_sum = 0

    # Iterate over the rest of the elements
    for i in range(k, len(nums)):
        # Update the sum for the new window by including the new element and excluding the old
        current_sum += nums[i] - v
        # Update the sum for the previous window
        prev_sum += nums[i - k] - v
        # Keep track of the minimum sum encountered so far
        # min_sum = min(min_sum, prev_sum)
        if min_sum > prev_sum:
            min_sum = prev_sum
            ind = i - k + 1
        # If the current window sum is greater than any seen before, return True
        if current_sum >= min_sum:
            if max_len <= i - ind + 1:
                max_len = i - ind + 1
                res = ind, max_len
    return res


arr_great, k_great = [random.randint(0, 1) for _ in range(1_000_000)], 366_665

start_ = time.perf_counter()
print(f'avg, rpi, max_len: {solve(arr_great, k_great)}')
runtime = round(1000 * (time.perf_counter() - start_), 2)
print(f'time elapsed: {runtime} milliseconds')
# print(f'res: {longest_sub(arr_xxx[::], 95, 0.8, 63)}')

# print(f'{sum(arr_xxx[22: 22 + 70]) / 70}')


















                                                                                      # 36 366 98 989 98989 LL
