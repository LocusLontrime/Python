def product_except_self(nums: list[int]) -> list[int]:
    prefix_left, prefix_right, zeroes_q, zi = create_prefix_arrays(nums)
    print(f'prefix_left: {prefix_left}')
    print(f'prefix_right: {prefix_right}')
    print(f'zeroes quantity: {zeroes_q}')
    if zeroes_q > 1:
        return [0 for _ in range(len(nums))]
    elif zeroes_q == 1:
        res = [0 for _ in range(len(nums))]
        res[zi - 1] = prefix_left[zi - 1] * prefix_right[zi]
        return res
    return [prefix_left[i] * prefix_right[i + 1] for i in range(len(nums))]


def create_prefix_arrays(nums: list[int]) -> tuple[list[int], list[int], int, int | None]:
    zeroes_counter = 0
    zero_ind = None
    prefix_left = [1 for _ in range(len(nums) + 1)]
    prefix_right = [1 for _ in range(len(nums) + 1)]
    for i in range(1, l_ := len(prefix_left)):
        if (num_ := nums[i - 1]) == 0:
            zeroes_counter += 1
            zero_ind = i
        prefix_left[i] = prefix_left[i - 1] * num_
        prefix_right[l_ - i - 1] = prefix_right[l_ - i] * nums[l_ - i - 1]
    return prefix_left, prefix_right, zeroes_counter, zero_ind


arr = [1, 2, 3, 4, 6, 7]
arr_ = [-1, 1, 7, 11, 0, -3, 3]
arr_x = [0, 0, 0, 0]

print(f'res: {product_except_self(arr)}')
print(f'res: {product_except_self(arr_)}')
print(f'res: {product_except_self(arr_x)}')


