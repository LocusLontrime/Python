# Написать программу преобразования десятичного числа в двоичное

def dec_to_bin(dec_number):
    """
    :param dec_number: a number in dec representation
    :return: bin representation of the dec number given
    """
    if dec_number == 0:
        return 0
    if dec_number % 2 == 0:
        return 0 + 10 * dec_to_bin(dec_number // 2)
    else:
        return 1 + 10 * dec_to_bin(dec_number // 2)


f = lambda dec_number: 0 if dec_number == 0 else f(dec_number // 2) * 10 + (0 if dec_number % 2 == 0 else 1)  # just a way to solve

print(dec_to_bin(98))
print(f(98))
