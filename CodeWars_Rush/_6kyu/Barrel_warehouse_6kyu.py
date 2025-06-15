# accepted on codewars.com

def insert_barrels(warehouse: list[str], barrels: list[str]) -> list[str]:
    min_space_possible: int = len(warehouse) + 1
    min_ind: int = -1
    ind: int = 0
    barrels_length: int = len(barrels)

    while ind < len(warehouse):
        temp_ind: int = ind
        current_space: int = 0
        while ind < len(warehouse) and warehouse[ind] == '':
            ind += 1
            current_space += 1
        if current_space >= barrels_length:
            if current_space < min_space_possible:
                min_space_possible = current_space
                min_ind = temp_ind
        ind += 1

    return warehouse if min_ind < 0 else warehouse[:min_ind] + barrels + warehouse[min_ind + barrels_length:]


# print(f'res: {insert_barrels(['0','','','0','','','','0'], ['0','0'])}')  # ['0','0','0','0','','','','0']
# print(f'res: {insert_barrels(['','','0','0','','','','','0'], ['0','0','0'])}')  # ['','','0','0','0','0','0','','0']
# print(f'res: {insert_barrels(['', ''], ['0'])}')  # ['0', '']
print(
    f"res: {insert_barrels(['0', '0', '', '0', '0', '0', '', '', '0'], ['0', '0', '0'])}")  # ['0','0','','0','0','0','','','0']
