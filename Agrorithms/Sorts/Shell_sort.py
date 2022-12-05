import math
import time
from random import random


# TODO: LEVI GIN!!!
# auxiliary methods for finding different sequences for shell insertion sort:
def find_shell_simple_elements(n: int):
    elements = []
    sequence_element = n // 2
    while sequence_element >= 1:
        elements = [sequence_element] + elements
        sequence_element //= 2
    return elements


def find_shell_elements_hibbard(n: int):
    elements = []
    sequence_element, i = 1, 2
    while sequence_element <= n:
        elements.append(sequence_element)
        sequence_element = 2 ** i - 1
        i += 1
    return elements


def find_shell_elements_knuth(n: int):
    elements = []
    sequence_element, i = 1, 2
    while sequence_element <= n // 3:
        elements.append(sequence_element)
        sequence_element = (3 ** i - 1) // 2
        i += 1
    return elements


# too slow !!!
# the fastest one:
def find_shell_elements_pratt(n: int):
    st = time.time_ns()
    elements = []
    sequence_element = 1
    i, j = 0, -1
    while 2 ** i <= n // 2:
        while sequence_element <= n // 2:
            elements.append(sequence_element)
            sequence_element = 2 ** i * 3 ** j
            j += 1
        j = 1
        i += 1
        sequence_element = 2 ** i

    en = time.time_ns()

    print(f'Pratt building: {(en - st) // 10 ** 6} milliseconds')

    return list(sorted(elements))[2:]


empiric_marcin_ciura_seq = [1, 4, 10, 23, 57, 132, 301, 701, 1750]


# best for arrays with length less than 4 * 10 ** 3
def find_shell_elements_marcin_ciura(n: int):
    elements = [el for el in empiric_marcin_ciura_seq if el < n]
    return elements


def find_shell_elements_insertion(n: int):
    return [_ for _ in range(1, n)]


def find_shell_elements_fibonacci(n: int):
    elements = []
    prev_fib, next_fib = 0, 1
    while prev_fib < n:
        elements.append(prev_fib)
        prev_fib, next_fib = next_fib, prev_fib + next_fib
    return elements


def find_shell_elements_locus_lontrime(n: int):
    golden_ratio = (1.0 + math.sqrt(5)) / 2
    elements = []
    sequence_element = n // golden_ratio
    while sequence_element >= 1:
        elements = [int(sequence_element)] + elements
        sequence_element //= golden_ratio
    return elements


sequences = {0: find_shell_simple_elements, 1: find_shell_elements_hibbard, 2: find_shell_elements_knuth,
             3: find_shell_elements_pratt, 4: find_shell_elements_marcin_ciura, 5: find_shell_elements_insertion,
             6: find_shell_elements_locus_lontrime, 7: find_shell_elements_fibonacci}
names = {0: 'Simple', 1: 'Hibbard', 2: 'Knuth', 3: 'Pratt', 4: 'Marcin Ciura', 5: 'Insertion-sort', 6: 'Locus Lontrime', 7: 'Fibonacci'}


# improved variations of insertion sort:
def shell_sort(array: list[int], seq: int):
    sorted_array = array.copy()

    if seq not in [0, 1, 2, 3, 4, 5, 6, 7]:
        print(f'Please choose natural number from 1 to 3')
        return

    steps_counter = 0
    length = len(sorted_array)
    shell_sequence = sequences[seq](length)
    print(f'shell sequence formed: {shell_sequence}')

    for k in range(len(shell_sequence) - 1, -1, -1):
        distance = shell_sequence[k]
        for i in range(distance, length):
            current_value = sorted_array[i]
            j = i - distance
            while j >= 0 and sorted_array[j] > current_value:
                sorted_array[j + distance] = sorted_array[j]
                j -= distance
                steps_counter += 1
            sorted_array[j + distance] = current_value

    print(f'Shell sort with {names[seq]} sequence has made: {steps_counter} steps')
    return sorted_array


# print(find_shell_simple_elements(100))
# print(find_shell_elements_hibbard(1000))
# print(find_shell_elements_knuth(1000))
# print(find_shell_elements_pratt(10000))

arr = [1, 1, 11, 1, 0, -1, 1, 9, 98, 7, 77, 6, 5, 4, 3, 2, 1, -1, -11, -111, 989, 98, 99, 97, 96, 0, 1, 11111, 9898989, 98989]
larger_array = [int(1000 * (random() - random())) for _ in range(1000 * 1000)]

for ind in range(5 + 1 + 1 + 1):
    if ind != 5:
        start = time.time_ns()
        print(f'{ind + 1}-th TEST:')
        shell_sort(larger_array, ind)
        end = time.time_ns()
        print(f'time elapsed: {(end - start) // 10 ** 6} milliseconds')

# print(f'Loc seq: {find_shell_elements_locus_lontrime(1000)}')
print(f'Fibonacci: {find_shell_elements_fibonacci(1000)}')



