# Посчитать сумму цифр в вещественном числе

def get_digit_sum(number):
    while number % 1 != 0:
        number *= 10
    print(f'number = {number}')

    sum = 0

    while number > 0:
        sum += number % 10
        number //= 10

    return sum


print(get_digit_sum(987.123))  # an example for 4th task
