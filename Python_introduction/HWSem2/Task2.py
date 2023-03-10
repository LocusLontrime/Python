# Найти произведение пар чисел в списке. Парой считаем первый и последний элемент, второй и предпоследний и т.д.
# Пример: [2, 3, 4, 5, 6] => [12, 15, 16]; [2, 3, 5, 6] => [12, 15]

def get_product(numbers_list):
    """
    :param numbers_list: numbers
    :return: list of products of following elements: first * last, second * one before last and so on...
    """
    left, right, product, prod_list = 0, len(numbers_list) - 1, 0, []  # two-pointers approach
    while left <= right:  # stop conditional
        product = numbers_list[left] * numbers_list[right]
        prod_list.append(product)
        left += 1  # pointers walking
        right -= 1
    return prod_list


print(get_product([2, 3, 4, 5, 6]))
print(get_product([2, 3, 5, 6]))