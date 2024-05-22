# -*- coding: utf-8 -*-


x = 5
y = 10


def my_func(z):
    a = 3
    print(globals())  # выводит все глобальные переменные
    print(locals())  # выводит все локальные переменные


my_func(7)


def func_outer():
    z = 98
    print(f'func_outer -> {z}')

    def func_inner():
        nonlocal z
        print(f'func_inner -> {z}')

        def func_nested():
            nonlocal z
            print(f'func_nested -> {z}')

        func_nested()

    func_inner()


func_outer()
