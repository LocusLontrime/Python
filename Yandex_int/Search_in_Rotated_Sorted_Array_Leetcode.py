def search(nums: list[int], target: int) -> int:
    lp, rp = 0, len(nums) - 1
    target_index = -1
    counter = 0
    while lp <= rp:
        counter += 1
        pivot_index = (lp + rp) // 2
        pivot_el = nums[pivot_index]
        # main logic:
        if pivot_el == target:
            return pivot_index
        if nums[rp] > nums[lp]:
            # usual bin-search:
            if pivot_el > target:
                rp = pivot_index - 1
            else:
                lp = pivot_index + 1
        else:
            # modified part of bin-search:
            if pivot_el >= nums[lp]:
                if nums[lp] <= target <= pivot_el:
                    rp = pivot_index - 1
                else:
                    lp = pivot_index + 1
            else:
                if pivot_el <= target <= nums[rp]:
                    lp = pivot_index + 1
                else:
                    rp = pivot_index - 1
        print(f'{counter} -> pi, pe: {pivot_index, pivot_el}; lp, rp: {lp, rp}')
    return target_index


nums_ = [_ for _ in range(900_000, 10_000_000)] + [_ for _ in range(1, 900_000)]  # [3, 1]  # [4, 5, 6, 7, 0, 1, 2]
target_ = 899_998  # 6
print(f'index of {target_}: {search(nums_, target_)}')






























































