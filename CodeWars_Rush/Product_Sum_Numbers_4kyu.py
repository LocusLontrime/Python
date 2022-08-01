# accepted on codewars -> need to be understood a bit better
max_k = 12000
n = [2 * max_k for i in range(max_k)]


def getpsn(num_in, sump, product, start):
    # print(num,' ',sump,' ',product)
    k = num_in - sump + product
    if k < max_k:
        if num_in < n[k]:
            n[k] = num_in
        for i in range(start, max_k // num_in * 2):  # Control num <= 2 * maxk
            getpsn(num_in * i, sump + i, product + 1, i)


getpsn(1, 1, 1, 2)


def productsum(num):
    return sum(set(n[2: num + 1]))


print(productsum(3))
print(productsum(6))
print(productsum(12))
print(productsum(2))
print(productsum(1115))
