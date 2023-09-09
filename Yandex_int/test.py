def longest_1s_vector_coords(array: list[int]) -> tuple[int] or None:
    i, li, ri = 0, 0, 0
    tmp = 0
    while i < (n := len(array)):
        while i < n and array[i] == 0:
            i += 1
        tmp = i
        while i < n and array[i] == 1:
            i += 1
        if i - tmp > ri - li:
            ri, li = i, tmp
    if ri - li == 0:
        return None
    return li, ri - 1


arr = [0, 0, 1, 1, 1, 1, 0, 1, 0, 1]  # -> (2, 5)
arr1 = [0, 0, 0]  # -> None
arr2 = [0, 1, 0, 0]  # -> (1, 1)
arr3 = [1]  # -> (0, 0)

print(f'longest_1s_vector_coords: {longest_1s_vector_coords(arr)}')
