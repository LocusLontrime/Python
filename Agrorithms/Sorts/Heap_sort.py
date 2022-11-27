def heapify(array, arr_length, index, iteration):
    # indexes of leafs:
    left_leaf, right_leaf = 2 * index + 1, 2 * index + 2
    largest_el_index = index
    # if the left leaf value is larger than the value in the root:
    if left_leaf < arr_length:
        if array[left_leaf] > array[largest_el_index]:
            largest_el_index = left_leaf
    # if the right leaf value is larger than the value in the root:
    if right_leaf < arr_length:
        if array[right_leaf] > array[largest_el_index]:
            largest_el_index = right_leaf
    # if there is at least one value in leafs that is bigger than root val:
    if largest_el_index != index:
        # swaps the elements of array, so as the largest one should be in the root:
        array[index], array[largest_el_index] = array[largest_el_index], array[index]
        heapify(array, arr_length, largest_el_index, iteration)
    # section for algorithm's iteration:
    elif iteration > 0:
        heapify(array, arr_length, iteration - 1, iteration - 1)


def heap_sort(array):
    arr_length = len(array)
    # building the max heap structure:
    heapify(array, arr_length, arr_length, arr_length)
    # excluding the elements:
    for i in range(arr_length - 1, 0, -1):
        array[i], array[0] = array[0], array[i]
        heapify(array, i, 0, 0)  # only one call, therefore the iterations quantity is equal to 1


# test case:
arr = [12, 11, 13, 5, 6, 7, 66, 98, 1, 0, 0, 7, 0, 98989, 1, 9898989]
heap_sort(arr)
print(f'Sorted array: {arr}')










