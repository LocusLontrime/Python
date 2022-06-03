# Единичная дробь имеет 1 в числителе. Десятичные представления единичных дробей со знаменателями от 2 до 10 даны ниже:
#
# 1/2=0.5
# 1/3=0.(3)
# 1/4=0.25
# 1/5=0.2
# 1/6=0.1(6)
# 1/7=0.(142857)
# 1/8=0.125
# 1/9=0.(1)
# 1/10=0.1
# Где 0.1(6) значит 0.166666..., и имеет повторяющуюся последовательность из одной цифры. Заметим, что 1/7 имеет повторяющуюся последовательность из 6 цифр.
# Найдите значение d < 1000, для которого 1/d в десятичном виде содержит самую длинную повторяющуюся последовательность цифр.

def get_value(border: int) -> (int, int):
    max_length = 1
    best_d = 1

    for d in range(3, border):
        if d % 2 != 0 and d % 5 != 0:
            curr_length = get_periodic_length(d)
            if max_length < curr_length:
                max_length = curr_length
                best_d = d
            print(f'd = {d}, curr_cycling_length = {curr_length}')
    return best_d, max_length


def get_periodic_length(n) -> int:
    currVal = 1

    iterator = 0
    while True:
        iterator += 1
        currVal = (currVal * 10) % n
        if currVal == 1:
            break

    return iterator


# print(get_periodic_length(23))

print(f'Best d and relative length: {get_value(1000)}')

