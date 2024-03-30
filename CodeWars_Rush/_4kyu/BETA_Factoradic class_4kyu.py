# accepted on codewars.com


class Factoradic:
    LETTERS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    DICT_ = {ch: i for i, ch in enumerate(LETTERS)}

    def __init__(self, number):
        self.neg = False
        if number:
            if str(number)[0] == '-':
                self.neg = True
        if isinstance(number, int):
            self.number = number
            # translating dec n to factoradic:
            s = self.translate_to_f()
            self.f_num = (f'-' if self.neg else '') + s if s else f'0'
        elif isinstance(number, str):
            self.f_num = number
            # translating factoradic n to dec:
            self.number = self.neg_ * self.translate_to_dec()
        else:
            raise Exception(f'Number must be of int or str types...')

    @property
    def neg_(self):
        return -1 if self.neg else 1

    def translate_to_f(self) -> str:
        f_num = self.rec_core(abs(self.number), 2)
        print(f'{f_num = }')
        return f_num

    def rec_core(self, n: int, base_: int) -> str:
        print(f'{n, base_ = }')
        return self.rec_core(n // base_, base_ + 1) + f'{self.LETTERS[n % base_]}' if n else ''

    def translate_to_dec(self) -> int:
        number = self.rec_core_(self.f_num[1:] if self.neg else self.f_num, 1)
        print(f'{number = }')
        return number

    def rec_core_(self, n: str, base_: int) -> int:
        print(f'{n, base_ = }')
        return base_ * (self.DICT_[n[-base_]] + self.rec_core_(n, base_ + 1) if base_ <= len(n) else 0)

    def __int__(self):
        return self.number

    def __str__(self):
        return self.f_num

    def __add__(self, other: 'Factoradic'):
        return Factoradic(self.number + other.number)

    def __sub__(self, other: 'Factoradic'):
        return Factoradic(self.number - other.number)

    def __mul__(self, other: 'Factoradic'):
        return Factoradic(self.number * other.number)

    def __floordiv__(self, other: 'Factoradic'):
        return Factoradic(self.number // other.number)

    def __neg__(self):
        return Factoradic(-self.number)

    def __eq__(self, other: 'Factoradic'):
        return self.number == other.number

    def __lt__(self, other: 'Factoradic'):
        return self.number < other.number

    def __gt__(self, other: 'Factoradic'):
        return self.number > other.number

    def __le__(self, other: 'Factoradic'):
        return self.number <= other.number

    def __ge__(self, other: 'Factoradic'):
        return self.number >= other.number







                                                                                      # 36.6 98 989 98989 LL
