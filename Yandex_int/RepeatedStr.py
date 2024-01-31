# -*- coding: utf-8 -*-
# Напишите программу, которая проверяет, верно ли, что данная строка представляет из себя некоторую другую строку, повторённую несколько раз.
# Например, строка dabudabudabu — это трижды повторённая строка dabu. Строка kapkap — это дважды повторённая строка kap.
# А вот строку abdabdab или строку gogolmogol нельзя представить как повторение некоторой другой строки.
# На вход программа должна принимать строку и выдавать ответ Yes, если строка является повторением некоторой другой строки, и No, если это не так.


def is_repeated_x(string: str) -> bool:
    # candidate searching:
    j = 0
    doubledStr = string * 2
    repeatedCandidate = ""  # ???
    for i, ch in enumerate(doubledStr[1:], 1):
        print(f'({j, i}) -> string[j], string[i]: {doubledStr[j], doubledStr[i]}, repeated: {repeatedCandidate}')
        if doubledStr[j] == ch:
            repeatedCandidate += ch
            j += 1
            if j == len(string):
                return True
        else:
            repeatedCandidate = ""
            j = 0

    return False


print(f'res: {is_repeated_x("kmfkmflkmfkmfl")}\n')
print(f'res: {is_repeated_x(f"kmfnfnkmflkmfn")}\n')
print(f'res: {is_repeated_x(f"aaaaa")}\n')
