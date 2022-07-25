# accepted on codewars.com
def levenshtein(a: str, b: str):

    def recursive_seeker(curr_a, curr_b):

        # base cases:
        if len(curr_a) == 0:
            return len(curr_b)

        if len(curr_b) == 0:
            return len(curr_a)

        if curr_a[0] == curr_b[0]:
            return recursive_seeker(curr_a[1:], curr_b[1:])

        return 1 + min(recursive_seeker(curr_a[1:], curr_b), recursive_seeker(curr_a, curr_b[1:]), recursive_seeker(curr_a[1:], curr_b[1:]))

    return recursive_seeker(a, b)


# fast and optimized
def memoi_levenshtein(a: str, b: str):

    memo_table = {}

    def recursive_seeker(curr_a_index: int, curr_b_index: int):

        # base cases:
        if curr_a_index == len(a):
            return len(b) - curr_b_index

        if curr_b_index == len(b):
            return len(a) - curr_a_index

        if (curr_a_index, curr_b_index) not in memo_table.keys():

            result = 0

            if a[curr_a_index] == b[curr_b_index]:
                result = recursive_seeker(curr_a_index + 1, curr_b_index + 1)
            else:
                result = 1 + min(recursive_seeker(curr_a_index + 1, curr_b_index), recursive_seeker(curr_a_index, curr_b_index + 1), recursive_seeker(curr_a_index + 1, curr_b_index + 1))

            memo_table[(curr_a_index, curr_b_index)] = result

        return memo_table[(curr_a_index, curr_b_index)]

    return recursive_seeker(0, 0)






print([1, 2, 3, 4, 5, 6][1:])

print(levenshtein('kitten', 'sitting'))
print(memoi_levenshtein('kitten', 'sitting'))

