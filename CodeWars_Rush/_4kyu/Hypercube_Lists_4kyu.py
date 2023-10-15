# accepted on codewars.com
import copy
from typing import List

cube_size = 0
depth = 0


def normalize(nested_list: List, growing_value: int = 0) -> List:
    global cube_size, depth
    copied_list = copy.deepcopy(nested_list)
    """Converts the given nested list to hypercube format with the given <growing_value> and return it.
    """
    # TODO: implement
    cube_size = 0
    depth = 0

    recursive_seeker_cube_size(copied_list)
    recursive_filler(copied_list, growing_value)

    return copied_list


def recursive_seeker_cube_size(upper_list: List, current_depth=1):
    global cube_size, depth

    if type(upper_list) is int:
        return

    if len(upper_list) > cube_size:
        cube_size = len(upper_list)

    if current_depth > depth:
        depth = current_depth

    for lower_list in upper_list:
        recursive_seeker_cube_size(lower_list, current_depth + 1)


def recursive_filler(upper_list: List, growing_value, current_depth=1):
    global cube_size, depth

    if current_depth < depth:
        for i in range(cube_size - len(upper_list)):
            upper_list.append([])
    else:
        for i in range(cube_size - len(upper_list)):
            upper_list.append(growing_value)
        return

    for lower_list in upper_list:
        if type(lower_list) is not int:
            recursive_filler(lower_list, growing_value, current_depth + 1)
        else:
            num = lower_list
            upper_list[i := upper_list.index(num)] = []
            recursive_filler(upper_list[i], num, current_depth + 1)


sample = [[[2, 3, 4], [1, 2], 2, [1]], [2, [2, 3], 1, 4, [2, 2, 6, 7]], 5]

sampleX = [1, 2, 3, 4, []]

print(normalize(sample))

# print(normalize(sampleX))

# print(normalize(sampleX, 3))

list_for_Levi_Gin = [_ for _ in range(98)]
list_X = [_ for _ in (1, 2, 3)]
print(*list_for_Levi_Gin)
print(*list_X)
