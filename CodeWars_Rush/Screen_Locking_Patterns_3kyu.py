def count_patterns_from(first_point, length):

    buttons_dict = {'A': (0, 0), 'B': (0, 1), 'C': (0, 2), 'D': (1, 0), 'E': (1, 1), 'F': (1, 2), 'G': (2, 0), 'H': (2, 1), 'I': (2, 2)}

    initial_buttons = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    chains_counter = 0

    def recursive_seeker(curr_button, buttons_remained, length_remained):

        if length_remained == 0:
            pass

        if curr_button in ['B', 'D', 'F', 'H']:
            pass
        elif curr_button in ['A', 'C', 'G', 'I']:
            pass
        else:
            pass

        pass

    recursive_seeker(first_point, initial_buttons, length)

    return chains_counter







