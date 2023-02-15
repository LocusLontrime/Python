import random
import sys
import threading
import time

sys.setrecursionlimit(2 * 1000 + 2)

rec_counter: int


# main method-covering
def heap_sort_bottom_up(array: list[int]):
    global rec_counter
    rec_counter = 0
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
    global rec_counter
    rec_counter += 1
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
    # print(f'curr_index: {curr_index}, size: {size}')
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
# arr = [1, 7, 7, 0, 7, 8, 98, 1, -111, -1, -1, 0, 0, 1, -1, 111, 98, 98, 9, 8, 7, 6, 5, 55, 111, 0, -1, -1001, 98, 9898989, 98]
# arr_x = [9, 8, 7, 77, 1, 2, 3, 0, 989, 98]
# heap_sort_bottom_up(arr)
# print(f'Sorted array: {arr}')


def get_random_array(border: int, size: int):
    if border < 0 or size < 0:
        raise AttributeError(f'border and size must be greater than zero...')
    return [random.randint(0, border) for _ in range(size)]


def get_ms(time_ns_start: int, time_ns_finish: int):
    return (time_ns_finish - time_ns_start) // 10 ** 6


def main():
    r_array = get_random_array(100000, 100000)
    # print(f'random array: {r_array}')
    start = time.time_ns()
    heap_sort_bottom_up(r_array)
    finish = time.time_ns()
    # print(f'Sorted array: {r_array}')
    print(f'rec counter: {rec_counter}')
    print(f'time elapsed: {get_ms(start, finish)} ms')


if __name__ == '__main__':
    sys.setrecursionlimit(2 * 100000 + 2)
    threading.stack_size(200000000)
    thread = threading.Thread(target=main)
    thread.start()


