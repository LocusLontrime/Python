# -*- coding: utf-8 -*-

# 1. Дан список повторяющихся элементов. Вернуть список с дублирующимися элементами. В результирующем списке не должно быть дубликатов.


repeated_elements = [1, 1, 2, 3, 0, 1, 11, 98, 98, 89, 101, 989, 1, 0, 0, 8, 88, 8, 98, 9, 989]


def get_duplicates(elements: list):
    unique_elements, dups = set(), set()
    for element in elements:
        if element in unique_elements:
            dups.add(element)
        unique_elements.add(element)
    return list(dups)


print(f'dups: {get_duplicates(repeated_elements)}')

