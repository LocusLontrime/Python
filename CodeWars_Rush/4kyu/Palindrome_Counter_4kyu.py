# accepted on codewars (very fast)
import math


def count_palindromes(a: float | int, b: float | int):
    if a < 0 or b < 0:
        raise ValueError(f'a and b cannot be lower than zero!')
    if a > b:
        return 0
    return count_palindromes_aux(math.floor(b)) - (count_palindromes_aux(math.ceil(a) - 1) if a else 0)


def count_palindromes_aux(a: int):
    a_str = str(a)
    max_power_of_ten_in = len(a_str) - 1
    palindromes_counter = count_palindromes_before_power_of_ten(max_power_of_ten_in)
    for i in range((len(a_str) + 1) // 2):
        digit_ = int(a_str[i])
        palindromes_counter += (d_ := (digit_ - (0 if i else 1)) * 10 ** ((len(a_str) + 1) // 2 - i - 1))
    last_one = 1 if int((part := a_str[:(l_ := len(a_str) // 2)]) + (f'' if len(a_str) % 2 == 0 else f'{a_str[l_]}') + part[::-1]) <= a else 0
    return palindromes_counter + last_one


def count_palindromes_at_power_of_ten(power_of_ten: int):
    return 1 if power_of_ten == 0 else 9 * 10 ** ((power_of_ten - 1) // 2)


def count_palindromes_before_power_of_ten(power_of_ten: int):
    return sum([count_palindromes_at_power_of_ten(p_) for p_ in range(power_of_ten + 1)])


l, r = 56748922948543545847328463278, 97366778594947372920949843857843284637284627462141427896478568343767366878093  # 5, 55  # 35, 64
print(f'RES palindromes counter{l, r}: {count_palindromes(l, r)}')

