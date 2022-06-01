# Дан список чисел. Создать список в который попадают числа, описывающие возрастающую последовательность и содержащие максимальное количество элементов.
# Пример: [1, 5, 2, 3, 4, 6, 1, 7] => [1, 2, 3, 4, 6, 7]
# [5, 2, 3, 4, 6, 1, 7] => [2, 3, 4, 6, 7]
# Порядок элементов менять нельзя

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
    print('LIS: ', end='')
    return result


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
