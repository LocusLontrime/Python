# accepted on codewars.com
curr_ship_length: int
dirs: list[int]


def validate_battlefield(field: list[list[int]]):
    global curr_ship_length, dirs
    J, I = len(field), len(field[0])
    # if some region/regions have diagonal neigh/neighs:
    if touch_or_not(field, J, I): return False
    ships = {}
    for j in range(J):
        for i in range(I):
            if field[j][i] != 0:
                curr_ship_length = 0
                dirs = [0, 0]
                dfs(j, i, field, 0, J, I)
                if sum(dirs) > 1 or curr_ship_length > 4:
                    return False
                else:
                    if curr_ship_length in ships.keys():
                        ships[curr_ship_length] += 1
                    else:
                        ships[curr_ship_length] = 1
    print(f'SHIPS: ')
    for key in ships.keys():
        print(f'Length of ship: {key}, quantity: {ships[key]}')
    if len(ships) != 4: return False
    for key in ships:
        if key != 5 - ships[key]:
            return False
    return True


# checks for diag touching:
def touch_or_not(field: list[list[int]], j_max: int, i_max: int):
    for j in range(j_max - 1):
        for i in range(i_max - 1):
            if field[j][i] == 1 and field[j][i + 1] == 0 and field[j + 1][i] == 0 and field[j + 1][i + 1] == 1:
                return True
            if field[j][i] == 0 and field[j][i + 1] == 1 and field[j + 1][i] == 1 and field[j + 1][i + 1] == 0:
                return True
    return False

def dfs(j, i, field, dir_: int, j_max, i_max):
    global curr_ship_length, dirs
    if 0 <= j < j_max and 0 <= i < i_max and field[j][i] == 1:
        # memoization:
        field[j][i] = 0
        # all ships are lined:
        if dir_ == 1: dirs[0] = 1
        elif dir_ == -1: dirs[1] = 1
        if sum(dirs) > 1: return
        curr_ship_length += 1
        # next steps (widening):
        dfs(j + 1, i, field, 1, j_max, i_max)
        dfs(j - 1, i, field, 1, j_max, i_max)
        dfs(j, i + 1, field, -1, j_max, i_max)
        dfs(j, i - 1, field, -1, j_max, i_max)


field1 = [
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

print(validate_battlefield(field1))
