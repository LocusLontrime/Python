from collections import deque


def get_symbols(math_expression: str):
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

    return 97


def evaluate_math_expr(math_expression: str) -> float:
    m_smbls, op_prs, cl_pars = get_symbols(math_expression)






get_symbols("-7.0987 * -(6 / 3)")








q = deque()
q.append(1)
q.append(2)
q.append(3)

print(q)

q.pop()

print(q)
