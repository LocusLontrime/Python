# accepted on codewars.com


def chained(functions: list):
    def func(arg):
        val_ = arg
        for func_ in functions:
            val_ = func_(val_)
        return val_

    return func


def f1(x): return x * 2


def f2(x): return x + 2


def f3(x): return x ** 2


res1 = chained([f1, f2, f3])(0)  # 4
res2 = chained([f1, f2, f3])(2)  # 36
res3 = chained([f3, f2, f1])(2)  # 12

print(f'{res1, res2, res3 = }')
