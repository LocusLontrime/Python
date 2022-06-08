# 1 - Написать программу вычисления арифметического выражения заданного строкой. Используются операции +,-,/,*.
# приоритет операций стандартный. Функцию eval не использовать!
# Пример: 2+2 => 4; 1+2*3 => 7; 1-2*3 => -5;
# Дополнительно: Добавить возможность использования скобок, меняющих приоритет операций.
# Пример: 1+2*3 => 7; (1+2)*3 => 9;
import time
from collections import deque


def evaluate_math_expr(math_expression: str) -> float:  # accepted on codewars
    m_smbls, op_prs, cl_pars = get_symbols(math_expression)  # getting all the math symbols in the list m_smbls and pars indexes dicts

    return evaluate_parentheses_in_depth(0, len(m_smbls) - 1, m_smbls, op_prs, cl_pars)


def get_symbols(math_expression: str):  # 3.6 3,6 36 366 98 989
    math_symbols = []  # all the symbols from math expr -> it means: all operators, parentheses and nu,bers: float and ints
    opening_pars = dict()  # dict for convenient excluding the opening parenthesis' index for every closing one
    closing_pars = dict()  # inverse dict for finding closing parenthesis' index for every closing one

    deq = deque()

    index = 0
    while index < len(math_expression):
        if math_expression[index] == ' ':
            index += 1
            continue

        if math_expression[index].isdigit():  # building a full valid number (float or int)
            saved_index = index  # here we save the index to get the array sliced further
            while math_expression[index].isdigit() or math_expression[index] == '.':
                index += 1  # defining the length of a number, here we're moving to the right, iterating
                if index >= len(math_expression):
                    break
            number_found = float(math_expression[saved_index: index])  # getting the value of a number found
            math_symbols.append(number_found)  # adding the value above to the math_symbols list
        else:
            if math_expression[index] == '(':  # here we're creating two parentheses' dicts
                deq.append(len(math_symbols))
            elif math_expression[index] == ')':
                closing_index = len(math_symbols)
                opening_pars[closing_index] = deq.pop()
                closing_pars[opening_pars[closing_index]] = closing_index

            math_symbols.append(math_expression[index])  # if the symbol is not a parenthesis or digit -> it will be automatically added to math_symbols list
            index += 1  # iterating

    # print(f'all symbols: {math_symbols}')
    # print(f'opening pars -> closing ones dict: {opening_pars}')
    # print(f'closing pars -> opening ones dict: {closing_pars}')

    return math_symbols, opening_pars, closing_pars


def evaluate_parentheses_in_depth(l_pointer, r_pointer, math_symbols: list, opening_pars: dict, closing_pars: dict):
    index = l_pointer
    simplified_expressions = []  # here we remove parentheses and get the simplified expression that can be computed easily

    while index <= r_pointer:  # while we are in the expr length
        if math_symbols[index] == '(':  # if we encounter a parenthesis we invoke a recursive function evaluate_parentheses_in_depth for expression located inside these parentheses
            # and so on no matter the depth of nested parentheses
            simplified_expression = evaluate_parentheses_in_depth(index + 1, closing_pars[index] - 1, math_symbols, opening_pars, closing_pars)  # simplifying the nested expression
            simplified_expressions.append(simplified_expression)  # then we add it to the simplified_expressions list
            index = closing_pars[index]  # proceeding to the closing parenthesis relative to the current opening one
        else:
            simplified_expressions.append(math_symbols[index])  # if the re is no parenthesis for now we're just adding the symbol to simplified_expressions list

        index += 1  # iterating

    # print(f'simplified_expressions: {simplified_expressions}')

    # what to do with neg operator??? -> implement a special method!!!
    simplified_expressions_without_neg = get_non_negative_expressions(simplified_expressions)

    # print(f'no_neg_expression: {simplified_expressions_without_neg}')

    return calculate(simplified_expressions_without_neg)


def get_non_negative_expressions(simplified_expressions: list) -> list:  # here we get rid of annoying neg (not subtract) operators (like: -9, 989 + -98)
    simplified_expressions_without_neg = []  # just a new expression without neg operators

    if simplified_expressions[0] == '-':  # a starting case, needs additional checking
        simplified_expressions_without_neg.append(-simplified_expressions[1])  # if the expressions starts with neg sign
        index = 2
    else:
        index = 0  # if there is no starting neg sign

    while index < len(simplified_expressions):  # below lies a careful stop condition, got from some testing and checking
        if index + 1 + 1 < len(simplified_expressions) and \
                simplified_expressions[index] in ['/', '-', '*', '+'] and simplified_expressions[index + 1] == '-':
            simplified_expressions_without_neg.append(simplified_expressions[index])  # here are the signs
            simplified_expressions_without_neg.append(-simplified_expressions[index + 1 + 1])  # neg, applied to a number
            index += 3  # iterating through two signs and number
        else:
            simplified_expressions_without_neg.append(simplified_expressions[index])  # if there is no neg sign we can continue moving
            index += 1  # iterating

    return simplified_expressions_without_neg


def calculate(simplified_expressions: list) -> float:  # base recursive method to calculate mul, div, add and sub in a sequence
    def recursive_seeker(curr_index: int, curr_mult_div: float, result: float, last_operation_is_mult_div: bool) -> float or None:
        # print(f'curr_index: {curr_index}, curr_mult_div: {curr_mult_div}, result: {result}')

        # base case:
        if len(simplified_expressions) == 0:
            return None

        # border case:
        if curr_index >= len(simplified_expressions):  # here the calculations end
            return result + curr_mult_div

        # recurrent relation:
        if simplified_expressions[curr_index] == '+':  # '+' and '-' easy cases
            return recursive_seeker(curr_index + 1, 1.0, result + curr_mult_div, False)  # now we're adding the curr_mult_div result to the main result value

        elif simplified_expressions[curr_index] == '-':
            return recursive_seeker(curr_index + 1, -1.0, result + curr_mult_div, False)  # now we're subtracting the curr_mult_div result from the main result value

        if last_operation_is_mult_div:  # if the last operations before was a multiplication or division
            # continue building a mul-div sequence
            if simplified_expressions[curr_index] == '*':
                curr_mult_div *= simplified_expressions[curr_index + 1]
            elif simplified_expressions[curr_index] == '/':
                curr_mult_div /= simplified_expressions[curr_index + 1]
            return recursive_seeker(curr_index + 2, curr_mult_div, result, True)

        else:  # if not -> we should start building a new mult-div sequence
            curr_mult_div *= simplified_expressions[curr_index]
            return recursive_seeker(curr_index + 1, curr_mult_div, result, True)

    return recursive_seeker(0, 1.0, 0.0, False)  # initial parameters


print(f"result1: {evaluate_math_expr('-7 * -(6 / 3)')}")

tic = time.perf_counter()

print(f"result2: {evaluate_math_expr('(35 - (46 * (7.7 - 1.12 / (5 * 97 - 3.36)) - -74 * -(59 + 1 - 98) / -31 + -58) * -61 - 7 * (1 + 2 * 6.6666))/(3 * 366.98 / (2 + 2 * 2) + 98.98) + 989')}")

toc1 = time.perf_counter()
print(f"Time elapsed for calculations: {toc1 - tic:0.8f} seconds")
