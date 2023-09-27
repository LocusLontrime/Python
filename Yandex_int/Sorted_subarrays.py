# The Task: Count all sorted subarrays:


# O(n^2)
def i_am_brut(arr: list[int]):
    counter = 0
    for j in range(len(arr)):
        i = j
        while i < len(arr) - 1 and arr[i] <= arr[i + 1]:
            i += 1
        counter += i - j + 1
    return counter


# O(n)
def sorted_subarrays(arr: list[int]):
    counter = 0
    i = 0
    while i < len(arr) - 1:
        temp = i
        while i < len(arr) - 1 and arr[i] <= arr[i + 1]:
            i += 1
        delta = (i - temp + 2) * (i - temp + 1) // 2
        counter += delta
        i += 1
    return counter


arr_ = [1, 2, 3, 4, 5, 3, 4, 7, 6, 5, 4, 3, 2, 5, 4, 3, 6, 1, 2, 3, 5, 1, 8, 9]
print(f'i_am_brut: {i_am_brut(arr_)}')
print(f'sorted_subarrays: {sorted_subarrays(arr_)}')
