# Дана последовательность чисел. Получить список неповторяющихся элементов исходной последовательности
# Пример: [1, 2, 3, 5, 1, 5, 3, 10] => [1, 2, 3, 5, 10]

list_of_elements = [1, 2, 3, 5, 1, 5, 3, 10]


def remove_repeating_elements(elements):
    set_of_elements = set()
    for element in elements:
        set_of_elements.add(element)
    return set_of_elements


print(remove_repeating_elements(list_of_elements))
