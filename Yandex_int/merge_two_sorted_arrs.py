def merge_two_sorted(arr1: list[int], arr2: list[int]) -> list[int]:
    merged_arr = []
    i1, i2 = 0, 0
    l1, l2 = len(arr1), len(arr2)
    while i1 < l1 and i2 < l2:
        if (el1 := arr1[i1]) < (el2 := arr2[i2]):
            merged_arr.append(el1)
            i1 += 1
        else:
            merged_arr.append(el2)
            i2 += 1
    print(f'i1, i2: {i1, i2}')
    # there might be some elements remained in one of two arrays given:
    for i in range(i1, l1):
        merged_arr.append(arr1[i])
    for i in range(i2, l2):
        merged_arr.append(arr2[i])
    return merged_arr


arr1_ = [1, 5, 7, 9]
arr2_ = [3, 6, 11, 19, 74, 98]

print(f'merged two: {merge_two_sorted(arr1_, arr2_)}')
