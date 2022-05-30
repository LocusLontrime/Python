import time
from functools import reduce


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


def get_sums(elements: list) -> None:
    partitions = get_list_partitions(elements)

    for partition in partitions:
        curr_partition_sum = sum(partition)
        if curr_partition_sum in elements:
            print(f'element {curr_partition_sum} = {reduce(lambda x, y: str(x) + " + " + str(y), partition)}')


print(get_list_partitions([1, 2, 3]))
print(get_list_partitions([1, 2, 3, 4, 5]))
print(get_list_partitions([1, 2, 3, 4, 5, 6, 7, 8, 9]))
get_list_partitions([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

tic = time.perf_counter()


get_sums([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

# get_list_partitions([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
toc = time.perf_counter()
print(f"Time elapsed: {toc - tic:0.4f} seconds")
