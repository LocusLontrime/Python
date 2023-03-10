# Создать функцию, которая из списка чисел возвращает число, являющее суммой двух или нескольких других элементов, либо возвращающее None, если такого числа нет.
import time
from functools import reduce


# gets all the partitions of initial array, counts diff indexes as diff values (special condition)
def get_list_partitions(elements: list) -> list:
    partitions = []

    def recursive_seeker(curr_elements_in_sequence: list, prev_index: int):
        # base cases
        if len(curr_elements_in_sequence) <= len(elements):
            partitions.append(curr_elements_in_sequence)
        else:
            return
        # body of recursion
        for i in range(prev_index + 1, len(elements)):
            temporal_list = curr_elements_in_sequence.copy()
            temporal_list.append(elements[i])
            # recurrent relation
            recursive_seeker(temporal_list, i)
            # backtracking is not necessary here coz of copying elements list
    recursive_seeker([], -1)
    print(f'partitions count: {len(partitions)}')
    return partitions


# get the numbers needed if they exist or None if not
def get_sums(elements: list) -> list or None:
    partitions = get_list_partitions(elements)  # here we get all the partitions
    result_list = []
    for partition in partitions:
        if len(partition) >= 2:
            curr_partition_sum = sum(partition)  # checking of the main condition for sum
            if curr_partition_sum in elements:  # creating a list of possible representations of numbers located in the array given if such exist
                result_list.append(f'{curr_partition_sum} = {reduce(lambda x, y: str(x) + " + " + str(y), partition)}')
    return result_list if len(result_list) else None


print(get_list_partitions([1, 2, 3]))
print(get_list_partitions([1, 2, 3, 4, 5]))
print(get_list_partitions([1, 2, 3, 4, 5, 6, 7, 8, 9]))

get_list_partitions([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

print(get_sums([5, 6, 7]))  # answer is None

tic = time.perf_counter()
print(get_sums([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]))  # there are many answers
# get_list_partitions([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
toc = time.perf_counter()
print(f"Time elapsed: {toc - tic:0.4f} seconds")
