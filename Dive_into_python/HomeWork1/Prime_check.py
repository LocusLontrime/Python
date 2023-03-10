# Task 2.
# Ќапишите код, который запрашивает число и сообщает €вл€етс€ ли оно простым или составным.
# »спользуйте правило дл€ проверки: У„исло €вл€етс€ простым, если делитс€ нацело только на единицу и на себ€Ф.
# —делайте ограничение на ввод отрицательных чисел и чисел больше 100 тыс€ч.


import math


def is_prime(number: int):
    if number < 0 or number > 100_000:
        raise ValueError(f'the number is negative or too large (>100000)')
    # base cases:
    if number in [0, 1]:
        return False, f'0 and 1 are not prime numbers...'
    # main cycle-check:
    for i in range(2, int(math.sqrt(number))):
        if number % i == 0:
            return False, f'divisor found: {i}'
    return True, f'no divisor found'


# print(f'{int(math.sqrt(7))}')

num1 = 107
print(f'Is {num1} prime? -->> {is_prime(num1)}')

num2 = 1000
print(f'Is {num2} prime? -->> {is_prime(num2)}')

