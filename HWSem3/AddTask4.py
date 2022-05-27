# Сумма квадратов первых десяти натуральных чисел равна
# 12 + 22 + ... + 102 = 385
# Квадрат суммы первых десяти натуральных чисел равен
# (1 + 2 + ... + 10)2 = 552 = 3025
# Следовательно, разность между суммой квадратов и квадратом суммы первых десяти натуральных чисел составляет 3025 − 385 = 2640.
# Найдите разность между суммой квадратов и квадратом суммы первых ста натуральных чисел.

def get_diff(n):  # a mega-slow one
    def get_list(n):
        list = []
        for i in range(1, n + 1):
            list.append(i)
        return list
    elements = get_list(n)
    diff = 0
    for i in range(0, len(elements)):
        for j in range(i + 1, len(elements)):
            diff += 2 * elements[i] * elements[j]
    return diff


def get_diff_alt(n):  # a super-ultra-fast one
    diff = n * (n + 1) / 2
    diff *= (n * n / 2 - (n + 2) / 6)
    return diff


# print(get_diff(100000))
print(get_diff_alt(100000))


