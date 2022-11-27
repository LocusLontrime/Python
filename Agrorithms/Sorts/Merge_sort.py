def merge_sort(nums: list[int]):
    rec_counter = 0
    length = len(nums)
    print(f'Merge sort is finished, {rec_counter} steps done')
    return recursive_merge_sort(nums, 0, length - 1, rec_counter)


def recursive_merge_sort(nums, left_index: int, right_index: int, rec_counter: int):
    rec_counter += 1

    if left_index == right_index:
        return [nums[left_index]]  # base case of recursion, when the one element in array remained

    pivotIndex = (left_index + right_index) // 2  # calculating a pivot element

    leftArray = recursive_merge_sort(nums, left_index, pivotIndex, rec_counter)  # recurrent defining of a new left and right arrays
    rightArray = recursive_merge_sort(nums, pivotIndex + 1, right_index, rec_counter)

    return merge(leftArray, rightArray)  # merging the two parts in one array


def merge(left_array: list[int], right_array: list[int]):
    leftLength = len(left_array)
    rightLength = len(right_array)

    result = []
    lP, rP = 0, 0  # two pointers strategy

    while lP < leftLength and rP < rightLength:  # while no array is finished

        # the least one is added to the final array
        if left_array[lP] < right_array[rP]:
            result.append(left_array[lP])
            lP += 1
        else:
            result.append(right_array[rP])
            rP += 1

    # now we're adding the elements remained in one of arrays to the resulting one

    # the case in which the elements remained in the left array
    for i in range(lP, leftLength):
        result.append(left_array[i])

    # the case in which the elements remained in the right array
    for i in range(rP, rightLength):
        result.append(right_array[i])

    return result


array = [1, 5, 67, 7, 9, 0, 9, 98, 989, 98989, 36666]
print(merge_sort(array))
