# accepted on codewars.com
groups: list


def pair_em_up(n: int):
    global groups
    # solution to n = 3 is given
    groups = []
    rec_seeker(-1, n, [])
    return groups  # [[0, 1], [0, 2], [1, 2]]


def rec_seeker(prev: int, n: int, group_: list[int]) -> None:
    # body of rec:
    for i in range(prev + 1, n):
        # recurrent relation (just a rec call):
        rec_seeker(i, n, group_ + [i])
    # border case:
    if group_ and not len(group_) % 2:
        groups.append(group_)


print(f'res: {(groups_ := pair_em_up(20))}')
print(f'size: {len(groups_)}')


