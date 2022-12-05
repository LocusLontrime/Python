# Levi Gin
def radix_sort(arr: list):
    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    max_value = len(str(max(arr)))
    start = 0
    step = 1
    while start < max_value:

        discharge_list = [[] for _ in range(10)]
        for index, num in enumerate(digits):
            for i in arr:
                if num == i % (step * 10) // step:
                    discharge_list[index].append(i)

        arr = recreate_arr(discharge_list)
        step *= 10
        start += 1

    return arr


def recreate_arr(nums):
    new_arrays = []

    for item in nums:
        for j in item:
            new_arrays.append(j)

    return new_arrays


array = [10, 7, 33, 575, 3, 2, 1, 0, 0, 2, 95, 244, 21, 24, 64, 53]
print(radix_sort(array))
