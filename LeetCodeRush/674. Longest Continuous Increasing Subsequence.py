def max_cont_incr_subseq(nums: list[int]) -> int:
    maxCounter = 0
    ind = 0

    while ind < len(nums):

        temp = ind
        while ind < len(nums) - 1 and nums[ind] < nums[ind + 1]:  # counts 1s!
            ind += 1

        maxCounter = max(maxCounter, ind - temp + 1)

        ind += 1

    return maxCounter


nums_ = [9, 8, 7, 6, 5, 4, 3, 2, 1]  # [2, 2, 2, 2, 2]  # [1, 3, 5, 4, 7]

print(f'Max length of continues increasing subsequence: {max_cont_incr_subseq(nums_)}')
