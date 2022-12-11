# accepted on codewars.com
def doubles(maxk, maxn):
    vals = []

    for n in range(1, maxn + 1):
        vals.append(1 / (n + 1) ** 2)

    general_sum = 0
    for k in range(1, maxk + 1):
        general_sum += (1 / k) * sum(val ** k for val in vals)

    return general_sum


print(doubles(1, 10))
print(doubles(10, 1000))




