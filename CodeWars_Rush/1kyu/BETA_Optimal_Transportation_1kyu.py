# accepted on codewars.com
import math
import random
import time as t
from functools import reduce
import numpy as np

SHOW_FLAG = True
RED = "\033[31m{}"
GREEN = "\033[32m{}"
YELLOW = "\033[33m{}"
PURPLE = "\033[35m{}"
CYAN = "\033[36m{}"
END = "\033[0m{}"


def minimum_transportation_price(suppliers, consumers, costs):  # 36 366 98 989 LL
    # quantities of rows and columns:
    rows, cols = len(costs), len(costs[0])
    # table for X(j, i) --> optimal (min) total price:
    sol_table = [[None for _ in range(cols)] for _ in range(rows)]
    # building basic solution (it can be not optimal):
    rows_basis_cells, columns_basis_cells, coords = get_basic_solution_min_price_method(sol_table, suppliers, consumers,
                                                                                        costs)
    # time section -->> needed for further testing:
    start_t, potentials_t, deltas_t, getting_cycle_t, cycle_recounting_t = 0, 0, 0, 0, 0
    # now cycling through all the approximating iterations needed until the optimal solution found:
    main_cycle_iterations = 0
    while True:
        print(f'main_cycle_iterations: {main_cycle_iterations}')
        s_t = t.time_ns()
        u, v = find_potentials(costs, sol_table, rows_basis_cells, columns_basis_cells, coords)
        p_t = t.time_ns()
        potentials_t += p_t - s_t
        # max delta estimation (numpy optimization for deltas section, works too slow without numpy optimization):
        max_delta, j_max_d, i_max_d = deltas_calc(u, v, costs, cols)
        d_t = t.time_ns()
        deltas_t += d_t - p_t
        # stop-condition of finding the optimal solution:
        if max_delta <= 0:
            break
        # finding the cycle:
        path = get_cycle_path(j_max_d, i_max_d, rows_basis_cells, columns_basis_cells)
        if SHOW_FLAG:
            show_cycle(sol_table, rows_basis_cells, path)
        g_t = t.time_ns()
        getting_cycle_t += g_t - d_t
        # changing the X-elements (table) along the cycle-path:
        cycle_recounting(path, sol_table, rows_basis_cells, columns_basis_cells)
        c_t = t.time_ns()
        cycle_recounting_t += c_t - g_t

        main_cycle_iterations += 1

    # time distribution:
    print(f'time elapsed--------->>>>>>>>>')
    print(f'1. finding potentials: {potentials_t // 10 ** 6} milliseconds')
    print(f'2. calculating deltas: {deltas_t // 10 ** 6} milliseconds')
    print(f'3. getting cycle path: {getting_cycle_t // 10 ** 6} milliseconds')
    print(f'4. cycle recounting: {cycle_recounting_t // 10 ** 6} milliseconds')
    print(f'optimal solution been found at {main_cycle_iterations}-th iteration')
    # return the aggregated min transportation price:
    # return sum([sol_table[j][i] * costs[j][i] for j in range(rows) for i in range(cols) if sol_table[j][i] is not None]) -->> optimized:
    return sum(sum([sol_table[cell[0]][cell[1]] * costs[cell[0]][cell[1]] for cell in row_cells]) for row_cells in
               rows_basis_cells)


def get_basic_solution_min_price_method(table, suppliers, consumers, costs):
    # all the cells:
    cells_queue = [(j, i) for i in range(len(costs[0])) for j in range(len(costs))]
    # auxiliary queue for degenerated case:
    aux_queue = cells_queue.copy()
    # sorting by price -> from min (leftmost el) to max(rightmost el)
    cells_queue = sorted(cells_queue, key=lambda x: costs[x[0]][x[1]], reverse=True)
    # rows and columns basis cells -->_ needed for cycle and potentials finding optimization:
    rows_basis_cells = [[] for _ in range(len(costs))]
    columns_basis_cells = [[] for _ in range(len(costs[0]))]
    # starting min price method:
    # rows and columns left (not crossed of):
    rows = {_ for _ in range(len(costs))}
    cols = {_ for _ in range(len(costs[0]))}
    # here we start crossing off the rows and columns and find the basis cells:
    while len(cells_queue) > 0:
        # takes the current minimal price (cost) from queue:
        curr_j, curr_i = cells_queue.pop()
        # if an element located in crossed off row or column:
        if curr_j not in rows or curr_i not in cols:
            continue
        # delete the basis element from non_basis cells aux queue
        aux_queue.pop(aux_queue.index((curr_j, curr_i)))
        # finds the min between supply and demand and changes data:
        supply = suppliers[curr_j]
        demand = consumers[curr_i]
        if supply == demand:
            # it means that we cross off only column in case of demand and supply equality:
            suppliers[curr_j] = 0
            cols.remove(curr_i)
            # we could cross off only row instead of doing actions above:
            # consumers[curr_i] = 98
            # rows.remove(curr_j)
        # here we cross off the min of demand and supply and decrease the rest value by corresponding amount:
        elif supply < demand:
            suppliers[curr_j] = 0
            consumers[curr_i] -= supply
            rows.remove(curr_j)
        else:
            consumers[curr_i] = 0
            suppliers[curr_j] -= demand
            cols.remove(curr_i)
        # adding the basis cell to the table:
        table[curr_j][curr_i] = min(supply, demand)
        rows_basis_cells[curr_j].append((curr_j, curr_i))
        columns_basis_cells[curr_i].append((curr_j, curr_i))
        # stop-condition (basis solution found):
        if len(rows) == 0 or len(cols) == 0:
            break
    # degenerated case:
    additional_cell_coords = (0, 0)
    if sum([len(cells) for cells in rows_basis_cells]) < len(costs) + len(costs[0]) - 1:
        print(f'degenerated case!')
        # adding the missing basis cell:
        aux_queue = sorted(aux_queue, key=lambda x: costs[x[0]][x[1]])
        additional_cell_coords = aux_queue[0]
        table[j := additional_cell_coords[0]][i := additional_cell_coords[1]] = 0
        rows_basis_cells[j].append((j, i))
        columns_basis_cells[i].append((j, i))
    # returns auxiliary data:
    return rows_basis_cells, columns_basis_cells, additional_cell_coords


def deltas_calc(u, v, costs, cols):
    deltas_matrix = np.array(v) + np.array(u)[:, None] - np.array(costs)
    flat_index = np.argmax(deltas_matrix)
    # max_delta = np.amax(deltas_matrix)
    # double inds from the flat one:
    j_max_d = flat_index // cols
    i_max_d = flat_index - j_max_d * cols
    return deltas_matrix[j_max_d][i_max_d], j_max_d, i_max_d


def find_potentials(costs, table, rows_basis_cells, columns_basis_cells, coords):
    u = [None for _ in range(len(costs))]
    v = [None for _ in range(len(costs[0]))]

    # method of calculating potentials:
    def row_search(row):
        # only the basis elements, not all the cells are counted:
        for cell in rows_basis_cells[row]:
            if v[cell[1]] is None and u[row] is not None:
                v[cell[1]] = costs[row][cell[1]] - u[row]
                column_search(cell[1])

    def column_search(column):
        # only the basis elements, not all the cells are counted:
        for cell in columns_basis_cells[column]:
            if u[cell[0]] is None and v[column] is not None:
                u[cell[0]] = costs[cell[0]][column] - v[column]
                row_search(cell[0])

    # now we start from u1 and go along the row if we meet any basis var -> we define the value of corresponding v potential
    # and so on for every v-potential one found:
    u[0] = 0
    row_search(0)

    # degenerated case:
    if None in u or None in v:
        print(f'degenerated case!')
        # potentials that cannot be defined because of degenerated case:
        j_unknowns = [j for j, el in enumerate(u) if el is None]
        i_unknowns = [i for i, el in enumerate(v) if el is None]
        # all the possible places for new basis element:
        possible_placements = []
        for j_unknown in j_unknowns:
            possible_placements += [(j_unknown, i) for i in range(len(costs[0])) if table[j_unknown][i] is None]
        for i_unknown in i_unknowns:
            possible_placements += [(j, i_unknown) for j in range(len(costs)) if table[j][i_unknown] is None]
        # sorting all the possible places for new basis element by relative cost:
        possible_placements = sorted(possible_placements, key=lambda x: costs[x[0]][x[1]])
        # changing values section:
        new_basis_cell_coords = possible_placements[0]
        # we remove auxiliary Zero-var from basis cells and place a new one (zero too) and do some aux-manipulations needed:
        table[coords[0]][coords[1]] = None
        rows_basis_cells[coords[0]].remove(coords)
        columns_basis_cells[coords[1]].remove(coords)
        table[j := new_basis_cell_coords[0]][i := new_basis_cell_coords[1]] = 0
        rows_basis_cells[j].append(new_basis_cell_coords)
        columns_basis_cells[i].append(new_basis_cell_coords)
        # define the rest potentials:
        row_search(j)
        # one or two REALLY NEEDED???????
        column_search(i)
    # return the potentials found:
    return u, v


def cycle_recounting(cycle_path, table, rows_basis_cells, columns_basis_cells):
    # finding the min X-element at '-' position in cycle:
    min_el_coords = sorted([cycle_path[i] for i in range(1, len(cycle_path), 2)], key=lambda x: table[x[0]][x[1]])[0]
    min_el = table[min_el_coords[0]][min_el_coords[1]]
    # start and min cells' values changing:
    table[cycle_path[0][0]][cycle_path[0][1]] = min_el
    table[j2 := min_el_coords[0]][i2 := min_el_coords[1]] = None
    # updating rows_basis_cells and columns_basis_cells data:
    rows_basis_cells[j2].remove((j2, i2))
    columns_basis_cells[i2].remove((j2, i2))
    # cycle redistribution:
    for index, cell in enumerate(cycle_path):
        if cell != min_el_coords and index:
            if index % 2 == 0:
                table[cell[0]][cell[1]] += min_el
            else:
                table[cell[0]][cell[1]] -= min_el


def get_cycle_path(start_j, start_i, row_basis_cells, columns_basis_cells):
    get_cycle_path.cycle_path = []
    # start coords should be added to aux lists to make the methods below work, this cell will be basis one:
    row_basis_cells[start_j].append((start_j, start_i))
    columns_basis_cells[start_i].append((start_j, start_i))

    # cycle finding methods:
    def row_search(row, curr_path):
        # only the basis elements, not all the cells are counted:
        for cell in row_basis_cells[row]:
            if cell == (start_j, start_i) and len(curr_path) > 1:
                get_cycle_path.cycle_path = curr_path.copy()
                return
            if cell not in curr_path:
                column_search(cell[1], curr_path + [cell])

    def column_search(column, curr_path):
        # only the basis elements, not all the cells are counted:
        for cell in columns_basis_cells[column]:
            if cell == (start_j, start_i) and len(curr_path) > 1:
                get_cycle_path.cycle_path = curr_path.copy()
                return
            if cell not in curr_path:
                row_search(cell[0], curr_path + [cell])

    # start search:
    row_search(start_j, [(start_j, start_i)])
    # return a path found:
    return get_cycle_path.cycle_path


# auxiliary method for showing cycles:
def show_cycle(table, rows_basis_cells, cycle):
    np_table = reduce(
        lambda y, x: y + reduce(lambda m, n: m + ([table[n[0]][n[1]]] if table[n[0]][n[1]] is not None else []), x, []),
        rows_basis_cells, [])
    # print(f'np_table: {np_table}')
    # [[table[cell[0]][cell[1]] for cell in cells] for cells in rows_basis_cells]
    max_el = np.amax(np_table)
    max_length = len(str(max_el))
    table_copy = []
    # table copy creating:
    for j, row in enumerate(table):
        table_copy.append([])
        for el in row:
            if el is None:
                table_copy[j].append('N' * max_length)
            elif type(el) is int:
                table_copy[j].append(colour_(str(el) + ' ' * (max_length - len(str(el))), PURPLE, True))
            else:
                table_copy[j].append(el)
    # cycle elements changing:
    for i, step in enumerate(cycle):
        curr_j, curr_i = step
        if i == 0:
            table_copy[curr_j][curr_i] = colour_('S' + ' ' * (max_length - 1), YELLOW, True)
        elif i % 2 == 0:
            table_copy[curr_j][curr_i] = colour_('+' + ' ' * (max_length - 1), GREEN, True)
        else:
            table_copy[curr_j][curr_i] = colour_('-' + ' ' * (max_length - 1), CYAN, True)
        if i + 1 < len(cycle):
            connect_two(table_copy, cycle[i], cycle[i + 1], max_length)
        else:
            connect_two(table_copy, cycle[i], cycle[0], max_length)
    # table with cycle printing:
    for j, row in enumerate(table_copy):
        for i, el in enumerate(row):
            print(f'{el} ', end='')
        print()
    print(end='\n')


# aux method for connecting two table cells with '=' (horizontal case) or '|' (vertical case):
def connect_two(table, point1: tuple[int, int], point2: tuple[int, int], max_length):
    # defines a linking symbol:
    if point1[0] == point2[0]:
        symbol = colour_('=' * max_length, RED, True)
    else:
        symbol = colour_('|' + ' ' * (max_length - 1), RED, True)
    # building a neck:
    for j in range(m := min(point1[0], point2[0]), m + abs(point1[0] - point2[0]) + 1):
        for i in range(n := min(point1[1], point2[1]), n + abs(point1[1] - point2[1]) + 1):
            if (j, i) not in [point1, point2]:
                table[j][i] = symbol


def colour_(char, colour, flag=False):
    s = "\033[1m" if flag else ''
    return f"{(s + colour).format(char)}{END.format('')}"


# method for creating an example of closed transport task with parameters given:
def create_an_example(rows: int, columns: int, values_range=100):
    # preparing the supp and cons arrays:
    suppliers = [None for j in range(rows)]
    consumers = [None for i in range(columns)]
    # costs matrix building:
    costs = [[int(values_range * random.random()) for i in range(columns)] for j in range(rows)]
    # suppliers list filling:
    rem = values_range * (rows + columns)
    shuffled_rows = [row for row in range(rows)]
    random.shuffle(shuffled_rows)
    for ind, j in enumerate(shuffled_rows):
        suppliers[j] = np.random.randint(rem // int(math.sqrt(rows)) + 1) if ind != len(shuffled_rows) - 1 else rem
        # print(f'j, suppliers[j]: {j, suppliers[j]}')
        rem -= suppliers[j]
    # consumers list filling:
    rem = values_range * (rows + columns)
    shuffled_columns = [column for column in range(columns)]
    random.shuffle(shuffled_columns)
    for ind, i in enumerate(shuffled_columns):
        consumers[i] = np.random.randint(rem // int(math.sqrt(columns)) + 1) if ind != len(
            shuffled_columns) - 1 else rem
        # print(f'i, consumers[i]: {i, consumers[i]}')
        rem -= consumers[i]
    # returning the lists built:
    print(f'suppliers: {suppliers}')
    print(f'consumers: {consumers}')
    print(f'costs: ')
    for costs_row in costs:
        print(f'{costs_row}')

    return costs, suppliers, consumers


# an example:
costs_b, suppliers_b, consumers_b = create_an_example(35, 50)

# examples from codewars.com

# 1. degenerated case:
suppliers_d = [31, 50, 93, 11, 122, 172]
consumers_d = [86, 103, 177, 46, 1, 16, 30, 20]
costs_d = [
    [41, 1, 96, 37, 33, 80, 27, 68],
    [88, 22, 94, 90, 29, 87, 74, 19],
    [6, 12, 88, 21, 29, 83, 88, 82],
    [73, 94, 17, 77, 13, 95, 94, 77],
    [0, 71, 93, 21, 52, 61, 99, 37],
    [21, 23, 24, 44, 54, 29, 50, 97]
]

# 2. large case:
suppliers_x = [20, 28, 34, 96, 10, 4, 9, 55, 54, 127, 51, 27, 25, 92, 89, 6, 15, 6, 66, 44, 13, 58, 50, 81, 29, 86, 71,
               29, 1, 10, 17, 25, 65, 9, 20, 11, 197, 2, 145, 93, 22, 50, 2, 126, 18, 41, 42, 34, 19, 77, 10, 2, 4, 33,
               24, 52, 8, 92, 24, 44, 17, 127, 49, 13, 26, 83, 33, 24, 107, 103, 55, 5, 42, 28, 90, 55, 5, 100, 34, 29,
               104, 17, 119, 40, 42, 110, 20, 1, 5, 34, 9, 8, 26, 23, 26, 5, 13, 35, 9, 42, 136, 26, 71, 15, 85, 2, 22,
               3, 49, 22, 42, 64, 11, 5, 1, 10, 65, 58, 22, 4, 40, 27, 21, 21, 35, 3, 56, 6, 13, 13, 66, 22, 50, 21, 35,
               7, 14, 12, 60, 3, 23, 25, 56, 42, 53, 26, 50, 133, 29, 8]
consumers_x = [45, 1, 25, 32, 68, 22, 42, 1, 10, 68, 140, 134, 3, 15, 58, 21, 23, 3, 11, 21, 4, 8, 75, 50, 7, 15, 19,
               13, 1, 74, 27, 34, 48, 24, 14, 89, 31, 27, 11, 85, 209, 112, 96, 142, 13, 10, 18, 15, 6, 176, 105, 50,
               23, 7, 4, 75, 11, 1, 82, 122, 10, 8, 12, 9, 189, 56, 28, 24, 13, 74, 8, 7, 43, 35, 44, 27, 17, 8, 8, 10,
               35, 41, 16, 31, 15, 37, 19, 5, 1, 11, 42, 37, 20, 75, 106, 11, 88, 44, 2, 10, 1, 24, 72, 129, 40, 45, 5,
               32, 70, 19, 26, 19, 100, 30, 42, 2, 8, 33, 122, 8, 12, 14, 2, 29, 7, 90, 16, 51, 21, 55, 10, 25, 28, 50,
               27, 25, 12, 87, 37, 18, 124, 65, 19, 101, 78, 48, 80, 17, 35, 28]
costs_x = [
    [10, 93, 29, 95, 36, 41, 31, 32, 9, 35, 30, 92, 17, 90, 79, 94, 25, 24, 73, 38, 58, 71, 32, 50, 41, 43, 48, 38, 63,
     16, 99, 70, 84, 49, 90, 53, 19, 10, 16, 8, 29, 20, 91, 83, 21, 97, 69, 27, 60, 85, 49, 33, 17, 99, 27, 26, 77, 41,
     87, 19, 76, 4, 86, 22, 13, 55, 65, 15, 29, 84, 95, 29, 78, 33, 18, 68, 2, 55, 96, 27, 77, 4, 83, 84, 55, 97, 31,
     16, 2, 94, 34, 48, 15, 16, 88, 52, 97, 31, 90, 48, 58, 78, 80, 45, 98, 13, 16, 38, 90, 5, 97, 60, 34, 91, 1, 88,
     87, 52, 97, 32, 44, 4, 52, 88, 29, 3, 98, 51, 61, 37, 74, 16, 84, 22, 23, 17, 17, 52, 44, 64, 82, 29, 68, 6, 60,
     77, 59, 54, 85, 88],
    [24, 4, 43, 60, 35, 10, 37, 55, 59, 72, 40, 21, 19, 6, 0, 55, 60, 58, 72, 86, 50, 85, 11, 47, 84, 38, 48, 39, 71, 6,
     43, 49, 88, 88, 78, 33, 6, 63, 22, 42, 76, 63, 35, 1, 72, 21, 99, 0, 47, 36, 70, 81, 51, 2, 46, 15, 75, 81, 99, 18,
     34, 85, 96, 26, 27, 91, 67, 45, 23, 84, 99, 91, 95, 43, 14, 66, 16, 17, 62, 63, 42, 59, 70, 92, 59, 98, 30, 28, 12,
     59, 0, 78, 39, 70, 61, 88, 27, 36, 54, 19, 21, 44, 60, 8, 38, 96, 92, 56, 78, 75, 99, 29, 43, 43, 32, 57, 93, 41,
     32, 75, 54, 59, 50, 98, 0, 60, 28, 1, 5, 60, 69, 77, 72, 5, 47, 98, 82, 52, 51, 63, 43, 29, 7, 6, 45, 56, 36, 52,
     85, 71],
    [87, 49, 18, 95, 12, 22, 80, 0, 33, 32, 73, 9, 14, 87, 68, 70, 38, 64, 93, 50, 14, 9, 41, 45, 32, 19, 25, 83, 70,
     84, 61, 56, 20, 74, 77, 10, 67, 30, 3, 23, 24, 16, 26, 8, 92, 29, 95, 5, 51, 22, 57, 11, 47, 84, 11, 42, 28, 77,
     43, 92, 75, 45, 15, 96, 71, 20, 63, 74, 7, 90, 38, 83, 58, 45, 12, 26, 41, 2, 17, 49, 79, 46, 87, 75, 60, 62, 62,
     47, 88, 12, 72, 8, 72, 68, 40, 22, 0, 74, 24, 77, 17, 66, 90, 85, 14, 52, 35, 3, 17, 36, 30, 16, 90, 9, 24, 14, 55,
     16, 74, 44, 33, 93, 20, 2, 53, 82, 46, 3, 8, 3, 76, 79, 39, 41, 83, 46, 55, 76, 83, 15, 95, 74, 29, 88, 37, 73, 37,
     72, 2, 25],
    [90, 52, 34, 13, 49, 91, 43, 25, 87, 43, 76, 45, 10, 70, 37, 76, 55, 17, 88, 61, 96, 72, 3, 4, 3, 79, 97, 81, 49,
     95, 72, 10, 71, 99, 95, 20, 35, 85, 98, 47, 20, 0, 22, 49, 61, 67, 6, 55, 35, 81, 27, 43, 5, 19, 1, 50, 69, 39, 5,
     35, 97, 60, 33, 35, 33, 51, 3, 93, 96, 38, 86, 28, 36, 81, 37, 13, 51, 19, 80, 62, 63, 76, 85, 22, 35, 57, 22, 53,
     55, 43, 47, 29, 83, 71, 95, 56, 80, 30, 6, 75, 33, 50, 89, 7, 89, 56, 36, 72, 56, 64, 15, 0, 78, 84, 82, 46, 91,
     19, 26, 60, 21, 92, 63, 87, 72, 76, 59, 39, 92, 75, 26, 82, 40, 68, 76, 96, 30, 77, 40, 36, 44, 0, 33, 94, 18, 30,
     1, 62, 81, 0],
    [39, 48, 21, 31, 45, 65, 7, 41, 80, 39, 82, 62, 92, 71, 36, 51, 62, 43, 58, 51, 53, 49, 62, 3, 83, 81, 29, 26, 41,
     56, 37, 49, 41, 16, 81, 22, 13, 95, 2, 91, 27, 61, 45, 31, 22, 93, 82, 62, 42, 99, 6, 10, 64, 66, 53, 64, 84, 21,
     51, 21, 45, 58, 74, 9, 46, 98, 42, 63, 92, 52, 6, 75, 71, 15, 37, 10, 35, 80, 62, 63, 80, 87, 91, 10, 27, 31, 79,
     84, 28, 36, 55, 63, 78, 46, 47, 38, 17, 22, 39, 87, 95, 43, 60, 75, 65, 41, 86, 31, 4, 10, 86, 84, 99, 53, 97, 67,
     65, 22, 56, 10, 48, 1, 48, 45, 29, 43, 41, 48, 99, 93, 60, 97, 83, 94, 35, 34, 44, 22, 90, 50, 22, 76, 47, 38, 20,
     32, 97, 27, 64, 24],
    [2, 13, 48, 4, 25, 6, 6, 23, 80, 43, 80, 62, 20, 55, 63, 3, 8, 96, 55, 14, 87, 8, 25, 79, 66, 99, 30, 81, 4, 38, 96,
     47, 79, 11, 64, 9, 25, 24, 31, 37, 3, 15, 88, 13, 78, 65, 40, 29, 77, 63, 9, 90, 90, 27, 47, 26, 76, 88, 12, 92,
     97, 86, 29, 90, 65, 95, 54, 93, 35, 43, 88, 86, 65, 68, 51, 8, 44, 41, 27, 90, 99, 90, 10, 45, 56, 56, 20, 61, 89,
     21, 33, 76, 43, 67, 32, 93, 14, 37, 34, 24, 48, 6, 0, 93, 25, 28, 78, 41, 67, 55, 1, 32, 85, 89, 28, 62, 91, 20,
     59, 87, 66, 92, 34, 73, 78, 48, 98, 83, 14, 9, 59, 70, 68, 66, 10, 64, 47, 46, 26, 64, 57, 24, 31, 27, 65, 86, 61,
     66, 83, 23],
    [16, 79, 0, 96, 22, 42, 83, 49, 53, 45, 60, 74, 28, 45, 99, 15, 75, 39, 27, 47, 51, 67, 41, 31, 50, 7, 76, 10, 18,
     29, 69, 38, 10, 55, 83, 35, 86, 37, 4, 65, 36, 98, 39, 95, 96, 75, 62, 48, 74, 48, 2, 56, 61, 10, 86, 80, 83, 65,
     22, 51, 86, 92, 87, 97, 50, 26, 45, 85, 82, 44, 51, 41, 96, 8, 52, 32, 87, 19, 11, 0, 57, 32, 22, 68, 67, 59, 93,
     91, 45, 70, 76, 58, 62, 6, 59, 14, 87, 21, 92, 74, 18, 91, 75, 12, 8, 41, 6, 61, 36, 27, 28, 30, 91, 90, 24, 80,
     91, 53, 93, 71, 87, 56, 62, 67, 47, 90, 49, 22, 56, 13, 60, 98, 84, 54, 66, 14, 95, 8, 35, 1, 27, 18, 89, 54, 0,
     98, 28, 39, 35, 6],
    [56, 16, 95, 74, 39, 73, 20, 95, 12, 39, 61, 61, 10, 61, 7, 48, 84, 79, 46, 69, 33, 57, 73, 71, 80, 61, 27, 53, 17,
     97, 72, 96, 67, 75, 80, 72, 40, 85, 45, 93, 64, 51, 86, 38, 18, 65, 55, 15, 72, 78, 70, 15, 74, 26, 29, 66, 80, 12,
     74, 70, 73, 86, 27, 45, 26, 6, 44, 74, 26, 50, 51, 32, 97, 19, 40, 9, 66, 69, 93, 79, 95, 63, 66, 38, 38, 70, 23,
     63, 33, 95, 12, 36, 39, 7, 94, 18, 35, 19, 4, 41, 18, 94, 1, 6, 30, 61, 72, 5, 59, 32, 70, 85, 60, 73, 33, 88, 90,
     3, 56, 6, 36, 77, 33, 19, 99, 72, 25, 80, 79, 6, 37, 79, 94, 3, 68, 83, 61, 32, 2, 82, 30, 67, 68, 2, 64, 31, 48,
     36, 45, 11],
    [90, 38, 51, 96, 21, 96, 29, 12, 46, 79, 57, 47, 27, 18, 88, 79, 52, 16, 89, 27, 80, 86, 52, 87, 58, 67, 13, 15, 79,
     41, 30, 96, 75, 26, 68, 82, 5, 22, 29, 69, 94, 14, 34, 41, 85, 60, 78, 99, 39, 5, 24, 98, 44, 79, 63, 64, 74, 79,
     26, 86, 45, 59, 55, 38, 82, 50, 13, 44, 18, 47, 20, 16, 95, 4, 65, 23, 87, 40, 63, 43, 72, 98, 47, 70, 21, 27, 53,
     6, 3, 36, 15, 18, 15, 87, 46, 82, 29, 47, 11, 69, 25, 67, 10, 23, 56, 20, 5, 81, 25, 70, 29, 78, 65, 96, 48, 59,
     63, 93, 64, 9, 64, 19, 32, 37, 0, 2, 40, 43, 97, 44, 49, 46, 60, 69, 1, 79, 45, 66, 96, 39, 47, 91, 51, 68, 58, 97,
     53, 72, 93, 66],
    [7, 89, 83, 39, 88, 58, 35, 80, 30, 32, 45, 82, 62, 27, 42, 52, 93, 3, 61, 95, 63, 44, 93, 46, 88, 47, 53, 4, 64,
     77, 71, 83, 97, 17, 90, 48, 53, 33, 60, 31, 38, 85, 17, 42, 9, 52, 28, 14, 26, 57, 65, 34, 40, 40, 57, 20, 43, 1,
     25, 10, 44, 31, 87, 26, 78, 62, 83, 18, 51, 4, 42, 47, 66, 99, 89, 76, 74, 88, 80, 7, 36, 65, 92, 82, 68, 63, 51,
     20, 29, 63, 18, 27, 73, 22, 33, 28, 51, 87, 24, 72, 44, 50, 76, 14, 32, 39, 80, 16, 82, 34, 19, 60, 34, 22, 24, 66,
     61, 36, 53, 36, 31, 62, 90, 78, 82, 75, 29, 78, 85, 44, 99, 2, 88, 73, 17, 13, 67, 89, 38, 86, 53, 57, 54, 80, 60,
     26, 80, 13, 29, 59],
    [57, 27, 6, 66, 67, 45, 75, 82, 64, 31, 47, 70, 91, 30, 58, 27, 41, 73, 90, 40, 11, 32, 12, 14, 8, 46, 48, 16, 78,
     93, 83, 59, 67, 56, 28, 29, 23, 91, 85, 78, 8, 5, 66, 82, 53, 61, 29, 71, 16, 70, 22, 94, 6, 1, 51, 85, 77, 95, 34,
     64, 31, 37, 84, 11, 87, 99, 50, 60, 55, 23, 79, 5, 63, 73, 30, 71, 68, 13, 71, 37, 11, 32, 55, 34, 57, 97, 44, 60,
     9, 71, 15, 93, 4, 82, 68, 11, 32, 30, 6, 36, 6, 16, 23, 43, 89, 9, 1, 31, 34, 97, 0, 29, 89, 35, 63, 82, 37, 99,
     38, 68, 59, 95, 44, 65, 47, 28, 66, 18, 57, 15, 33, 82, 19, 78, 34, 99, 63, 30, 26, 55, 43, 13, 31, 9, 54, 2, 61,
     65, 26, 8],
    [25, 1, 23, 20, 44, 16, 60, 14, 42, 25, 25, 36, 56, 90, 55, 32, 37, 97, 67, 78, 4, 93, 81, 91, 62, 56, 65, 99, 54,
     0, 28, 94, 40, 6, 73, 51, 71, 17, 7, 16, 84, 72, 87, 16, 21, 57, 11, 9, 33, 86, 35, 5, 50, 4, 88, 30, 10, 46, 41,
     72, 24, 45, 99, 15, 2, 37, 16, 94, 34, 64, 6, 75, 31, 47, 76, 78, 83, 21, 44, 54, 98, 8, 71, 89, 80, 31, 54, 92,
     37, 15, 76, 51, 79, 71, 54, 66, 64, 98, 1, 71, 86, 83, 58, 78, 69, 9, 22, 3, 27, 75, 46, 2, 49, 79, 17, 75, 31, 99,
     39, 74, 94, 1, 87, 94, 63, 65, 81, 49, 16, 57, 10, 14, 97, 68, 92, 16, 46, 60, 12, 37, 48, 25, 76, 31, 94, 6, 54,
     30, 19, 25],
    [47, 31, 1, 17, 39, 46, 68, 67, 16, 7, 11, 9, 82, 71, 62, 34, 41, 46, 25, 55, 62, 74, 63, 95, 77, 40, 33, 60, 41, 8,
     11, 21, 12, 82, 97, 15, 16, 14, 27, 45, 68, 59, 60, 88, 62, 89, 15, 6, 26, 63, 78, 8, 15, 82, 52, 33, 33, 35, 80,
     96, 62, 68, 22, 38, 74, 66, 20, 72, 13, 13, 86, 60, 6, 69, 70, 72, 41, 64, 79, 92, 82, 86, 56, 39, 44, 52, 0, 13,
     67, 74, 21, 1, 45, 25, 4, 66, 34, 7, 76, 27, 50, 5, 59, 50, 55, 79, 85, 74, 78, 17, 24, 78, 13, 70, 71, 3, 35, 37,
     86, 78, 75, 36, 57, 85, 43, 26, 45, 35, 99, 58, 95, 7, 44, 66, 33, 27, 5, 73, 0, 18, 82, 54, 92, 80, 46, 38, 67,
     76, 8, 12],
    [96, 67, 92, 75, 76, 89, 90, 39, 97, 8, 82, 60, 51, 33, 73, 4, 64, 27, 22, 54, 36, 6, 80, 96, 79, 26, 23, 24, 52,
     36, 79, 88, 41, 28, 20, 63, 6, 68, 49, 76, 52, 96, 65, 49, 19, 41, 17, 55, 98, 8, 96, 89, 41, 42, 5, 67, 68, 25, 5,
     41, 21, 54, 21, 90, 66, 97, 78, 72, 78, 58, 33, 41, 92, 25, 30, 58, 65, 92, 31, 71, 28, 46, 43, 25, 71, 19, 34, 33,
     78, 21, 46, 77, 72, 91, 72, 43, 62, 42, 78, 33, 12, 62, 86, 18, 25, 49, 45, 77, 75, 79, 89, 98, 65, 4, 17, 61, 77,
     64, 4, 53, 44, 66, 66, 82, 73, 40, 3, 66, 29, 15, 95, 49, 36, 72, 47, 54, 98, 84, 69, 7, 52, 91, 8, 80, 78, 6, 58,
     97, 7, 38],
    [14, 99, 10, 98, 28, 86, 35, 90, 58, 82, 20, 27, 3, 84, 98, 56, 41, 54, 67, 72, 20, 2, 1, 62, 12, 56, 89, 63, 95, 8,
     77, 32, 48, 36, 46, 81, 83, 67, 40, 42, 54, 12, 3, 78, 47, 24, 80, 90, 71, 26, 84, 92, 97, 50, 12, 89, 19, 19, 96,
     33, 23, 94, 62, 54, 73, 90, 1, 97, 15, 40, 95, 37, 28, 20, 45, 94, 8, 34, 44, 55, 47, 94, 12, 41, 4, 39, 96, 89,
     88, 81, 32, 5, 72, 69, 80, 77, 81, 71, 99, 92, 46, 31, 96, 10, 40, 9, 11, 0, 21, 7, 76, 3, 2, 0, 99, 63, 99, 84,
     59, 97, 32, 91, 90, 47, 45, 82, 88, 8, 15, 76, 84, 32, 15, 5, 32, 12, 25, 58, 74, 0, 73, 97, 84, 42, 82, 57, 98, 5,
     10, 33],
    [66, 74, 99, 9, 73, 46, 23, 41, 5, 40, 85, 61, 37, 67, 47, 55, 24, 20, 33, 87, 4, 25, 71, 14, 40, 53, 93, 90, 1, 7,
     98, 91, 57, 79, 61, 86, 16, 71, 96, 64, 50, 12, 64, 4, 9, 15, 88, 75, 40, 89, 73, 1, 33, 58, 33, 92, 42, 26, 4, 1,
     88, 28, 27, 14, 95, 76, 67, 0, 35, 56, 6, 82, 79, 7, 55, 31, 21, 81, 50, 71, 11, 67, 9, 90, 72, 20, 15, 28, 93, 16,
     13, 66, 14, 35, 61, 17, 20, 25, 46, 1, 16, 57, 29, 69, 15, 61, 49, 23, 76, 82, 36, 47, 68, 84, 57, 25, 58, 1, 91,
     74, 55, 25, 35, 97, 42, 55, 64, 99, 5, 97, 96, 43, 57, 49, 48, 24, 18, 1, 51, 60, 76, 41, 95, 96, 71, 56, 18, 50,
     68, 69],
    [74, 72, 78, 71, 4, 33, 54, 27, 18, 27, 51, 58, 39, 22, 7, 38, 67, 56, 69, 76, 11, 89, 97, 31, 52, 29, 77, 96, 39,
     87, 25, 36, 25, 10, 21, 28, 26, 18, 14, 10, 26, 4, 85, 39, 49, 31, 32, 25, 81, 53, 94, 86, 8, 12, 29, 97, 83, 4,
     35, 35, 81, 51, 7, 79, 56, 75, 62, 48, 22, 64, 86, 29, 97, 48, 46, 82, 59, 71, 44, 11, 74, 17, 49, 27, 29, 38, 44,
     3, 76, 91, 16, 59, 89, 93, 57, 74, 24, 74, 73, 35, 93, 94, 81, 8, 16, 78, 14, 73, 67, 76, 29, 83, 50, 95, 93, 69,
     30, 68, 81, 56, 1, 64, 29, 54, 32, 49, 87, 5, 16, 5, 19, 59, 65, 34, 28, 12, 96, 88, 19, 24, 26, 64, 73, 27, 29,
     24, 76, 75, 21, 92],
    [49, 3, 15, 46, 69, 73, 46, 47, 93, 37, 26, 25, 41, 84, 66, 35, 17, 0, 66, 15, 54, 57, 74, 31, 94, 10, 22, 15, 68,
     3, 46, 27, 66, 94, 25, 22, 60, 68, 52, 60, 3, 42, 74, 89, 68, 91, 20, 53, 71, 4, 17, 7, 8, 2, 26, 24, 96, 35, 88,
     39, 42, 54, 63, 95, 90, 87, 81, 58, 74, 10, 85, 18, 31, 18, 30, 34, 42, 42, 93, 52, 49, 71, 1, 21, 29, 88, 35, 24,
     88, 36, 36, 59, 10, 46, 91, 92, 37, 27, 43, 57, 47, 70, 33, 12, 53, 48, 25, 21, 32, 78, 84, 23, 76, 88, 43, 31, 90,
     77, 33, 24, 58, 83, 20, 77, 10, 85, 45, 98, 63, 45, 15, 65, 60, 76, 36, 31, 68, 47, 84, 35, 2, 64, 20, 13, 54, 93,
     12, 71, 28, 57],
    [45, 26, 97, 32, 73, 13, 72, 2, 37, 53, 24, 56, 89, 8, 29, 23, 18, 63, 26, 51, 33, 73, 56, 99, 96, 17, 33, 25, 3,
     77, 1, 10, 35, 58, 56, 94, 47, 6, 49, 65, 65, 51, 81, 85, 71, 35, 21, 46, 0, 47, 67, 30, 97, 75, 28, 97, 94, 62,
     35, 53, 82, 93, 3, 36, 45, 36, 53, 48, 97, 10, 32, 38, 25, 94, 67, 56, 27, 24, 95, 43, 14, 97, 83, 64, 54, 4, 30,
     95, 63, 36, 62, 38, 13, 40, 95, 59, 8, 87, 12, 31, 49, 24, 9, 87, 81, 83, 94, 81, 34, 91, 81, 36, 70, 82, 13, 24,
     9, 6, 75, 45, 2, 31, 70, 59, 75, 12, 82, 70, 93, 43, 71, 22, 56, 45, 42, 94, 7, 31, 27, 38, 60, 36, 91, 31, 38, 26,
     60, 90, 9, 65],
    [89, 94, 78, 41, 47, 32, 38, 39, 77, 62, 76, 36, 32, 79, 60, 43, 16, 88, 57, 5, 3, 73, 47, 8, 46, 97, 11, 5, 2, 67,
     3, 81, 35, 65, 19, 75, 60, 69, 21, 74, 64, 79, 5, 59, 60, 2, 18, 71, 31, 63, 79, 94, 74, 13, 91, 10, 29, 63, 58,
     14, 0, 44, 42, 71, 72, 85, 82, 95, 27, 40, 88, 7, 52, 13, 27, 91, 82, 23, 78, 59, 89, 54, 89, 32, 96, 83, 83, 6,
     25, 14, 70, 2, 43, 76, 93, 11, 47, 10, 33, 37, 7, 16, 61, 72, 68, 51, 63, 11, 96, 51, 26, 80, 2, 78, 37, 96, 73, 9,
     47, 48, 53, 54, 9, 75, 16, 69, 49, 86, 32, 53, 34, 72, 26, 48, 64, 84, 83, 50, 96, 33, 87, 68, 90, 6, 66, 62, 59,
     82, 56, 88],
    [31, 94, 59, 48, 45, 21, 82, 50, 4, 11, 34, 28, 52, 11, 42, 90, 57, 31, 34, 91, 29, 28, 10, 11, 21, 40, 14, 65, 51,
     35, 34, 94, 46, 95, 93, 1, 28, 96, 17, 12, 10, 71, 10, 47, 53, 87, 83, 84, 68, 6, 32, 46, 69, 76, 24, 68, 62, 13,
     80, 30, 55, 30, 66, 12, 76, 0, 23, 66, 84, 4, 12, 22, 10, 99, 0, 56, 60, 0, 87, 18, 74, 81, 71, 71, 89, 22, 57, 23,
     36, 1, 97, 51, 58, 98, 78, 34, 67, 50, 73, 8, 11, 66, 50, 7, 13, 93, 58, 38, 20, 44, 39, 7, 71, 50, 76, 24, 53, 51,
     2, 22, 76, 44, 53, 82, 91, 67, 32, 88, 30, 94, 79, 9, 36, 7, 1, 62, 92, 34, 97, 84, 85, 89, 81, 92, 15, 80, 7, 94,
     28, 99],
    [30, 36, 67, 89, 52, 7, 89, 53, 51, 44, 31, 26, 70, 70, 76, 83, 38, 21, 87, 13, 37, 14, 90, 5, 93, 21, 76, 18, 50,
     86, 55, 88, 79, 4, 73, 62, 9, 58, 86, 13, 73, 3, 62, 40, 69, 6, 76, 45, 98, 95, 89, 30, 55, 49, 38, 57, 62, 32, 35,
     55, 5, 40, 46, 75, 90, 92, 11, 48, 93, 39, 78, 9, 97, 56, 29, 84, 21, 76, 29, 6, 0, 38, 40, 70, 88, 63, 70, 89, 69,
     14, 99, 47, 96, 37, 49, 26, 93, 6, 3, 41, 91, 93, 10, 80, 36, 15, 91, 72, 25, 38, 54, 19, 67, 28, 64, 44, 47, 99,
     4, 5, 13, 68, 35, 25, 12, 43, 92, 91, 33, 33, 5, 9, 37, 44, 66, 99, 51, 23, 60, 43, 0, 90, 64, 11, 73, 3, 0, 57, 6,
     46],
    [99, 56, 31, 61, 17, 78, 42, 17, 22, 80, 45, 85, 97, 37, 69, 54, 92, 7, 61, 5, 89, 63, 26, 85, 52, 11, 36, 83, 17,
     23, 58, 53, 60, 79, 57, 88, 82, 72, 19, 12, 80, 80, 89, 24, 32, 9, 20, 90, 78, 75, 27, 64, 78, 23, 87, 0, 43, 95,
     67, 29, 72, 17, 37, 11, 37, 16, 61, 39, 74, 11, 35, 31, 59, 23, 11, 80, 55, 27, 73, 84, 7, 29, 27, 98, 74, 10, 97,
     1, 17, 26, 46, 1, 3, 21, 28, 32, 83, 27, 75, 26, 22, 54, 92, 89, 66, 2, 66, 5, 69, 78, 86, 13, 72, 12, 26, 9, 32,
     45, 84, 65, 33, 24, 18, 6, 16, 12, 45, 22, 90, 75, 48, 49, 77, 24, 73, 34, 44, 85, 22, 71, 48, 81, 11, 8, 41, 84,
     11, 12, 65, 15],
    [35, 97, 66, 1, 54, 5, 91, 40, 57, 61, 16, 25, 7, 97, 49, 97, 41, 46, 67, 83, 76, 85, 33, 92, 27, 31, 96, 76, 16,
     78, 16, 24, 14, 31, 38, 69, 17, 25, 66, 46, 63, 2, 52, 49, 51, 85, 26, 59, 83, 37, 50, 35, 89, 90, 47, 95, 0, 34,
     11, 48, 79, 36, 86, 47, 60, 85, 26, 21, 4, 29, 55, 69, 61, 57, 87, 93, 38, 10, 73, 18, 75, 16, 3, 90, 57, 29, 84,
     98, 3, 31, 69, 16, 67, 61, 68, 94, 48, 34, 38, 12, 22, 9, 39, 23, 12, 14, 54, 90, 20, 48, 57, 66, 1, 36, 76, 78,
     36, 7, 6, 41, 21, 29, 35, 74, 22, 96, 64, 53, 19, 60, 65, 23, 86, 92, 61, 24, 68, 50, 2, 4, 33, 86, 95, 98, 9, 39,
     22, 3, 22, 72],
    [23, 83, 33, 64, 32, 91, 18, 40, 36, 83, 35, 49, 99, 23, 9, 7, 44, 36, 84, 90, 16, 62, 66, 82, 12, 43, 97, 76, 30,
     76, 17, 29, 98, 71, 24, 56, 22, 26, 36, 91, 22, 4, 21, 19, 47, 58, 79, 98, 62, 31, 62, 98, 54, 19, 81, 9, 48, 4, 3,
     43, 93, 6, 78, 71, 98, 20, 41, 52, 20, 77, 71, 90, 4, 16, 80, 0, 16, 51, 4, 29, 25, 60, 65, 81, 9, 13, 62, 98, 46,
     19, 77, 36, 83, 65, 73, 57, 14, 79, 83, 61, 43, 84, 49, 99, 1, 87, 10, 4, 10, 6, 81, 16, 59, 88, 77, 15, 72, 12,
     68, 6, 97, 33, 9, 90, 16, 29, 17, 43, 46, 79, 13, 40, 98, 93, 1, 24, 36, 16, 99, 64, 53, 61, 32, 51, 80, 11, 33,
     38, 98, 16],
    [11, 65, 40, 42, 89, 48, 99, 56, 83, 63, 20, 3, 94, 11, 34, 30, 3, 79, 47, 29, 33, 36, 43, 98, 93, 45, 5, 34, 33,
     32, 93, 42, 66, 36, 72, 80, 12, 47, 91, 97, 45, 0, 31, 60, 24, 46, 10, 46, 59, 38, 16, 67, 19, 76, 35, 75, 70, 90,
     2, 66, 43, 1, 70, 65, 90, 11, 76, 26, 18, 7, 49, 72, 63, 14, 1, 68, 11, 13, 5, 30, 39, 18, 61, 12, 82, 23, 27, 93,
     35, 90, 69, 63, 4, 89, 14, 9, 37, 73, 64, 86, 86, 32, 88, 41, 90, 37, 92, 69, 2, 93, 64, 73, 85, 52, 81, 35, 61,
     27, 74, 56, 41, 55, 91, 86, 82, 87, 10, 83, 12, 33, 29, 37, 78, 28, 25, 16, 27, 68, 45, 14, 51, 81, 83, 63, 39, 90,
     97, 79, 33, 80],
    [26, 45, 19, 87, 5, 32, 0, 9, 23, 25, 94, 69, 78, 82, 15, 3, 30, 25, 79, 84, 60, 39, 73, 20, 46, 80, 19, 45, 25, 39,
     96, 0, 42, 88, 15, 68, 48, 50, 94, 65, 53, 10, 41, 99, 22, 28, 93, 1, 12, 97, 41, 10, 21, 73, 18, 76, 12, 56, 79,
     5, 33, 27, 18, 7, 91, 31, 56, 81, 45, 43, 48, 54, 83, 88, 90, 88, 1, 72, 53, 63, 33, 83, 14, 5, 15, 0, 46, 33, 22,
     37, 87, 61, 20, 31, 47, 78, 94, 49, 4, 0, 78, 2, 78, 4, 33, 3, 88, 58, 52, 95, 68, 34, 52, 94, 84, 59, 30, 41, 70,
     23, 56, 13, 20, 50, 12, 26, 17, 35, 14, 31, 32, 68, 98, 75, 63, 37, 52, 61, 62, 11, 63, 70, 59, 59, 31, 80, 30, 64,
     82, 77],
    [41, 40, 61, 20, 9, 15, 97, 44, 57, 56, 32, 78, 74, 9, 43, 75, 75, 48, 17, 63, 74, 28, 60, 28, 40, 28, 96, 63, 7,
     19, 67, 0, 35, 0, 42, 71, 71, 1, 13, 54, 62, 87, 50, 3, 82, 19, 26, 2, 52, 42, 16, 89, 14, 15, 7, 81, 8, 62, 58,
     19, 40, 49, 60, 91, 51, 35, 70, 0, 85, 53, 24, 41, 3, 89, 36, 48, 58, 73, 18, 19, 76, 53, 53, 12, 99, 71, 95, 87,
     33, 34, 83, 90, 38, 74, 11, 83, 69, 67, 45, 58, 61, 63, 35, 12, 5, 72, 96, 95, 67, 56, 12, 6, 17, 12, 13, 36, 98,
     86, 46, 32, 2, 73, 54, 11, 89, 29, 41, 75, 29, 81, 72, 32, 32, 55, 7, 68, 62, 35, 90, 11, 1, 87, 4, 36, 56, 13, 18,
     84, 37, 13],
    [82, 56, 62, 67, 56, 28, 0, 46, 0, 26, 20, 10, 48, 92, 13, 1, 80, 27, 87, 33, 48, 7, 64, 37, 66, 37, 60, 88, 76, 57,
     80, 42, 19, 69, 18, 33, 32, 47, 98, 38, 78, 73, 65, 70, 27, 57, 84, 64, 45, 67, 91, 50, 77, 60, 10, 45, 94, 11, 13,
     70, 7, 86, 37, 34, 74, 46, 83, 3, 90, 63, 7, 9, 99, 33, 82, 25, 85, 61, 26, 11, 93, 46, 65, 93, 78, 56, 90, 28, 2,
     73, 83, 56, 49, 91, 17, 67, 37, 60, 46, 82, 87, 96, 39, 44, 48, 5, 40, 31, 14, 55, 0, 9, 28, 21, 50, 40, 83, 7, 93,
     68, 74, 0, 89, 78, 85, 56, 33, 81, 61, 35, 54, 75, 18, 76, 98, 73, 82, 2, 38, 71, 65, 67, 61, 60, 80, 34, 42, 75,
     20, 97],
    [54, 84, 64, 37, 61, 34, 1, 71, 18, 25, 73, 85, 56, 94, 48, 42, 27, 44, 63, 13, 68, 51, 74, 22, 92, 42, 12, 67, 52,
     25, 32, 82, 77, 99, 55, 38, 48, 72, 96, 92, 94, 99, 53, 56, 59, 66, 57, 57, 52, 74, 44, 89, 38, 46, 27, 4, 21, 26,
     51, 95, 11, 1, 66, 22, 40, 28, 24, 87, 24, 19, 73, 34, 97, 37, 52, 43, 78, 60, 43, 6, 17, 41, 18, 4, 15, 7, 96, 79,
     5, 74, 2, 86, 62, 1, 95, 86, 14, 56, 2, 97, 40, 90, 49, 83, 88, 95, 59, 45, 97, 13, 62, 82, 65, 75, 33, 89, 2, 32,
     22, 41, 49, 57, 39, 68, 8, 58, 64, 34, 66, 87, 55, 8, 83, 65, 27, 86, 28, 98, 5, 3, 53, 67, 64, 90, 72, 54, 22, 14,
     84, 66],
    [50, 0, 63, 48, 64, 63, 12, 60, 1, 53, 36, 46, 0, 92, 81, 40, 98, 20, 55, 21, 53, 55, 61, 75, 0, 22, 61, 39, 14, 6,
     31, 77, 58, 60, 8, 26, 97, 15, 32, 47, 23, 95, 98, 63, 11, 72, 65, 95, 52, 77, 61, 1, 89, 57, 44, 50, 29, 70, 64,
     0, 99, 1, 56, 76, 27, 8, 47, 64, 86, 63, 33, 49, 12, 37, 98, 58, 29, 60, 82, 93, 62, 67, 71, 65, 68, 49, 48, 85, 9,
     91, 25, 25, 88, 99, 62, 95, 37, 30, 67, 85, 95, 79, 62, 79, 69, 71, 89, 1, 33, 72, 74, 45, 96, 28, 4, 29, 35, 93,
     19, 51, 38, 0, 58, 41, 86, 23, 79, 14, 84, 21, 49, 60, 36, 28, 29, 10, 4, 88, 6, 93, 91, 4, 38, 37, 49, 64, 28, 76,
     30, 99],
    [61, 84, 0, 39, 94, 56, 56, 66, 65, 60, 96, 26, 26, 63, 31, 10, 76, 65, 79, 7, 67, 70, 58, 73, 80, 89, 87, 95, 21,
     22, 13, 46, 96, 59, 75, 61, 20, 43, 19, 54, 41, 88, 67, 1, 79, 36, 11, 46, 45, 69, 90, 12, 9, 26, 9, 60, 59, 34, 4,
     63, 72, 39, 76, 90, 2, 52, 62, 30, 70, 82, 20, 83, 36, 84, 89, 62, 12, 66, 37, 52, 56, 89, 51, 60, 81, 56, 78, 71,
     95, 14, 1, 67, 85, 45, 66, 72, 50, 0, 63, 53, 75, 3, 7, 43, 88, 4, 78, 37, 81, 15, 77, 10, 22, 85, 21, 42, 68, 48,
     36, 35, 59, 73, 12, 38, 86, 75, 64, 45, 39, 44, 78, 67, 87, 47, 11, 94, 0, 94, 31, 0, 86, 85, 90, 11, 48, 90, 58,
     75, 16, 86],
    [34, 65, 22, 96, 10, 58, 73, 87, 5, 45, 28, 97, 60, 41, 64, 50, 11, 65, 1, 5, 24, 65, 3, 94, 20, 68, 46, 26, 21, 44,
     10, 78, 99, 26, 35, 37, 26, 96, 91, 76, 25, 26, 62, 51, 43, 24, 27, 55, 31, 70, 74, 47, 88, 12, 0, 94, 60, 6, 73,
     39, 71, 24, 98, 14, 72, 78, 53, 32, 71, 8, 80, 52, 78, 20, 96, 59, 46, 47, 3, 47, 78, 23, 50, 10, 40, 45, 43, 33,
     99, 48, 15, 76, 42, 33, 30, 57, 1, 80, 33, 46, 14, 92, 30, 52, 66, 37, 96, 73, 89, 76, 85, 2, 94, 4, 37, 21, 23,
     34, 82, 31, 51, 79, 22, 20, 19, 19, 69, 48, 72, 19, 53, 22, 89, 1, 83, 92, 49, 19, 78, 75, 57, 22, 0, 52, 26, 34,
     6, 23, 40, 87],
    [57, 40, 57, 34, 30, 84, 40, 49, 25, 27, 65, 41, 91, 48, 24, 91, 69, 96, 51, 44, 86, 16, 96, 63, 85, 98, 64, 19, 26,
     72, 45, 2, 15, 21, 90, 6, 20, 61, 3, 72, 48, 79, 89, 47, 40, 12, 97, 63, 96, 84, 33, 49, 77, 65, 91, 89, 98, 36,
     54, 61, 89, 31, 65, 6, 74, 94, 64, 97, 18, 59, 81, 17, 39, 26, 9, 43, 62, 89, 26, 85, 34, 65, 91, 24, 6, 23, 35,
     83, 23, 94, 30, 80, 53, 48, 58, 6, 9, 4, 39, 65, 74, 70, 29, 41, 77, 21, 15, 73, 42, 90, 91, 32, 88, 95, 31, 66,
     47, 25, 29, 97, 19, 24, 75, 42, 52, 46, 69, 68, 66, 51, 57, 54, 3, 54, 80, 33, 91, 41, 5, 86, 21, 26, 91, 30, 69,
     17, 16, 5, 54, 7],
    [38, 40, 38, 88, 42, 54, 95, 37, 15, 85, 16, 82, 45, 46, 62, 76, 68, 16, 77, 4, 83, 67, 9, 32, 53, 13, 3, 96, 43,
     98, 37, 65, 94, 42, 94, 74, 21, 72, 70, 2, 53, 88, 25, 85, 13, 42, 67, 65, 34, 66, 42, 26, 64, 52, 66, 37, 0, 87,
     36, 13, 43, 26, 53, 7, 73, 18, 45, 92, 56, 41, 35, 92, 49, 11, 73, 40, 9, 53, 15, 57, 30, 44, 49, 50, 28, 38, 30,
     85, 70, 19, 19, 75, 53, 65, 26, 83, 32, 37, 74, 98, 95, 62, 85, 2, 67, 80, 57, 34, 44, 90, 7, 63, 44, 48, 70, 61,
     20, 78, 99, 37, 0, 10, 53, 46, 95, 50, 1, 67, 59, 19, 66, 58, 30, 29, 58, 81, 62, 44, 13, 73, 54, 79, 97, 22, 62,
     30, 99, 15, 14, 67],
    [44, 0, 24, 80, 41, 67, 50, 56, 29, 73, 43, 20, 86, 30, 53, 57, 47, 94, 83, 64, 28, 23, 14, 43, 76, 95, 29, 45, 39,
     61, 80, 34, 65, 67, 56, 45, 80, 43, 30, 71, 24, 85, 93, 34, 22, 58, 38, 15, 58, 87, 52, 90, 7, 0, 7, 88, 24, 5, 51,
     37, 30, 96, 78, 0, 54, 6, 20, 15, 92, 32, 77, 98, 84, 96, 24, 47, 55, 61, 66, 54, 10, 37, 34, 36, 87, 92, 2, 37,
     85, 51, 49, 18, 17, 65, 29, 20, 35, 40, 42, 98, 92, 12, 50, 53, 88, 8, 70, 26, 95, 18, 92, 67, 91, 15, 88, 53, 48,
     59, 68, 90, 90, 0, 42, 17, 47, 68, 9, 95, 98, 92, 92, 90, 33, 77, 73, 69, 59, 17, 93, 45, 65, 79, 40, 68, 77, 84,
     87, 0, 41, 89],
    [43, 68, 36, 34, 12, 15, 52, 8, 80, 7, 56, 35, 10, 39, 82, 0, 17, 26, 99, 8, 4, 40, 44, 68, 44, 36, 32, 58, 27, 75,
     49, 98, 26, 26, 50, 68, 64, 50, 33, 44, 22, 99, 29, 88, 33, 76, 96, 35, 61, 19, 9, 2, 7, 53, 12, 37, 77, 25, 19,
     85, 80, 52, 85, 55, 12, 90, 55, 67, 83, 59, 61, 76, 13, 55, 3, 5, 75, 54, 51, 11, 84, 26, 7, 37, 95, 88, 31, 52,
     65, 61, 88, 50, 68, 51, 31, 50, 59, 9, 27, 20, 63, 45, 49, 24, 91, 71, 83, 93, 79, 52, 79, 28, 81, 88, 74, 98, 46,
     68, 46, 51, 62, 35, 27, 25, 44, 44, 72, 93, 48, 70, 84, 35, 40, 14, 66, 53, 98, 7, 45, 82, 57, 4, 80, 45, 62, 38,
     51, 79, 29, 75],
    [27, 9, 38, 51, 66, 59, 63, 0, 39, 7, 40, 7, 25, 18, 71, 30, 49, 13, 61, 17, 70, 22, 88, 50, 71, 91, 76, 19, 10, 29,
     59, 93, 34, 86, 73, 65, 37, 46, 0, 75, 55, 92, 17, 31, 41, 55, 96, 96, 38, 47, 38, 46, 14, 24, 55, 73, 54, 53, 11,
     6, 61, 99, 9, 82, 53, 79, 91, 45, 86, 43, 15, 12, 90, 83, 23, 43, 22, 72, 35, 17, 59, 51, 99, 66, 9, 27, 1, 50, 57,
     94, 1, 10, 11, 75, 47, 83, 60, 80, 71, 41, 50, 45, 87, 92, 16, 2, 20, 97, 15, 58, 39, 81, 56, 25, 3, 70, 19, 2, 47,
     10, 52, 22, 54, 20, 20, 9, 63, 37, 65, 82, 33, 47, 39, 64, 50, 67, 89, 32, 81, 32, 57, 59, 58, 67, 31, 39, 52, 89,
     21, 77],
    [45, 64, 63, 8, 72, 22, 12, 4, 47, 2, 68, 44, 66, 26, 46, 79, 57, 37, 35, 32, 50, 41, 41, 42, 97, 79, 85, 2, 94, 9,
     41, 57, 29, 99, 92, 9, 0, 74, 83, 18, 62, 42, 63, 49, 94, 28, 82, 22, 47, 32, 74, 89, 50, 56, 77, 72, 45, 66, 70,
     35, 69, 17, 18, 65, 72, 56, 30, 26, 30, 11, 61, 9, 71, 60, 83, 98, 57, 59, 94, 64, 63, 77, 39, 68, 76, 6, 84, 52,
     14, 14, 99, 22, 12, 35, 51, 19, 93, 87, 26, 37, 12, 47, 61, 6, 76, 92, 34, 68, 60, 30, 9, 67, 35, 34, 10, 25, 97,
     74, 85, 63, 46, 73, 0, 95, 56, 27, 22, 87, 27, 28, 34, 94, 6, 54, 18, 41, 56, 71, 46, 37, 39, 43, 65, 67, 36, 21,
     15, 21, 99, 74],
    [65, 93, 24, 39, 83, 38, 42, 11, 58, 44, 99, 82, 56, 4, 72, 3, 8, 67, 77, 31, 83, 3, 2, 10, 98, 91, 94, 17, 10, 80,
     75, 68, 84, 96, 51, 53, 70, 42, 53, 48, 71, 64, 23, 48, 67, 98, 31, 77, 92, 60, 71, 82, 12, 16, 19, 36, 71, 40, 29,
     15, 77, 61, 5, 76, 6, 17, 46, 1, 35, 10, 70, 87, 69, 93, 25, 15, 40, 48, 18, 83, 53, 82, 35, 75, 8, 40, 10, 91, 84,
     94, 6, 11, 95, 85, 42, 33, 82, 42, 54, 22, 77, 23, 96, 9, 93, 35, 4, 90, 21, 2, 15, 19, 0, 85, 55, 92, 50, 45, 74,
     91, 64, 84, 90, 72, 2, 11, 42, 94, 64, 34, 90, 83, 34, 36, 79, 93, 64, 76, 6, 64, 58, 42, 76, 36, 82, 88, 22, 62,
     10, 90],
    [21, 95, 41, 16, 12, 85, 18, 92, 88, 76, 43, 36, 37, 38, 89, 91, 52, 15, 23, 20, 31, 3, 14, 93, 17, 42, 45, 84, 49,
     18, 90, 90, 71, 55, 14, 6, 25, 45, 15, 49, 41, 93, 58, 67, 20, 47, 2, 58, 9, 21, 19, 53, 53, 87, 71, 25, 57, 78,
     92, 27, 12, 43, 69, 2, 72, 97, 94, 68, 25, 69, 15, 61, 87, 87, 35, 60, 41, 66, 42, 41, 87, 92, 77, 63, 30, 30, 74,
     54, 61, 78, 73, 30, 31, 33, 90, 11, 68, 86, 20, 88, 13, 46, 16, 18, 51, 88, 51, 35, 42, 14, 0, 99, 64, 7, 66, 15,
     85, 64, 75, 6, 61, 97, 0, 18, 96, 3, 40, 29, 40, 66, 1, 26, 55, 6, 7, 87, 12, 28, 57, 75, 79, 0, 7, 89, 94, 96, 43,
     38, 36, 82],
    [62, 88, 63, 3, 24, 66, 55, 11, 27, 40, 59, 61, 22, 88, 69, 29, 68, 41, 77, 28, 47, 84, 26, 92, 35, 44, 58, 91, 62,
     38, 35, 12, 58, 89, 50, 0, 26, 95, 34, 36, 53, 89, 55, 5, 18, 80, 0, 62, 95, 51, 52, 94, 41, 58, 40, 24, 68, 37,
     76, 54, 82, 23, 92, 95, 93, 44, 3, 18, 53, 13, 25, 2, 86, 96, 67, 70, 32, 48, 54, 2, 17, 19, 64, 88, 1, 51, 37, 44,
     75, 27, 1, 44, 51, 21, 7, 51, 58, 89, 44, 43, 63, 15, 44, 7, 39, 37, 62, 84, 73, 1, 72, 58, 47, 13, 91, 12, 24, 75,
     65, 25, 17, 26, 75, 13, 70, 61, 61, 78, 88, 50, 97, 78, 47, 21, 87, 84, 5, 14, 60, 70, 48, 18, 1, 68, 36, 17, 94,
     8, 53, 88],
    [68, 40, 67, 69, 8, 87, 98, 15, 58, 62, 32, 10, 16, 73, 29, 48, 44, 33, 77, 56, 66, 0, 99, 18, 64, 80, 94, 34, 93,
     78, 48, 87, 5, 76, 28, 78, 72, 94, 87, 63, 23, 35, 73, 88, 77, 0, 26, 84, 73, 20, 87, 82, 3, 95, 79, 70, 98, 10,
     69, 31, 21, 45, 38, 22, 41, 17, 95, 73, 47, 43, 41, 28, 87, 46, 65, 77, 60, 14, 18, 79, 69, 62, 35, 94, 42, 32, 52,
     81, 72, 17, 31, 67, 37, 65, 5, 10, 65, 20, 87, 78, 86, 78, 74, 83, 90, 81, 24, 66, 42, 14, 0, 62, 34, 25, 88, 53,
     79, 61, 7, 11, 23, 57, 24, 45, 34, 99, 29, 74, 8, 5, 34, 57, 0, 23, 75, 25, 30, 9, 71, 39, 59, 44, 4, 56, 88, 93,
     11, 44, 81, 14],
    [16, 23, 64, 77, 72, 94, 99, 79, 23, 55, 63, 56, 12, 16, 1, 46, 78, 45, 3, 92, 85, 62, 19, 92, 49, 3, 29, 62, 12,
     60, 36, 78, 98, 95, 94, 63, 48, 84, 38, 97, 29, 51, 91, 52, 50, 11, 89, 3, 20, 5, 35, 43, 98, 80, 18, 91, 75, 61,
     81, 31, 99, 19, 14, 48, 81, 33, 85, 90, 65, 8, 94, 55, 61, 96, 29, 43, 33, 68, 23, 64, 58, 90, 24, 72, 7, 17, 45,
     0, 68, 32, 76, 87, 8, 44, 80, 51, 89, 1, 41, 78, 61, 42, 90, 53, 20, 23, 45, 23, 6, 79, 80, 62, 79, 4, 30, 11, 5,
     68, 87, 13, 21, 68, 77, 6, 2, 33, 81, 26, 3, 38, 45, 52, 91, 95, 16, 8, 8, 14, 55, 35, 89, 19, 49, 93, 41, 46, 94,
     99, 85, 55],
    [85, 5, 28, 73, 4, 33, 76, 6, 98, 52, 42, 57, 86, 96, 61, 40, 39, 86, 52, 84, 26, 23, 43, 87, 25, 77, 61, 55, 5, 81,
     65, 68, 60, 95, 60, 44, 8, 83, 45, 76, 31, 1, 68, 92, 34, 88, 97, 21, 71, 53, 73, 39, 51, 42, 41, 78, 58, 96, 11,
     4, 17, 27, 45, 34, 56, 38, 31, 14, 7, 58, 60, 97, 78, 27, 3, 72, 44, 98, 45, 58, 5, 74, 25, 95, 17, 56, 75, 21, 62,
     95, 37, 65, 22, 84, 86, 53, 12, 27, 65, 46, 46, 68, 19, 52, 15, 25, 63, 22, 1, 95, 6, 72, 23, 49, 6, 97, 32, 31, 1,
     71, 93, 4, 58, 40, 1, 82, 49, 1, 62, 76, 71, 73, 41, 24, 69, 1, 55, 51, 21, 90, 64, 22, 80, 65, 24, 10, 92, 70, 88,
     92],
    [89, 54, 87, 68, 16, 96, 59, 31, 21, 95, 80, 30, 50, 36, 91, 16, 89, 85, 74, 35, 59, 44, 16, 2, 19, 6, 59, 41, 25,
     10, 22, 77, 74, 2, 74, 65, 43, 50, 41, 75, 21, 73, 10, 87, 7, 2, 12, 36, 47, 41, 67, 49, 68, 49, 0, 93, 2, 65, 18,
     87, 91, 14, 45, 27, 74, 8, 17, 60, 43, 32, 52, 5, 24, 70, 90, 45, 20, 68, 77, 82, 44, 24, 27, 99, 14, 90, 89, 57,
     78, 88, 19, 42, 46, 27, 60, 9, 4, 99, 49, 94, 94, 8, 27, 18, 54, 45, 57, 44, 3, 87, 53, 54, 54, 46, 18, 23, 17, 13,
     57, 6, 61, 31, 49, 58, 59, 53, 75, 82, 23, 70, 8, 34, 47, 54, 21, 22, 60, 6, 97, 50, 48, 23, 55, 30, 62, 54, 79,
     75, 86, 97],
    [52, 7, 97, 39, 3, 93, 14, 41, 29, 46, 40, 23, 62, 6, 97, 13, 58, 61, 99, 87, 26, 25, 18, 85, 75, 64, 16, 37, 43,
     31, 0, 40, 18, 26, 55, 45, 29, 83, 16, 83, 98, 8, 60, 39, 63, 55, 57, 59, 17, 46, 52, 24, 72, 65, 78, 37, 69, 27,
     18, 99, 42, 57, 80, 87, 2, 8, 1, 77, 79, 50, 74, 99, 65, 23, 20, 12, 26, 6, 3, 93, 61, 58, 36, 19, 28, 22, 57, 24,
     65, 81, 44, 74, 47, 10, 88, 78, 61, 72, 90, 91, 71, 0, 9, 31, 16, 61, 92, 95, 10, 99, 33, 25, 30, 13, 97, 44, 34,
     42, 38, 92, 92, 13, 7, 44, 28, 50, 31, 4, 68, 74, 44, 76, 31, 75, 29, 30, 28, 1, 34, 13, 92, 44, 63, 55, 13, 73,
     58, 99, 20, 69],
    [68, 72, 28, 4, 1, 49, 38, 97, 5, 4, 68, 19, 76, 13, 22, 8, 22, 35, 53, 96, 74, 18, 48, 31, 19, 19, 69, 94, 52, 21,
     72, 83, 65, 50, 79, 12, 8, 30, 53, 46, 37, 67, 73, 46, 10, 59, 45, 57, 99, 94, 73, 87, 95, 83, 87, 89, 17, 66, 43,
     44, 56, 27, 62, 72, 23, 68, 22, 44, 28, 3, 4, 49, 8, 23, 34, 56, 67, 17, 14, 46, 17, 30, 29, 7, 17, 63, 24, 92, 90,
     70, 93, 40, 11, 67, 41, 31, 61, 38, 55, 58, 86, 49, 25, 72, 10, 15, 12, 32, 6, 3, 51, 69, 29, 2, 62, 83, 80, 73,
     85, 33, 13, 85, 97, 27, 52, 80, 48, 46, 79, 55, 24, 2, 3, 54, 2, 26, 62, 43, 86, 25, 75, 13, 1, 5, 67, 70, 73, 88,
     62, 42],
    [30, 24, 50, 29, 61, 92, 35, 96, 45, 26, 80, 11, 33, 91, 16, 68, 5, 96, 46, 20, 14, 10, 79, 88, 9, 46, 3, 47, 5, 46,
     36, 54, 4, 98, 25, 77, 68, 26, 22, 77, 45, 1, 49, 90, 88, 53, 39, 63, 27, 84, 62, 58, 37, 61, 72, 4, 56, 45, 30,
     26, 67, 7, 63, 14, 90, 5, 13, 13, 68, 0, 10, 38, 91, 69, 91, 62, 10, 35, 13, 40, 10, 26, 60, 45, 34, 96, 36, 17,
     80, 20, 17, 96, 68, 27, 98, 60, 85, 86, 18, 63, 71, 85, 15, 4, 56, 40, 14, 69, 40, 13, 4, 13, 7, 13, 23, 8, 40, 39,
     36, 46, 2, 39, 20, 77, 73, 23, 60, 43, 50, 88, 2, 14, 83, 35, 2, 3, 1, 26, 2, 96, 88, 67, 32, 63, 72, 42, 69, 67,
     55, 55],
    [58, 12, 98, 75, 79, 96, 50, 43, 53, 61, 80, 96, 96, 40, 81, 94, 31, 82, 84, 31, 24, 65, 39, 5, 89, 58, 48, 22, 42,
     57, 83, 23, 45, 50, 15, 70, 51, 91, 65, 42, 47, 69, 25, 86, 58, 88, 41, 30, 24, 67, 66, 25, 2, 32, 91, 42, 66, 27,
     30, 36, 19, 46, 23, 38, 64, 6, 87, 55, 58, 40, 72, 46, 6, 18, 91, 36, 83, 54, 72, 28, 63, 26, 96, 37, 91, 67, 46,
     10, 6, 46, 39, 60, 33, 45, 9, 97, 52, 52, 60, 82, 8, 63, 12, 45, 47, 37, 81, 34, 34, 83, 54, 16, 76, 95, 82, 22,
     46, 92, 8, 37, 38, 17, 85, 55, 8, 69, 51, 13, 62, 99, 45, 52, 23, 11, 25, 93, 21, 29, 14, 96, 32, 99, 50, 59, 45,
     83, 31, 85, 82, 94],
    [52, 20, 84, 61, 62, 75, 27, 6, 61, 47, 23, 91, 94, 83, 13, 52, 45, 53, 56, 51, 81, 59, 6, 67, 32, 13, 15, 96, 25,
     32, 6, 94, 71, 85, 44, 8, 74, 67, 52, 86, 39, 37, 99, 25, 4, 82, 84, 39, 6, 17, 85, 17, 54, 4, 61, 66, 86, 87, 75,
     83, 66, 72, 86, 92, 62, 7, 23, 48, 14, 47, 26, 26, 16, 79, 12, 87, 24, 25, 61, 15, 57, 78, 59, 85, 71, 16, 83, 31,
     45, 78, 99, 29, 66, 50, 51, 33, 71, 75, 65, 96, 69, 51, 36, 5, 34, 74, 8, 13, 89, 7, 69, 78, 89, 23, 27, 28, 41,
     59, 99, 44, 76, 53, 28, 14, 53, 32, 49, 80, 85, 67, 79, 67, 34, 2, 3, 39, 91, 46, 74, 5, 88, 56, 92, 47, 77, 38,
     86, 90, 37, 16],
    [78, 55, 33, 57, 20, 88, 55, 36, 31, 84, 48, 32, 7, 36, 6, 10, 58, 3, 36, 6, 5, 31, 56, 45, 80, 48, 77, 84, 86, 4,
     45, 67, 95, 74, 9, 76, 88, 52, 95, 37, 50, 7, 34, 84, 48, 36, 36, 34, 99, 19, 23, 94, 30, 83, 0, 4, 74, 97, 8, 21,
     40, 98, 63, 98, 6, 95, 47, 37, 17, 28, 71, 60, 32, 83, 5, 59, 45, 38, 8, 46, 52, 8, 89, 26, 47, 31, 0, 64, 95, 62,
     83, 13, 39, 59, 63, 14, 33, 34, 48, 92, 10, 12, 71, 32, 9, 55, 67, 4, 18, 52, 94, 97, 69, 31, 61, 53, 71, 85, 34,
     37, 35, 42, 20, 59, 25, 4, 68, 42, 24, 79, 37, 47, 55, 54, 57, 39, 59, 10, 49, 13, 88, 31, 75, 25, 19, 59, 87, 16,
     88, 76],
    [7, 98, 28, 58, 17, 89, 13, 23, 24, 22, 86, 37, 39, 71, 3, 20, 0, 82, 48, 65, 72, 1, 25, 84, 70, 32, 25, 45, 1, 49,
     6, 11, 27, 63, 23, 13, 41, 94, 41, 17, 4, 70, 97, 9, 24, 2, 18, 80, 53, 98, 21, 31, 88, 84, 15, 90, 51, 93, 24, 36,
     76, 50, 35, 51, 83, 7, 50, 78, 88, 45, 60, 61, 54, 65, 23, 73, 29, 23, 68, 94, 91, 8, 58, 62, 25, 57, 69, 63, 40,
     58, 80, 28, 37, 99, 66, 69, 73, 25, 31, 27, 61, 38, 60, 16, 47, 69, 26, 62, 47, 81, 46, 90, 90, 1, 17, 43, 93, 17,
     0, 6, 67, 4, 47, 94, 31, 8, 91, 29, 53, 4, 27, 82, 1, 45, 84, 26, 49, 21, 79, 13, 22, 5, 71, 48, 93, 16, 1, 17, 37,
     75],
    [29, 12, 53, 90, 75, 64, 78, 8, 95, 57, 66, 46, 14, 85, 5, 23, 72, 49, 45, 59, 80, 18, 70, 43, 63, 3, 57, 63, 2, 18,
     33, 76, 47, 71, 77, 19, 75, 25, 11, 0, 57, 57, 21, 6, 79, 66, 99, 96, 52, 63, 82, 20, 41, 22, 63, 99, 91, 0, 80,
     39, 45, 74, 45, 88, 31, 49, 14, 87, 39, 69, 40, 59, 55, 94, 92, 55, 77, 13, 40, 66, 97, 67, 29, 47, 64, 88, 13, 89,
     26, 72, 55, 87, 20, 90, 97, 85, 9, 16, 55, 33, 86, 31, 92, 91, 59, 32, 95, 14, 29, 68, 6, 63, 86, 50, 36, 42, 98,
     48, 2, 91, 25, 30, 42, 22, 17, 15, 72, 67, 11, 63, 96, 49, 69, 51, 56, 23, 65, 52, 70, 23, 54, 86, 29, 34, 47, 41,
     4, 91, 28, 6],
    [48, 60, 1, 56, 97, 67, 8, 91, 75, 35, 96, 73, 25, 5, 71, 73, 96, 45, 22, 11, 73, 47, 75, 76, 22, 22, 45, 23, 64, 0,
     80, 76, 47, 58, 90, 35, 47, 49, 10, 82, 43, 54, 32, 79, 36, 88, 11, 16, 24, 42, 62, 7, 37, 65, 18, 69, 89, 51, 41,
     1, 8, 14, 25, 62, 27, 48, 75, 51, 96, 44, 82, 29, 48, 61, 2, 48, 83, 39, 90, 78, 24, 86, 9, 5, 5, 57, 99, 84, 3,
     85, 15, 47, 6, 80, 68, 87, 5, 37, 48, 68, 87, 10, 94, 76, 78, 98, 10, 41, 16, 82, 83, 27, 12, 57, 87, 46, 81, 3,
     78, 64, 16, 73, 28, 75, 2, 57, 90, 34, 17, 57, 77, 2, 90, 90, 44, 81, 9, 19, 89, 31, 57, 84, 80, 85, 44, 36, 8, 6,
     87, 75],
    [37, 35, 42, 29, 8, 79, 53, 78, 99, 5, 33, 5, 98, 61, 67, 19, 13, 85, 29, 32, 4, 19, 30, 37, 69, 19, 48, 29, 9, 91,
     41, 98, 69, 99, 93, 26, 46, 40, 97, 85, 97, 89, 50, 45, 38, 79, 43, 64, 95, 7, 21, 8, 13, 62, 28, 49, 47, 64, 35,
     71, 40, 26, 51, 51, 44, 26, 73, 51, 8, 72, 19, 22, 77, 77, 54, 66, 25, 17, 95, 7, 22, 68, 47, 50, 86, 63, 42, 33,
     79, 94, 80, 93, 18, 97, 47, 6, 12, 13, 63, 12, 27, 39, 48, 72, 57, 66, 94, 87, 59, 53, 0, 29, 76, 14, 60, 12, 3,
     88, 43, 73, 88, 72, 18, 54, 54, 0, 0, 56, 67, 68, 31, 46, 87, 25, 84, 21, 3, 7, 86, 73, 9, 80, 17, 75, 19, 87, 94,
     74, 55, 95],
    [82, 27, 68, 34, 26, 17, 33, 14, 67, 30, 88, 28, 0, 80, 63, 60, 88, 93, 18, 80, 40, 39, 20, 58, 26, 89, 72, 71, 54,
     20, 63, 65, 69, 11, 75, 30, 1, 56, 11, 78, 33, 73, 51, 41, 6, 93, 50, 87, 64, 42, 91, 86, 55, 6, 93, 7, 69, 63, 92,
     41, 28, 71, 82, 35, 74, 31, 52, 62, 57, 43, 17, 29, 78, 51, 38, 67, 17, 37, 57, 77, 46, 2, 7, 96, 42, 74, 77, 39,
     4, 75, 71, 80, 53, 75, 29, 74, 17, 14, 53, 72, 53, 64, 54, 83, 78, 63, 53, 30, 76, 48, 33, 87, 36, 75, 81, 17, 21,
     39, 59, 73, 75, 40, 86, 36, 77, 15, 68, 7, 5, 72, 28, 32, 71, 93, 99, 22, 61, 74, 47, 70, 48, 93, 46, 34, 56, 55,
     96, 44, 99, 97],
    [57, 71, 20, 6, 24, 45, 55, 61, 39, 21, 70, 82, 54, 14, 9, 75, 73, 70, 91, 92, 81, 27, 45, 96, 94, 4, 44, 29, 36,
     45, 73, 95, 51, 64, 88, 47, 78, 29, 95, 67, 62, 15, 93, 15, 12, 67, 61, 81, 94, 54, 67, 10, 67, 51, 68, 41, 26, 53,
     66, 63, 1, 86, 11, 38, 65, 66, 32, 69, 12, 80, 88, 25, 74, 58, 51, 69, 8, 82, 8, 83, 77, 59, 34, 88, 11, 77, 56,
     78, 64, 48, 15, 36, 19, 61, 74, 48, 22, 25, 2, 98, 92, 24, 47, 26, 71, 89, 58, 53, 97, 9, 95, 57, 73, 26, 46, 12,
     30, 71, 96, 94, 50, 11, 2, 94, 1, 93, 16, 98, 97, 55, 43, 36, 98, 60, 16, 34, 72, 5, 42, 3, 97, 45, 75, 73, 22, 74,
     80, 76, 13, 3],
    [57, 77, 19, 23, 35, 47, 73, 79, 17, 73, 22, 75, 62, 59, 82, 74, 68, 17, 68, 23, 88, 68, 9, 99, 25, 64, 7, 4, 2, 42,
     63, 8, 10, 74, 87, 35, 16, 86, 51, 25, 27, 92, 68, 75, 97, 13, 58, 97, 62, 54, 77, 65, 68, 95, 55, 42, 36, 37, 36,
     36, 27, 42, 81, 93, 60, 7, 14, 52, 2, 81, 92, 66, 66, 80, 84, 34, 9, 64, 18, 28, 14, 82, 1, 66, 29, 91, 4, 50, 54,
     53, 92, 27, 25, 88, 1, 17, 30, 40, 23, 48, 41, 55, 52, 45, 63, 65, 28, 23, 66, 27, 49, 22, 18, 0, 95, 24, 48, 47,
     77, 16, 85, 24, 73, 94, 32, 62, 68, 53, 50, 12, 21, 13, 83, 31, 28, 74, 82, 36, 96, 1, 46, 16, 72, 38, 56, 5, 72,
     79, 87, 68],
    [7, 40, 13, 64, 37, 1, 1, 38, 40, 79, 87, 17, 50, 32, 6, 27, 30, 43, 39, 76, 5, 40, 71, 25, 21, 40, 31, 6, 6, 18,
     43, 77, 37, 73, 36, 51, 3, 62, 56, 62, 93, 86, 19, 75, 18, 79, 77, 74, 77, 89, 52, 47, 38, 46, 77, 19, 44, 91, 60,
     41, 92, 53, 2, 14, 63, 57, 39, 81, 10, 99, 56, 14, 61, 79, 79, 95, 63, 26, 4, 35, 69, 60, 44, 35, 57, 18, 6, 14,
     86, 23, 50, 25, 64, 72, 72, 88, 66, 50, 35, 47, 75, 47, 23, 98, 7, 45, 64, 36, 99, 57, 53, 24, 94, 38, 62, 35, 13,
     72, 98, 78, 17, 98, 22, 91, 66, 88, 24, 54, 0, 1, 72, 0, 82, 69, 25, 39, 96, 41, 13, 81, 48, 98, 11, 10, 70, 19, 8,
     86, 60, 22],
    [55, 81, 51, 44, 10, 4, 74, 61, 26, 42, 7, 68, 80, 44, 50, 4, 41, 32, 50, 44, 16, 82, 22, 20, 29, 32, 37, 39, 81,
     46, 26, 90, 55, 21, 77, 18, 91, 86, 88, 77, 51, 0, 66, 84, 8, 95, 41, 25, 50, 87, 81, 27, 62, 7, 82, 84, 67, 19,
     77, 8, 89, 72, 34, 55, 76, 52, 74, 44, 81, 83, 17, 28, 22, 65, 22, 19, 63, 64, 51, 62, 90, 94, 60, 73, 57, 2, 8,
     97, 8, 88, 30, 73, 52, 53, 90, 14, 74, 4, 92, 31, 76, 48, 60, 60, 33, 45, 63, 16, 58, 77, 7, 15, 46, 92, 78, 57,
     92, 72, 71, 64, 12, 87, 10, 39, 68, 86, 93, 23, 45, 24, 29, 45, 94, 62, 4, 42, 1, 34, 42, 66, 70, 34, 21, 84, 13,
     74, 43, 38, 60, 34],
    [54, 32, 73, 66, 33, 31, 49, 47, 34, 58, 26, 56, 63, 43, 52, 54, 7, 48, 50, 23, 35, 17, 87, 89, 13, 96, 57, 91, 3,
     13, 32, 58, 64, 64, 31, 26, 29, 13, 84, 28, 20, 92, 33, 57, 26, 1, 36, 87, 89, 29, 94, 16, 93, 59, 90, 55, 58, 85,
     84, 97, 65, 61, 49, 78, 82, 53, 43, 98, 24, 25, 92, 15, 8, 33, 72, 10, 19, 10, 5, 9, 97, 85, 66, 90, 63, 5, 5, 2,
     98, 17, 40, 61, 45, 61, 66, 79, 71, 45, 38, 27, 47, 32, 24, 64, 49, 75, 21, 51, 52, 92, 86, 33, 53, 37, 11, 95, 42,
     75, 90, 91, 13, 13, 31, 25, 93, 63, 37, 57, 99, 9, 22, 9, 46, 40, 75, 18, 46, 55, 42, 9, 93, 1, 6, 74, 27, 45, 98,
     62, 13, 30],
    [81, 94, 41, 60, 21, 66, 69, 93, 58, 62, 15, 17, 56, 65, 43, 10, 66, 16, 35, 95, 73, 82, 67, 22, 13, 10, 77, 43, 12,
     53, 72, 74, 85, 21, 23, 76, 85, 74, 48, 93, 46, 69, 85, 13, 63, 96, 26, 53, 26, 29, 43, 32, 14, 87, 60, 7, 48, 25,
     93, 50, 87, 95, 0, 18, 68, 19, 26, 55, 93, 64, 40, 26, 38, 47, 96, 85, 63, 23, 31, 51, 19, 78, 97, 61, 97, 27, 36,
     69, 19, 87, 49, 19, 1, 2, 13, 33, 32, 9, 91, 18, 70, 87, 16, 60, 59, 44, 21, 75, 43, 27, 24, 45, 12, 27, 14, 28,
     10, 68, 11, 68, 78, 95, 44, 91, 93, 93, 79, 51, 88, 42, 27, 87, 51, 0, 25, 94, 95, 20, 55, 2, 16, 79, 17, 55, 19,
     45, 92, 31, 27, 40],
    [20, 70, 52, 59, 46, 6, 47, 53, 35, 9, 37, 2, 41, 36, 93, 80, 42, 4, 65, 28, 61, 97, 32, 26, 26, 26, 80, 37, 33, 20,
     54, 62, 44, 76, 69, 45, 49, 97, 59, 20, 70, 3, 75, 76, 94, 33, 77, 73, 17, 82, 98, 54, 76, 61, 35, 99, 92, 98, 96,
     68, 93, 36, 7, 92, 11, 17, 9, 41, 52, 0, 88, 74, 28, 7, 79, 52, 8, 97, 1, 9, 25, 26, 26, 7, 10, 69, 28, 3, 43, 94,
     94, 0, 64, 48, 91, 96, 55, 87, 22, 58, 38, 8, 71, 37, 36, 69, 63, 45, 67, 50, 39, 29, 84, 9, 77, 22, 54, 37, 79,
     42, 39, 32, 35, 95, 15, 48, 94, 61, 89, 80, 77, 3, 53, 25, 91, 56, 75, 65, 28, 90, 84, 24, 29, 70, 97, 46, 42, 13,
     69, 16],
    [53, 89, 80, 13, 50, 15, 16, 56, 33, 16, 9, 47, 98, 51, 91, 53, 28, 38, 18, 57, 1, 65, 68, 79, 67, 90, 23, 63, 99,
     69, 7, 36, 22, 8, 47, 2, 79, 94, 71, 87, 16, 68, 44, 38, 38, 90, 37, 92, 66, 38, 1, 99, 71, 70, 28, 28, 29, 78, 76,
     43, 87, 35, 17, 41, 38, 59, 17, 27, 19, 7, 68, 82, 95, 52, 18, 91, 3, 0, 67, 99, 79, 69, 45, 44, 40, 22, 85, 33, 5,
     48, 25, 31, 75, 10, 68, 94, 82, 63, 74, 97, 90, 81, 11, 84, 14, 98, 38, 72, 84, 19, 75, 75, 53, 24, 81, 44, 50, 32,
     20, 24, 25, 33, 44, 32, 90, 79, 40, 25, 85, 86, 43, 72, 62, 59, 96, 77, 72, 3, 47, 63, 45, 50, 64, 88, 13, 46, 55,
     40, 90, 54],
    [44, 24, 35, 58, 40, 61, 60, 40, 63, 74, 47, 9, 40, 91, 78, 99, 84, 15, 90, 0, 98, 77, 16, 41, 99, 41, 1, 65, 44,
     48, 86, 7, 44, 76, 43, 91, 86, 36, 47, 17, 72, 49, 97, 29, 2, 78, 37, 65, 91, 75, 93, 61, 82, 22, 33, 66, 99, 84,
     19, 87, 50, 10, 21, 95, 79, 41, 2, 17, 41, 98, 77, 76, 73, 75, 26, 84, 10, 96, 10, 25, 4, 51, 7, 0, 5, 95, 53, 41,
     23, 0, 79, 34, 59, 51, 67, 77, 13, 2, 58, 67, 6, 45, 48, 2, 40, 72, 12, 97, 61, 69, 14, 19, 55, 93, 6, 39, 56, 38,
     48, 49, 64, 97, 51, 78, 6, 23, 90, 43, 87, 72, 36, 50, 88, 5, 28, 75, 80, 76, 80, 31, 3, 69, 6, 43, 70, 63, 13, 74,
     72, 42],
    [34, 47, 90, 34, 88, 54, 14, 10, 67, 44, 17, 88, 34, 75, 9, 16, 33, 87, 40, 66, 33, 11, 98, 82, 98, 73, 92, 37, 36,
     84, 79, 26, 78, 31, 48, 58, 14, 57, 0, 30, 31, 82, 46, 42, 89, 44, 97, 28, 30, 96, 88, 76, 11, 59, 27, 69, 72, 86,
     90, 23, 78, 6, 90, 97, 46, 58, 49, 7, 9, 20, 57, 34, 84, 74, 53, 27, 16, 21, 66, 50, 95, 21, 3, 18, 17, 84, 42, 91,
     22, 69, 52, 33, 31, 71, 93, 28, 54, 50, 39, 34, 48, 85, 8, 25, 82, 51, 8, 14, 74, 28, 31, 11, 3, 55, 0, 92, 84, 74,
     2, 18, 62, 10, 70, 57, 38, 78, 73, 9, 18, 54, 34, 32, 80, 22, 27, 18, 34, 59, 89, 6, 22, 89, 74, 7, 22, 53, 21, 32,
     77, 1],
    [70, 56, 54, 80, 8, 98, 25, 72, 62, 76, 82, 25, 39, 55, 21, 53, 76, 50, 5, 43, 46, 37, 27, 63, 17, 93, 5, 90, 16,
     16, 34, 92, 56, 32, 85, 71, 51, 0, 5, 81, 54, 5, 13, 47, 99, 73, 77, 53, 9, 82, 16, 8, 4, 79, 84, 53, 23, 94, 42,
     30, 32, 76, 32, 86, 83, 80, 68, 99, 87, 2, 98, 52, 0, 9, 5, 35, 67, 86, 25, 48, 54, 73, 29, 13, 56, 4, 94, 23, 96,
     99, 16, 96, 34, 3, 10, 43, 54, 73, 23, 58, 62, 75, 30, 90, 20, 13, 30, 61, 63, 29, 22, 24, 39, 84, 4, 38, 90, 7,
     75, 32, 97, 93, 0, 30, 32, 27, 31, 33, 30, 13, 35, 94, 1, 52, 32, 19, 78, 56, 16, 13, 80, 49, 96, 52, 96, 28, 42,
     46, 42, 87],
    [65, 63, 49, 75, 19, 8, 5, 44, 48, 63, 46, 60, 87, 80, 16, 88, 95, 70, 54, 98, 37, 24, 95, 83, 95, 4, 46, 93, 60,
     85, 55, 19, 76, 46, 67, 30, 46, 3, 78, 5, 75, 44, 30, 12, 61, 92, 84, 16, 2, 10, 38, 35, 55, 34, 42, 10, 21, 80,
     39, 75, 75, 87, 46, 36, 48, 2, 73, 92, 20, 88, 49, 0, 57, 9, 18, 17, 79, 30, 33, 99, 76, 85, 1, 88, 52, 79, 91, 27,
     31, 8, 10, 65, 69, 82, 32, 72, 34, 51, 18, 57, 71, 5, 53, 89, 28, 75, 53, 7, 41, 82, 13, 64, 49, 98, 41, 76, 67,
     13, 34, 34, 52, 9, 64, 84, 80, 78, 66, 49, 20, 44, 37, 37, 92, 93, 73, 73, 35, 16, 54, 94, 35, 30, 27, 54, 24, 27,
     58, 34, 73, 74],
    [61, 33, 29, 22, 52, 99, 38, 37, 96, 9, 36, 6, 55, 60, 48, 41, 60, 58, 53, 63, 60, 42, 33, 56, 57, 65, 33, 3, 90, 9,
     32, 52, 50, 91, 93, 14, 44, 61, 44, 78, 29, 68, 21, 53, 83, 83, 81, 65, 86, 64, 73, 4, 43, 55, 46, 7, 95, 69, 44,
     52, 71, 72, 35, 87, 58, 86, 47, 63, 75, 97, 6, 57, 23, 58, 10, 48, 18, 45, 99, 0, 97, 34, 10, 95, 70, 86, 83, 0,
     89, 38, 11, 32, 17, 78, 71, 74, 94, 64, 95, 82, 84, 48, 34, 23, 88, 82, 96, 62, 0, 49, 43, 3, 55, 26, 56, 12, 26,
     58, 87, 91, 88, 31, 20, 69, 45, 74, 15, 62, 77, 2, 52, 32, 2, 17, 82, 93, 68, 29, 88, 15, 46, 28, 81, 53, 79, 66,
     81, 69, 59, 36],
    [83, 62, 31, 65, 13, 44, 91, 63, 35, 75, 97, 26, 78, 16, 35, 41, 63, 73, 4, 33, 33, 40, 32, 19, 17, 98, 72, 0, 51,
     14, 62, 25, 46, 84, 98, 75, 36, 37, 70, 61, 74, 66, 27, 94, 20, 6, 37, 22, 86, 69, 5, 16, 29, 12, 46, 22, 60, 69,
     50, 56, 52, 61, 50, 76, 37, 52, 28, 46, 28, 74, 41, 27, 24, 64, 51, 68, 40, 55, 72, 28, 39, 15, 16, 7, 59, 25, 12,
     86, 66, 80, 7, 3, 64, 9, 85, 4, 97, 59, 0, 23, 54, 57, 60, 67, 84, 75, 82, 70, 94, 48, 66, 63, 36, 81, 42, 75, 21,
     19, 7, 45, 19, 20, 56, 50, 61, 96, 41, 67, 67, 43, 77, 25, 68, 93, 4, 53, 73, 94, 24, 42, 40, 22, 53, 22, 0, 75,
     60, 84, 56, 95],
    [35, 99, 84, 9, 37, 66, 26, 55, 93, 45, 24, 5, 26, 82, 47, 79, 7, 12, 3, 80, 15, 27, 25, 76, 69, 44, 25, 70, 91, 75,
     74, 47, 85, 87, 13, 32, 46, 18, 83, 93, 96, 12, 79, 26, 77, 94, 16, 35, 25, 73, 42, 79, 6, 82, 25, 30, 81, 64, 9,
     5, 62, 15, 51, 52, 79, 58, 52, 38, 59, 51, 87, 76, 92, 86, 16, 17, 54, 91, 65, 47, 33, 35, 98, 18, 6, 26, 28, 58,
     77, 8, 63, 28, 29, 50, 83, 79, 67, 2, 41, 78, 89, 48, 69, 16, 75, 98, 80, 61, 56, 22, 71, 23, 3, 6, 68, 31, 86, 40,
     56, 28, 66, 95, 89, 31, 46, 15, 7, 50, 32, 41, 7, 83, 40, 74, 84, 33, 37, 79, 31, 99, 20, 4, 80, 55, 66, 57, 16,
     93, 9, 77],
    [7, 61, 79, 23, 53, 19, 50, 25, 38, 80, 88, 21, 59, 36, 34, 77, 33, 71, 8, 38, 50, 2, 91, 64, 52, 83, 3, 47, 12, 47,
     9, 96, 77, 13, 50, 79, 99, 90, 58, 25, 78, 49, 30, 71, 99, 63, 99, 35, 91, 79, 61, 8, 51, 58, 80, 61, 75, 36, 66,
     64, 42, 51, 23, 2, 86, 66, 21, 5, 79, 67, 24, 82, 22, 82, 4, 6, 68, 18, 68, 9, 53, 56, 31, 29, 38, 80, 23, 30, 39,
     32, 27, 70, 38, 73, 11, 68, 6, 30, 17, 72, 0, 69, 74, 74, 39, 29, 69, 57, 98, 10, 65, 69, 6, 0, 59, 75, 42, 38, 3,
     14, 35, 41, 69, 31, 1, 82, 15, 39, 47, 25, 29, 80, 16, 39, 2, 75, 97, 61, 10, 98, 16, 0, 19, 7, 6, 90, 34, 27, 70,
     87],
    [50, 40, 3, 42, 8, 50, 73, 20, 71, 9, 94, 76, 1, 16, 36, 30, 60, 70, 22, 50, 40, 74, 60, 41, 31, 53, 99, 80, 27, 22,
     18, 40, 31, 96, 16, 6, 18, 59, 59, 44, 91, 71, 6, 18, 15, 94, 41, 75, 6, 3, 86, 32, 37, 70, 20, 78, 38, 78, 20, 12,
     68, 44, 69, 19, 34, 52, 41, 11, 66, 82, 81, 90, 80, 50, 22, 26, 64, 5, 84, 54, 89, 56, 24, 93, 25, 81, 71, 59, 67,
     25, 12, 3, 20, 12, 82, 34, 58, 19, 79, 41, 51, 56, 89, 58, 23, 88, 33, 23, 39, 80, 4, 72, 70, 17, 59, 73, 38, 60,
     6, 45, 54, 41, 36, 60, 18, 25, 60, 8, 47, 98, 34, 31, 10, 89, 98, 65, 19, 16, 93, 25, 64, 67, 98, 17, 48, 78, 24,
     47, 90, 72],
    [12, 75, 58, 0, 79, 45, 96, 77, 27, 21, 34, 62, 13, 25, 23, 87, 73, 45, 71, 41, 64, 31, 17, 72, 18, 39, 51, 71, 72,
     70, 67, 39, 98, 13, 97, 36, 4, 52, 98, 24, 77, 2, 32, 41, 6, 62, 40, 70, 48, 69, 27, 95, 11, 52, 12, 18, 55, 94,
     18, 21, 54, 98, 13, 47, 48, 63, 0, 21, 17, 14, 53, 92, 88, 20, 28, 44, 57, 39, 84, 96, 89, 92, 4, 91, 59, 31, 17,
     64, 31, 83, 69, 63, 8, 72, 97, 89, 68, 33, 85, 34, 20, 7, 93, 39, 40, 77, 98, 9, 70, 2, 8, 74, 69, 58, 28, 64, 96,
     86, 88, 82, 96, 33, 51, 75, 83, 23, 83, 72, 58, 58, 91, 85, 91, 11, 94, 0, 3, 28, 27, 86, 18, 6, 2, 46, 36, 92, 98,
     67, 72, 44],
    [28, 21, 47, 14, 44, 70, 84, 54, 96, 54, 88, 16, 57, 81, 86, 53, 33, 39, 91, 47, 60, 74, 11, 74, 24, 21, 18, 11, 50,
     20, 63, 68, 31, 39, 43, 86, 6, 21, 32, 78, 96, 76, 2, 45, 77, 49, 43, 13, 77, 57, 0, 97, 95, 39, 37, 60, 72, 44,
     49, 75, 89, 87, 35, 58, 80, 80, 31, 27, 98, 3, 90, 23, 47, 10, 85, 20, 2, 89, 39, 20, 62, 58, 57, 25, 46, 95, 23,
     65, 92, 34, 94, 10, 33, 60, 6, 66, 17, 24, 52, 81, 92, 62, 27, 52, 66, 48, 16, 54, 66, 21, 36, 0, 66, 99, 21, 65,
     54, 96, 58, 79, 39, 42, 92, 75, 45, 96, 44, 27, 80, 33, 19, 61, 95, 55, 65, 2, 24, 43, 5, 59, 75, 27, 77, 9, 30,
     45, 33, 52, 90, 33],
    [5, 9, 6, 29, 76, 9, 22, 88, 76, 31, 39, 56, 58, 3, 7, 44, 8, 60, 65, 5, 88, 88, 93, 29, 79, 83, 47, 38, 86, 41, 82,
     20, 64, 70, 90, 90, 93, 70, 57, 84, 75, 79, 7, 88, 61, 8, 93, 1, 38, 67, 71, 32, 70, 50, 89, 53, 68, 71, 92, 8, 43,
     71, 26, 83, 44, 90, 11, 2, 92, 11, 12, 18, 14, 28, 78, 43, 91, 63, 58, 22, 66, 59, 55, 53, 57, 81, 39, 6, 84, 60,
     76, 93, 31, 75, 96, 79, 60, 69, 39, 57, 53, 42, 2, 44, 68, 61, 2, 55, 82, 9, 92, 75, 86, 86, 27, 21, 50, 35, 36,
     40, 74, 63, 72, 76, 76, 56, 85, 79, 22, 62, 89, 92, 66, 53, 90, 56, 14, 39, 15, 23, 31, 0, 27, 72, 84, 86, 4, 43,
     72, 32],
    [51, 25, 64, 58, 30, 53, 56, 26, 81, 53, 71, 70, 18, 31, 14, 90, 56, 89, 37, 62, 56, 51, 78, 53, 28, 23, 17, 27, 50,
     54, 13, 69, 40, 5, 22, 47, 12, 13, 54, 40, 45, 78, 21, 96, 94, 44, 90, 11, 93, 18, 23, 34, 40, 46, 94, 63, 7, 96,
     73, 87, 53, 35, 46, 16, 79, 71, 38, 9, 93, 33, 28, 22, 34, 78, 69, 72, 45, 49, 97, 36, 89, 41, 42, 15, 4, 8, 26,
     64, 53, 31, 12, 93, 15, 25, 47, 51, 61, 35, 34, 43, 3, 18, 95, 27, 77, 22, 42, 0, 85, 13, 82, 42, 41, 92, 18, 0, 4,
     51, 65, 0, 52, 2, 96, 65, 22, 49, 45, 32, 76, 73, 72, 58, 87, 99, 60, 68, 17, 4, 80, 34, 48, 89, 71, 48, 15, 58,
     58, 29, 10, 2],
    [73, 84, 73, 74, 34, 42, 76, 43, 5, 62, 4, 27, 89, 46, 26, 50, 24, 52, 41, 4, 76, 34, 9, 97, 3, 62, 94, 90, 36, 77,
     79, 30, 90, 61, 35, 55, 81, 94, 84, 80, 28, 92, 96, 23, 60, 25, 90, 57, 25, 22, 0, 55, 2, 32, 2, 83, 58, 55, 59,
     41, 80, 51, 28, 72, 55, 76, 16, 15, 83, 10, 91, 70, 42, 76, 26, 23, 42, 80, 52, 7, 2, 65, 27, 29, 22, 57, 69, 68,
     9, 22, 61, 12, 53, 25, 7, 34, 72, 28, 11, 44, 23, 92, 6, 35, 52, 27, 17, 85, 1, 47, 83, 35, 90, 14, 69, 81, 20, 89,
     2, 21, 89, 38, 10, 21, 84, 56, 12, 24, 45, 97, 7, 69, 79, 52, 53, 77, 14, 27, 12, 40, 27, 56, 46, 27, 59, 11, 76,
     61, 66, 71],
    [23, 39, 15, 76, 80, 39, 42, 38, 1, 24, 82, 54, 69, 99, 0, 79, 35, 91, 31, 48, 38, 44, 51, 42, 83, 15, 76, 50, 20,
     39, 24, 31, 52, 54, 69, 19, 63, 51, 31, 68, 3, 2, 75, 95, 11, 10, 5, 18, 25, 96, 44, 37, 4, 19, 51, 7, 58, 72, 40,
     43, 52, 99, 86, 44, 87, 72, 78, 87, 78, 77, 67, 28, 19, 54, 64, 97, 55, 66, 21, 57, 58, 9, 30, 67, 19, 17, 24, 62,
     89, 28, 85, 84, 7, 42, 91, 54, 15, 45, 84, 91, 10, 59, 22, 66, 48, 77, 78, 7, 78, 63, 5, 57, 13, 64, 35, 44, 73,
     25, 73, 49, 31, 21, 79, 52, 34, 80, 85, 70, 64, 31, 56, 47, 25, 49, 57, 5, 43, 30, 29, 48, 53, 55, 15, 34, 25, 67,
     76, 66, 52, 72],
    [8, 62, 84, 25, 46, 57, 86, 48, 18, 15, 31, 46, 6, 87, 89, 38, 64, 90, 93, 92, 49, 16, 7, 1, 69, 60, 24, 99, 59, 28,
     93, 53, 85, 38, 92, 81, 40, 4, 2, 68, 46, 34, 83, 64, 75, 53, 85, 70, 98, 34, 30, 27, 40, 51, 39, 62, 33, 9, 56,
     94, 46, 13, 79, 33, 12, 36, 94, 60, 53, 40, 36, 15, 67, 26, 17, 22, 80, 46, 78, 52, 54, 47, 57, 43, 90, 28, 22, 46,
     59, 0, 94, 53, 89, 45, 80, 30, 36, 27, 90, 75, 85, 42, 55, 35, 47, 83, 85, 78, 54, 50, 28, 22, 71, 47, 7, 51, 59,
     10, 46, 51, 26, 88, 32, 82, 41, 31, 43, 49, 34, 57, 84, 81, 12, 46, 3, 96, 67, 99, 52, 50, 46, 40, 81, 16, 59, 17,
     43, 26, 19, 94],
    [39, 21, 6, 96, 72, 29, 52, 27, 5, 25, 21, 17, 8, 25, 14, 0, 36, 36, 62, 0, 35, 26, 92, 49, 7, 16, 46, 97, 33, 85,
     63, 30, 8, 12, 92, 6, 57, 97, 60, 25, 21, 87, 24, 5, 26, 41, 10, 6, 57, 34, 15, 62, 26, 75, 78, 51, 56, 62, 47, 80,
     83, 32, 89, 9, 45, 87, 79, 9, 23, 67, 98, 52, 66, 24, 97, 34, 27, 17, 11, 43, 35, 92, 70, 45, 58, 98, 77, 39, 55,
     26, 89, 79, 20, 85, 87, 3, 76, 48, 93, 59, 51, 3, 60, 51, 30, 35, 32, 62, 20, 77, 87, 59, 56, 13, 8, 84, 8, 70, 4,
     63, 2, 79, 86, 43, 61, 53, 68, 83, 6, 30, 6, 86, 61, 26, 74, 37, 99, 24, 83, 33, 2, 58, 63, 93, 67, 3, 14, 33, 50,
     68],
    [92, 64, 84, 37, 16, 95, 24, 20, 38, 84, 4, 51, 78, 8, 76, 30, 58, 6, 26, 69, 60, 59, 0, 99, 66, 18, 39, 61, 13, 54,
     76, 17, 3, 33, 5, 66, 64, 48, 15, 67, 1, 29, 62, 65, 49, 57, 11, 32, 89, 37, 86, 0, 69, 86, 92, 71, 92, 24, 92, 63,
     71, 29, 36, 22, 12, 12, 28, 58, 60, 79, 54, 54, 33, 69, 3, 84, 97, 83, 17, 56, 58, 41, 22, 2, 11, 78, 28, 48, 26,
     19, 0, 0, 51, 83, 0, 79, 28, 0, 92, 62, 40, 78, 98, 81, 7, 54, 76, 32, 43, 20, 20, 40, 36, 5, 89, 26, 59, 2, 27,
     18, 3, 55, 81, 20, 12, 96, 24, 56, 64, 18, 53, 60, 87, 87, 15, 95, 37, 32, 11, 59, 70, 2, 81, 41, 80, 76, 9, 4, 42,
     16],
    [27, 12, 75, 66, 68, 6, 18, 12, 54, 55, 16, 50, 91, 45, 57, 7, 80, 23, 38, 10, 10, 50, 26, 8, 39, 88, 42, 30, 39, 8,
     82, 71, 25, 87, 7, 61, 39, 81, 30, 21, 43, 98, 93, 27, 0, 9, 52, 41, 18, 21, 49, 93, 62, 27, 5, 38, 41, 92, 87, 70,
     96, 24, 17, 98, 39, 70, 12, 6, 76, 81, 93, 62, 42, 64, 41, 90, 24, 35, 9, 17, 57, 77, 87, 93, 80, 45, 77, 70, 64,
     60, 15, 75, 33, 0, 71, 89, 49, 19, 79, 53, 88, 48, 95, 37, 62, 84, 41, 63, 13, 28, 78, 72, 67, 90, 91, 96, 64, 52,
     34, 96, 92, 92, 55, 67, 13, 38, 10, 56, 88, 93, 61, 68, 68, 82, 16, 58, 8, 30, 62, 75, 75, 10, 10, 34, 74, 9, 62,
     77, 99, 50],
    [73, 87, 93, 19, 12, 90, 75, 33, 47, 93, 4, 27, 11, 69, 81, 42, 46, 42, 35, 26, 24, 56, 59, 14, 73, 15, 4, 76, 47,
     43, 1, 97, 79, 33, 49, 93, 14, 74, 95, 33, 96, 90, 60, 99, 19, 16, 65, 15, 0, 73, 91, 55, 93, 29, 47, 12, 91, 89,
     47, 49, 31, 64, 2, 64, 65, 39, 31, 97, 15, 85, 88, 75, 71, 69, 14, 9, 45, 27, 24, 73, 50, 52, 3, 18, 61, 14, 61, 3,
     13, 24, 27, 85, 98, 74, 99, 19, 16, 14, 73, 78, 18, 50, 47, 12, 25, 42, 8, 21, 69, 17, 21, 22, 74, 76, 14, 56, 32,
     44, 69, 84, 39, 54, 19, 17, 5, 21, 96, 64, 94, 58, 0, 74, 56, 47, 93, 44, 96, 63, 20, 73, 12, 21, 10, 77, 59, 28,
     9, 48, 36, 26],
    [26, 22, 27, 90, 74, 37, 75, 76, 57, 1, 9, 40, 96, 45, 12, 13, 46, 98, 25, 26, 20, 73, 82, 51, 9, 92, 24, 47, 82,
     15, 42, 75, 3, 78, 90, 52, 68, 45, 29, 31, 33, 89, 94, 72, 0, 90, 23, 48, 51, 88, 34, 22, 5, 3, 64, 71, 24, 49, 10,
     16, 41, 4, 68, 97, 70, 81, 66, 31, 16, 92, 91, 58, 80, 17, 62, 14, 94, 87, 20, 48, 18, 69, 52, 83, 15, 41, 31, 83,
     58, 13, 40, 80, 55, 76, 91, 81, 44, 43, 2, 78, 23, 6, 34, 4, 69, 7, 41, 81, 41, 65, 52, 65, 51, 80, 18, 73, 3, 32,
     46, 97, 74, 54, 10, 44, 46, 11, 16, 93, 86, 23, 7, 73, 47, 50, 66, 25, 24, 55, 64, 83, 51, 56, 93, 29, 23, 67, 28,
     2, 54, 32],
    [57, 30, 36, 5, 98, 44, 51, 40, 33, 85, 19, 54, 87, 6, 15, 46, 19, 75, 12, 42, 86, 24, 5, 75, 82, 89, 5, 50, 87, 41,
     18, 17, 41, 19, 25, 52, 70, 55, 18, 83, 92, 8, 25, 83, 44, 83, 42, 96, 59, 10, 23, 88, 76, 2, 96, 8, 58, 94, 23, 0,
     42, 84, 73, 41, 27, 35, 41, 79, 82, 55, 45, 62, 52, 61, 34, 90, 13, 30, 86, 49, 27, 9, 6, 75, 50, 89, 77, 81, 76,
     3, 96, 72, 51, 75, 34, 42, 92, 23, 44, 91, 17, 8, 89, 98, 37, 64, 52, 16, 20, 25, 25, 58, 35, 97, 59, 6, 11, 1, 5,
     64, 11, 11, 49, 81, 4, 76, 86, 5, 41, 78, 90, 59, 95, 72, 50, 73, 47, 25, 57, 12, 19, 22, 57, 58, 76, 42, 25, 68,
     33, 40],
    [71, 5, 77, 42, 19, 58, 40, 62, 42, 82, 65, 33, 23, 92, 78, 94, 60, 17, 66, 53, 49, 19, 39, 20, 47, 87, 18, 5, 0,
     34, 7, 59, 23, 61, 87, 77, 76, 74, 37, 36, 88, 7, 65, 80, 25, 76, 0, 26, 95, 82, 62, 13, 9, 66, 14, 29, 58, 11, 53,
     61, 40, 55, 26, 99, 86, 88, 67, 2, 76, 91, 62, 56, 10, 87, 19, 12, 2, 99, 11, 79, 11, 63, 43, 54, 52, 83, 88, 50,
     24, 99, 76, 81, 0, 16, 15, 12, 87, 24, 62, 66, 13, 5, 45, 50, 71, 54, 27, 94, 21, 55, 9, 46, 35, 45, 23, 33, 46,
     37, 63, 64, 77, 3, 76, 77, 49, 20, 97, 8, 58, 63, 3, 50, 55, 44, 92, 12, 38, 65, 10, 72, 26, 76, 33, 80, 19, 87, 6,
     70, 67, 47],
    [31, 88, 89, 95, 19, 32, 2, 86, 27, 18, 16, 25, 51, 58, 85, 24, 87, 18, 82, 65, 66, 21, 88, 99, 61, 73, 92, 32, 54,
     82, 78, 1, 86, 62, 68, 60, 64, 66, 55, 35, 62, 7, 50, 18, 46, 12, 23, 39, 75, 35, 51, 50, 28, 56, 41, 57, 36, 68,
     54, 86, 89, 18, 69, 10, 2, 58, 77, 94, 78, 77, 16, 62, 28, 95, 71, 2, 47, 9, 22, 80, 37, 58, 7, 67, 9, 89, 85, 69,
     27, 69, 68, 33, 68, 4, 29, 58, 12, 5, 97, 64, 23, 57, 36, 45, 17, 72, 49, 57, 22, 29, 87, 50, 54, 77, 97, 99, 25,
     0, 22, 37, 54, 6, 37, 8, 0, 51, 61, 25, 0, 50, 79, 58, 89, 34, 36, 84, 13, 31, 4, 41, 72, 68, 18, 95, 50, 2, 76,
     72, 97, 72],
    [10, 18, 98, 15, 86, 21, 42, 83, 15, 80, 72, 39, 32, 84, 7, 69, 41, 3, 72, 78, 58, 33, 13, 62, 47, 60, 17, 33, 74,
     16, 82, 3, 98, 57, 60, 69, 91, 84, 73, 36, 28, 28, 39, 29, 40, 64, 75, 9, 2, 33, 59, 53, 4, 87, 40, 44, 92, 47, 63,
     98, 34, 0, 8, 62, 24, 88, 29, 4, 64, 15, 51, 81, 61, 13, 87, 89, 12, 42, 21, 18, 80, 18, 83, 85, 91, 16, 38, 95,
     96, 93, 40, 76, 90, 14, 66, 47, 86, 49, 60, 63, 80, 93, 73, 15, 0, 63, 34, 24, 26, 8, 99, 79, 15, 44, 87, 84, 44,
     48, 24, 56, 85, 86, 52, 98, 71, 40, 94, 29, 48, 95, 82, 92, 83, 94, 23, 66, 99, 84, 99, 59, 17, 2, 93, 49, 58, 52,
     54, 37, 60, 18],
    [94, 2, 29, 32, 92, 56, 68, 96, 93, 56, 51, 34, 12, 61, 1, 83, 68, 85, 71, 10, 22, 24, 77, 52, 10, 84, 41, 7, 88,
     62, 26, 81, 38, 8, 85, 0, 3, 11, 68, 96, 15, 55, 0, 5, 17, 4, 35, 16, 75, 0, 22, 81, 17, 36, 38, 1, 17, 56, 8, 69,
     93, 1, 64, 43, 57, 97, 63, 0, 12, 6, 48, 93, 98, 4, 9, 48, 64, 19, 4, 7, 78, 58, 22, 4, 72, 75, 86, 94, 36, 93, 21,
     54, 54, 62, 61, 90, 40, 31, 29, 72, 69, 11, 23, 70, 29, 96, 89, 85, 20, 30, 32, 28, 81, 34, 68, 47, 84, 60, 24, 8,
     30, 16, 84, 88, 58, 33, 67, 93, 40, 6, 28, 88, 45, 83, 27, 86, 57, 17, 26, 3, 73, 32, 52, 80, 76, 89, 71, 95, 53,
     16],
    [43, 49, 33, 60, 9, 23, 49, 35, 94, 97, 13, 20, 83, 62, 84, 10, 34, 94, 62, 96, 60, 29, 64, 88, 54, 86, 0, 39, 77,
     57, 62, 16, 86, 82, 32, 16, 2, 4, 55, 18, 24, 54, 36, 0, 60, 0, 91, 13, 8, 33, 83, 78, 2, 57, 51, 44, 81, 26, 39,
     87, 49, 13, 91, 91, 49, 64, 25, 41, 30, 93, 23, 91, 57, 7, 64, 96, 46, 0, 83, 72, 56, 62, 77, 88, 80, 12, 6, 39,
     80, 70, 13, 39, 55, 46, 92, 31, 65, 49, 72, 19, 24, 45, 0, 53, 99, 56, 51, 56, 66, 14, 8, 66, 61, 42, 33, 91, 22,
     8, 70, 81, 48, 40, 56, 37, 82, 69, 71, 75, 79, 29, 20, 93, 35, 18, 71, 12, 29, 65, 91, 11, 40, 66, 28, 23, 78, 57,
     19, 57, 44, 37],
    [76, 41, 63, 9, 2, 85, 35, 56, 10, 63, 70, 35, 30, 6, 29, 43, 83, 76, 35, 57, 23, 62, 92, 74, 44, 61, 3, 29, 10, 64,
     4, 78, 47, 18, 68, 19, 77, 13, 22, 4, 8, 59, 89, 30, 34, 90, 14, 34, 3, 42, 9, 5, 84, 54, 29, 95, 12, 16, 26, 85,
     96, 18, 65, 34, 80, 56, 71, 67, 82, 98, 86, 40, 62, 15, 62, 3, 52, 93, 29, 90, 34, 73, 99, 76, 50, 29, 57, 20, 0,
     39, 89, 40, 63, 91, 38, 86, 31, 83, 7, 21, 83, 47, 27, 96, 78, 19, 17, 65, 28, 27, 12, 11, 93, 32, 91, 76, 99, 10,
     19, 29, 92, 39, 56, 34, 40, 85, 49, 11, 88, 18, 17, 31, 38, 44, 22, 47, 3, 96, 29, 41, 46, 86, 24, 44, 63, 64, 77,
     50, 31, 3],
    [19, 94, 91, 11, 26, 81, 35, 35, 34, 82, 85, 14, 74, 21, 4, 32, 25, 17, 82, 36, 88, 49, 4, 21, 10, 75, 77, 26, 51,
     24, 93, 95, 91, 73, 44, 99, 45, 66, 73, 47, 76, 95, 44, 9, 14, 45, 39, 10, 65, 81, 35, 90, 50, 25, 3, 63, 1, 27,
     28, 67, 68, 75, 95, 12, 97, 92, 83, 81, 8, 5, 65, 55, 40, 21, 50, 2, 94, 80, 14, 73, 59, 81, 66, 98, 9, 65, 44, 13,
     75, 42, 32, 22, 40, 17, 40, 41, 78, 76, 90, 29, 90, 65, 31, 12, 89, 92, 45, 74, 27, 44, 31, 41, 67, 41, 32, 36, 50,
     83, 70, 54, 50, 29, 83, 48, 85, 47, 3, 99, 86, 4, 93, 55, 30, 2, 46, 61, 3, 51, 47, 33, 7, 17, 71, 39, 6, 68, 10,
     55, 35, 47],
    [33, 98, 93, 12, 88, 79, 20, 65, 57, 22, 86, 63, 53, 93, 83, 14, 42, 62, 19, 63, 26, 56, 29, 73, 26, 56, 97, 85, 12,
     73, 12, 78, 13, 45, 49, 44, 90, 77, 60, 18, 69, 22, 39, 46, 30, 7, 92, 36, 88, 4, 3, 16, 69, 57, 19, 33, 11, 65,
     40, 62, 63, 96, 5, 64, 64, 0, 18, 26, 82, 90, 50, 17, 69, 51, 53, 0, 88, 80, 85, 57, 39, 91, 94, 62, 31, 2, 23, 35,
     37, 79, 71, 1, 88, 19, 79, 44, 87, 13, 50, 40, 12, 71, 2, 97, 20, 74, 7, 68, 27, 93, 26, 81, 49, 11, 92, 57, 81,
     30, 38, 69, 49, 30, 37, 85, 55, 24, 42, 12, 13, 82, 54, 73, 98, 55, 90, 41, 56, 93, 75, 41, 0, 71, 88, 45, 15, 2,
     3, 62, 40, 19],
    [1, 70, 48, 87, 40, 78, 58, 51, 4, 28, 59, 51, 48, 83, 67, 38, 62, 84, 17, 48, 67, 57, 93, 49, 88, 6, 5, 28, 10, 0,
     28, 93, 48, 67, 17, 43, 50, 23, 80, 64, 98, 96, 17, 70, 28, 92, 44, 63, 92, 23, 36, 27, 2, 93, 97, 34, 68, 86, 92,
     60, 87, 16, 33, 75, 60, 48, 82, 93, 18, 88, 29, 89, 11, 67, 81, 82, 38, 13, 81, 46, 72, 40, 14, 68, 78, 29, 1, 84,
     60, 1, 13, 45, 51, 25, 64, 86, 65, 74, 73, 52, 28, 56, 25, 42, 50, 35, 84, 40, 88, 44, 45, 55, 38, 21, 7, 13, 83,
     32, 34, 92, 50, 23, 73, 22, 71, 11, 42, 31, 86, 98, 43, 27, 76, 66, 45, 47, 93, 58, 37, 79, 27, 32, 85, 56, 44, 39,
     41, 22, 98, 43],
    [92, 61, 48, 21, 46, 12, 56, 87, 0, 83, 11, 2, 52, 64, 11, 72, 56, 24, 0, 71, 34, 31, 12, 87, 95, 37, 27, 7, 73, 24,
     26, 22, 50, 72, 49, 40, 56, 84, 26, 50, 64, 93, 79, 8, 66, 37, 64, 57, 70, 3, 41, 77, 71, 42, 70, 46, 89, 46, 82,
     25, 93, 72, 38, 29, 88, 7, 0, 70, 72, 83, 7, 43, 95, 29, 20, 45, 53, 75, 45, 21, 52, 90, 65, 30, 10, 72, 95, 87,
     68, 48, 30, 84, 39, 1, 37, 90, 82, 12, 79, 12, 85, 88, 99, 79, 94, 87, 33, 33, 12, 84, 76, 40, 3, 81, 7, 41, 5, 20,
     17, 19, 19, 13, 64, 32, 70, 67, 53, 38, 24, 6, 67, 68, 16, 16, 48, 13, 30, 16, 81, 98, 27, 80, 48, 78, 62, 93, 33,
     38, 43, 7],
    [42, 35, 78, 93, 40, 11, 32, 96, 63, 85, 11, 47, 33, 97, 68, 39, 96, 44, 75, 46, 25, 33, 16, 55, 23, 51, 70, 9, 16,
     2, 66, 30, 76, 6, 72, 26, 90, 88, 57, 53, 29, 91, 73, 89, 91, 58, 37, 39, 28, 45, 72, 76, 38, 1, 79, 91, 23, 63,
     92, 46, 75, 55, 71, 44, 75, 20, 20, 49, 30, 10, 50, 75, 50, 13, 22, 35, 69, 19, 25, 7, 93, 16, 16, 73, 98, 99, 4,
     13, 73, 50, 88, 30, 28, 7, 21, 52, 47, 66, 90, 54, 57, 66, 69, 70, 78, 14, 31, 37, 42, 65, 17, 97, 64, 36, 34, 35,
     19, 42, 14, 86, 67, 30, 6, 24, 24, 89, 58, 62, 52, 8, 65, 86, 20, 59, 52, 84, 90, 46, 54, 56, 35, 39, 99, 84, 67,
     11, 9, 61, 27, 44],
    [77, 78, 51, 36, 14, 48, 67, 74, 43, 49, 76, 37, 11, 90, 13, 47, 35, 29, 19, 3, 78, 71, 38, 54, 58, 2, 29, 90, 82,
     88, 23, 90, 77, 1, 41, 76, 86, 75, 95, 1, 17, 72, 74, 11, 46, 54, 33, 36, 99, 26, 79, 17, 4, 52, 18, 6, 72, 57, 81,
     83, 46, 34, 95, 68, 64, 15, 92, 88, 66, 44, 54, 85, 1, 23, 80, 19, 84, 29, 5, 82, 63, 97, 73, 76, 40, 69, 31, 35,
     78, 5, 81, 86, 43, 67, 89, 3, 79, 63, 77, 83, 80, 99, 48, 21, 58, 73, 35, 24, 2, 93, 12, 56, 9, 21, 67, 59, 11, 9,
     43, 83, 79, 91, 61, 10, 97, 12, 86, 74, 13, 10, 89, 88, 64, 4, 47, 62, 72, 47, 83, 96, 21, 80, 88, 89, 85, 19, 70,
     8, 30, 15],
    [51, 69, 10, 74, 62, 14, 6, 23, 88, 6, 22, 93, 38, 73, 3, 89, 66, 76, 87, 51, 93, 14, 99, 92, 29, 19, 48, 39, 88, 1,
     30, 66, 19, 43, 29, 26, 94, 8, 88, 11, 77, 40, 17, 91, 57, 13, 36, 56, 88, 36, 68, 87, 80, 39, 84, 35, 93, 55, 40,
     60, 42, 68, 42, 5, 34, 29, 27, 75, 59, 84, 89, 18, 3, 24, 36, 60, 86, 37, 50, 58, 18, 30, 20, 56, 79, 55, 24, 10,
     80, 59, 63, 60, 54, 31, 55, 97, 41, 57, 58, 31, 91, 54, 76, 30, 58, 86, 63, 93, 35, 48, 56, 99, 91, 34, 91, 0, 73,
     63, 56, 76, 41, 86, 4, 72, 37, 9, 40, 3, 95, 30, 2, 83, 97, 32, 42, 87, 37, 91, 94, 68, 8, 58, 35, 44, 91, 65, 16,
     25, 88, 79],
    [3, 91, 22, 22, 28, 33, 24, 25, 38, 14, 83, 24, 30, 70, 69, 16, 51, 24, 17, 2, 26, 24, 64, 58, 90, 51, 5, 66, 74,
     28, 82, 16, 48, 31, 33, 99, 25, 42, 41, 42, 3, 0, 45, 56, 18, 30, 0, 40, 81, 38, 49, 49, 53, 91, 93, 43, 28, 53,
     11, 72, 88, 51, 72, 85, 5, 88, 33, 76, 38, 3, 15, 23, 95, 61, 56, 27, 44, 69, 56, 66, 51, 33, 3, 20, 56, 52, 35, 7,
     89, 14, 35, 77, 34, 80, 47, 14, 15, 66, 72, 53, 14, 98, 99, 0, 56, 17, 63, 2, 49, 68, 28, 4, 79, 24, 92, 78, 39, 9,
     21, 25, 42, 71, 46, 93, 57, 60, 56, 96, 43, 23, 56, 98, 56, 97, 86, 70, 35, 68, 63, 49, 29, 32, 67, 40, 95, 47, 2,
     51, 58, 6],
    [38, 36, 65, 16, 68, 22, 13, 66, 26, 15, 1, 1, 15, 18, 77, 22, 89, 2, 36, 90, 28, 68, 15, 5, 14, 12, 9, 25, 61, 35,
     70, 95, 79, 18, 6, 76, 2, 97, 46, 29, 7, 66, 83, 84, 22, 58, 49, 45, 64, 42, 33, 63, 93, 78, 76, 61, 83, 99, 90,
     73, 63, 1, 15, 12, 77, 27, 23, 50, 62, 67, 24, 65, 84, 0, 43, 9, 33, 65, 96, 33, 25, 41, 5, 7, 2, 63, 1, 49, 22,
     43, 15, 22, 88, 92, 64, 54, 83, 28, 43, 43, 13, 44, 97, 89, 87, 69, 86, 14, 50, 36, 69, 67, 85, 51, 0, 60, 35, 14,
     31, 32, 73, 13, 87, 95, 58, 7, 10, 12, 89, 41, 83, 24, 17, 20, 28, 58, 54, 29, 68, 44, 94, 15, 33, 98, 31, 81, 81,
     67, 3, 25],
    [99, 38, 2, 11, 36, 56, 84, 58, 71, 65, 2, 35, 23, 78, 4, 12, 77, 6, 15, 56, 84, 6, 46, 96, 80, 87, 46, 73, 78, 31,
     86, 11, 9, 49, 47, 43, 95, 52, 93, 78, 25, 12, 80, 43, 50, 90, 64, 49, 66, 35, 89, 19, 9, 43, 29, 61, 92, 44, 57,
     88, 46, 66, 94, 65, 53, 98, 63, 75, 59, 44, 37, 28, 76, 98, 61, 81, 40, 11, 29, 21, 15, 33, 58, 15, 22, 29, 34, 72,
     96, 32, 89, 55, 34, 11, 88, 31, 78, 6, 44, 71, 92, 63, 7, 25, 38, 6, 36, 43, 99, 70, 64, 35, 80, 90, 83, 91, 53,
     83, 26, 79, 25, 31, 82, 59, 24, 37, 68, 95, 89, 24, 8, 81, 6, 14, 48, 13, 81, 0, 6, 96, 83, 77, 65, 31, 49, 3, 0,
     96, 89, 17],
    [8, 68, 29, 17, 36, 60, 79, 94, 20, 51, 53, 86, 23, 79, 85, 86, 72, 89, 70, 34, 14, 26, 22, 70, 93, 16, 49, 13, 21,
     11, 29, 42, 36, 69, 35, 9, 34, 31, 5, 95, 32, 3, 64, 44, 21, 33, 91, 81, 39, 63, 9, 40, 63, 76, 63, 11, 31, 60, 49,
     10, 44, 34, 60, 88, 27, 20, 9, 93, 45, 93, 27, 24, 52, 7, 84, 19, 22, 43, 14, 83, 56, 68, 70, 3, 73, 8, 88, 64, 76,
     13, 56, 42, 17, 37, 59, 5, 38, 3, 71, 63, 5, 17, 20, 58, 17, 97, 56, 21, 21, 66, 20, 81, 84, 97, 31, 37, 82, 5, 70,
     97, 44, 15, 63, 35, 47, 93, 97, 0, 12, 22, 88, 88, 16, 42, 2, 54, 47, 52, 33, 99, 12, 78, 55, 22, 86, 62, 50, 63,
     36, 27],
    [91, 20, 79, 3, 85, 15, 32, 40, 96, 11, 81, 45, 28, 38, 87, 97, 50, 76, 64, 2, 51, 78, 32, 4, 65, 94, 5, 70, 44, 69,
     3, 39, 80, 27, 24, 26, 59, 39, 47, 70, 29, 34, 73, 24, 49, 81, 41, 10, 68, 57, 50, 43, 5, 31, 36, 98, 49, 69, 20,
     25, 85, 91, 87, 87, 82, 3, 43, 37, 98, 54, 36, 82, 14, 73, 84, 40, 92, 22, 73, 56, 91, 15, 36, 33, 15, 72, 60, 83,
     92, 61, 39, 19, 54, 91, 34, 80, 19, 22, 25, 26, 34, 79, 58, 26, 74, 95, 11, 65, 65, 39, 66, 9, 28, 29, 66, 75, 52,
     35, 19, 12, 44, 81, 64, 11, 9, 25, 28, 96, 32, 52, 27, 43, 62, 88, 60, 77, 78, 66, 11, 24, 29, 26, 8, 91, 58, 85,
     58, 78, 7, 75],
    [31, 51, 60, 71, 19, 1, 82, 59, 56, 78, 74, 19, 75, 95, 68, 8, 86, 14, 1, 23, 21, 88, 22, 91, 68, 38, 79, 32, 49,
     92, 30, 57, 1, 93, 15, 0, 76, 43, 83, 16, 12, 95, 19, 46, 70, 1, 79, 31, 59, 13, 63, 91, 3, 45, 46, 57, 9, 51, 17,
     71, 31, 72, 55, 36, 45, 96, 40, 38, 90, 48, 96, 44, 7, 68, 99, 98, 74, 43, 31, 81, 39, 97, 59, 2, 63, 5, 93, 51,
     77, 97, 59, 39, 39, 92, 16, 73, 15, 15, 52, 63, 82, 14, 82, 63, 51, 36, 18, 78, 29, 91, 95, 10, 44, 84, 66, 78, 37,
     46, 59, 26, 36, 89, 34, 18, 24, 40, 51, 90, 58, 30, 81, 15, 51, 99, 51, 22, 34, 49, 73, 32, 75, 41, 99, 25, 6, 13,
     7, 67, 76, 75],
    [50, 40, 76, 50, 40, 99, 29, 87, 8, 82, 51, 60, 38, 25, 64, 62, 49, 10, 66, 64, 43, 33, 63, 27, 24, 46, 76, 87, 64,
     15, 4, 1, 56, 54, 56, 32, 4, 45, 96, 89, 89, 84, 57, 82, 5, 90, 69, 41, 20, 60, 52, 66, 63, 76, 38, 41, 68, 49, 31,
     37, 64, 25, 37, 31, 88, 14, 38, 2, 85, 30, 72, 49, 35, 72, 89, 30, 36, 13, 17, 29, 73, 22, 35, 21, 61, 62, 94, 28,
     50, 58, 31, 3, 70, 40, 53, 36, 80, 47, 60, 23, 62, 10, 43, 55, 59, 76, 81, 78, 19, 87, 38, 22, 11, 96, 2, 24, 63,
     98, 15, 66, 80, 29, 78, 63, 51, 47, 29, 48, 63, 38, 51, 12, 36, 7, 97, 57, 61, 29, 72, 59, 52, 15, 91, 78, 7, 21,
     24, 58, 59, 95],
    [59, 14, 58, 54, 89, 52, 94, 92, 89, 87, 18, 14, 2, 56, 27, 51, 45, 25, 20, 2, 96, 22, 73, 82, 59, 44, 18, 6, 53,
     15, 41, 47, 41, 44, 29, 3, 9, 18, 99, 83, 50, 70, 74, 21, 91, 90, 90, 32, 83, 58, 44, 58, 31, 60, 16, 98, 76, 9,
     42, 8, 77, 51, 8, 39, 26, 25, 46, 97, 91, 56, 60, 95, 67, 3, 42, 17, 43, 78, 58, 39, 83, 4, 57, 48, 76, 19, 57, 59,
     58, 23, 89, 94, 82, 55, 98, 84, 89, 82, 61, 60, 92, 25, 26, 89, 58, 8, 33, 54, 57, 68, 89, 61, 58, 56, 93, 29, 32,
     36, 41, 0, 93, 82, 45, 6, 62, 33, 10, 55, 37, 20, 22, 49, 88, 70, 92, 91, 95, 61, 49, 56, 2, 91, 43, 40, 20, 65,
     83, 0, 95, 30],
    [91, 65, 82, 84, 25, 62, 94, 58, 97, 0, 3, 12, 74, 71, 26, 3, 87, 81, 16, 58, 97, 90, 23, 78, 95, 2, 19, 94, 2, 99,
     22, 60, 98, 20, 99, 40, 94, 38, 5, 48, 0, 24, 1, 63, 4, 44, 85, 95, 58, 18, 47, 3, 80, 30, 64, 98, 52, 78, 60, 55,
     32, 71, 34, 72, 3, 5, 75, 5, 54, 50, 8, 61, 71, 76, 39, 23, 81, 51, 59, 43, 91, 63, 87, 90, 93, 93, 53, 89, 99, 3,
     85, 38, 46, 28, 75, 56, 25, 21, 37, 82, 53, 29, 81, 72, 63, 67, 19, 87, 68, 14, 47, 24, 76, 26, 0, 2, 92, 77, 67,
     46, 29, 59, 84, 34, 59, 77, 58, 18, 49, 95, 17, 47, 21, 45, 62, 29, 3, 7, 62, 93, 30, 86, 1, 95, 89, 83, 68, 23,
     26, 5],
    [18, 51, 20, 19, 77, 63, 67, 4, 74, 6, 55, 23, 62, 72, 84, 66, 2, 49, 7, 68, 82, 68, 40, 87, 0, 92, 60, 44, 79, 66,
     44, 78, 83, 98, 39, 35, 9, 60, 22, 77, 89, 94, 83, 20, 67, 50, 88, 72, 0, 28, 73, 94, 75, 7, 40, 41, 66, 13, 2, 3,
     86, 18, 94, 54, 37, 45, 17, 44, 35, 61, 73, 46, 58, 95, 38, 75, 33, 2, 65, 43, 87, 30, 36, 52, 72, 43, 54, 32, 26,
     0, 4, 36, 65, 22, 11, 84, 97, 95, 78, 38, 84, 12, 87, 38, 17, 54, 36, 98, 19, 9, 66, 91, 61, 47, 61, 99, 54, 84,
     53, 41, 98, 37, 30, 25, 85, 12, 72, 57, 86, 34, 96, 5, 93, 35, 56, 49, 95, 29, 73, 38, 29, 17, 17, 50, 70, 76, 86,
     96, 23, 80],
    [11, 47, 41, 83, 72, 12, 16, 16, 9, 65, 74, 13, 44, 64, 42, 51, 77, 74, 46, 12, 95, 46, 27, 4, 1, 44, 36, 14, 59,
     17, 68, 2, 47, 89, 65, 35, 75, 57, 5, 6, 40, 68, 81, 46, 61, 36, 40, 31, 5, 64, 63, 98, 73, 54, 81, 78, 66, 65, 38,
     47, 28, 97, 73, 95, 59, 90, 45, 12, 12, 91, 99, 22, 26, 85, 79, 96, 91, 33, 72, 61, 4, 70, 9, 80, 15, 39, 19, 56,
     99, 10, 95, 93, 67, 91, 42, 40, 32, 37, 63, 10, 72, 29, 28, 51, 77, 37, 71, 21, 68, 4, 30, 26, 55, 39, 65, 70, 94,
     53, 82, 56, 55, 93, 34, 94, 25, 65, 42, 98, 72, 1, 18, 1, 60, 71, 57, 32, 11, 51, 96, 1, 6, 15, 23, 43, 66, 56, 96,
     3, 16, 38],
    [18, 13, 60, 87, 76, 44, 25, 18, 73, 40, 13, 14, 45, 94, 18, 14, 95, 60, 61, 78, 98, 48, 57, 88, 63, 72, 44, 63, 17,
     74, 64, 7, 69, 1, 20, 85, 34, 73, 42, 19, 9, 3, 43, 76, 60, 12, 91, 45, 73, 25, 72, 76, 83, 55, 25, 65, 43, 28, 49,
     96, 10, 94, 99, 47, 35, 84, 32, 34, 16, 76, 85, 1, 81, 19, 70, 53, 14, 75, 38, 30, 92, 95, 93, 72, 46, 4, 75, 98,
     49, 37, 26, 80, 52, 81, 28, 83, 38, 60, 41, 72, 0, 47, 87, 63, 69, 70, 67, 20, 52, 4, 25, 25, 10, 36, 1, 42, 94,
     38, 20, 75, 60, 1, 72, 70, 35, 44, 69, 20, 67, 38, 66, 38, 44, 38, 30, 51, 54, 16, 79, 67, 85, 59, 2, 92, 88, 27,
     60, 83, 64, 22],
    [1, 48, 1, 97, 24, 86, 94, 17, 85, 80, 19, 45, 59, 74, 20, 32, 80, 72, 38, 85, 2, 39, 31, 8, 36, 29, 98, 24, 18, 20,
     85, 21, 85, 75, 48, 3, 4, 92, 88, 85, 14, 82, 78, 97, 26, 22, 17, 41, 59, 12, 61, 81, 97, 11, 18, 93, 69, 62, 67,
     18, 40, 91, 8, 73, 52, 35, 93, 84, 68, 44, 46, 96, 42, 12, 83, 25, 23, 69, 4, 41, 11, 80, 81, 9, 57, 67, 92, 51, 8,
     95, 33, 6, 21, 62, 86, 54, 65, 12, 82, 47, 41, 94, 47, 12, 41, 91, 5, 56, 26, 27, 14, 78, 93, 66, 4, 56, 58, 79,
     85, 63, 70, 66, 36, 71, 18, 82, 10, 3, 22, 9, 91, 76, 83, 3, 8, 47, 18, 92, 30, 12, 77, 0, 97, 27, 53, 83, 4, 55,
     90, 5],
    [33, 6, 73, 87, 60, 56, 90, 55, 9, 35, 91, 5, 23, 37, 7, 49, 43, 57, 39, 8, 29, 3, 95, 2, 83, 3, 24, 37, 1, 50, 38,
     13, 41, 80, 26, 25, 48, 29, 2, 8, 97, 44, 11, 57, 62, 72, 48, 1, 33, 16, 43, 72, 99, 83, 9, 62, 56, 12, 67, 90, 54,
     34, 33, 2, 76, 87, 9, 43, 65, 84, 73, 86, 71, 40, 59, 14, 71, 26, 43, 74, 30, 12, 80, 56, 67, 57, 56, 72, 14, 21,
     7, 47, 24, 44, 97, 87, 14, 36, 62, 79, 70, 37, 28, 74, 77, 49, 37, 26, 28, 39, 30, 41, 25, 4, 40, 98, 17, 34, 93,
     85, 97, 59, 73, 93, 13, 43, 0, 90, 30, 57, 41, 60, 56, 85, 6, 98, 84, 91, 82, 97, 38, 64, 9, 13, 13, 36, 53, 0, 17,
     49],
    [1, 67, 23, 82, 49, 69, 62, 68, 58, 96, 63, 41, 99, 81, 71, 79, 18, 59, 68, 86, 33, 73, 27, 90, 57, 61, 29, 69, 9,
     76, 92, 9, 66, 75, 96, 48, 38, 93, 62, 41, 7, 57, 26, 12, 1, 35, 93, 92, 97, 89, 50, 2, 7, 8, 67, 46, 81, 65, 42,
     20, 88, 53, 69, 2, 89, 27, 97, 20, 49, 66, 54, 83, 99, 12, 82, 41, 73, 2, 7, 58, 92, 39, 10, 97, 7, 5, 54, 49, 41,
     71, 85, 27, 2, 72, 18, 45, 87, 63, 21, 82, 51, 37, 23, 35, 48, 62, 36, 85, 76, 25, 46, 44, 35, 96, 21, 31, 22, 72,
     32, 53, 85, 58, 10, 49, 39, 45, 70, 0, 64, 97, 17, 51, 90, 13, 79, 59, 93, 33, 26, 27, 54, 13, 40, 15, 99, 49, 63,
     7, 8, 14],
    [61, 2, 32, 21, 86, 58, 87, 65, 59, 20, 72, 22, 83, 51, 36, 69, 68, 76, 89, 64, 33, 79, 73, 11, 9, 91, 50, 64, 86,
     78, 25, 50, 94, 2, 18, 28, 70, 56, 38, 33, 31, 47, 30, 8, 66, 48, 17, 54, 9, 51, 13, 76, 61, 6, 81, 28, 56, 75, 62,
     83, 11, 5, 41, 49, 42, 27, 30, 6, 49, 94, 5, 23, 94, 83, 31, 92, 76, 41, 18, 41, 69, 37, 22, 31, 96, 4, 53, 3, 46,
     44, 70, 78, 50, 60, 67, 53, 53, 28, 82, 54, 34, 26, 71, 84, 43, 46, 17, 53, 22, 39, 4, 6, 31, 86, 93, 9, 52, 17,
     30, 64, 91, 66, 46, 21, 70, 85, 32, 33, 27, 32, 83, 4, 23, 87, 54, 30, 69, 80, 96, 6, 88, 97, 86, 63, 92, 61, 5,
     43, 11, 34],
    [19, 48, 74, 33, 35, 89, 50, 79, 72, 73, 30, 26, 61, 36, 2, 69, 99, 11, 29, 49, 90, 3, 61, 47, 73, 89, 79, 95, 23,
     42, 28, 47, 7, 5, 71, 56, 65, 48, 43, 42, 56, 73, 79, 80, 99, 98, 92, 59, 94, 28, 5, 32, 80, 13, 0, 59, 76, 53, 66,
     13, 25, 49, 36, 29, 64, 8, 11, 27, 73, 96, 42, 84, 81, 26, 78, 73, 4, 78, 39, 81, 46, 91, 9, 18, 65, 23, 64, 5, 73,
     3, 38, 6, 3, 96, 81, 98, 70, 88, 8, 33, 41, 81, 71, 8, 33, 84, 62, 82, 64, 24, 76, 51, 6, 1, 91, 35, 37, 36, 69,
     27, 43, 57, 48, 71, 78, 58, 76, 68, 76, 36, 15, 73, 1, 51, 56, 19, 38, 5, 35, 19, 21, 83, 76, 31, 49, 36, 15, 88,
     51, 90],
    [61, 35, 86, 3, 16, 71, 35, 75, 76, 53, 24, 27, 28, 91, 71, 48, 76, 3, 61, 45, 38, 4, 74, 7, 7, 83, 11, 29, 77, 92,
     72, 61, 72, 30, 94, 13, 64, 72, 50, 98, 22, 78, 51, 96, 58, 43, 97, 32, 19, 59, 76, 51, 44, 27, 7, 12, 16, 5, 81,
     17, 93, 86, 95, 62, 16, 51, 24, 92, 68, 75, 47, 73, 93, 77, 28, 60, 86, 90, 77, 82, 46, 22, 18, 41, 42, 48, 67, 60,
     52, 89, 17, 25, 20, 73, 10, 60, 98, 79, 7, 6, 83, 77, 47, 18, 31, 37, 7, 68, 79, 77, 52, 41, 70, 87, 2, 2, 95, 37,
     13, 10, 83, 10, 10, 41, 49, 96, 34, 43, 65, 14, 13, 58, 90, 3, 67, 98, 31, 64, 8, 42, 53, 42, 90, 24, 0, 56, 35,
     77, 92, 37],
    [71, 15, 67, 85, 30, 70, 59, 77, 4, 49, 74, 36, 65, 4, 64, 45, 48, 4, 52, 71, 32, 73, 54, 15, 27, 56, 53, 46, 1, 2,
     12, 68, 92, 93, 80, 9, 95, 87, 1, 68, 94, 90, 14, 19, 3, 64, 55, 36, 2, 89, 81, 64, 87, 14, 87, 50, 97, 9, 51, 99,
     40, 56, 11, 70, 85, 45, 87, 97, 19, 53, 17, 64, 45, 9, 11, 94, 58, 79, 10, 59, 9, 29, 32, 21, 12, 53, 87, 81, 47,
     83, 37, 14, 57, 91, 85, 43, 20, 48, 21, 84, 47, 27, 39, 31, 19, 32, 17, 17, 50, 56, 11, 66, 45, 82, 85, 20, 36, 54,
     57, 7, 76, 92, 47, 45, 47, 65, 92, 55, 72, 59, 82, 66, 66, 52, 61, 51, 95, 19, 33, 41, 70, 65, 60, 5, 55, 20, 1,
     15, 35, 67],
    [16, 70, 38, 28, 12, 54, 35, 81, 47, 70, 59, 7, 99, 34, 86, 74, 6, 19, 23, 69, 81, 15, 18, 81, 21, 67, 74, 14, 9,
     56, 45, 40, 17, 79, 22, 67, 29, 46, 46, 34, 14, 48, 7, 24, 72, 35, 41, 57, 92, 27, 35, 18, 36, 9, 55, 60, 42, 52,
     78, 18, 30, 65, 10, 39, 94, 42, 81, 67, 12, 68, 51, 38, 51, 52, 67, 17, 93, 63, 76, 6, 12, 87, 40, 93, 34, 4, 11,
     8, 47, 33, 24, 23, 98, 28, 39, 96, 0, 22, 78, 66, 61, 33, 24, 58, 8, 38, 9, 70, 74, 4, 86, 73, 76, 91, 72, 95, 45,
     86, 85, 96, 29, 22, 20, 77, 5, 59, 14, 44, 95, 21, 59, 21, 2, 57, 55, 31, 62, 88, 16, 88, 34, 26, 63, 24, 83, 33,
     28, 35, 18, 55],
    [82, 17, 49, 2, 51, 37, 95, 37, 51, 69, 44, 95, 14, 39, 36, 94, 33, 40, 32, 60, 85, 59, 66, 74, 18, 3, 65, 0, 16,
     43, 17, 95, 74, 2, 14, 73, 45, 10, 17, 13, 70, 46, 0, 18, 69, 84, 13, 73, 26, 78, 23, 4, 94, 46, 20, 44, 44, 32,
     84, 72, 12, 80, 69, 22, 44, 74, 79, 5, 95, 77, 25, 73, 12, 59, 14, 60, 11, 35, 67, 85, 8, 47, 74, 47, 6, 53, 29,
     96, 24, 53, 36, 68, 85, 35, 35, 90, 27, 81, 30, 36, 24, 11, 77, 37, 77, 39, 46, 51, 15, 58, 58, 45, 32, 97, 84, 44,
     39, 61, 3, 63, 79, 4, 69, 47, 53, 29, 30, 37, 95, 11, 25, 50, 82, 64, 15, 72, 97, 4, 45, 0, 25, 11, 35, 88, 97, 40,
     9, 46, 1, 34],
    [95, 65, 95, 26, 85, 8, 16, 39, 7, 81, 52, 76, 36, 64, 60, 92, 89, 13, 47, 0, 79, 10, 67, 59, 58, 26, 78, 23, 36,
     65, 3, 75, 97, 28, 10, 57, 80, 56, 94, 33, 1, 62, 4, 20, 25, 92, 11, 75, 61, 89, 1, 47, 26, 63, 22, 96, 15, 12, 90,
     93, 86, 64, 38, 4, 56, 4, 10, 5, 37, 55, 54, 80, 26, 48, 7, 84, 7, 34, 97, 91, 10, 5, 81, 60, 54, 86, 60, 52, 67,
     40, 96, 38, 95, 26, 32, 99, 12, 20, 51, 86, 92, 59, 64, 69, 11, 56, 65, 59, 24, 15, 24, 3, 44, 2, 81, 6, 36, 98,
     59, 42, 86, 78, 18, 19, 52, 14, 1, 67, 7, 94, 16, 87, 31, 49, 15, 73, 66, 32, 64, 97, 56, 36, 74, 89, 84, 58, 5,
     12, 88, 94],
    [8, 34, 47, 52, 0, 70, 77, 12, 40, 61, 38, 16, 2, 35, 60, 44, 52, 82, 14, 38, 19, 81, 54, 71, 73, 0, 66, 4, 72, 39,
     54, 71, 14, 99, 8, 45, 44, 51, 79, 16, 41, 15, 44, 74, 59, 13, 30, 99, 98, 15, 93, 69, 78, 63, 88, 23, 2, 48, 74,
     4, 45, 5, 53, 91, 69, 77, 78, 87, 48, 27, 71, 64, 6, 41, 11, 76, 76, 64, 46, 78, 12, 47, 29, 20, 18, 19, 14, 98,
     10, 31, 5, 38, 92, 41, 34, 12, 65, 31, 12, 63, 1, 17, 77, 76, 75, 46, 11, 26, 67, 29, 78, 51, 93, 81, 74, 1, 14,
     48, 57, 47, 99, 61, 93, 45, 18, 51, 51, 51, 69, 33, 79, 71, 2, 78, 43, 21, 49, 4, 76, 79, 64, 9, 23, 44, 39, 70,
     16, 1, 45, 73],
    [38, 0, 57, 48, 69, 2, 88, 82, 55, 53, 80, 6, 0, 20, 2, 60, 13, 37, 72, 37, 79, 97, 6, 93, 92, 60, 43, 42, 86, 99,
     31, 18, 24, 18, 70, 14, 6, 91, 97, 89, 3, 10, 11, 15, 64, 65, 56, 81, 73, 25, 45, 64, 82, 71, 92, 60, 16, 32, 22,
     26, 14, 12, 86, 13, 39, 39, 22, 44, 22, 62, 56, 17, 1, 65, 0, 44, 54, 80, 75, 42, 72, 76, 57, 25, 1, 34, 62, 77,
     93, 52, 90, 74, 7, 48, 1, 12, 25, 59, 6, 78, 9, 35, 15, 48, 94, 13, 67, 84, 25, 33, 38, 45, 64, 87, 9, 29, 63, 97,
     25, 43, 2, 1, 14, 91, 76, 99, 14, 78, 34, 50, 6, 90, 26, 17, 44, 55, 3, 23, 63, 39, 72, 85, 85, 29, 92, 85, 37, 99,
     51, 24],
    [48, 29, 49, 29, 78, 79, 9, 62, 29, 18, 67, 65, 48, 88, 82, 86, 33, 60, 59, 91, 99, 43, 30, 79, 82, 44, 23, 1, 48,
     54, 97, 1, 49, 93, 70, 29, 25, 38, 65, 4, 74, 66, 0, 61, 24, 81, 65, 60, 58, 93, 23, 61, 21, 94, 0, 97, 64, 80, 14,
     66, 60, 79, 11, 98, 35, 7, 91, 51, 5, 82, 9, 83, 99, 87, 83, 67, 23, 68, 67, 7, 10, 91, 71, 10, 22, 52, 71, 98, 89,
     93, 74, 97, 21, 50, 37, 33, 36, 9, 39, 20, 44, 87, 75, 47, 28, 12, 1, 72, 64, 18, 73, 56, 2, 70, 99, 85, 7, 31, 67,
     94, 22, 19, 24, 41, 39, 72, 99, 2, 68, 87, 40, 30, 65, 34, 31, 15, 67, 90, 57, 75, 67, 5, 59, 31, 1, 88, 80, 40,
     97, 16],
    [60, 14, 18, 42, 57, 1, 27, 55, 97, 79, 28, 47, 38, 43, 59, 47, 40, 40, 28, 18, 79, 21, 34, 96, 11, 21, 26, 55, 72,
     32, 97, 62, 4, 17, 13, 72, 27, 72, 3, 97, 6, 91, 28, 77, 48, 53, 75, 69, 27, 31, 62, 30, 84, 95, 49, 91, 38, 95,
     44, 84, 43, 32, 31, 46, 7, 55, 28, 4, 51, 27, 50, 40, 63, 29, 17, 91, 49, 33, 54, 7, 74, 95, 22, 63, 32, 44, 36,
     99, 95, 88, 29, 78, 25, 41, 79, 31, 44, 68, 70, 45, 27, 58, 27, 15, 41, 78, 35, 21, 9, 63, 15, 2, 54, 35, 86, 73,
     54, 20, 13, 53, 76, 12, 19, 70, 59, 94, 31, 38, 18, 41, 7, 87, 4, 67, 56, 74, 97, 54, 71, 99, 81, 84, 62, 20, 90,
     0, 13, 54, 13, 12],
    [61, 90, 21, 91, 59, 50, 4, 90, 82, 85, 66, 22, 91, 74, 56, 95, 92, 61, 45, 81, 22, 11, 91, 48, 33, 95, 26, 52, 74,
     80, 14, 37, 70, 41, 85, 98, 78, 23, 96, 37, 85, 91, 36, 82, 41, 29, 13, 21, 83, 14, 84, 51, 57, 65, 88, 14, 56, 49,
     88, 81, 66, 78, 22, 79, 58, 54, 60, 92, 54, 30, 63, 32, 83, 84, 65, 40, 70, 41, 22, 98, 48, 39, 42, 65, 32, 19, 28,
     87, 11, 12, 86, 46, 81, 10, 9, 35, 79, 55, 50, 17, 40, 9, 4, 41, 8, 40, 88, 46, 80, 14, 60, 36, 50, 50, 39, 96, 79,
     60, 56, 10, 75, 44, 23, 23, 4, 35, 80, 94, 57, 70, 97, 1, 91, 39, 1, 71, 91, 97, 39, 54, 14, 56, 62, 73, 91, 19,
     78, 88, 72, 10],
    [79, 59, 43, 19, 5, 74, 58, 81, 4, 68, 55, 6, 97, 54, 14, 57, 92, 33, 90, 76, 94, 93, 11, 76, 80, 2, 13, 64, 98, 45,
     38, 65, 57, 9, 92, 6, 14, 97, 41, 95, 54, 8, 7, 88, 23, 33, 40, 53, 84, 3, 87, 46, 73, 91, 74, 57, 59, 44, 11, 49,
     16, 70, 17, 51, 21, 2, 56, 18, 32, 80, 2, 52, 19, 94, 65, 19, 48, 79, 6, 71, 43, 64, 93, 64, 56, 92, 62, 21, 22, 5,
     61, 96, 96, 66, 55, 49, 9, 92, 14, 93, 68, 29, 10, 81, 61, 23, 43, 48, 98, 7, 96, 61, 40, 38, 23, 1, 46, 80, 60, 2,
     88, 45, 77, 11, 27, 3, 26, 3, 78, 80, 4, 62, 70, 27, 7, 12, 16, 89, 93, 29, 76, 44, 84, 64, 95, 28, 86, 49, 20,
     25],
    [48, 66, 63, 98, 79, 80, 43, 60, 47, 10, 67, 80, 52, 79, 16, 38, 67, 34, 38, 92, 2, 37, 74, 34, 94, 38, 84, 30, 35,
     13, 36, 83, 23, 88, 97, 48, 25, 5, 61, 10, 92, 15, 73, 61, 14, 71, 6, 28, 14, 37, 69, 91, 67, 50, 99, 94, 60, 92,
     76, 5, 25, 20, 75, 22, 31, 77, 42, 50, 37, 29, 41, 80, 23, 23, 63, 48, 14, 16, 46, 68, 97, 11, 76, 10, 25, 44, 55,
     40, 57, 48, 72, 34, 92, 15, 86, 47, 27, 45, 78, 63, 48, 27, 8, 41, 90, 2, 27, 25, 15, 46, 38, 24, 47, 49, 99, 92,
     38, 70, 40, 39, 39, 86, 27, 51, 92, 29, 86, 52, 86, 88, 56, 37, 66, 12, 19, 46, 54, 64, 61, 21, 70, 36, 8, 77, 43,
     23, 41, 77, 54, 48],
    [7, 50, 47, 69, 90, 73, 62, 7, 82, 45, 54, 13, 58, 77, 59, 42, 35, 17, 95, 31, 86, 6, 82, 98, 18, 87, 85, 0, 47, 21,
     50, 27, 60, 39, 42, 88, 37, 24, 94, 44, 66, 61, 21, 74, 57, 92, 77, 82, 63, 6, 19, 1, 69, 96, 42, 17, 68, 25, 28,
     53, 23, 18, 37, 70, 82, 4, 20, 75, 72, 63, 9, 91, 54, 10, 51, 32, 80, 68, 33, 75, 97, 7, 25, 1, 97, 30, 55, 24, 67,
     50, 87, 70, 83, 86, 19, 63, 76, 35, 11, 65, 71, 92, 76, 79, 97, 59, 24, 76, 61, 20, 43, 5, 5, 28, 41, 66, 19, 48,
     48, 19, 88, 93, 8, 83, 54, 33, 27, 30, 30, 83, 75, 42, 25, 34, 18, 77, 94, 60, 94, 65, 15, 93, 73, 2, 90, 66, 68,
     12, 50, 71],
    [88, 24, 90, 20, 87, 34, 91, 20, 98, 13, 59, 60, 32, 13, 86, 8, 67, 19, 35, 46, 7, 27, 53, 84, 17, 18, 92, 22, 12,
     43, 68, 9, 66, 6, 33, 81, 64, 22, 1, 65, 25, 9, 43, 15, 37, 85, 62, 28, 78, 67, 75, 94, 16, 70, 49, 21, 61, 98, 80,
     11, 22, 88, 32, 11, 44, 35, 24, 93, 85, 49, 35, 27, 10, 58, 88, 6, 85, 36, 87, 28, 4, 44, 87, 79, 45, 25, 69, 97,
     47, 48, 37, 73, 94, 7, 75, 30, 43, 95, 7, 58, 33, 54, 2, 33, 32, 17, 98, 44, 72, 14, 1, 1, 52, 79, 44, 20, 85, 32,
     25, 45, 75, 93, 95, 92, 49, 39, 36, 25, 45, 1, 48, 66, 84, 99, 76, 4, 9, 5, 62, 57, 12, 85, 2, 99, 79, 40, 27, 70,
     70, 18],
    [40, 77, 78, 53, 13, 68, 48, 62, 27, 12, 13, 61, 88, 87, 2, 27, 17, 3, 78, 28, 20, 71, 6, 12, 33, 92, 58, 14, 40,
     21, 85, 8, 42, 49, 89, 42, 51, 39, 73, 98, 2, 99, 38, 13, 93, 47, 29, 83, 20, 0, 82, 4, 2, 88, 60, 16, 35, 64, 61,
     97, 11, 97, 88, 26, 13, 91, 56, 88, 1, 90, 77, 31, 96, 12, 48, 43, 2, 42, 73, 30, 58, 33, 13, 96, 88, 26, 47, 34,
     29, 36, 79, 56, 32, 36, 28, 29, 70, 49, 85, 33, 6, 42, 61, 67, 52, 73, 77, 86, 89, 93, 36, 43, 82, 50, 98, 45, 79,
     51, 92, 69, 21, 17, 19, 42, 19, 0, 99, 10, 71, 80, 91, 58, 44, 19, 83, 71, 99, 22, 19, 46, 63, 8, 50, 79, 10, 81,
     43, 45, 58, 78],
    [63, 88, 96, 21, 1, 8, 63, 96, 3, 32, 80, 20, 85, 96, 13, 28, 6, 47, 40, 26, 72, 42, 43, 66, 58, 73, 52, 13, 89, 54,
     18, 76, 95, 22, 19, 70, 42, 22, 63, 40, 49, 78, 86, 3, 89, 73, 96, 23, 89, 30, 55, 80, 37, 62, 33, 21, 83, 43, 41,
     16, 62, 9, 3, 27, 40, 26, 86, 14, 24, 19, 68, 63, 50, 33, 8, 75, 27, 22, 9, 79, 2, 94, 19, 76, 52, 91, 99, 61, 35,
     7, 25, 78, 81, 45, 50, 83, 75, 87, 97, 29, 47, 40, 43, 0, 16, 72, 20, 48, 1, 23, 81, 29, 35, 7, 32, 64, 61, 96, 90,
     31, 7, 95, 53, 47, 13, 60, 9, 73, 58, 31, 74, 50, 24, 52, 63, 34, 76, 23, 41, 17, 40, 27, 1, 61, 73, 33, 64, 27,
     48, 26],
    [65, 94, 36, 65, 38, 42, 35, 96, 75, 39, 5, 17, 40, 84, 9, 36, 85, 70, 12, 95, 13, 21, 83, 37, 83, 23, 32, 73, 17,
     45, 12, 42, 84, 21, 63, 21, 37, 44, 65, 30, 77, 22, 74, 35, 16, 16, 79, 95, 96, 90, 11, 51, 86, 85, 96, 67, 64, 23,
     60, 54, 81, 80, 52, 25, 24, 95, 33, 20, 6, 74, 19, 85, 51, 96, 38, 54, 7, 69, 63, 63, 59, 67, 70, 37, 41, 14, 2,
     10, 33, 15, 59, 3, 22, 75, 51, 47, 8, 85, 79, 34, 30, 39, 57, 66, 28, 11, 51, 89, 61, 64, 86, 56, 59, 7, 91, 72,
     14, 45, 29, 49, 76, 48, 65, 86, 67, 44, 80, 25, 29, 93, 63, 19, 81, 34, 82, 83, 16, 25, 80, 72, 81, 91, 96, 57, 51,
     71, 26, 18, 18, 22],
    [33, 92, 81, 96, 65, 57, 74, 2, 14, 94, 55, 85, 8, 10, 10, 1, 82, 24, 65, 16, 14, 94, 30, 44, 21, 14, 50, 72, 52,
     16, 93, 5, 33, 19, 14, 98, 26, 61, 98, 97, 12, 57, 48, 47, 56, 98, 59, 33, 99, 32, 44, 13, 91, 56, 32, 69, 91, 86,
     98, 31, 97, 34, 77, 82, 20, 27, 33, 19, 74, 60, 38, 78, 89, 45, 23, 62, 7, 44, 51, 86, 69, 59, 15, 32, 93, 26, 10,
     11, 89, 4, 34, 32, 89, 66, 95, 49, 85, 85, 5, 29, 80, 45, 42, 74, 20, 1, 38, 0, 28, 96, 55, 46, 55, 64, 64, 49, 20,
     1, 88, 91, 86, 24, 15, 28, 18, 97, 83, 62, 41, 91, 44, 68, 21, 72, 42, 71, 95, 44, 30, 47, 58, 56, 55, 71, 87, 48,
     42, 89, 25, 72],
    [17, 31, 8, 55, 54, 99, 63, 26, 10, 34, 98, 64, 78, 92, 90, 39, 2, 79, 25, 32, 58, 39, 56, 63, 92, 41, 55, 16, 93,
     14, 89, 59, 91, 76, 51, 71, 37, 97, 13, 43, 20, 64, 5, 15, 20, 25, 38, 49, 19, 54, 33, 84, 2, 70, 44, 19, 25, 85,
     36, 72, 20, 73, 4, 80, 67, 25, 31, 36, 40, 46, 18, 46, 84, 23, 50, 56, 34, 80, 44, 5, 4, 61, 80, 15, 32, 51, 73,
     22, 91, 20, 84, 95, 24, 75, 76, 9, 92, 17, 54, 31, 55, 86, 27, 46, 15, 54, 42, 15, 16, 60, 66, 41, 3, 53, 31, 10,
     85, 4, 12, 46, 88, 41, 38, 31, 46, 42, 37, 21, 70, 59, 75, 79, 84, 17, 92, 38, 15, 45, 4, 76, 54, 24, 60, 22, 23,
     36, 56, 94, 7, 31],
    [33, 5, 35, 73, 66, 80, 34, 94, 97, 69, 85, 34, 48, 36, 27, 57, 95, 88, 55, 55, 54, 11, 27, 61, 25, 25, 72, 48, 42,
     71, 17, 17, 51, 5, 96, 41, 80, 27, 26, 75, 48, 77, 56, 43, 40, 94, 23, 94, 38, 86, 4, 89, 23, 78, 28, 26, 25, 53,
     65, 49, 2, 70, 24, 54, 22, 73, 71, 98, 98, 7, 28, 77, 83, 3, 40, 83, 70, 90, 45, 49, 47, 23, 73, 32, 65, 85, 82,
     49, 7, 75, 59, 45, 25, 77, 5, 82, 96, 69, 43, 62, 13, 58, 15, 91, 16, 55, 2, 77, 36, 7, 3, 76, 67, 0, 9, 93, 73,
     64, 87, 61, 86, 43, 57, 32, 29, 65, 54, 67, 28, 47, 41, 36, 79, 44, 95, 8, 65, 50, 88, 32, 48, 9, 18, 8, 99, 95,
     39, 8, 37, 23],
    [15, 67, 99, 14, 47, 99, 49, 4, 2, 98, 54, 69, 31, 36, 99, 17, 39, 3, 72, 72, 69, 84, 25, 51, 17, 36, 12, 16, 27,
     19, 31, 51, 71, 85, 17, 46, 45, 15, 19, 45, 50, 22, 39, 90, 74, 89, 74, 74, 7, 30, 89, 97, 14, 69, 81, 87, 24, 87,
     92, 37, 14, 46, 89, 29, 40, 8, 92, 14, 30, 70, 48, 70, 28, 6, 53, 82, 81, 95, 43, 12, 69, 34, 31, 63, 67, 37, 87,
     5, 63, 93, 72, 7, 12, 14, 14, 47, 28, 27, 64, 29, 93, 74, 6, 56, 55, 25, 59, 81, 80, 21, 51, 91, 40, 58, 88, 27,
     78, 35, 38, 13, 73, 56, 0, 57, 28, 44, 35, 52, 19, 63, 65, 34, 61, 65, 96, 36, 53, 54, 40, 55, 55, 71, 44, 89, 62,
     55, 34, 76, 25, 27],
    [85, 15, 11, 53, 91, 17, 10, 46, 41, 25, 91, 1, 15, 18, 82, 17, 42, 53, 21, 64, 0, 28, 76, 79, 31, 36, 2, 77, 93,
     54, 3, 67, 47, 94, 40, 96, 2, 49, 55, 61, 25, 74, 18, 79, 42, 79, 4, 74, 20, 82, 33, 22, 18, 21, 51, 33, 0, 3, 62,
     60, 59, 10, 60, 58, 43, 86, 99, 0, 76, 6, 20, 42, 74, 12, 27, 90, 46, 62, 72, 31, 93, 4, 11, 99, 29, 27, 78, 41,
     29, 87, 59, 0, 97, 34, 79, 97, 74, 33, 24, 77, 26, 45, 59, 40, 70, 33, 7, 7, 79, 96, 0, 13, 7, 75, 51, 11, 7, 6,
     96, 93, 30, 6, 20, 14, 30, 63, 7, 75, 52, 79, 33, 49, 24, 33, 52, 19, 18, 50, 30, 67, 14, 79, 9, 79, 85, 93, 15,
     28, 32, 76],
    [26, 84, 59, 64, 96, 12, 66, 77, 86, 50, 24, 60, 17, 28, 9, 29, 23, 92, 6, 42, 54, 18, 35, 66, 6, 6, 3, 38, 6, 53,
     32, 4, 87, 97, 18, 40, 39, 13, 4, 54, 4, 44, 47, 16, 95, 59, 83, 32, 58, 22, 52, 60, 79, 56, 1, 1, 69, 48, 59, 70,
     85, 47, 71, 65, 68, 34, 6, 68, 76, 89, 94, 22, 61, 95, 32, 38, 19, 26, 59, 40, 64, 95, 90, 74, 76, 49, 80, 94, 17,
     52, 7, 28, 68, 1, 46, 12, 67, 26, 8, 1, 90, 69, 98, 87, 99, 16, 25, 54, 79, 21, 39, 27, 38, 99, 58, 44, 11, 20, 58,
     7, 94, 45, 68, 87, 46, 35, 46, 60, 86, 22, 83, 43, 15, 25, 50, 87, 51, 52, 67, 79, 54, 16, 9, 77, 27, 38, 36, 19,
     28, 37],
    [78, 89, 1, 62, 78, 54, 69, 49, 97, 28, 77, 90, 63, 96, 69, 93, 17, 70, 13, 89, 82, 12, 80, 18, 53, 97, 75, 41, 14,
     35, 32, 3, 62, 1, 61, 13, 29, 42, 75, 99, 47, 16, 45, 77, 33, 48, 28, 29, 12, 5, 65, 55, 67, 93, 30, 29, 9, 28, 28,
     25, 19, 27, 65, 24, 7, 50, 23, 3, 99, 19, 19, 99, 86, 3, 38, 49, 43, 87, 29, 15, 56, 58, 86, 59, 17, 12, 32, 75,
     79, 61, 73, 18, 10, 38, 83, 66, 16, 41, 86, 84, 0, 13, 67, 87, 58, 34, 48, 18, 33, 46, 93, 62, 90, 80, 23, 87, 53,
     82, 66, 42, 32, 55, 72, 67, 12, 38, 62, 88, 49, 24, 26, 85, 68, 10, 20, 32, 92, 57, 12, 10, 73, 43, 39, 48, 47, 41,
     41, 88, 66, 24],
    [64, 12, 3, 38, 20, 42, 59, 7, 61, 88, 76, 82, 84, 47, 91, 14, 12, 27, 95, 21, 99, 69, 58, 8, 39, 12, 11, 72, 30,
     18, 80, 30, 12, 30, 13, 65, 4, 51, 64, 99, 47, 16, 66, 7, 16, 73, 86, 76, 76, 84, 90, 58, 77, 5, 13, 37, 96, 7, 64,
     21, 43, 40, 96, 68, 45, 86, 12, 7, 36, 43, 45, 68, 11, 98, 21, 0, 35, 20, 38, 16, 90, 0, 54, 71, 99, 83, 14, 40,
     59, 32, 77, 15, 90, 77, 25, 45, 51, 21, 6, 43, 0, 88, 7, 76, 52, 21, 34, 94, 52, 55, 7, 77, 22, 28, 10, 71, 48, 86,
     61, 74, 67, 63, 29, 99, 59, 25, 90, 89, 6, 63, 38, 95, 35, 75, 15, 30, 71, 14, 84, 64, 21, 7, 87, 20, 72, 84, 63,
     61, 23, 86],
    [3, 75, 67, 69, 20, 58, 20, 64, 79, 79, 4, 6, 68, 79, 62, 38, 51, 92, 83, 85, 25, 59, 7, 40, 98, 28, 12, 56, 60, 26,
     37, 3, 85, 16, 51, 49, 87, 27, 26, 18, 78, 16, 86, 54, 14, 22, 11, 91, 28, 42, 12, 33, 40, 73, 34, 96, 11, 13, 92,
     63, 46, 47, 0, 53, 52, 17, 69, 52, 67, 25, 56, 11, 98, 97, 81, 8, 51, 88, 0, 65, 50, 87, 32, 31, 69, 29, 23, 18,
     45, 13, 22, 79, 29, 76, 53, 59, 83, 63, 75, 40, 9, 64, 76, 76, 7, 72, 52, 17, 42, 53, 75, 82, 50, 58, 5, 99, 39, 5,
     56, 68, 58, 92, 69, 97, 42, 54, 14, 10, 19, 84, 65, 78, 45, 83, 94, 65, 7, 44, 44, 95, 28, 7, 92, 37, 99, 83, 92,
     22, 16, 85],
    [18, 94, 28, 43, 49, 73, 82, 67, 70, 48, 13, 12, 70, 32, 59, 33, 31, 39, 29, 77, 68, 57, 99, 4, 87, 48, 2, 12, 17,
     55, 15, 16, 68, 41, 45, 33, 90, 24, 78, 17, 52, 65, 98, 60, 18, 10, 2, 29, 49, 84, 53, 77, 2, 52, 58, 37, 71, 10,
     31, 63, 27, 59, 71, 75, 59, 18, 79, 36, 61, 43, 41, 70, 61, 88, 89, 6, 54, 32, 38, 71, 62, 47, 17, 42, 36, 31, 68,
     12, 4, 97, 51, 58, 47, 2, 34, 22, 13, 34, 23, 95, 31, 4, 1, 10, 92, 62, 87, 82, 57, 4, 54, 64, 97, 13, 55, 42, 76,
     69, 17, 88, 55, 86, 3, 1, 19, 19, 87, 88, 12, 65, 64, 44, 80, 56, 26, 68, 49, 11, 48, 13, 56, 56, 32, 14, 29, 66,
     20, 92, 30, 1],
    [39, 54, 7, 65, 45, 94, 72, 79, 24, 21, 37, 88, 50, 8, 69, 94, 13, 13, 56, 19, 71, 59, 57, 98, 30, 58, 99, 67, 18,
     25, 34, 49, 83, 13, 61, 43, 64, 26, 44, 14, 63, 57, 92, 83, 13, 16, 52, 20, 36, 94, 57, 90, 51, 98, 22, 94, 6, 27,
     38, 45, 46, 64, 24, 77, 19, 53, 78, 63, 9, 85, 69, 13, 58, 96, 40, 25, 89, 78, 12, 90, 40, 2, 12, 52, 46, 84, 98,
     51, 48, 74, 85, 11, 68, 26, 69, 15, 22, 10, 1, 21, 6, 87, 56, 82, 56, 2, 51, 39, 51, 73, 57, 30, 37, 79, 33, 23,
     26, 17, 74, 17, 29, 74, 46, 63, 63, 57, 16, 76, 68, 68, 87, 22, 37, 86, 70, 92, 99, 39, 50, 17, 87, 35, 2, 59, 13,
     89, 37, 52, 20, 19],
    [47, 23, 76, 56, 65, 90, 45, 88, 2, 35, 67, 13, 68, 73, 54, 97, 28, 62, 47, 42, 40, 98, 76, 65, 79, 49, 29, 68, 97,
     25, 94, 5, 54, 99, 15, 11, 48, 29, 89, 71, 82, 2, 4, 40, 9, 90, 67, 89, 8, 84, 85, 80, 61, 33, 22, 96, 7, 22, 52,
     73, 95, 59, 44, 26, 40, 43, 30, 33, 14, 85, 76, 47, 55, 81, 77, 14, 35, 33, 46, 16, 77, 52, 81, 33, 98, 71, 32, 84,
     16, 43, 93, 6, 87, 65, 99, 6, 29, 66, 10, 3, 0, 22, 7, 70, 87, 31, 92, 36, 39, 52, 83, 56, 3, 62, 2, 4, 94, 21, 59,
     71, 29, 26, 64, 17, 59, 86, 71, 79, 58, 6, 26, 7, 3, 27, 82, 64, 45, 88, 1, 40, 50, 7, 24, 43, 67, 85, 8, 21, 62,
     61],
    [33, 95, 54, 20, 60, 84, 53, 53, 45, 76, 65, 56, 75, 59, 24, 96, 13, 1, 63, 29, 39, 95, 14, 46, 20, 23, 33, 79, 14,
     28, 60, 29, 94, 71, 53, 80, 78, 77, 2, 21, 83, 80, 11, 89, 19, 4, 5, 90, 73, 46, 50, 3, 69, 98, 77, 32, 36, 15, 10,
     28, 14, 60, 92, 85, 81, 72, 77, 83, 33, 49, 1, 17, 37, 1, 6, 70, 29, 19, 87, 56, 52, 51, 7, 77, 15, 90, 12, 53, 77,
     17, 87, 89, 38, 29, 45, 43, 76, 57, 13, 17, 82, 67, 97, 41, 84, 44, 79, 0, 74, 63, 69, 82, 23, 0, 31, 89, 26, 34,
     26, 26, 23, 3, 35, 81, 71, 76, 51, 82, 20, 44, 31, 65, 42, 22, 91, 4, 8, 45, 42, 7, 19, 52, 60, 68, 83, 52, 66, 10,
     21, 24],
    [48, 61, 86, 26, 80, 4, 44, 30, 90, 30, 45, 96, 47, 56, 94, 39, 67, 96, 45, 3, 38, 93, 85, 81, 77, 34, 62, 58, 45,
     79, 55, 27, 3, 94, 15, 28, 2, 91, 27, 75, 67, 29, 69, 24, 45, 19, 0, 77, 74, 60, 34, 6, 73, 64, 19, 62, 64, 31, 3,
     29, 67, 24, 73, 97, 9, 96, 46, 11, 15, 13, 46, 69, 9, 43, 44, 58, 59, 64, 2, 59, 4, 22, 23, 10, 53, 93, 19, 57, 13,
     39, 17, 95, 11, 46, 28, 8, 29, 43, 81, 53, 11, 87, 13, 2, 75, 84, 27, 18, 80, 78, 28, 23, 76, 82, 69, 71, 82, 97,
     41, 27, 57, 31, 16, 52, 82, 3, 57, 32, 76, 51, 14, 21, 15, 97, 95, 6, 77, 44, 50, 92, 6, 84, 85, 16, 39, 59, 81,
     63, 59, 70],
    [89, 71, 18, 81, 33, 76, 4, 77, 26, 31, 30, 28, 44, 35, 1, 37, 34, 75, 53, 15, 43, 17, 81, 47, 75, 11, 77, 65, 1,
     96, 19, 51, 50, 53, 57, 23, 67, 92, 53, 92, 4, 2, 13, 56, 27, 47, 25, 92, 89, 80, 65, 57, 6, 79, 83, 54, 29, 1, 67,
     6, 86, 63, 96, 60, 37, 68, 49, 7, 12, 23, 56, 74, 41, 99, 18, 55, 70, 81, 84, 81, 64, 2, 32, 83, 75, 81, 94, 47,
     44, 13, 75, 27, 59, 36, 48, 86, 38, 5, 1, 22, 76, 84, 9, 93, 93, 4, 13, 6, 35, 76, 48, 72, 30, 10, 43, 22, 88, 97,
     87, 44, 96, 94, 2, 3, 85, 12, 19, 38, 3, 64, 76, 57, 65, 41, 31, 13, 85, 97, 55, 26, 2, 98, 23, 43, 73, 50, 0, 62,
     10, 78],
    [42, 35, 40, 18, 47, 57, 66, 40, 85, 69, 52, 84, 68, 11, 1, 94, 4, 5, 65, 92, 79, 76, 47, 90, 16, 38, 43, 63, 29,
     13, 5, 99, 65, 48, 1, 70, 60, 49, 73, 72, 64, 20, 70, 79, 36, 48, 4, 51, 68, 52, 2, 47, 59, 66, 76, 74, 12, 26, 42,
     54, 17, 67, 70, 88, 70, 54, 88, 58, 62, 92, 92, 87, 84, 92, 78, 52, 92, 27, 74, 23, 66, 11, 57, 96, 89, 86, 19, 27,
     87, 91, 33, 73, 93, 57, 87, 29, 81, 34, 22, 21, 90, 12, 78, 94, 4, 65, 9, 21, 5, 66, 19, 15, 67, 34, 63, 91, 36,
     58, 99, 86, 64, 55, 53, 0, 56, 49, 22, 5, 14, 12, 18, 37, 35, 62, 69, 13, 10, 72, 18, 5, 81, 37, 96, 77, 70, 45,
     66, 17, 91, 5],
]  # 11360

start = t.time_ns()
print(minimum_transportation_price(suppliers_b, consumers_b, costs_b))  #
finish = t.time_ns()
print(f'total time: {(finish - start) // 10 ** 6} milliseconds')

c = colour_('===', RED)
print(f"{c}")
print(f'length: {len(c)}')
