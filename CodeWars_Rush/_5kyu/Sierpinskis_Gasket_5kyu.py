# accepted on codewars.com


def sierpinski(n: int) -> str:
    """Returns a string containing the nth iteration of the Sierpinski Gasket fractal"""
    if n == 0:
        return 'L'
    # new_fractal_level:
    prev_level = sierpinski(n - 1)
    new_level = '\n'.join(f'{row + " " * (2 ** n - len(row)) + row}' for row in prev_level.split('\n'))
    # returns new frac:
    return f'{prev_level}\n{new_level}'


k = 7

print(f'Sierpinski({k})\n{sierpinski(k)}')



