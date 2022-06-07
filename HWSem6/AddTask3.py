# Пятиугольные числа вычисляются по формуле: Pn=n(3n−1)/2. Первые десять пятиугольных чисел:
# 1, 5, 12, 22, 35, 51, 70, 92, 117, 145, ...
# Можно убедиться в том, что P4 + P7 = 22 + 70 = 92 = P8. Однако, их разность, 70 − 22 = 48, не является пятиугольным числом.
# Найдите пару пятиугольных чисел Pj и Pk, для которых сумма и разность являются пятиугольными числами и значение
# D = |Pk− Pj| минимально, и дайте значение D в качестве ответа.
import math


def is_pentagonal(number):
    expr = math.sqrt(1 + 24 * number)
    return (expr + 1) % 6 == 0


def min_delta():
    pentagonal_numbers = [1, 5]
    pent_num = 5

    for n in range(7, 6500, 3):
        pent_num += n
        pentagonal_numbers.append(pent_num)

        for pentagonal_one in pentagonal_numbers:

            if is_pentagonal(pent_num + pentagonal_one) and is_pentagonal(pent_num - pentagonal_one):
                print(f'pent num1 = {pent_num}, pent num2 = {pentagonal_one}')
                return pent_num - pentagonal_one


print(f'min Delta = {min_delta()}')
