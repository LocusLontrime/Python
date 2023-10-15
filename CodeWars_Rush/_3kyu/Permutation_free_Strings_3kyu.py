# accepted on codewars.com

memo_table = []

for i in range(0, 3):
    memo_table.append({})


# should be calculated mathematically 36 366 98 989
# memo_table[0][0] = 21
# memo_table[0][1] = 51
#
# memo_table[1][0] = 232
# memo_table[1][1] = 856
# memo_table[1][2] = 3160
#
# memo_table[2][0] = 3005
# memo_table[2][1] = 14545
# memo_table[2][2] = 70445
# memo_table[2][3] = 341185

# initial values
for i in range(3, 6):
    for j in range(1, i):
        memo_table[i - 3][j] = i ** j


def fact(n: int) -> int:
    return n * fact(n - 1) if n != 0 else 1


# recursive relations for permutation free strings
def recursive_seeker_3(length: int) -> int:

    if length not in memo_table[0].keys():
        memo_table[0][length] = 2 * recursive_seeker_3(length - 1) + recursive_seeker_3(length - 2)

    return memo_table[0][length]


def recursive_seeker_4(length: int) -> int:

    if length not in memo_table[1].keys():
        memo_table[1][length] = 3 * recursive_seeker_4(length - 1) + 2 * recursive_seeker_4(length - 2) + 2 * recursive_seeker_4(length - 3)

    return memo_table[1][length]


def recursive_seeker_5(length: int) -> int:

    if length not in memo_table[2].keys():
        memo_table[2][length] = 4 * recursive_seeker_5(length - 1) + 3 * recursive_seeker_5(length - 2) + 4 * recursive_seeker_5(length - 3) + 6 * recursive_seeker_5(length - 4)

    return memo_table[2][length]


# the main method
def permutation_free(n, l):

    if n == 3:
        result = recursive_seeker_3(l)
    elif n == 4:
        result = recursive_seeker_4(l)
    elif n == 5:
        result = recursive_seeker_5(l)
    else:
        print('Error')
        return -1

    return result % 12345787


# tests
print(permutation_free(3, 5))
# print(permutation_free(3, 100))
# print(permutation_free(5, 100))
# print(permutation_free(4, 99))
print(permutation_free(3, 11))
print(permutation_free(5, 8))
print(permutation_free(5, 10))
print(permutation_free(4, 6))
print(permutation_free(4, 9))

# print(recursive_seeker(2, 3))

# print(fact(10))
