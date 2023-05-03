# tested, codewars task requires JS version...

def stop_zombie(city: list[list[int]]) -> list[list[int]]:
    walk = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    max_y, max_x = len(city), len(city[0])
    res = [[0 for _ in range(max_x)] for _ in range(max_y)]

    def dfs(y_: int, x_: int):
        if 0 <= y_ < max_y and 0 <= x_ < max_x and res[y_][x_] != 1 and city[y_][x_] == city[0][0]:
            res[y_][x_] = 1
            for dy, dx in walk:
                dfs(y_ + dy, x_ + dx)

    dfs(0, 0)
    return res


city1 = [
    [7, 2, 3],
    [7, 2, 3],
    [1, 2, 7]
]

city2 = [
    [9, 1, 2],
    [9, 9, 9],
    [7, 4, 9],
    [7, 9, 7]
]

city3 = [
    [9, 7, 8, 98, 9, 9, 9, 9, 9],
    [9, 9, 9, 9, 9, 11, 3, 6, 9],
    [10, 6, 6, 5, 6, 1, 9, 9, 9],
    [9, 1, 1, 11, 6, 6, 9, 1, 4],
    [9, 10, 1, 1, 1, 1, 9, 9, 9],
    [9, 9, 9, 9, 10, 1, 8, 8, 9],
    [9, 1, 11, 1, 1, 9, 9, 9, 9],
    [9, 9, 9, 9, 9, 9, 9, 99, 9]
]


for city_ in [city1, city2, city3]:
    print(f'result: ')
    for row in stop_zombie(city_):
        print(row)
    print()



