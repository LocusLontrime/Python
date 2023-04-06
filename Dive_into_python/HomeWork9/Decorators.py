import csv
import functools
import json
import math
import random


def cycle_call_parametrized(string_q: int, left_b: int, right_b: int):
    def cycle_call(func):
        # print(f'LALA')

        def wrapper_(*args, **kwargs):
            # creating a csv-file:
            generate_csv(string_q, left_b, right_b)
            roots = dict()
            with open('info.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f, dialect='excel')
                for i, row in enumerate(reader):
                    if row:
                        a, b, c = row
                        a, b, c, = int(a), int(b), int(c)
                        roots[i // 2] = str(func(a, b, c))
            return roots

        return wrapper_

    return cycle_call


def jsonize(func):
    def wrapper_(*args, **kwargs):
        # getting info:
        roots = func(args, kwargs)
        with open('info.json', 'w', encoding='utf-8') as f:
            json.dump(roots, f, indent='\n')
    return wrapper_


@jsonize
@cycle_call_parametrized(100, 100, 1000)
def solve_quadratic_equation(a: int, b: int, c: int):
    """solves a * x^2 + b * x + c = 0 equation..."""
    sqrt_d = (b ** 2 - 4 * a * c) ** .5
    x1, x2 = (-b + sqrt_d) / (2 * a), (-b - sqrt_d) / (2 * a)
    return x1, x2 if x1 != x2 else x1


def generate_csv(string_q: int, left_b: int, right_b: int):  # 100 -->> 1000 strings...
    with open('info.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='excel', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for ind in range(string_q + 1):
            k = [random.randint(left_b, right_b + 1) for _ in [0, 1, 2]]
            # print(f'k: {k}')
            writer.writerow(k)


# generate_csv(100, 100, 1000)

solve_quadratic_equation()
solve_quadratic_equation()


