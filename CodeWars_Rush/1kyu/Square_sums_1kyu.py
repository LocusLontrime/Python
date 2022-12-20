# accepted on codewars.com
import time

perfect_squares = [(n * n) for n in range(2, 51)]
graph_to_be_updated = dict()


def square_sums(num):
    # print(f'num: {num}')

    global graph_to_be_updated

    # accurate graph making
    def get_graph() -> None:
        global graph_to_be_updated
        graph_to_be_updated = dict()

        for number1 in range(1, num + 1):
            for sq in perfect_squares:
                if sq >= 2 * number1:
                    break
                elif sq > number1:
                    if sq - number1 in graph_to_be_updated.keys():
                        graph_to_be_updated[sq - number1].add(number1)
                    else:
                        graph_to_be_updated[sq - number1] = {number1}
                    if number1 in graph_to_be_updated.keys():
                        graph_to_be_updated[number1].add(sq - number1)
                    else:
                        graph_to_be_updated[number1] = {sq - number1}

    def update_graph(new_vertex: int):  # need for consecutive calls of square sums method (for consecutive nums)
        global graph_to_be_updated

        for sq in perfect_squares:
            if sq >= 2 * new_vertex:
                break
            elif sq > new_vertex:
                # print(f'sq: {sq}')
                graph_to_be_updated[sq - new_vertex].add(new_vertex)
                if new_vertex in graph_to_be_updated.keys():
                    graph_to_be_updated[new_vertex].add(sq - new_vertex)
                else:
                    graph_to_be_updated[new_vertex] = {sq - new_vertex}

    # here we finds a hamiltanian path in the graph using a minimal neighbours heuristic
    def find_hamilton_path(start_num: int):
        global graph_to_be_updated
        path = []
        # for the better runtime:
        visited_vertices = set([])
        # used as stack:
        vertices_to_visit = [None, start_num]
        # while this set if not empty:
        while vertices_to_visit:
            curr_vertex = vertices_to_visit.pop()
            # if it is not None:
            if curr_vertex:
                path.append(curr_vertex)
                if len(path) == num:
                    break
                # memoization of visited vertices:
                visited_vertices.add(curr_vertex)
                # heuristic itself:
                if len(k := list(graph_to_be_updated[curr_vertex] - visited_vertices)) != 0:
                    min_length = min([len(graph_to_be_updated[i] - visited_vertices) for i in k])
                    best_fit_vertices = [el for el in k if len(graph_to_be_updated[el] - visited_vertices) == min_length]
                    # next step:
                    for vertex_remained in best_fit_vertices:
                        vertices_to_visit.append(None)
                        vertices_to_visit.append(vertex_remained)
            # removing element:
            else:
                visited_vertices.remove(path.pop())
        # returning the result:
        return path

    # here we are building a graph
    get_graph()

    # print(f'graph: {graph_to_be_updated}')

    # searching for the starting vertex to build a valid result (the 0 index is not the best vertex to start always)
    for vertex_to_start in (s := sorted(graph_to_be_updated, key=lambda x: len(graph_to_be_updated[x]))):
        res = find_hamilton_path(vertex_to_start)
        if res:
            print(f'index: {s.index(vertex_to_start)}')
            return res

    return False


t1 = time.perf_counter_ns()

# print(perfect_squares)
numb = 1000
for numb in range(1, 1098 + 1):
    sums = square_sums(numb)
    if type(sums) is not bool:
        print(f'{numb}, length of sums: {len(sums)}, row: {sums}')
    else:
        print(f'{numb}, no solution found: {[]}')

t2 = time.perf_counter_ns()

print(f'time elapsed: {(t2 - t1) / 10 ** 9} seconds')


