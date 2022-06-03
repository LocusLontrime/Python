# Чисто для тренировки новый функций, ничего сложного. Создайте два списка — один с названиями языков программирования,
# другой — с числами от 1 до длины первого плюс 1. Вам нужно сделать две функции: первая из которых создаст список кортежей,
# состоящих из номера и языка, написанного большими буквами. Вторая — которая отфильтрует этот список следующим образом:
# если сумма очков слова имеет в делителях номер, с которым она в паре в кортеже, то кортеж остается, его номер заменяется
# на сумму очков. Если нет — удаляется. Суммой очков называется сложение порядковых номеров букв в слове. Порядковые номера смотрите в этой таблице,
# в третьем столбце: https://www.charset.org/utf-8
# Это — 16-ричная система, поищите, как правильнее и быстрее получать эти символы. С помощью reduce сложите получившиеся числа и верните из функции в качестве ответа.
from functools import reduce


def get_sum():
    programming_languages = ['Java', 'C', 'C#', 'C++', 'Kotlin', 'Python', 'Ruby', 'JavaScript', 'TypeScript', 'Swift']
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # what for +1?..

    new_list = [(i, programming_languages[i - 1].upper()) for i in numbers if i <= len(programming_languages)]
    uber_new_list = [(reduce(lambda x, y: x + ord(y), i[1], 0), i[1]) for i in new_list if reduce(lambda x, y: x + ord(y), i[1], 0) % i[0] == 0]

    print(new_list)
    print(uber_new_list)

    return reduce(lambda x, y: x + y[0], uber_new_list, 0)


print(get_sum())


# just a funny code in Python:
programming_languages = ['Java', 'C', 'C#', 'C++', 'Kotlin', 'Python', 'Ruby', 'JavaScript', 'TypeScript', 'Swift']
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # what for +1?..


def get_sum_alt():
    return reduce(lambda x, y: x + y[0], [(reduce(lambda x, y: x + ord(y), i[1], 0), i[1]) for i in [(i, programming_languages[i - 1].upper()) for i in numbers if i <= len(programming_languages)] if reduce(lambda x, y: x + ord(y), i[1], 0) % i[0] == 0], 0)


print(get_sum_alt())

