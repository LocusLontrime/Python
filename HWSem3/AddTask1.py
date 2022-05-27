# Определите функцию, которая принимает римскую цифру в качестве аргумента и возвращает ее значение
# в виде числового десятичного целого числа. Вам не нужно проверять форму римской цифры.
# Современные римские цифры записываются путем выражения каждой десятичной цифры числа,
# которое должно быть закодировано отдельно, начиная с самой левой цифры. Таким образом,
# 1990 отображается "MCMXC" (1000 = M, 900 = CM, 90 = XC), а 2008 отображается "MMVIII" (2000 = MM, 8 = VIII). 
# Римская цифра для 1666, "MDCLXVI", использует каждую букву в порядке убывания.
# Пример: имя_вашей_функции ('XXI') # должно вернуть 21

def get_dec_from_roman(roman_symbols: str) -> int:
    roman_symbols_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M':1000}
    result = 0
    for index in range(len(roman_symbols) - 1, 0, -1):
        if roman_symbols_dict[roman_symbols[index]] <= roman_symbols_dict[roman_symbols[index - 1]]:
            result += roman_symbols_dict[roman_symbols[index - 1]]
        else:
            result -= roman_symbols_dict[roman_symbols[index - 1]]
    return result + roman_symbols_dict[roman_symbols[len(roman_symbols) - 1]]


print(get_dec_from_roman("CXCVII"))
print(get_dec_from_roman('MDCLXVI'))
print(get_dec_from_roman('MCMXC'))
print(get_dec_from_roman('I'))
print(get_dec_from_roman('IV'))



