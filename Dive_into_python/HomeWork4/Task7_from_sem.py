# -*- coding: utf-8 -*-


# Task7. Функция получает на вход словарь с названием компании в качестве ключа
# и списком с доходами и расходами (3-10 чисел) в качестве значения.
# Вычислите итоговую прибыль или убыток каждой компании. Если все компании
# прибыльные, верните истину, а если хотя бы одна убыточная — ложь.


pnl = {
    'Neuro.net': [100_000, 125_000, -7_000_000, -61_000_000, 1_000_000_000],
    'AmberCorp': [1_000_000_000_000, -17_000_000_000, -1_500_000_000, 98_000_000],
    "Askold'n'Lensdorf": [1_000, 2_500, 100, 500, -200_000, -2_000_000, 5_000_000, 6_000_000],
    'TV_reality_dom2': [1_000_000, 5_000_000, -1_000_000_000]
}


# checks if all the companies of the given pool are profitable:
def is_profitable(companies_pnl: dict):  # TODO: what about 3-10 nums?
    return all([sum(val) >= 0 for val in companies_pnl.values()])


print(f'is profitable: {is_profitable(pnl)}')


