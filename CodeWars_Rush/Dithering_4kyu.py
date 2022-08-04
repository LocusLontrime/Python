# accepted on codewars.com 36 366 98 989
import math


# the main algo
def dithering(width, height):
    # testing and memo
    print(f'h: {height}, w: {width}')
    memo_table = {0: [(0, 0)]}
    power_of_two_in = math.floor(math.log2(max(width, height)))

    # core method
    def recursive_builder(max_power_of_two: int):
        # power memoized or not
        if max_power_of_two not in memo_table.keys():
            # auxiliary values
            side = 2 ** (max_power_of_two - 1)
            shifts = [[0, 0], [side, side], [side, 0], [0, side]]
            memo_table[max_power_of_two] = []
            # cycling through the previous power of two side dithering matrix
            for coordinates in recursive_builder(max_power_of_two - 1):
                # all the four vertexes
                for k in range(len(shifts)):
                    # checking if the coords are within width and height
                    if coordinates[0] + shifts[k][0] < width and coordinates[1] + shifts[k][1] < height:
                        memo_table[max_power_of_two].append((coordinates[0] + shifts[k][0], coordinates[1] + shifts[k][1]))

        return memo_table[max_power_of_two]
    # returning the iterable obj
    return iter(recursive_builder(power_of_two_in + 1))


# only for visualization
def get_matrix(coordinates_list: list, h, w):

    result_matrix = [[0] * w for _ in range(h)]
    counter = 1

    for coordinates_pair in coordinates_list:
        result_matrix[coordinates_pair[1]][coordinates_pair[0]] = counter
        counter += 1

    return result_matrix


def print_matrix(matrix: list[list[int]]) -> None:

    for j in range(len(matrix)):
        for i in range(len(matrix[0])):
            print(matrix[j][i], end=' ')
        print()


def show(width, height):
    return print_matrix(get_matrix(dithering(width, height), height, width))


show(3, 3)
show(6, 5)
show(8, 8)
