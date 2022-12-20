# accepted on codewars.com
bulb_symbol = 'B'


def switch_bulbs(game_map):  # 36 366 98 989
    bulbs = find_bulbs(game_map)
    graph = build_graph(bulbs)
    path = None
    bulbs = list(sorted(bulbs, key=lambda x: len(graph[x])))
    for start_vertex in bulbs:
        p = get_path(graph, len(bulbs), start_vertex)
        if p:
            path = p
            break
    if path is None:
        return None
    print(f'length of path: {len(path)}')
    return [(j - 1, i - 1) for (j, i) in path]


def get_path(graph: dict[tuple[int, int]], length: int, start_vertex):
    path = []
    vertices_to_visit = [None, start_vertex]
    visited_vertices = set([])
    # cycle through all the vertices:
    while vertices_to_visit:
        curr_vertex = vertices_to_visit.pop()
        if curr_vertex:
            path.append(curr_vertex)
            if len(path) == length:
                 break
            # memoization of visited vertices:
            visited_vertices.add(curr_vertex)
            # cycling through all the neighbours:
            for next_vertex in graph[curr_vertex]:
                if next_vertex not in visited_vertices:
                    vertices_to_visit.append(None)
                    vertices_to_visit.append(next_vertex)
        # removing element:
        else:
            visited_vertices.remove(path.pop())
    return path

def build_graph(bulbs: list[tuple[int, int]]):
    graph = dict()
    length = len(bulbs)
    for j in range(length):
        # vertical, horizontal, +diag and -diag neighbours:
        neighs_j = [[], [], [], []]
        for i in range(length):
            if j != i:
                j1, j2, i1, i2 = bulbs[j][0], bulbs[i][0], bulbs[j][1], bulbs[i][1]
                if j1 == j2:
                    neighs_j[0].append((bulbs[i], i1 - i2))
                elif i1 == i2:
                    neighs_j[1].append((bulbs[i], j1 - j2))
                elif j1 + i1 == j2 + i2:
                    neighs_j[2].append((bulbs[i], j1 - j2))
                elif j1 - i1 == j2 - i2:
                    neighs_j[3].append((bulbs[i], j1 - j2))
        for line_neighs in neighs_j:
            line_neighs.append((bulbs[j], 0))
        neighs_j = [sorted(line_neighs, key=lambda x: x[1]) for line_neighs in neighs_j]
        # constructing a graph from neighs:
        graph[bulbs[j]] = []
        for line_neighs in neighs_j:
            # index of current el:
            ind = line_neighs.index((bulbs[j], 0))
            # getting two nearest possible neighs for all 4 lines -->> -, |, /, \:
            if ind + 1 < len(line_neighs):
                graph[bulbs[j]].append(line_neighs[ind + 1][0])
            if ind - 1 >= 0:
                graph[bulbs[j]].append(line_neighs[ind - 1][0])
    return graph


def find_bulbs(game_map):
    bulbs = []
    for j, row in enumerate(game_map.split('\n')):
        for i, symbol in enumerate(row):
            if symbol == bulb_symbol:
                bulbs.append((j, i))
    return bulbs


game_map_v = [
"+--------+\n"+
"|...B....|\n"+
"|........|\n"+
"|.B......|\n"+
"|......B.|\n"+
"|......B.|\n"+
"|.B......|\n"+
"|......BB|\n"+
"|BB......|\n"+
"+--------+"][0]

game_map_x = [
"+------------------------+\n" +
"|.....................B..|\n" +
"|........................|\n" +
"|............B...........|\n" +
"|........................|\n" +
"|........................|\n" +
"|......B....B.........B..|\n" +
"|........................|\n" +
"|...................B....|\n" +
"|........................|\n" +
"|........................|\n" +
"|........B..B............|\n" +
"|........................|\n" +
"|........................|\n" +
"|........B...............|\n" +
"|B.......................|\n" +
"|.B......................|\n" +
"|.............BB....B....|\n" +
"|............B.....B.....|\n" +
"|.................B......|\n" +
"|........................|\n" +
"|........................|\n" +
"|........................|\n" +
"|........................|\n" +
"|............B...........|\n" +
"|........................|\n" +
"|........................|\n" +
"|........................|\n" +
"|........................|\n" +
"+------------------------+"][0]

print(switch_bulbs(game_map_v))
# print(b := find_bulbs(game_map_x))
# print(f'graph: \n{build_graph(b)}')





