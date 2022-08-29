# accepted on codewars.com
def n_linear(m, n):
    u_m = [1]

    # n pointer
    pointers = [0] * len(m)

    for i in range(1, n + 1):

        # for convenience, bigger then all values in tests
        min_current_one = 10000000001

        # searching for the min element
        for j in range(len(m)):
            min_current_one = min(min_current_one, u_m[pointers[j]] * m[j] + 1)

        # increments the pointers needed
        for j in range(len(m)):
            if min_current_one == u_m[pointers[j]] * m[j] + 1:
                pointers[j] += 1

        # print(f'i: {i}, min: {min_current_one}, u m: {u_m}')

        # appending the new element to the seq u(m)
        if min_current_one != 1:
            u_m.append(min_current_one)

    return u_m[n]


print(n_linear([5, 7, 8], 10))
print(n_linear([5, 7, 8], 11))
print(n_linear([2, 3, 5, 10000000], 200000))
print(n_linear([2, 98, 100, 72, 44, 46, 79, 82, 19, 20, 53, 86, 23, 18, 62, 25, 27, 94], 45762))

