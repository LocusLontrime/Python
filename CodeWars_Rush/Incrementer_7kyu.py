def incrementer(nums):
    # your code here
    for i in range(len(nums)):
        nums[i] += i + 1
        nums %= 10
    return nums

