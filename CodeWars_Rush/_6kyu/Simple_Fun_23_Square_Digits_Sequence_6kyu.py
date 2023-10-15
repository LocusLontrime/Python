# acc
def square_digits_sequence(n: int):
    n_ = n
    counter = 0
    encountered_ones = {n}
    while True:
        counter += 1
        n_ = sum(map(square, str(n_)))
        # print(f'{counter}. n_: {n_}')
        if n_ in encountered_ones:
            return counter + 1
        encountered_ones.add(n_)


def square(n: str) -> int:
    return int(n) ** 2


ks = 16, 103, 1, 86, 6
for k in ks:
    print(f'steps: {square_digits_sequence(k)}')


