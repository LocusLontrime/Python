def maximums_quantity(m: int, n: int, ops: list[list[int]]) -> int:
    min_x, min_y = m, n
    for i, op in enumerate(ops):
        if op[0] < min_x:
            min_x = op[0]
        if op[1] < min_y:
            min_y =  op[1]
    return min_x * min_y
