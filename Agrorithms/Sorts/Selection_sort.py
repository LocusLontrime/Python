def selection_sort(array: list[int]):
    for i, el in enumerate(array):
        min_ind = min(range(i, len(array)), key=array.__getitem__)
        array[i], array[min_ind] = array[min_ind], array[i]


arr = [1, 1, 0, -1, -111, 98, 98, 97, 66, 76, 90, 100, 101, 0, 0, -11, 98989]

selection_sort(arr)
print(arr)
