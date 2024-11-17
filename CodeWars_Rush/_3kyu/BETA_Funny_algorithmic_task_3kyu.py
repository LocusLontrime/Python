# accepted on codewars.com

def generator(size, position):

    if position < 1 or position > size ** size:
        return -1

    return translate_to_nary_based_system(position - 1, size) + int('1' * size)


def translate_to_nary_based_system(decimal_num: int, n_base: int) -> int:
    if not decimal_num:
        return 0

    return 10 * translate_to_nary_based_system(decimal_num // n_base, n_base) + decimal_num % n_base


print(f'res: {translate_to_nary_based_system(10, 3)}')


x, y = 7, 200017
print(f'gen({x}, {y}) = {generator(x, y)}')



