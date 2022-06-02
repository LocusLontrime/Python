def tower_builder(n_floors):  # accepted on codewars
    tower_list = []
    for i in range(1, n_floors + 1):
        if i != 1:
            for j in range(len(tower_list)):
                tower_list[j] = ' ' + tower_list[j] + ' '
        tower_list.append('*' * (2 * i - 1))
    return tower_list


print(tower_builder(5))
print(str(['*'] * 10))
