# accepted on codewars.com
from collections import OrderedDict


def to_roman(val):
    roman_dict = OrderedDict()
    roman_dict[1000] = "M"
    roman_dict[900] = "CM"
    roman_dict[500] = "D"
    roman_dict[400] = "CD"
    roman_dict[100] = "C"
    roman_dict[90] = "XC"
    roman_dict[50] = "L"
    roman_dict[40] = "XL"
    roman_dict[10] = "X"
    roman_dict[9] = "IX"
    roman_dict[5] = "V"
    roman_dict[4] = "IV"
    roman_dict[1] = "I"

    def roman_num(num):
        for roman_key in roman_dict.keys():
            x, y = num // roman_key, num % roman_key
            yield roman_dict[roman_key] * x  # generates a roman symbols
            num -= (roman_key * x)
            if num <= 0:
                break

    return "".join([i for i in roman_num(val)])


def from_roman(roman_num):
    roman_symbols_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    for index in range(len(roman_num) - 1, 0, -1):
        flag = roman_symbols_dict[roman_num[index]] <= roman_symbols_dict[roman_num[index - 1]]
        result += (1 if flag else -1) * roman_symbols_dict[roman_num[index - 1]]
    return result + roman_symbols_dict[roman_num[len(roman_num) - 1]]


print(from_roman('MDCLXVI'))


print(to_roman(1666))
print(to_roman(4))
print(to_roman(98))

