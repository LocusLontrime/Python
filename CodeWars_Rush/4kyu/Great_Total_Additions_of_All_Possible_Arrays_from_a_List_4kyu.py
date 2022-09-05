# accepted on codewars.com 36 366 98 989 98989
import math


def gta(limit, *args):  # find the base_list first
    #your code here    # I can't get out of my mind these words "Round Robin"
    nums = list(str(s) for s in args)
    res = []
    i = 0
    while len(nums) > 0 and i < limit:  # 12348, 47, 3639
        el = nums.pop(0)
        if (d := int(el[0])) not in res:
            res.append(d)
            i += 1
        if new_el := el[1:]:
            nums.append(new_el)

    print(f'digits: {res}')
    general_sum = sum(res)
    print(f'general_sum: {general_sum}')

    GTA, curr_prod = 0, 1
    for x in range(limit, 0, -1):
        curr_prod *= x
        print(f'curr_prod: {curr_prod}')
        GTA += curr_prod * (limit - x + 1)

    return general_sum * GTA // limit


# print(gta(8, 16789, 112, 573, 66669))
print(gta(5, 1267, 3234, 5368))  # 1 3 5 2 6
# print(gta(8, 12348, 47, 3639))
# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12][1:])



