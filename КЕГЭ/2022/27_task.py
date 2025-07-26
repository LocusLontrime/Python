# -*- coding: utf-8 -*-
import math


# На кольцевой дороге с двусторонним движением установлены магазины для продажи яблок.
# Все магазины находятся на расстоянии 1 километра друг от друга.
# Специальные роботы доставщики развозят яблоки со склада по этим магазинам.
# Длина кольцевой дороги равна N километров. Нулевой километр и N-й километр автодороги находятся в одной точке.
# Известно количество килограмм яблок, которое необходимо ежедневно доставлять в каждый из магазинов.
# Для каждого пункта яблоки возит отдельный робот доставщик.
# Стоимость доставки яблок вычисляется как произведение количества яблок (в килограммах) на расстояние от склада до магазина.
# Склад открыли в одном из магазинов таким образом, чтобы общая стоимость доставки яблок во все магазины была минимальной.

# Определите минимальные расходы на доставку яблок в магазины

# Входные данные

# Дано два входных файла (файл A и файл B),
# каждый из которых в первой строке содержит число N (1 ≤ N ≤ 10 000 000) – количество магазинов на кольцевой дороге.
# В каждой из следующих N строк находится число – количество килограмм яблок,
# необходимых для доставки в магазин (все числа натуральные, количество килограмм не превышает 1000).
# Числа указаны в порядке расположения магазинов на дороге, начиная с первого километра.

# В ответе укажите два числа: сначала значение искомой величины для файла А, затем – для файла B.

# Algorithm's runtime -> O(n), memory usage -> O(n) both linear.


def compute_min_costs(shops: list[int]):
    # n of shops"
    n = len(shops)
    print(f'{n = }')
    # let us check every shop spot for possibility of placing the min costs warehouse
    # (firstly, the shop under the index of 0 and then clockwise):
    ind_ = 0
    # minimal costs:
    min_costs = math.inf
    # left sum (_sum) and right one (sum_) -> sums of apples amount needed for the left half of shops and the right one relatively:
    _sum = sum(l_shops := shops[0:n // 2])
    sum_ = sum(r_shops := shops[n // 2:])
    # initial costs (at the shop of 0 ind):
    l_costs = sum(i * apple_amount for i, apple_amount in enumerate(l_shops))
    r_costs = sum((len(r_shops) - i) * apple_amount for i, apple_amount in enumerate(r_shops))
    costs = l_costs + r_costs
    # the core cycle of clockwise moving the current shop:
    while ind_ < n:
        # check for min_costs:
        # print(f'{ind_ }[{shops[ind_]}] -> {costs = }')
        min_costs = min(min_costs, costs)
        # spinning:
        # 1. left and right sums changing:
        _sum += shops[(ind_ + n // 2) % n] - shops[ind_]
        sum_ -= shops[(ind_ + n // 2) % n] - shops[ind_]
        # 2. costs changing:
        costs += sum_ - _sum
        # next step:
        ind_ += 1
    # returns the min_costs found:
    return min_costs


test_ex = [8, 20, 5, 13, 7, 19]

print(f'min_costs -> {compute_min_costs(test_ex)}')
print(f'res: {eval(f"1 * 7 + 0 * 19 + 1 * 8 + 2 * 20 + 3 * 5 + 2 * 13")}')
