# accepted on codewars.com
buttons_dict = {(0, 0): 'A', (0, 1): 'B', (0, 2): 'C', (1, 0): 'D', (1, 1): 'E', (1, 2): 'F', (2, 0): 'G', (2, 1): 'H', (2, 2): 'I'}
coordinates_dict = {'A': (0, 0), 'B': (0, 1), 'C': (0, 2), 'D': (1, 0), 'E': (1, 1), 'F': (1, 2), 'G': (2, 0), 'H': (2, 1), 'I': (2, 2)}

initial_buttons = {'A', 'C', 'I', 'G', 'B', 'F', 'H', 'D', 'E'}

directions = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
aux_directions = [[-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1]]

chains_counter = 0
results: list[list[str]]


def count_patterns_from(first_letter: str, length: int) -> int:
    global chains_counter, results

    if length >= 10:
        return 0

    chains_counter = 0
    results = []

    def is_coords_valid(j: int, i: int) -> bool:
        return 0 <= j < 3 and 0 <= i < 3

    def find_neighs(letter: str, buts_rem: set[str]) -> list:
        neighs = []
        letter_coordinates = coordinates_dict[letter]

        for pair in directions:
            curr_j = letter_coordinates[0] + pair[0]
            curr_i = letter_coordinates[1] + pair[1]

            if is_coords_valid(curr_j, curr_i):
                if buttons_dict[p := (curr_j, curr_i)] in buts_rem:
                    neighs.append(p)
                else:
                    curr_j += pair[0]
                    curr_i += pair[1]

                    if is_coords_valid(curr_j, curr_i):
                        if buttons_dict[p := (curr_j, curr_i)] in buts_rem:
                            neighs.append(p)

        for pair in aux_directions:
            curr_j = letter_coordinates[0] + pair[0]
            curr_i = letter_coordinates[1] + pair[1]

            if is_coords_valid(curr_j, curr_i):
                if buttons_dict[p := (curr_j, curr_i)] in buts_rem:
                    neighs.append(p)

        return neighs

    def recursive_seeker(curr_button: str, buttons_remained: set[str], length_remained: int, sequence: list[str]) -> None:
        global chains_counter, results

        print(f'curr but: {curr_button}, buts rem: {buttons_remained}, l rem: {length_remained}')

        if length_remained == 0:
            chains_counter += 1
            results.append(sequence)
            return

        for next_button in find_neighs(curr_button, buttons_remained):
            recursive_seeker(el := buttons_dict[next_button], buttons_remained - {el}, length_remained - 1, sequence + [el])

    recursive_seeker(first_letter, initial_buttons - {first_letter}, length - 1, [first_letter])

    for res in results:
        print(f'seq: {res}')

    return chains_counter


# print([1, 2, 3, 4, 5][:4])

print(count_patterns_from('E', 4))
print(count_patterns_from('E', 5))





