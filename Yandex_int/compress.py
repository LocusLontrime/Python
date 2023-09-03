def compress(array: list[int]) -> str:
    nums = sorted(array)
    print(f'nums: {nums}')
    result = []
    i = 0
    temp_left = 0
    while i < len(nums):
        while i < len(nums) - 1 and nums[i + 1] == nums[i] + 1:
            i += 1
        if temp_left == i:
            s = f'{nums[temp_left]}'
        else:
            s = f'{nums[temp_left]}-{nums[i]}'
        result.append(s)
        i += 1
        temp_left = i

    return ','.join(result)


arr = [1, 4, 5, 2, 3, 6, 8, 9, 11, 0]
arr_x = [1, 2, 3, 4]
arr_xxx = [1, 4]
arr_y = [1, 4, 98, 2, 989, 988, 98989]

print(f'res: {compress(arr_y)}')

