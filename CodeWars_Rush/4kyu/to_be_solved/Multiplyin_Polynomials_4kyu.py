import re


def polynomial_product(polynomial_1: str, polynomial_2: str) -> str:
    ...


def pars_poly(polynomial: str):
    pattern = r'[+-]'
    exprs = re.split(pattern, polynomial)
    print(f'exprs: {exprs}')


pars_poly(f'3v^5+v^4+3v^3-1')


