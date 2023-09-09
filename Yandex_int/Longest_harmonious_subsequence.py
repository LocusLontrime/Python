from collections import defaultdict as d


def find_lhs(nums: list[int]) -> int:
    dict_ = d(int)

    for i in nums:
        d[i] += 1

    list_keys = sorted(dict_.keys(), key=lambda x: x)
    max_length = 0
    for i, key in enumerate(list_keys[:-1]):
        if (k1 := list_keys[i + 1]) - key == 1:
            max_length = max(max_length, dict_[k1] + dict_[key])

    return max_length

