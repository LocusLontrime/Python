import math
from collections import deque

constants = {"pi": math.pi, "exp_base": math.e, "phi": (1 + math.sqrt(2)) / 2}

operators = ['/', '-', '*', '+', '^']

words_operators = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": lambda x: math.asin(x) if -1 <= x <= 1 else "ERROR",
    "acos": lambda x: math.acos(x) if -1 <= x <= 1 else "ERROR",
    "atan": math.atan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "log": lambda x: math.log(x) if x > 0 else "ERROR",
    "exp": math.exp,
    "sqrt": lambda x: math.sqrt(x) if x >= 0 else "ERROR",
    "ln": lambda x: math.log(x, constants["e"]) if x > 0 else "ERROR",
    "abs": lambda x: abs(x)
}

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def evaluate_math_expr(math_expression: str):  # accepted on codewars, powers calculations been added

    data = get_symbols(math_expression)

    if data == "ERROR":
        return "ERROR"

    m_smbls, op_prs, cl_pars = data

    return evaluate_parentheses_in_depth(0, len(m_smbls) - 1, m_smbls, op_prs, cl_pars)


def get_symbols(math_expression: str):  # 3.6 3,6 36 366 98 989
    math_symbols = []
    opening_pars = dict()
    closing_pars = dict()

    op_counter, cl_counter = 0, 0

    deq = deque()

    index = 0
    while index < len(math_expression):
        if math_expression[index] == ' ':
            print(f'index: {index}')
            index += 1
            continue
        # now includes scientific notation
        if math_expression[index].isdigit():
            saved_index = index
            while math_expression[index].isdigit() or math_expression[index] in ['.', 'e'] or (math_expression[index] in ['+', '-'] and math_expression[index - 1] == 'e' and index != 0):
                index += 1
                if index >= len(math_expression):
                    break
            try:
                number_found = float(math_expression[saved_index: index])
            except ValueError as e:  # can be improved with the explanation about Exception raised
                return 'ERROR'
            math_symbols.append(number_found)
        # includes words-operators like: sin, ln, sqrt, abs, etc and constants like: pi, e, phi, etc
        elif math_expression[index].lower() in letters:
            saved_index = index
            while math_expression[index].lower() in letters:
                index += 1
                if index >= len(math_expression):
                    break
            word_found = math_expression[saved_index: index].lower()
            math_symbols.append(word_found)
        else:
            if math_expression[index] == '(':
                op_counter += 1
                deq.append(len(math_symbols))
            elif math_expression[index] == ')':
                cl_counter += 1
                if cl_counter > op_counter:
                    return "ERROR"
                closing_index = len(math_symbols)
                opening_pars[closing_index] = deq.pop()
                closing_pars[opening_pars[closing_index]] = closing_index

            math_symbols.append(math_expression[index])
            index += 1

    print(math_symbols)
    print(opening_pars)
    print(closing_pars)

    if cl_counter != op_counter:
        return "ERROR"

    for i in range(len(math_symbols) - 1):  # [3.66, '-', '-', '-', 9.0, '-', 98.9]
        if math_symbols[i: i + 1 + 1] == ['+'] * 2:
            return "ERROR"

    index = 0
    while index < len(math_symbols):
        if math_symbols[index] == '-':
            saved_index = index
            while math_symbols[index] == '-':
                index += 1

            if (index - saved_index) % 2 == 1:  # 7
                math_symbols = math_symbols[:saved_index + 1] + math_symbols[index:]
                index = saved_index + 1
            else:
                math_symbols = math_symbols[:saved_index] + ['+'] + math_symbols[index:]
                index = saved_index

        else:
            index += 1

    print(math_symbols)

    return [math_symbols, opening_pars, closing_pars]


def evaluate_parentheses_in_depth(l_pointer, r_pointer, math_symbols: list, opening_pars: dict, closing_pars: dict):
    index = l_pointer
    simplified_expressions = []  # here we remove parentheses

    if math_symbols[l_pointer] == '+':
        return "ERROR"

    while index <= r_pointer:
        if math_symbols[index] in words_operators:
            argument = evaluate_parentheses_in_depth(index + 1 + 1, closing_pars[index + 1] - 1, math_symbols, opening_pars, closing_pars)
            if argument == "ERROR":
                return "ERROR"
            operator_applied_value = words_operators[math_symbols[index]](argument)
            if operator_applied_value == "ERROR":
                return "ERROR"
            simplified_expressions.append(operator_applied_value)
            index = closing_pars[index + 1]
            print(f'operator_applied_value: {operator_applied_value}')
        elif math_symbols[index] in constants.keys():
            constant_value = constants[math_symbols[index]]
            simplified_expressions.append(constant_value)
            print(f'constant_value: {constant_value}')
        elif math_symbols[index] == '(':
            simplified_expression = evaluate_parentheses_in_depth(index + 1, closing_pars[index] - 1, math_symbols, opening_pars, closing_pars)
            simplified_expressions.append(simplified_expression)
            index = closing_pars[index]
        elif type(math_symbols[index]) in [int, float] or math_symbols[index] in operators:
            simplified_expressions.append(math_symbols[index])
        else:
            print("lala")
            return "ERROR"

        index += 1

    print(f'simplified_expressions: {simplified_expressions}')

    if "ERROR" in simplified_expressions:
        return "ERROR"

    # some powers-cutting
    evaluate_powers(simplified_expressions)
    print(f'no_powers_expression: {simplified_expressions}')

    # what to do with neg operator???
    simplified_expressions_without_neg_and_powers = get_non_negative_expressions(simplified_expressions)
    print(f'no_neg_and_powers_expression: {simplified_expressions_without_neg_and_powers}')

    if simplified_expressions_without_neg_and_powers == "ERROR":
        return "ERROR"

    return calculate(simplified_expressions_without_neg_and_powers)


# should be checked: ['/', '-', '*', '+', '^'] can be not enough -> OPTIMIZATION!!!
def get_non_negative_expressions(simplified_expressions: list) -> list:

    simplified_expressions_without_neg = []

    if simplified_expressions[0] == '-':
        simplified_expressions_without_neg.append(-simplified_expressions[1])
        index = 2
    else:
        index = 0

    while index < len(simplified_expressions):
        if index + 1 + 1 < len(simplified_expressions) and \
                simplified_expressions[index] in operators and simplified_expressions[index + 1] == '-':
            simplified_expressions_without_neg.append(simplified_expressions[index])
            simplified_expressions_without_neg.append(-simplified_expressions[index + 1 + 1])
            index += 3
        else:
            simplified_expressions_without_neg.append(simplified_expressions[index])
            index += 1

    return simplified_expressions_without_neg


# in-place algo, O(n ^ 2) -> can be re-built to O(n), but it will require additional memory
def evaluate_powers(simplified_expressions: list):  # TODO: [98, '+', 4, '^', 3, '^', 2, '^', 1, '-', 3, '*', 68, '+', 98, '/', 1, '+', 98989]
    index = len(simplified_expressions) - 2
    while index >= 1:
        exponent_value = simplified_expressions[index + 1]
        if simplified_expressions[index] == '^' and type(exponent_value) in [float, int]:
            del simplified_expressions[index + 1]
            while type(a := simplified_expressions[index - 1]) in [float, int] and (k := simplified_expressions[index]) == '^':
                exponent_value = a ** exponent_value
                if type(exponent_value) is complex:
                    return "ERROR"
                del simplified_expressions[index], simplified_expressions[index - 1]
                index -= 2
            simplified_expressions.insert(index + 1, exponent_value)  # = simplified_expressions[: index + 1] + [exponent_value] + simplified_expressions[saved_index + 2:]
        else:
            index -= 1

# def evaluate_powers(simplified_expressions_without_neg: list):  # 4 + 7 * 5 + 6 ^ 4 ^ 3 - 69999 + 9 ^ 98
#
#     simplified_expressions_without_neg_and_powers = []
#
#     index = len(simplified_expressions_without_neg) - 1
#     while True:
#
#         while index >= 1 and simplified_expressions_without_neg[index - 1] != '^':
#             simplified_expressions_without_neg_and_powers.insert(0, simplified_expressions_without_neg[index])
#             index -= 1
#
#         if index < 0:
#             break
#
#         exponent_value = 0
#         saved_index = index
#         while simplified_expressions_without_neg[index - 1] == '^':
#             exponent_value = simplified_expressions_without_neg[index - 2] ** exponent_value if index != saved_index\
#                 else simplified_expressions_without_neg[index - 2] ** simplified_expressions_without_neg[index]
#
#             if type(exponent_value) is complex:
#                 return "ERROR"
#
#             index -= 2
#
#         index -= 1
#
#         simplified_expressions_without_neg_and_powers.insert(0, exponent_value)
#
#     return simplified_expressions_without_neg_and_powers


def calculate(simplified_expressions: list) -> float:

    def recursive_seeker(curr_index: int, curr_mult_div: float, result: float, last_operation_is_mult_div: bool) -> float or None:
        print(f'curr_index: {curr_index}, curr_mult_div: {curr_mult_div}, result: {result}')

        # base case:
        if len(simplified_expressions) == 0:
            return "ERROR"

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
                if simplified_expressions[curr_index + 1] != 0:
                    curr_mult_div /= simplified_expressions[curr_index + 1]
                else:
                    return "ERROR"
            return recursive_seeker(curr_index + 2, curr_mult_div, result, True)

        else:
            curr_mult_div *= simplified_expressions[curr_index]
            return recursive_seeker(curr_index + 1, curr_mult_div, result, True)

    return recursive_seeker(0, 1.0, 0.0, False)


# print(evaluate_math_expr('-7 * -(6 / 3)'))
# print(evaluate_math_expr('(35.57 * 3.66 ^ 3 ^ 2 - 3 ^ 2.843 ^ 3.66 / (3 + 5 ^ 5 ^ 1.33) - (46 * (7.7 - 1.12 / (5 * 97 ^ 2.98 - 3.36)) ^ (1.1 - 0.09) ^ (0.01 + 1) - -74 * -(59 + 1 - 98) / -31 + -58) * -61 - 7 * (1 + 2 * 6.6666))/(3 * 366.98 / (2 + 2 * 2) + 98.98) + 989'))
# print(eval('(35.57 * 3.66 ** 3 ** 2 - 3 ** 2.843 ** 3.66 / (3 + 5 ** 5 ** 1.33) - (46 * (7.7 - 1.12 / (5 * 97 ** 2.98 - 3.36)) ** (1.1 - 0.09) ** (0.01 + 1) - -74 * -(59 + 1 - 98) / -31 + -58) * -61 - 7 * (1 + 2 * 6.6666))/(3 * 366.98 / (2 + 2 * 2) + 98.98) + 989'))
# print(evaluate_math_expr('2 + (2 ^ 3 ^ 2 - 1) * 6.88'))
# print(evaluate_powers([2, '+', 3, '^', 3, '^', 2, '-', 1]))
# print(evaluate_powers([2, '^', 3, '^', 2, '+', 1]))
# print(evaluate_powers([2, '+', 2]))
# print(evaluate_powers([2]))
# print(3 ** 169)
# num = 9899999999999999999999999999999999999999999999999999999999999999999
# print(num)
# get_symbols("sin(5 + 3 ^ 2)")
# print(evaluate_math_expr("sin(5 + 3 ^ 2)"))
# print(evaluate_math_expr("4^3^2"))
# print(math.sin(14))

# print(evaluate_math_expr("sin(pi * sin(1 + 2) + 4 ^ 3.088 ^ sin(1))"))  # good
# # print(words_operators["sin"](math.pi / 2))
# print(calculate([5.0, "+", 98, "/", 0]))
# print(evaluate_math_expr("5 + 98 / (93 - 2 - 1) + sqrtinus(-2)"))

# print(evaluate_math_expr("(((5)) * (s) + 4 * 9 + 100 + 800)"))

# print(evaluate_math_expr("---5"))

# print(float("3.66e-100") / 1000000000000000000000000000)
#
# print(float("3.66e100"))

# print(evaluate_math_expr("abs(-(-1+(2*(4--3)))&2)"))

# print(evaluate_math_expr("abs(1 - 98.989e+100e/10)"))
# print(evaluate_math_expr("e-100e1e98e + 9 - 1"))

# print(evaluate_math_expr("5 --6 + -7 - 1"))

# print(evaluate_math_expr("sinh(sin(98.98e+1 + tan(asin(4 ^ 3 ^ 2 ^ cos(log(9 + 1 * 2 - 3.66)))) ^ 3 - 1) + 98.989) * 3 - 1"))

# print(evaluate_math_expr("2 ^ sin(cosh(9 + 4^-1^1.98e+1 / 3) * sin(98) ^ 9 / 100.1 - log(100 - 1) ^ -1) + 3 * 4 * 5 / 2 - 1"))

# print(evaluate_math_expr("4.3 ^ -1 ^ 3"))

# print(math.asin(98))

# print(evaluate_math_expr("cosh(9 + 4^-1^1.98e+1 / 3)"))

# print(evaluate_math_expr("++7 ^ 8 + + 98.989 - 98"))
# print(float("98.98e+1"))
# print(evaluate_powers(" --- 7"))
# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][3: 3 + 1 + 1])

# math_symbols = [3.66, '-', '-', '-', 9.0, '-', '-', 98.9]
#
# index = 0
# while index < len(math_symbols):
#     if math_symbols[index] == '-':
#         saved_index = index
#         while math_symbols[index] == '-':
#             index += 1
#
#         if (index - saved_index) % 2 == 1:  # 7
#             math_symbols = math_symbols[:saved_index + 1] + math_symbols[index:]
#             index = saved_index + 1
#         else:
#             math_symbols = math_symbols[:saved_index] + ['+'] + math_symbols[index:]
#             index = saved_index
#
#     else:
#         index += 1
#
# print(evaluate_math_expr("1 ----7 ^ 2 -- (1.98989 + 1)"))

pws = [98, '+', 4, '^', 3, '^', 2, '^', 1, '-', 3, '*', 68, '+', 98, '/', 1, '+', 98989]

evaluate_powers(pws)

print(f'length: {len(pws)}, pws: {pws}')

