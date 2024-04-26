# accepted on codewars.com
djdi = ((0, 1), (1, 0), (0, -1), (-1, 0))


def has_exit(maze: list[str]):
    # several ks check:
    if sum(1 if ch == 'k' else 0 for j in range(len(maze)) for ch in maze[j]) != 1:
        raise Exception(f'There should be only one Kate in a maze!')

    for j_ in range(j_max := len(maze)):
        for i_ in range(i_max := len(maze[0])):
            if maze[j_][i_] == 'k':
                k_j, k_i = j_, i_

    visited = [[False for _ in range(i_max)] for _ in range(j_max)]

    return dfs(k_j, k_i, maze, visited, j_max, i_max)


def dfs(j: int, i: int, maze: list[str], visited: list[list[int]], j_max: int, i_max: int) -> bool:
    print(f'{j, i=}')

    # base case:
    if j == 0 or i == 0 or j == j_max - 1 or i == i_max - 1:
        if maze[j][i] != '#':
            return True

    # body of rec:
    for dj, di in djdi:
        j_, i_ = j + dj, i + di
        if 0 <= j_ < j_max and 0 <= i_ < i_max:
            if not visited[j_][i_] and maze[j_][i_] == ' ':
                # visiting:
                visited[j_][i_] = True
                # recursive call:
                if dfs(j_, i_, maze, visited, j_max, i_max):
                    return True

    # zero return:
    return False


maze_ = ["########",
         "# # ####",
         "# #k#   ",
         "# # # ##",
         "# # # ##",
         "#      #",
         "########"]

maze_x = ["k"]

print(f'res: {has_exit(maze_x)}')
