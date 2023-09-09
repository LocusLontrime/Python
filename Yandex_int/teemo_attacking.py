def overall_poisoned_duration(nums: list[int], duration: int) -> int:
    prev_right_border, res = 0, 0

    for i, num in enumerate(nums):
        res += duration - ((prev_right_border - num) if num < prev_right_border else 0)
        prev_right_border = num + duration

    return res