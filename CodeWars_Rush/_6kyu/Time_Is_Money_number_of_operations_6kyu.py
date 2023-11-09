# accepted on codewars.com


def operations(number):
    return int(number.bit_length()) + number.bit_count() - 1


print(f'ops: {operations(12)}')



