# calculate a mathematical expression without neg and parentheses
def calculate(simplified_expressions: list) -> float:

    def recursive_seeker(curr_index: int, curr_mult_div: float, result: float, last_operation_is_mult_div: bool) -> float or None:
        print(f'curr_index: {curr_index}, curr_mult_div: {curr_mult_div}, result: {result}')

        # base case
        if len(simplified_expressions) == 0:
            return None

        # border case:
        if curr_index >= len(simplified_expressions):
            return result + curr_mult_div

        if simplified_expressions[curr_index] == '+':
            return recursive_seeker(curr_index + 1, 1.0, result + curr_mult_div, False)

        elif simplified_expressions[curr_index] == '-':
            return recursive_seeker(curr_index + 1, -1.0, result + curr_mult_div, False)

        if last_operation_is_mult_div:

            if simplified_expressions[curr_index] == '*':
                curr_mult_div *= simplified_expressions[curr_index + 1]
            elif simplified_expressions[curr_index] == '/':
                curr_mult_div /= simplified_expressions[curr_index + 1]
            return recursive_seeker(curr_index + 2, curr_mult_div, result, True)

        else:
            curr_mult_div *= simplified_expressions[curr_index]
            return recursive_seeker(curr_index + 1, curr_mult_div, result, True)

    return recursive_seeker(0, 1.0, 0.0, False)


print(calculate([36.0, '*', 6.0, '/', 6.6, '-', 77.7, '/', 7.0]))
print(calculate([2, '+', 2, '*', 2]))


