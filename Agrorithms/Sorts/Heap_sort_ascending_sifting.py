# main method-covering
def heap_sort_bottom_up(array: list[int]):
    # border case:
    if array is None or len(array) == 0:
        print('The array is empty, there is nothing to sort')
        return None
    # array size
    size = len(array)
    # building a heap, using the ascending sifting:
    # (there is no need to sift the elements with no descendants)
    for i in range((size - 2) // 2, -1, -1):
        bottom_up_root_sifting(array, i, size)
    # building the sorted array:
    for last_index in range(size - 1, 0, -1):
        # locate the current maximum of the heap at the end of it:
        array[last_index], array[0] = array[0], array[last_index]
        # then make a step of heapifying:
        bottom_up_root_sifting(array, 0, last_index)


# here we find the leaf of the heap built with the max array's element
def top_down_max_leaf_search(array: list[int], upper_ind: int, size: int):
    # here we start:
    curr_index = upper_ind
    # indexes of leafs:
    left_leaf_index = curr_index * 2 + 1
    right_leaf_index = curr_index * 2 + 2
    # checks if the right leaf exist:
    if right_leaf_index >= size:
        if left_leaf_index < size:
            return left_leaf_index
        else:
            return curr_index
    # compare two leafs' values:
    if array[left_leaf_index] > array[right_leaf_index]:
        return top_down_max_leaf_search(array, left_leaf_index, size)
    else:
        return top_down_max_leaf_search(array, right_leaf_index, size)


# locate the root at the place of the first leaf that is bigger than the root itself
# and then shifts all the parent nodes on the one level higher
def bottom_up_root_sifting(array: list[int], upper_ind: int, size: int):
    # find the max leaf position:
    curr_index = top_down_max_leaf_search(array, upper_ind, size)
    print(f'curr_index: {curr_index}, size: {size}')
    # ascending until the first bigger
    while array[curr_index] < array[upper_ind]:
        # proceeding to the parent (on the one level higher)
        curr_index = (curr_index - 1) // 2
    # memorize the curr_index and locate the upper leaf at the place of current leaf:
    memoized_current_leaf = array[curr_index]
    array[curr_index] = array[upper_ind]
    # now shifting all the leafs on the one level higher:
    while curr_index > upper_ind:
        # proceeding to the parent (on the one level higher)
        curr_index = (curr_index - 1) // 2
        # swap the leafs' values
        array[curr_index], memoized_current_leaf = memoized_current_leaf, array[curr_index]


# test-case:
arr = [1, 7, 7, 0, 7, 8, 98, 1, -111, -1, -1, 0, 0, 1, -1, 111, 98, 98, 9, 8, 7, 6, 5, 55, 111, 0, -1, -1001, 98, 9898989, 98]
arr_x = [9, 8, 7, 77, 1, 2, 3, 0, 989, 98]
heap_sort_bottom_up(arr)
print(arr)
