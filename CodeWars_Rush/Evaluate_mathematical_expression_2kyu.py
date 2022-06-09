from collections import deque


def evaluate_math_expr(math_expression: str) -> float:  # accepted on codewars, powers calculations been added
    m_smbls, op_prs, cl_pars = get_symbols(math_expression)

    return evaluate_parentheses_in_depth(0, len(m_smbls) - 1, m_smbls, op_prs, cl_pars)


def get_symbols(math_expression: str):  # 3.6 3,6 36 366 98 989
    math_symbols = []
    opening_pars = dict()
    closing_pars = dict()

    deq = deque()

    index = 0
    while index < len(math_expression):
        if math_expression[index] == ' ':
            index += 1
            continue

        if math_expression[index].isdigit():
            saved_index = index
            while math_expression[index].isdigit() or math_expression[index] == '.':
                index += 1
                if index >= len(math_expression):
                    break
            number_found = float(math_expression[saved_index: index])
            math_symbols.append(number_found)
        else:
            if math_expression[index] == '(':
                deq.append(len(math_symbols))
            elif math_expression[index] == ')':
                closing_index = len(math_symbols)
                opening_pars[closing_index] = deq.pop()
                closing_pars[opening_pars[closing_index]] = closing_index

            math_symbols.append(math_expression[index])
            index += 1

    print(math_symbols)
    print(opening_pars)
    print(closing_pars)

    return math_symbols, opening_pars, closing_pars


def evaluate_parentheses_in_depth(l_pointer, r_pointer, math_symbols: list, opening_pars: dict, closing_pars: dict):
    index = l_pointer
    simplified_expressions = []  # here we remove parentheses

    while index <= r_pointer:
        if math_symbols[index] == '(':
            simplified_expression = evaluate_parentheses_in_depth(index + 1, closing_pars[index] - 1, math_symbols, opening_pars, closing_pars)
            simplified_expressions.append(simplified_expression)
            index = closing_pars[index]
        else:
            simplified_expressions.append(math_symbols[index])

        index += 1

    print(f'simplified_expressions: {simplified_expressions}')

    # what to do with neg operator???
    simplified_expressions_without_neg = get_non_negative_expressions(simplified_expressions)

    print(f'no_neg_expression: {simplified_expressions_without_neg}')

    # some powers-cutting
    simplified_expressions_without_neg_and_powers = evaluate_powers(simplified_expressions_without_neg)

    print(f'no_neg_and_powers_sexpression: {simplified_expressions_without_neg_and_powers}')

    return calculate(simplified_expressions_without_neg_and_powers)


def get_non_negative_expressions(simplified_expressions: list) -> list:

    simplified_expressions_without_neg = []

    if simplified_expressions[0] == '-':
        simplified_expressions_without_neg.append(-simplified_expressions[1])
        index = 2
    else:
        index = 0

    while index < len(simplified_expressions):
        if index + 1 + 1 < len(simplified_expressions) and \
                simplified_expressions[index] in ['/', '-', '*', '+', '^'] and simplified_expressions[index + 1] == '-':
            simplified_expressions_without_neg.append(simplified_expressions[index])
            simplified_expressions_without_neg.append(-simplified_expressions[index + 1 + 1])
            index += 3
        else:
            simplified_expressions_without_neg.append(simplified_expressions[index])
            index += 1

    return simplified_expressions_without_neg


def evaluate_powers(simplified_expressions_without_neg: list) -> list:  # 4 + 7 * 5 + 6 ^ 4 ^ 3 - 69999 + 9 ^ 98

    simplified_expressions_without_neg_and_powers = []

    index = len(simplified_expressions_without_neg) - 1
    while True:

        while index >= 0 and simplified_expressions_without_neg[index - 1] != '^':
            simplified_expressions_without_neg_and_powers.insert(0, simplified_expressions_without_neg[index])
            index -= 1

        if index < 0:
            break

        exponent_value = 0
        saved_index = index
        while simplified_expressions_without_neg[index - 1] == '^':
            exponent_value = simplified_expressions_without_neg[index - 2] ** exponent_value if index != saved_index\
                else simplified_expressions_without_neg[index - 2] ** simplified_expressions_without_neg[index]
            index -= 2

        index -= 1

        simplified_expressions_without_neg_and_powers.insert(0, exponent_value)

    return simplified_expressions_without_neg_and_powers


def calculate(simplified_expressions: list) -> float:

    def recursive_seeker(curr_index: int, curr_mult_div: float, result: float, last_operation_is_mult_div: bool) -> float or None:
        print(f'curr_index: {curr_index}, curr_mult_div: {curr_mult_div}, result: {result}')

        # base case:
        if len(simplified_expressions) == 0:
            return None

        # border case:
        if curr_index >= len(simplified_expressions):
            return result + curr_mult_div

        # recurrent relation:
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


print(evaluate_math_expr('-7 * -(6 / 3)'))
print(evaluate_math_expr('(35 - (46 * (7.7 - 1.12 / (5 * 97 - 3.36)) - -74 * -(59 + 1 - 98) / -31 + -58) * -61 - 7 * (1 + 2 * 6.6666))/(3 * 366.98 / (2 + 2 * 2) + 98.98) + 989'))
print(evaluate_math_expr('2 + (2 ^ 3 ^ 2 - 1) * 6.88'))

print(evaluate_powers([2, '+', 3, '^', 3, '^', 2, '-', 1]))
print(evaluate_powers([2, '^', 3, '^', 2, '+', 1]))
print(evaluate_powers([2, '+', 2]))
print(evaluate_powers([2]))
print(3 ** 69)
