# accepted on codewars.com
fractal_sequence = None


def a112382(n):  # 366 36 98 989
    global fractal_sequence

    if fractal_sequence is None:
        fractal_sequence = generate(100001)

    print(f'The {n}-th element of fractal sequence is: ', end='')
    return fractal_sequence[n]


# 1, 1, 2, 1, 3, 4, 2, 5, 1, 6, 7, 8, 3
def generate(n):
    print(f'generating {n} sequence elements: ')

    seq = [1, 1]
    current_natural = 2
    step = 2

    index = 2
    while index < n:
        # 1 part --> adding a new natural number:
        el = seq[step - 1]
        print(f'step: {step}, el: {el}, current_natural: {current_natural}')

        i = 0
        while index < n and i < el:
            seq += [current_natural]
            index += 1
            current_natural += 1
            i += 1

        # 2 part --> adding a quantity of consecutive natural ones:
        if index < n:
            seq += [el]
            index += 1

        # 3 part --> variables mutation:
        step += 1

    return seq


# print(generate(100000))
print(a112382(100000))  # 366 36 98 989 98989

