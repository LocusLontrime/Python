# 1. Написать программу преобразования двоичного числа в десятичное.

def bin_to_dec(bin_number):
    """
    :param bin_number: a number in bin representation
    :return: dec representation of the bin number given
    """
    if bin_number == 0:
        return 0
    if bin_number % 10 == 1:
        return bin_to_dec(bin_number // 10) * 2 + 1
    else:
        return bin_to_dec(bin_number // 10) * 2


k = lambda bin_number: 0 if bin_number == 0 else bin_to_dec(bin_number // 10) * 2 + (1 if bin_number % 10 == 1 else 0)  # just a way to solve

print(bin_to_dec(1100010))
print(k(1100010))

