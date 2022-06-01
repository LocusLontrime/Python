# Дан список чисел. Создать список, в который попадают числа, описываемые возрастающую последовательность.
# Пример: [1, 5, 2, 3, 4, 6, 1, 7] => [1, 2, 3] или [1, 7] или [1, 6, 7] и т.д. Порядок элементов менять нельзя

def get_all_increasing_partitions(elements: list) -> list:
    partitions = []

    def recursive_seeker(curr_elements_in_sequence: list, prev_index: int):
        # base cases
        if len(curr_elements_in_sequence) <= len(elements):
            partitions.append(curr_elements_in_sequence)
        else:
            return
        # body of recursion
        for i in range(prev_index + 1, len(elements)):
            if elements[prev_index] < elements[i] or prev_index == -1:
                temporal_list = curr_elements_in_sequence.copy()
                temporal_list.append(elements[i])
                # recurrent relation
                recursive_seeker(temporal_list, i)
                # backtracking is not necessary here coz of copying elements list
    recursive_seeker([], -1)
    print(f'partitions count: {len(partitions)}')
    return partitions


print(get_all_increasing_partitions([1, 5, 2, 3, 4, 6, 1, 7]))
