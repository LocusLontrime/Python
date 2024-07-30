# accepted on codewars.com
from collections import Counter


def count_contiguous_distinct(k, arr: list[int]) -> list[int]:
    counter = Counter(arr[:k])
    print(f'{counter = }')

    size_ = len(counter)
    res = [size_]

    for i in range(k, len(arr)):
        print(f'{i = } | {counter = }')
        if counter[arr[i]] == 0:
            size_ += 1
        counter[arr[i]] += 1
        counter[arr[i - k]] -= 1
        if counter[arr[i - k]] == 0:
            size_ -= 1
        res += [size_]

    return res


array = [1, 2, 1, 3, 4, 2, 3]
print(f'res -> {count_contiguous_distinct(4, array)}')

