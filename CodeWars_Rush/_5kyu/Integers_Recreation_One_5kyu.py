# accepted on codewars.com
results = [[1, 1], [42, 2500], [246, 84100], [287, 84100], [728, 722500], [1434, 2856100], [1673, 2856100], [1880, 4884100], [4264, 24304900], [6237, 45024100], [9799, 96079204], [9855, 113635600]]


def list_squared(m, n):
    list_res = []
    for pair in results:
        if m <= pair[0] <= n:
            list_res.append(pair)
    return list_res


print(list_squared(5000, 10000))
