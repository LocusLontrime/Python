import random
import sys
import threading
import time

rec_counter: int


def heapify(array, arr_length, index, iteration):
    global rec_counter
    rec_counter += 1
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
    global rec_counter
    rec_counter = 0
    arr_length = len(array)
    # building the max heap structure:
    heapify(array, arr_length, arr_length, arr_length)
    # excluding the elements:
    for i in range(arr_length - 1, 0, -1):
        array[i], array[0] = array[0], array[i]
        heapify(array, i, 0, 0)  # only one call, therefore the iterations quantity is equal to 1


# test case:
# arr = [12, -177, 989, 9, 9, 0, -1, -1001, 9, 0, 0, 1, 11, 13, 5, 6, 7, 66, 98, 1, 0, 0, 7, 0, 98989, 1, 9898989, 989, 98]
# heap_sort(arr)
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
    heap_sort(r_array)
    finish = time.time_ns()
    # print(f'Sorted array: {r_array}')
    print(f'rec counter: {rec_counter}')
    print(f'time elapsed: {get_ms(start, finish)} ms')


if __name__ == '__main__':
    sys.setrecursionlimit(2 * 100000 + 2)
    threading.stack_size(200000000)
    thread = threading.Thread(target=main)
    thread.start()





