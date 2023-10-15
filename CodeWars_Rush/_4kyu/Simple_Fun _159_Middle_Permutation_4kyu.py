#accepted on codewars.com
import math


def middle_permutation(string):

    # just sorting
    sorted_string = sorted(string)
    str_len = len(string)
    result = ''

    # starting factorial (we want to translate the middle num to factorials based numeric system)
    curr_n = str_len - 1
    middle_num = math.factorial(str_len) // 2 - 1  # the middle number

    # translating
    while curr_n > 0:

        # coefficients in the new numeric system
        curr_coeff = middle_num // math.factorial(curr_n)

        # here we get symbols of middle string
        symbol = sorted_string[curr_coeff]
        result += symbol  # building the result
        sorted_string.remove(symbol)  # we need to remove the symbol used from the initial string, because there must be no repeats at all

        # preparing to the next step of cycle!
        middle_num -= curr_coeff * math.factorial(curr_n)
        curr_n -= 1

    return result + sorted_string[0]  # here we add the coefficient at 0! = 1


print(math.factorial(7))
print(middle_permutation('abcdxgz'))
print(middle_permutation('abcdxg'))
print(middle_permutation('abc'))
print(middle_permutation('ab'))
print(middle_permutation('abcdefgjklmop'))
print(middle_permutation('abcd'))


print(middle_permutation('shujlbacefgizpwkxmoqvydrtn'))
