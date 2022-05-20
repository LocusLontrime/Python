def get_first_n_members_of_seq(length):  # Сформировать список из N членов последовательности. Для N = 5: 1, -3, 9, -27, 81 и т.д.
    list = []
    pow = 1

    for i in range(0, length):
        list.append(pow)
        pow *= -3

    return list


def count_overlapping_substrings(s1, s2):  # Пользователь вводит две строки, определить количество вхождений одной строки s2 в другую s1
    counter = 0
    i = -1
    while True:
        i = s1.find(s2, i + 1)
        if i == -1:
            return counter
        counter += 1


def get_factorial_list(length):  # Сформировать программу, получающую набр произведений чисел от 1 до N. Для N = 4: [1, 2, 6, 24]
    list = []
    curr_fact = 1

    for i in range(1, length + 1):
        curr_fact *= i
        list.append(curr_fact)

    return list


def get_digit_sum(number):  # Посчитать сумму цифр в вещественном числе
    while (number % 1 != 0):
        number *= 10

    sum = 0

    while (number > 0):
        sum += number % 10
        number //= 10

    return sum


print(count_overlapping_substrings('avarnikabcdefabcdefabc', 'abcdefabc')) # an example for 1st task

print('avarnikabcdefabcdefabc'.count('abcdefabc'))
# -> 6

print(get_first_n_members_of_seq(8))  # an example for 2nd task

print(get_factorial_list(9))  # an example for 3rd task

print(get_digit_sum(0.123))  # an example for 4th task
