# -*- coding: utf-8 -*-
# Task 2.
# Напишите код, который запрашивает число и сообщает является ли оно простым или составным.
# Используйте правило для проверки: “Число является простым, если делится нацело только на единицу и на себя”.
# Сделайте ограничение на ввод отрицательных чисел и чисел больше 100 тысяч.


import math


def is_prime(number: int):
    """"""
    if number < 0 or number > 100_000:
        raise ValueError(f'the number is negative or too large (>100000)')
    # base cases:
    if number in [0, 1]:
        return False, f'0 and 1 are not prime numbers...'
    # main cycle-check:
    for i in range(2, int(math.sqrt(number))):
        if number % i == 0:
            return False, f'divisor found: {i}'
    return True, f'no divisors found besides 1 and self'


# print(f'{int(math.sqrt(7))}')

num1 = 107
print(f'Is {num1} prime? -->> {is_prime(num1)}')

num2 = 1000
print(f'Is {num2} prime? -->> {is_prime(num2)}')




