# Найти сумму чисел списка стоящих на нечетной позиции (Locus_Lontrime HW)

def get_sum(numbers_list):
    """
    :param numbers_list: numbers
    :return: sum of elements with odd indexes
    """
    sum = 0
    for i in range(0, len(numbers_list), 2):
        sum += numbers_list[i]
    return sum


print(get_sum([1, 2, 3, 4, 5, 6, 7, 8, 9]))
