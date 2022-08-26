thresholds = [3 ** i + 1 for i in range(1, 20)]
colours = 'RGB'


def diff_btw_len_and_nearest_threshold(length):
    def sort_key(x):
        return abs(length - x)

    nearest = sorted(thresholds, key=sort_key)

    for val in nearest:
        if val <= length:
            return length - val + 1


def triangle(row):
    def solve_two(cl1, cl2):
        return cl1 if cl1 == cl2 else colours.replace(cl1, '').replace(cl2, '')

    if len(row) == 1:
        return row
    elif len(row) == 2:
        return solve_two(row[0], row[1])
    elif len(row) == 3:
        return solve_two(solve_two(row[0], row[1]), solve_two(row[1], row[2]))
    diff = diff_btw_len_and_nearest_threshold(len(row))

    left_simplified, right_simplified = triangle(row[:diff]), triangle(row[-diff:])

    return solve_two(left_simplified, right_simplified)


print(triangle('BGBGRBGRRBGRBGGGRBGRGBGRRGGRBGRGRBGBRGBGBGRGBGBGBGRRBRGRRGBGRGBRGRBGRBGRBBGBRGRGRBGRGBRGBBRGGBRBGGRB'))  # G
print(colours.replace('G', ''))
