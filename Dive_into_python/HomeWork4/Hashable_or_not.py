# -*- coding: utf-8 -*-

# 2. Напишите функцию, принимающую на вход только ключевые
# параметры и возвращающую словарь, где ключ — значение
# переданного аргумента, а значение — имя аргумента. Если
# ключ не хешируем, используйте его строковое представление.


def func(**kwargs):
    # aux func for hashability check:
    def hashable(obj):
        try:
            hash(obj)
            return True
        except TypeError as _:
            return False
    # core logic:
    return {val if hashable(val) else str(val): key for key, val in kwargs.items()}


# print(f'{hash([])}') -->> for error type check :)

print(f'new dict: {func(value=98, secret_val=99, levi_gin_list=[1,2,3,4,5,6,7,8,9,10,11], strange_name="Levi Gin", red_code=98)}')






