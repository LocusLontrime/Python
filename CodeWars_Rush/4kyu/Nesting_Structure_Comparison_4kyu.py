# accepted on codewars.com
types = [None, int, str]


def same_structure_as(original, other):

    if type(original) in types and type(other) in types:
        return True
    elif type(original) != type(other):
        return False

    if len(original) != len(other):
        return False

    flag = True
    for i in range(0, len(original)):
        flag = flag and same_structure_as(original[i], other[i])

    return flag


print(same_structure_as([1, [1, 1]], [2, [2, 2]]))
print(same_structure_as([1, [1, 1]], [[2, 2], 2]))







