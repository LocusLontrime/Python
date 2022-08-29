# accepted on codewars.com
def combos(n):

    result = []

    def recursive_seeker(remained_part_of_n, previous_number, curr_numbers):

        if remained_part_of_n == 0:
            result.append(curr_numbers)

        for i in range(previous_number, remained_part_of_n + 1):
            recursive_seeker(remained_part_of_n - i, i, curr_numbers + [i])

    recursive_seeker(n, 1, [])

    return result


def show(list_of_lists: list) -> None:
    for item in list_of_lists:
        print(item)


show(combos(30))
