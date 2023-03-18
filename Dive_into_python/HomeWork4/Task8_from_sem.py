# -*- coding: utf-8 -*-


# Task8. Создайте несколько переменных заканчивающихся и не оканчивающихся на «s».
# Напишите функцию, которая при запуске заменяет содержимое переменных
# оканчивающихся на s (кроме переменной из одной буквы s) на None.
# Значения не удаляются, а помещаются в одноимённые переменные без s на конце.


def replacer(**kwargs):
    # keys given:
    keys = list(kwargs.keys())
    # main keys-replacing-cycle:
    for key in keys:
        if key.endswith('s') and len(key) > 1:
            temp_val = kwargs[key]
            kwargs[key] = None
            kwargs[key[:-1]] = temp_val
    # returns kwargs for convenient printing:
    return kwargs


print(f'{replacer(las=98, faSss=99, LAsFA=98989, sSSsss="lala", s={1, 2, 3})}')



