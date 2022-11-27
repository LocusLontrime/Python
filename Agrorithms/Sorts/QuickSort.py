def quick_sort(array: list[int]) -> None:
    rec_counter = 0
    length = len(array)
    recursive_quick_sort(array, 0, length - 1, rec_counter)
    print(f'Quick sort is finished, {rec_counter} steps done')


# the core of sorting method
def recursive_quick_sort(array: list[int], left_border: int, right_border: int, rec_counter) -> None:
    rec_counter += 1

    # border case of list of 1 element
    if left_border == right_border:
        return

    # at first, we define the pivotElement(median)
    pivot_element = (array[left_border] + array[right_border]) // 2

    # Hoare's Partition, here we're finding the pivotIndex
    pivot_index = hoare_partition(array, left_border, right_border, pivot_element)

    # recursive tree building, divide and conquer tactics
    recursive_quick_sort(array, left_border, pivot_index, rec_counter)
    recursive_quick_sort(array, pivot_index + 1, right_border, rec_counter)


# Hoare's partition part, auxiliary to main method
def hoare_partition(array: list[int], left_border: int, right_border: int, pivot_element: int) -> int:

    while True:
        # skipping the elements that stayed at their place on the left side
        while array[left_border] < pivot_element:
            left_border += 1
        # skipping the elements that stayed at their place on the right side
        while array[right_border] > pivot_element:
            right_border -= 1
        # we are swapping two elements if they are both stay at wrong places
        if left_border < right_border:
            ints_permutation(array, left_border, right_border)
            left_border += 1
            right_border -= 1
        else:
            return right_border


# swapping two array's elements
def ints_permutation(array: list[int], i: int, j: int) -> None:
    temp = array[i]
    array[i] = array[j]
    array[j] = temp


arr = [1, 1, 0, 1, 0, 98, 989, 1, 1, 3, 36, 78, 11, 101, 98989]
quick_sort(arr)
print(arr)

