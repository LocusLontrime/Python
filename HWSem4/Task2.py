# Дан список чисел. Создать список в который попадают числа, описывающие возрастающую последовательность и содержащие максимальное количество элементов.
# Пример: [1, 5, 2, 3, 4, 6, 1, 7] => [1, 2, 3, 4, 6, 7]
# [5, 2, 3, 4, 6, 1, 7] => [2, 3, 4, 6, 7]
# Порядок элементов менять нельзя

# dynamic programming with memoization: runtime O(n^2), memory using: O(n)
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

            dp[index] = max_length
            best_indexes[index] = best_ind

        return dp[index]

    rec_seeker(len(elements))

    # back motion to capture the right numbers
    result = []
    ind = len(elements)
    while True:
        ind = best_indexes[ind]
        if ind != -1:
            result.insert(0, str(elements[ind]))
        else:
            break

    return result


print(dyn_prog([1, 5, 2, 3, 4, 6, 1, 7]))
print(dyn_prog([5, 2, 3, 4, 6, 1, 7]))
print(dyn_prog([1, 1, 1, 1, 1, 5, 2, 1, 3, 4, 6, 1, 2, 2, 7]))


# СВЕРХ БЫСТРОЕ решенике для нахождения ДЛИННЫ LIS, НЕ ГАРАНТИРУЕТ верную последовательность, НО ВЗАМЕН ГАРАНТИРУЕТ верную длинну, скорость: O(N*log(N))
def get_longest_increasing_subsequence(elements: list) -> list:  # Runtime O(n*log(n)), where n = len(elements)
    result = []
    print('Building of the longest increasing subsequence (LIS):')
    for i in range(len(elements)):
        expected_index = bin_search(0, len(result) - 1, elements[i], result)  # expected place of element in the resulting set
        if expected_index == len(result):  # if the elements lies outside of current set
            result.append(elements[i])
        else:  # inside case -> we change the greater element by the less one at th position found with the binary search above
            result[expected_index] = elements[i]
        print(f'index = {i}, el[i] = {elements[i]}, expected index = {expected_index}, res: {result}')
    print(f'The quick length of LIS = {len(result)}')
    print('outcome pseudo-LIS: ', end='')
    return result


# Binary search of position the current element to be located at
def bin_search(left_border: int, right_border: int, target: int, elems: list) -> int:
    if right_border == -1:  # border case -> when there is no elements in elems list
        return 0

    if left_border == right_border:  # ending case -> the searching is finished
        return left_border + (1 if target > elems[left_border] else 0)  # the element is not found, and consequently it can be located inside the set or outside
    pivot_index = (left_border + right_border) // 2  # median index
    if elems[pivot_index] < target:  # here we decide in which part of current interval the target should be distributed
        return bin_search(pivot_index + 1, right_border, target, elems)
    elif elems[pivot_index] > target:
        return bin_search(left_border, pivot_index, target, elems)
    else:
        return pivot_index  # the case of finding the target amongst the elements given


print(get_longest_increasing_subsequence([1, 5, 2, 3, 4, 6, 1, 7]))
print(get_longest_increasing_subsequence([5, 2, 3, 4, 6, 1, 7]))
