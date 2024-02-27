# Given a binary array nums, return the maximum number of consecutive 1's in the array.


# [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0]
# []
# [1]
# [0]
# [0, 1]
# [1, 0]


def max_cons_ones(nums: list[int]) -> int:
    maxCounter = 0
    ind = 0

    while ind < len(nums):

        temp = ind
        while ind < len(nums) and nums[ind] == 1:  # counts 1s!
            ind += 1

        maxCounter = max(maxCounter, ind - temp)

        while ind < len(nums) and nums[ind] == 0:  # skips zeroes...
            ind += 1

    return maxCounter


# [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0]
def max_cons_ones_jumi(nums: list[int]) -> int:
    counter = 0
    maxCounter = 0
    ind = 0

    while ind < len(nums):
        print(f'el: {nums[ind]}')

        if nums[ind] == 1:
            counter += 1
        else:
            counter = 0

        maxCounter = max(maxCounter, counter)
        ind += 1

    return maxCounter


nums_ = [0]  # [0, 1]
print(f'Max consecutive ones: {max_cons_ones_jumi(nums_)}')


