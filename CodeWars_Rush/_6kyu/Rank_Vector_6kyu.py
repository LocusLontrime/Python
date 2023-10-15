# accepted on codewars.com
def ranks(a):
    b = a.copy()
    b.sort(reverse=True)

    pairs = dict()

    counter = 1
    for i in range(len(b)):
        if b[i] not in pairs:
            pairs[b[i]] = counter
        counter += 1

    result = []

    for i in range(len(a)):
        result.append(pairs[a[i]])

    return result


print(ranks([3, 3, 3, 3, 3, 5, 1]))
print(ranks([9, 3, 6, 10]))

