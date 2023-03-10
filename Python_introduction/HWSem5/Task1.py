# 1. Напишите программу, удаляющую из текста все слова содержащие "абв". Используйте знания с последней лекции. Выполните ее в виде функции.
# -*- coding: utf-8 -*-
from functools import reduce


# working on list
def delete_char_sequence(text: list[str]) -> list:
    return list(filter(lambda x: x.lower().find('абв') == -1, text))  # just a base filter using on a list


print(delete_char_sequence(['лалалабвло', 'фбтатамв', 'абабавв']))


text = 'Что абвил там прячет? Дело "АБВ", значит... повторяю для зевак, в общем, дело было так: абвал пришел в барак и обувал старый башмак, ' \
       'да обул не так, и попал в просак, вот же старый дурак. "Так его растак!" - говорил абвул и его обул... а сам сел на стул, а стул сломался,' \
       ' так абвул на полу и остался, долго же абвил смеялся!'
test1 = 'абвал,'


signs = [',', '.', ':', ';', '!', '?', '-', '"', '(', ')']


# working on the text given
def filter_text(text_in: str):
    parts = text.split(' ')
    print(parts)

    new_parts = []

    for part in parts:
        flag = True

        new_part = part

        # checks the beginning signs
        if len(part) >= 2 and part[0] == '(' and part[1] == '"':
            new_parts.append(part[:-(len(part) - 2)])
            new_part = part[-(len(part) - 2):]
        elif len(part) >= 1 and (part[0] == '(' or part[0] == '"'):
            new_parts.append(part[:-(len(part) - 1)])
            new_part = part[-(len(part) - 1):]

        # checks the ending signs
        for index_of_character in range(len(new_part)):
            if new_part[index_of_character] in signs:
                new_parts.append(new_part[:-(len(new_part) - index_of_character)])
                new_parts.append(new_part[-(len(new_part) - index_of_character):])
                flag = False
                break
        if flag:
            new_parts.append(new_part)

    print(new_parts)

    # getting rid of non-needed words
    result_parts = delete_char_sequence(new_parts)

    # shaping the resulting text
    return reduce(lambda x, y: x + y + ' ', result_parts, '')


print(f'result text: {filter_text(text)}')
print([1, 2, 3, 4, 5, 6, 7][-2:])
print([1, 2, 3, 4, 5, 6, 7][:-2])

