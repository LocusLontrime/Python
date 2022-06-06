import random


def get_num():
    return random.randint(1, 100)


def buy_goods():
    pass


k = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
m = 98.98
str_s = 'Lena'

k += 1

list_of_nums = [1, 2, 3, 4, 5]
list_of_nums.append(1)
list_of_nums.append(9)


set_of_numbers = set()
set_of_numbers.add(1)
set_of_numbers.add(2)
set_of_numbers.add(1)


dictionary_of_numbers = {'A': 1, 'B': 2, 'C': 3}

print(list_of_nums)
print(set_of_numbers)
print(dictionary_of_numbers)

print(dictionary_of_numbers['A'])
print(dictionary_of_numbers.keys())

# print(k)
#
# print(get_num())
# print(buy_goods())

# Task1
# Есть список a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
# Выведите все элементы, которые меньше 5

a_list = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]


def print_less_than_5(some_list: list) -> None:
    for element in some_list:
        if element < 5:
            print(element, end=' ')
        else:
            print()
            break


print_less_than_5(a_list)


# Task2
# a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89];
# b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13].
# Нужно вернуть список, который состоит из элементов, общих для этих двух списков

a_l = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b_l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


def get_common_elements(list_1: list, list_2: list) -> set:
    set_res = set()

    for element in list_1:
        if element in list_2:
            set_res.add(element)

    return set_res


print(get_common_elements(a_l, b_l))

# get_common_elements(98, 'xxxxxxxxxxx')


# Task3

# Напишите программу, в которой рассчитывается сумма и произведение цифр положительного трёхзначного числа

def print_sum_and_product(three_digit_number: int) -> None:
    if 100 <= three_digit_number <= 999:
        digit_3 = three_digit_number % 10
        three_digit_number //= 10
        digit_2 = three_digit_number % 10
        three_digit_number //= 10
        digit_1 = three_digit_number

        print(f'sum: {digit_1 + digit_2 + digit_3}')
        print(f'product: {digit_1 * digit_2 * digit_3}')

    else:
        print('The number is not a three-digit one!!!')


print(print_sum_and_product(989))
