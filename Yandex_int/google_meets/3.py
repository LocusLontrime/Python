import random


# 3. Longest consecutive subsequence in array may contain duplicates.
# E.g. A = [1,6,10,4,7,9,5]] => 4,5,6,7


# 1 approach: sort and then search (n * log(n)) ->
def search_for_seq(arr: list[int]) -> tuple[str, int]:
    sorted_arr = quick_sort(arr)
    print(f'{sorted_arr = }')
    max_counter = 0
    best_seq = f''
    i = 0
    while i < len(sorted_arr):
        counter = 0
        seq = f'{sorted_arr[i]}'
        print(f'{i = }')
        while (i < len(sorted_arr) - 1) and (sorted_arr[i + 1] - sorted_arr[i] == 1):
            counter += 1
            seq += f'{sorted_arr[i + 1]}'
            i += 1
        print(f'{counter = }')
        if counter > max_counter:
            max_counter = counter
            best_seq = seq
        i += 1
    return best_seq, max_counter + 1


def quick_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    # border case:
    if n in [0, 1]:
        return arr
    # body of rec:
    median = arr[n // 2]
    left_arr, right_arr, middle = [], [], []
    for val in arr:
        if val > median:
            right_arr += [val]
        elif val < median:
            left_arr += [val]
        else:
            middle += [median]
    # recurrent relation:
    return quick_sort(left_arr) + [median] + quick_sort(right_arr)


test = [1, 6, 10, 4, 7, 9, 5]  # res -> 4,5,6,7
test_ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
test_large = [random.randint(0, 1_000_000) for i in range(100_000)]

# print(f'sorted arr -> {quick_sort(test_large)}')
print(f'longest sequence -> {search_for_seq(test)}')
