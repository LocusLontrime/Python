# -*- coding: utf-8 -*-
import csv


class Descriptor:
    MIN_MARK, MAX_MARK = 2, 5
    MIN_RES, MAX_RES = 0, 100

    def __set_name__(self, owner, name):
        self._param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self._param_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self._param_name, value)

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'This descriptor predestined only for working with str attrs...')
        else:
            if value:
                if not (value[0].isupper() and value.isalpha()):
                    raise ValueError(f'invalid {self._param_name} format!')
            else:
                raise ValueError(f'empty string, zhoskii ИНВЭЛИД!!!')


class Student:
    name = Descriptor()
    surname = Descriptor()
    patronymic = Descriptor()

    def __init__(self, name, surname, patronymic):
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self._disciplines = []
        self.progress: dict[str: list[int, int]] = dict()
        self.initialize()

    @property
    def disciplines(self):
        return self._disciplines

    def initialize(self):
        with open(f'Disciplines.csv', 'r') as f:
            reader = csv.reader(f, 'excel')
            for row in reader:
                self._disciplines.append(r := row[0])
                self.progress[r] = [None, None]

    def get_mark(self, discipline: str, mark: int):
        if not (2 <= mark <= 5):
            raise ValueError(f'mark should be larger than {2} and less than {5}')
        elif discipline not in self.progress.keys():
            raise ValueError(f'invalid discipline!..')
        else:
            self.progress[discipline][0] = mark

    def get_test_res(self, discipline: str, res: int):
        if not (0 <= res <= 100):
            raise ValueError(f'res should be larger than {0} and less than {100}')
        if discipline not in self.progress.keys():
            raise ValueError(f'invalid discipline!..')
        else:
            self.progress[discipline][1] = res

    def get_average(self) -> tuple[float, float]:
        average_mark, average_res = 0, 0
        mark_counter, res_counter = 0, 0
        for m_, r_ in self.progress.values():
            if m_ is not None:
                average_mark += m_
                mark_counter += 1
            if r_ is not None:
                average_res += r_
                res_counter += 1
        return average_mark / mark_counter, average_res / res_counter


s = Student('Ivan', 'Ivanov', 'Ivanovich')
print(f'disciplined: {s.disciplines}')

