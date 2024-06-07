# accepted on codewars.com


def crazy_rabbit(field: list[int], cr: int):
    ri, rp = cr, 0  # <- rabbit position index and rabbit power
    r_dir = 1  # rabbit jump direction (1 means to the right and 1 -> left respectively)
    counter = sum(1 for bean in field if bean)  # beans quantity
    visited = set()  # visited 'nodes' (ri, r_dir)
    while (ri, r_dir) not in visited:                                                                       # 36 366 98 989 98989 LL
        # delta power (increase):
        rp += (dp := field[ri])
        # consuming the bean:
        if dp:
            field[ri] = 0
            counter -= 1
            visited = set()
        else:
            visited |= {(ri, r_dir)}
        # True answer condition:
        if counter == 0:
            return True
        # jump logic:
        ri += r_dir * rp
        while ri < 0 or ri >= len(field):
            # bouncing back from boundaries:
            ri = -(ri + 1) if ri < 0 else (2 * len(field) - (ri + 1))
            # dir changes:
            r_dir *= -1
    return False


arr_, cr_ = [2, 2, 4, 1, 5, 2, 7], 0
arr_x, cr_x = [2, 0, 3, 0, 0, 1, 0], 0
arr_z, cr_z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 7, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 14], 10

print(f'res: {crazy_rabbit(arr_x, cr_x)}')



