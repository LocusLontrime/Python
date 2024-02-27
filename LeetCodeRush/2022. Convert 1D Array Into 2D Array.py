def construct_2d_array(original: list[int], m: int, n: int) -> list[list[int]]:
    if m * n != len(original):
        return []

    result = []

    for i in range(m):
        result.append(original[i * n: (i + 1) * n])

    return result


def print_2d_array(arr_2d: list[list[int]]):
    for j in range(len(arr_2d)):
        for i in range(len(arr_2d[0])):
            print(f'{arr_2d[j][i]} ', end='')
        print(f'')


original_ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
m_ = 3
n_ = 4
array_2d = construct_2d_array(original_, m_, n_)

print_2d_array(array_2d)


