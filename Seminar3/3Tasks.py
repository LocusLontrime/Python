#  Task1
import random
from typing import List
from functools import reduce


def get_multiplication(n):  # 36 366 98 989
    mult = 1
    def get_list(n):
        list = []
        for i in range(n):
            list.append(random.randint(-n, n + 1))
        return list
    with open("Values.txt", "w") as file:
        length = random.randint(1, n + 1)
        list = get_list(n)
        for i in range(length):
            file.write(str(random.randint(0, n)) + "\n")
    with open("Values.txt", "r") as file:
        lines = file.readlines()
        for i in lines:
            curr_coeff = int(i.split('\n')[0])
            mult *= curr_coeff
            print(f'beem multiplied by: {curr_coeff}')
    return mult


print(get_multiplication(10))


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


def max_min_array(elements):
    if len(elements) != 0:
        max_element = elements[0]
        min_element = elements[0]
        for i in elements:
            if i < min_element:
                min_element = i
            if i > max_element:
                max_element = i
        print(f'max = {max_element}, min = {min_element}')
    else:
        print('length of elements is equal to ZERO')


max_min_array([1, 4, 98, 7, 98, -999, 999])


def try_it(list:List, name:str) -> int:
    l = len(list)
    print(name)
    return 'sss'


try_it(98, 99)