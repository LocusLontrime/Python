# В заданном списке вещественных чисел найдите разницу между максимальным и минимальным значением дробной части элементов.
# Пример: [1.1, 1.2, 3.1, 5, 10.01] => 0.19

def get_diff(numbers_list):
    """
    :param numbers_list: float numbers
    :return: diff between max and min fractional parts
    """
    max_part = 0  # initial values for max and min vars
    min_part = 1
    for i in numbers_list:
        max_part = max(max_part, i % 1)
        min_part = min(min_part, (1 if i % 1 == 0 else i % 1))  # min fractional part cannot be equal to zero (0.0)
    return max_part - min_part


print(get_diff([1.1, 1.2, 3.1, 5, 10.01]))
