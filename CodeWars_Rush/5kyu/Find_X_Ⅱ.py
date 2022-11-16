# accepted on codewars.com

saved_values_dict = dict()


def find_x(n):
    if n == 0:
        return 0
    x = 0
    for i in range(1, n+1):
        x += find_x(i-1) + 3*i
    return x


def find_x_optimized(n):
    return (3 * (pow(2, n + 1, 10 ** 9 + 7) - n - 2)) % (10 ** 9 + 7)


print(find_x_optimized(500000))
