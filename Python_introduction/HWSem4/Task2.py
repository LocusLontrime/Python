# Дан список чисел. Создать список в который попадают числа, описывающие возрастающую последовательность и содержащие максимальное количество элементов.
# Пример: [1, 5, 2, 3, 4, 6, 1, 7] => [1, 2, 3, 4, 6, 7]
# [5, 2, 3, 4, 6, 1, 7] => [2, 3, 4, 6, 7]
# Порядок элементов менять нельзя

# dynamic programming with memoization: runtime O(n^2), memory using: O(n)
from math import ceil


def dyn_prog(elements: list) -> list:
    dp = [0] * (len(elements) + 1)  # memoization
    best_indexes = [0] * (len(elements) + 1)  # best indexes list

    def rec_seeker(index: int) -> int:
        # border case:
        if index == -1:
            return 0

        #recurrent relation
        if index == len(elements) or dp[index] == 0:
            max_length = 0
            best_ind = -1
            for inner_index in range(index):
                if index == len(elements) or elements[inner_index] < elements[index]:
                    rec_sec_val = rec_seeker(inner_index) + 1
                    if max_length < rec_sec_val:
                        max_length = rec_sec_val
                        best_ind = inner_index

            # here we save the new calculated values of dp and best index
            dp[index] = max_length
            best_indexes[index] = best_ind

        return dp[index]

    rec_seeker(len(elements))

    # back motion to capture the right numbers
    result = []  # resulting LIS
    ind = len(elements)
    while True:
        ind = best_indexes[ind]  # the best way's steps -> here we get the longest increasing subsequence char by char
        if ind != -1:
            result.insert(0, str(elements[ind]))
        else:
            break

    return result


print(dyn_prog([1, 5, 2, 3, 4, 6, 1, 7]))
print(dyn_prog([5, 2, 3, 4, 6, 1, 7]))
print(dyn_prog([1, 1, 1, 1, 1, 5, 2, 1, 3, 4, 6, 1, 2, 2, 7]))


# Линеаритмическое решение с построением LIS, runtime: O(N*log(N))
def get_longest_increasing_subsequence(elements: list) -> list:  # Runtime O(n*log(n)), where n = len(elements)
    list_of_min_indexes = [0] * (len(elements) + 1)
    prev_indexes_list = []  # to build the consecutive LIS
    max_length = 0

    print('Building of the longest increasing subsequence (LIS):')
    for i in range(len(elements)):

        leftPointer = 1
        rightPointer = max_length

        expected_index = bin_search(leftPointer, rightPointer, elements[i], elements, list_of_min_indexes)  # expected place of element in the resulting set

        prev_indexes_list.append(list_of_min_indexes[expected_index - 1])
        list_of_min_indexes[expected_index] = i

        if expected_index > max_length:
            max_length = expected_index

    print(f'Length of LIS = {max_length}')
    print(f'list_of_min_indexes = {list_of_min_indexes}')
    print(f'prev_indexes_list = {prev_indexes_list}')

    index = list_of_min_indexes[max_length]

    longest_increasing_subsequence = []

    for iterator in range(max_length):
        longest_increasing_subsequence.append(elements[index])
        index = prev_indexes_list[index]

    longest_increasing_subsequence.reverse()

    return longest_increasing_subsequence


# Binary search of position the current element to be located at
def bin_search(left_border: int, right_border: int, target: int, elems: list, min_list: list) -> int:
    if right_border < left_border:  # border case -> intersection
        return left_border

    pivot_index = (left_border + right_border) // 2 + (1 if (left_border + right_border) % 2 != 0 else 0)  # median index, rounded to the nearest integer
    if elems[min_list[pivot_index]] < target:  # here we decide in which part of current interval the target should be distributed
        return bin_search(pivot_index + 1, right_border, target, elems, min_list)
    else:
        return bin_search(left_border, pivot_index - 1, target, elems, min_list)


print(get_longest_increasing_subsequence([1, 5, 2, 3, 4, 6, 1, 7]))
print(get_longest_increasing_subsequence([5, 2, 3, 4, 6, 1, 7]))
print(get_longest_increasing_subsequence([9, 8, 7, 8, 9, 1, 1, 1, 4, 3, 2, 7, 1, 2, 3, 5, 6, 7, 8, 9, 1, 2, 3, 6, 9]))
