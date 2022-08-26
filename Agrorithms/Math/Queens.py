diag1_set: set[int]
diag2_set: set[int]
vertical_set: list[int]
results_list: list[list[tuple[int, int]]]


def find_queens_partitions(size: int):
    global diag1_set, diag2_set, vertical_set, results_list
    diag1_set = set()
    diag2_set = set()
    vertical_set = list()
    results_list = []

    def recursive_seeker(j: int):
        # border case
        if j == size:
            results_list.append([(k, vertical_set[k]) for k in range(size)])

        # body of recurs
        for i in range(size):
            if not (i in vertical_set or j + i in diag1_set or j - i in diag2_set):
                vertical_set.append(i)
                diag1_set.add(j + i)
                diag2_set.add(j - i)

                # recurrent relation
                recursive_seeker(j + 1)

                # backtracking
                vertical_set.remove(i)
                diag1_set.remove(j + i)
                diag2_set.remove(j - i)

    recursive_seeker(0)

    return results_list






ans = find_queens_partitions(9)

print(f'ans: {len(ans)}')

for an in ans:
    print(an)






