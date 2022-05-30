# Вот вам файл с тысячей чисел. https://cloud.mail.ru/public/DQgN/LqoQzPEec
# Задача: найти триплеты и просто выводить их на экран. Триплетом называются три числа,
# которые в сумме дают 0. (решение будет долгим, ибо является демонстрационным при теме многопоточного программирования).
import time

def get_pairs(elements: list, target: int) -> set:  # runtime -> O(n)
    set_elements = set(elements)
    distinct_elements = set()
    for set_element in set_elements:
        if target - set_element in set_elements:
            if target - set_element not in distinct_elements:
                distinct_elements.add(set_element)
    return distinct_elements


def get_triplets(elements: list) -> list:
    triplets = []
    for i in range(len(elements)):
        curr_set = get_pairs(elements[i + 1:], -elements[i])
        for pair in curr_set:
            if elements[i] != pair != -elements[i] - pair:
                triplets.append((elements[i], pair, -elements[i] - pair))
    return triplets


def get_triplets_from_file(file_path: str) -> list:
    with open(file_path, "r") as file:
        numbers_str_list = file.readlines()
        numbers_int_list = [int(i) for i in numbers_str_list]
        return get_triplets(numbers_int_list)


tic = time.perf_counter()
print(get_triplets_from_file('1000_of_numbers.txt'))
toc = time.perf_counter()
print(f"Time elapsed: {toc - tic:0.4f} seconds")