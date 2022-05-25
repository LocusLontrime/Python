def parts_sums(ls):
    # your code
    result = [0]
    part_sum = 0
    for i in range(len(ls) - 1, -1, -1):
        part_sum += ls[i]
        result.append(part_sum)
    return list(reversed(result))


print(parts_sums([0, 1, 3, 6, 10]))
print(parts_sums([744125, 935, 407, 454, 430, 90, 144, 6710213, 889, 810, 2579358]))

