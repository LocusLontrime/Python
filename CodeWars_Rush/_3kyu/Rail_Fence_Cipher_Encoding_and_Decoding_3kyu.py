# accepted on codewars.com
from functools import reduce


def encode_rail_fence_cipher(string, n):
    strings = []

    for i in range(0, n):
        strings.append("")

    j_coord = -1
    flag = True
    for i in range(len(string)):
        j_coord += 1 if flag else -1
        strings[j_coord] += string[i]

        if i != 0 and (j_coord == n - 1 or j_coord == 0):
            flag = not flag

    return reduce(lambda x, y: x + y, strings)


def decode_rail_fence_cipher(string, n):

    dictionary = dict()

    j_coord = -1
    i_coord = -1
    flag = True
    for i in range(len(string)):
        j_coord += 1 if flag else -1
        i_coord += 1
        dictionary[i] = (j_coord, i_coord)

        if i != 0 and (j_coord == n - 1 or j_coord == 0):
            flag = not flag

    sorted_ones = sorted(dictionary.items(), key=lambda x: x[1][0])
    new_dict = dict(sorted_ones)

    result = [" "] * len(string)

    i = 0
    for key in new_dict:
        result[key] = string[i]
        i += 1

    return "" if len(result) == 0 else reduce(lambda x, y: x + y, result)


print(encode_rail_fence_cipher("WEAREDISCOVEREDFLEEATONCE", 3))
print(encode_rail_fence_cipher("Hello, World!", 3))
print(encode_rail_fence_cipher("Hello, World!", 4))

print(decode_rail_fence_cipher("WECRLTEERDSOEEFEAOCAIVDEN", 3))

print(decode_rail_fence_cipher(encode_rail_fence_cipher("WEAREDISCOVEREDFLEEATONCE", 3), 3))
print(decode_rail_fence_cipher(encode_rail_fence_cipher("Hello, World!", 3), 3))
print(decode_rail_fence_cipher(encode_rail_fence_cipher("Hello, World!", 4), 4))
