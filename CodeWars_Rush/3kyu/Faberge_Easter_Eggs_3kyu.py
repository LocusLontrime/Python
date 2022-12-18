# accepted on codewars.com
def height(n, m):
    print(f'n, m: {n, m}')
    if n >= m:
        # power of two case:
        return base_summand(m)
    elif n * 2 <= m:
        delta = combs_sum(n, m)
        return delta - 1
    else:
        delta = combs_sum(m - n - 1, m)
        return base_summand(m) - delta


def combs_sum(count, m):
    delta = 1
    summa = 1
    for i in range(1, count + 1):
        delta *= m - (i - 1)
        delta //= i
        summa += delta
    return summa


def base_summand(m):
    return 2 ** m - 1


print(height(9477, 10000))
# print(height(0, 2))
print(height(2, 0))
# print(height(10000, 20000))


