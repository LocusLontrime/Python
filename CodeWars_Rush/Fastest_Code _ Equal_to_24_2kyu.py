import operator
import time

operators_dict = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}

rec_counter = 0


# too slow method, can beat 280 test cases
def equal_to_24_slow(a, b, c, d):

    global rec_counter

    digits_list = [a, b, c, d]
    rec_counter = 0
    res = recursive_seeker(digits_list, 0, '', 0, '', 24)
    print(f'rec counter: {rec_counter}')
    return res if res != "" else "It's not possible!"


def recursive_seeker(digits_remained: list, curr_sum, expression: str, curr_par_sum, curr_par_expr: str, target=24) -> str:

    global rec_counter

    rec_counter += 1

    if len(digits_remained) == 0:
        if curr_sum == target and len(curr_par_expr) == 0:
            return expression
        elif curr_sum + curr_par_sum == target:
            return expression + f'+{curr_par_expr}'
        elif len(curr_par_expr) == 0:
            print(f'expression: {expression}')
            return ""

    for digit in digits_remained:
        new_digits_remained = digits_remained.copy()
        new_digits_remained.remove(digit)

        if len(curr_par_expr) == 0:

            for key, value in operators_dict.items():
                if not (key == '*' or key == '/'):
                    res = recursive_seeker(new_digits_remained, operators_dict[key](curr_sum, digit), (f'({expression})' if key == '*' or key == '/' else expression) + f'{key}{digit}', curr_par_sum, curr_par_expr, target)
                    if res != "":
                        return res

            res = recursive_seeker(new_digits_remained, curr_sum, expression, curr_par_sum + digit, curr_par_expr + f'+{digit}', target)
            if res != "":
                return res
            res = recursive_seeker(new_digits_remained, curr_sum, expression, curr_par_sum - digit, curr_par_expr + f'-{digit}', target)
            if res != "":
                return res

        else:
            for key, value in operators_dict.items():
                res = recursive_seeker(new_digits_remained, curr_sum, expression, operators_dict[key](curr_par_sum, digit), '(' + curr_par_expr + f'){key}{digit}', target)
                if res != "":
                    return res

    if len(expression) != 0 and len(curr_par_expr) != 0:
        res = recursive_seeker(digits_remained, curr_sum * curr_par_sum, f'({expression})*({curr_par_expr})', 0, '', target)
        if res != "":
            return res
        if curr_par_sum != 0:
            res = recursive_seeker(digits_remained, curr_sum / curr_par_sum, f'({expression})/({curr_par_expr})', 0, '', target)
            if res != "":
                return res

    return ""


def equal_to_24(a, b, c, d):  # accepted on codewars.com

    global rec_counter

    rec_counter = 0

    for operators in perms(['+', '-', '*', '/'], 3, True):
        for numbers in perms([a, b, c, d], 4, False):

            try:

                op1, op2, op3 = operators
                n1, n2, n3, n4 = numbers

                if operators_dict[op1](operators_dict[op2](n1, n2), operators_dict[op3](n3, n4)) == 24:
                    return f'({n1}{op2}{n2}){op1}({n3}{op3}{n4})'

                if operators_dict[op1](operators_dict[op2](operators_dict[op3](n1, n2), n3), n4) == 24:
                    return f'(({n1}{op3}{n2}){op2}{n3}){op1}{n4}'

                if operators_dict[op1](operators_dict[op2](n1, operators_dict[op3](n2, n3)), n4) == 24:
                    return f'({n1}{op2}({n2}{op3}{n3})){op1}{n4}'

                if operators_dict[op1](n1, operators_dict[op2](operators_dict[op3](n2, n3), n4)) == 24:
                    return f'{n1}{op1}(({n2}{op3}{n3}){op2}{n4})'

                if operators_dict[op1](n1, operators_dict[op2](n2, operators_dict[op3](n3, n4))) == 24:
                    return f'{n1}{op1}({n2}{op2}({n3}{op3}{n4}))'

            except ZeroDivisionError:
                pass

    return "It's not possible!"


def perms(elems: list, elems_in_sample_quantity: int, is_rep_allowed: bool) -> set[tuple]:

    perms_with_reps_list = []

    def permutations_with_repetitions(elements: list[str], curr_sequence: tuple):

        if len(curr_sequence) == elems_in_sample_quantity:
            perms_with_reps_list.append(curr_sequence)
            return

        for i in range(len(elements)):
            permutations_with_repetitions(elements if is_rep_allowed else elements[:i] + elements[i + 1:], curr_sequence + (elements[i],))

    permutations_with_repetitions(elems, tuple())

    return set(perms_with_reps_list)


# print(equal_to_24(1, 2, 3, 4))
# print(equal_to_24(13, 13, 6, 12))
# print(equal_to_24(2, 7, 7, 13))
# print(equal_to_24(4, 3, 1, 6))
# print(equal_to_24(13, 13, 13, 13))
# print(equal_to_24(2, 3, 4, 5))
# print(equal_to_24(1, 1, 1, 13))
# print(equal_to_24(3, 4, 5, 6))
# print(equal_to_24(72, 11, 36, 98))
# print(equal_to_24(100, 35, 9, 81))

# tic = time.perf_counter()
#
# print(equal_to_24(8, 16, 69, 36))
# print(len(list(permutations([8, 16, 69, 36]))))
#
# toc1 = time.perf_counter()
# print(f"Time elapsed: {toc1 - tic:0.4f} seconds")

print(equal_to_24(1, 2, 3, 4))

print(perms(['+', '-', '*', '/'], 3, True))
print(perms([1, 2, 3, 4], 4, False))

ex_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

print(ex_list[:3] + ex_list[3 + 1:])
