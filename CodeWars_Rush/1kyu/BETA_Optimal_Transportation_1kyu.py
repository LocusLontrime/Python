# accepted on codewars.com
import numpy as np


def minimum_transportation_price(suppliers, consumers, costs):  # 36 366 98 989
    # quantities of rows and columns:
    rows, cols = len(costs), len(costs[0])
    # table for X(j, i) --> optimal (min) total price:
    sol_table = [[None for _ in range(cols)] for _ in range(rows)]
    # building basic solution (it can be not optimal):
    rows_basis_cells, columns_basis_cells, coords = get_basic_solution_min_price_method(sol_table, suppliers, consumers,costs)
    # time section -->> needed for further testing:
    potentials_t, deltas_t, getting_cycle_t, cycle_recounting_t = 0, 0, 0, 0
    # now cycling through all the approximating iterations needed until the optimal solution found:
    while True:
        u, v = find_potentials(costs, sol_table, rows_basis_cells, columns_basis_cells, coords)
        # max delta estimation:
        # numpy optimization for deltas section, works too slow without numpy optimization:
        deltas_matrix = np.array(v) + np.array(u)[:, None] - np.array(costs)
        flat_index = np.argmax(deltas_matrix)
        max_delta = np.amax(deltas_matrix)
        # double inds from the flat one:
        j_max_d = flat_index // cols
        i_max_d = flat_index - j_max_d * cols
        # stop-condition of finding the optimal solution:
        if max_delta <= 0:
            break
        # finding the cycle:
        path = get_cycle_path(j_max_d, i_max_d, sol_table, rows_basis_cells, columns_basis_cells)
        # changing the X-elements (table) along the cycle-path:
        cycle_recounting(path, sol_table, rows_basis_cells, columns_basis_cells)
    # return the aggregated min transportation price:
    return sum([sol_table[j][i] * costs[j][i] for j in range(rows) for i in range(cols) if sol_table[j][i] is not None])


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
    if (s1 := sum([len(cells) for cells in rows_basis_cells])) < (s2 := len(costs) + len(costs[0]) - 1):
        delta_rank = s2 - s1
        # adding the missing basis cell:
        aux_queue = sorted(aux_queue, key=lambda x: costs[x[0]][x[1]])
        additional_cell_coords = aux_queue[0]
        table[j := additional_cell_coords[0]][i := additional_cell_coords[1]] = 0
        rows_basis_cells[j].append((j, i))
        columns_basis_cells[i].append((j, i))
    # returns auxiliary data:
    return rows_basis_cells, columns_basis_cells, additional_cell_coords


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
    table[j1 := cycle_path[0][0]][i1 := cycle_path[0][1]] = min_el
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


def get_cycle_path(start_j, start_i, table, row_basis_cells, columns_basis_cells):
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


