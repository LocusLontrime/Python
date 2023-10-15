# accepted on codewars.com
def magic_square(dim: int):

    magic_square_array = [[0] * dim for _ in range(dim)]
    curr_position = [0, (dim - 1) // 2]
    magic_square_array[curr_position[0]][curr_position[1]] = 1

    for i in range(2, dim * dim + 1):

        if is_valid((curr_position[0] - 1, curr_position[1] + 1), dim):
            if magic_square_array[curr_position[0] - 1][curr_position[1] + 1] == 0:
                curr_position[0] -= 1
                curr_position[1] += 1
            else:
                curr_position[0] += 1
        else:
            if curr_position[1] + 1 < dim:
                curr_position[0] = dim - 1
                curr_position[1] += 1
            elif curr_position[0] - 1 >= 0:
                curr_position[0] -= 1
                curr_position[1] = 0
            else:
                curr_position[0] += 1

        magic_square_array[curr_position[0]][curr_position[1]] = i

    return magic_square_array


def is_valid(current_coords: tuple, dim: int) -> bool:
    return current_coords[0] >= 0 and current_coords[1] < dim


print(magic_square(5))
