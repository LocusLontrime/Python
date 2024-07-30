from collections import Counter

arr = [7, 9, 8, 1, 5, 4, 3, 2, 6, 0]


def guess_(i1: int, i2: int, word: str) -> int:
    if word not in {'max', 'min'}:
        raise ValueError(f'Wrong arg, it can be ONLY min or max...')
    return max(arr[i1], arr[i2]) if word == 'max' else min(arr[i1], arr[i2])


def guesser(n: int, guess):
    def block_guesser(ind: int) -> int:
        words = ['max', 'min']
        results = [guess(i - 1, i, word) for i in range(ind, ind + 2) for word in words]
        counter = Counter(results)
        print(f'{counter = }')
        return max(counter, key=lambda x: counter[x])

    # print(f'block_guesser[{1}] -> {block_guesser(1)}')

    return [block_guesser]


guesser(10, guess_)
