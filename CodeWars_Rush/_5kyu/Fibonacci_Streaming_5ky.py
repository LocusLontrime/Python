# accepted on codewars.com


def all_fibonacci_numbers():
    _f, f_ = 0, 1
    while 1:
        f_ = _f + f_
        yield (_f := f_ - _f)


gen_ = all_fibonacci_numbers()

for i in range(100):
    print(f'{next(gen_)}')
