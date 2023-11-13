letters = {ch: i + 1 for i, ch in enumerate("abcdefghijklmnopqrstuvwxyz")}


def spiralize(word: str):  # 36 366 98 989
    print(f'letters: {letters}')
    y_shift, x_shift = 0, 0
    max_y, max_x = 0, 0
    for i, ch_ in enumerate(word):
        if i % 4 == 0:
            y_shift -= letters[ch_]
            print(f'rem [{i % 4}]: {ch_}')
        elif i % 4 == 2:
            y_shift += letters[ch_]
            print(f'rem [{i % 4}]: {ch_}')
        elif i % 4 == 1:
            x_shift -= letters[ch_]
            print(f'rem [{i % 4}]: {ch_}')
        else:
            x_shift += letters[ch_]
            print(f'rem [{i % 4}]: {ch_}')
        max_y, max_x = max(max_y, y_shift), max(max_x, x_shift)
    print(f'y_shift, x_shift: {y_shift, x_shift}')
    print(f'max_y, max_x: {max_y, max_x}')


word_ = "abcdefghijklmnopqrstuvwxyz"
word__ = "adbbeb"
word_x = "wordspiral"
word_xx = "a"
# print(f'length: {len(word_)}')

spiralize(word_)
