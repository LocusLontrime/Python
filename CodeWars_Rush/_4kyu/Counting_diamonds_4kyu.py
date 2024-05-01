# accepted on codewars.com
def count_diamonds(diamond_map: list[list[int]], num_of_diamonds: int):
    parcels = []
    # count diamonds in parcels
    aux_m = precompute(diamond_map)
    for j in range(j_max := len(diamond_map)):
        for i in range(i_max := len(diamond_map[0])):
            for j_ in range(j, j_max):
                for i_ in range(i, i_max):
                    curr_sum = aux_m[j_][i_] - (aux_m[j_][i - 1] if i > 0 else 0) - (
                        aux_m[j - 1][i_] if j > 0 else 0) + (aux_m[j - 1][i - 1] if j > 0 and i > 0 else 0)
                    if curr_sum == num_of_diamonds:
                        parcels += [[(j, i), (j_, i_)]]
    # let us filter the minimal area parcels:
    min_area = min(parcels, key=(k := lambda x: (x[1][0] - x[0][0] + 1) * (x[1][1] - x[0][1] + 1)))
    print(f'{min_area = }')
    return [parcel for parcel in parcels if k(parcel) == k(min_area)]


def precompute(diamond_map: list[list[int]]) -> list[list[int]]:
    """creates sub-matrix aux_m[j][i] element of which keeps sum of all elements belonged to (0, 0) -> (j, i) rectangle"""
    aux_m = [[0 for _ in range(len(diamond_map[0]))] for _ in range(len(diamond_map))]
    # filling the sub-matrix:
    for j in range(len(diamond_map)):
        for i in range(len(diamond_map[0])):
            aux_m[j][i] += (aux_m[j - 1][i] if j > 0 else 0) + (aux_m[j][i - 1] if i > 0 else 0) - (
                aux_m[j - 1][i - 1] if j > 0 and i > 0 else 0) + diamond_map[j][i]
    # showing res:
    for row in aux_m:
        print(f'{row}')
    # returns aux matrix:
    return aux_m


diamond_map_ = [
    [4, 5, 0, 2],
    [10, 1, 2, 0],
    [1, 0, 2, 1],
    [0, 0, 1, 0]
]

num_of_diamonds_ = 3

diamond_map_x = [
    [8, 4, 2, 9, 9, 4, 5, 6, 10, 9],
    [3, 3, 6, 9, 7, 7, 5, 7, 7, 3],
    [0, 9, 8, 5, 5, 8, 0, 3, 9, 2],
    [1, 2, 8, 0, 0, 2, 9, 4, 7, 3],
    [10, 4, 7, 2, 6, 2, 10, 10, 9, 5],
    [3, 0, 4, 0, 5, 5, 2, 4, 6, 7],
    [0, 9, 2, 1, 4, 4, 1, 1, 8, 6],
    [0, 6, 7, 10, 9, 1, 6, 7, 3, 8],
    [4, 7, 10, 4, 1, 4, 10, 6, 8, 7],
    [8, 0, 5, 0, 7, 6, 0, 1, 6, 3]
]
num_of_diamonds_x = 98

# precompute(diamond_map_)

res = count_diamonds(diamond_map_x, num_of_diamonds_x)
print(f'{res = }')
