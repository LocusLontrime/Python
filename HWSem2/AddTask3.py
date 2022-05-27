# 3.Каждый следующий элемент ряда Фибоначчи получается при сложении двух предыдущих. Начиная с 1 и 2, первые 10 элементов будут:
# 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

def get_fib_list(n):
    """
    :param n: the length of the one wing of a fibs_list being built
    :return: list of fib numbers from -n to n
    """
    f1, f2, fibs_list = 1, 0, [0]
    for i in range(0, n):
        f2 = f2 + f1  # a next fib
        f1 = f2 - f1  # one before next
        fibs_list.append(f2)
        fibs_list.insert(0, f2 if i % 2 == 0 else -f2)  # building of the negative-wing of a fibs_list
    return fibs_list


print(get_fib_list(15))
