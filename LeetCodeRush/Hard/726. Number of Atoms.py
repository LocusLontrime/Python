# accepted on leetcode.com

from collections import defaultdict


def count_of_atoms(formula: str) -> str:
    # formula's length:
    n = len(formula)
    # stack:
    stack = [defaultdict(int)]
    # the core algo:
    i = 0
    iteration = 0
    while i < n:
        iteration += 1
        elements_, i = parse_before_parenthesis(formula, i, n)
        print(f'{iteration} iteration -> {elements_, i} been parsed')
        # adding to stack:
        add_elements(stack[-1], elements_)
        if i == n:
            break
        if formula[i] == "(":
            print(f'encountered a ( -> new stack level appended')
            i += 1
            # new stack level appended:
            stack += [defaultdict(int)]
        elif formula[i] == ")":
            i += 1
            # the highest stack level removed and appended (multiplied by num if it exists) to the previous one:
            num, i = parse_num(formula, i, n)
            add_elements(prev_lvl := stack[-2], highest_lvl := stack.pop(), num)
            print(f'encountered a ) -> the highest stack level removed and appended (multiplied by {num}) to the previous one')
            print(f'...{highest_lvl = }')
            print(f'...{prev_lvl = }')
    print(f'{stack = }')
    return ''.join(f"{el}{count if count > 1 else ''}" for el, count in sorted(stack[0].items(), key=lambda x: x[0]))


def parse_before_parenthesis(formula: str, i: int, n: int):
    elements = defaultdict(int)
    while i < n and formula[i] not in {"(", ")"}:
        # upper letter:
        element = formula[i]
        i += 1
        # lower ones:
        while i < n and formula[i].isalpha() and formula[i].islower():
            element += formula[i]
            i += 1
        num, i = parse_num(formula, i, n)
        elements[element] += num
    return elements, i


def parse_num(formula: str, i: int, n: int):
    num = 0
    while i < n and formula[i].isdigit():
        num = num * 10 + int(formula[i])
        i += 1
    return max(1, num), i


def add_elements(stack_elems: defaultdict, elems_to_be_added: defaultdict, multiplier=1):
    for elem, count in elems_to_be_added.items():
        stack_elems[elem] += count * multiplier


test_ex = "K4(ON(SO3)2)2"
test_ex_2 = "SO2(O9(Fe4He7C89)7Si9(O8(Fe8H17C2O7)5Pa8Mt9(Au7(Si4Pa7)5)9Mt)8O7Si3K2N)9O4Ar3H2O99"

print(f'test ex res -> {count_of_atoms(test_ex)}')                                    # 36 366 98 989 98989 LL LL
print(f'test ex 2 res -> {count_of_atoms(test_ex_2)}')

# Stack:

# SO2 (O9 Fe4He7C89 * 7 Si9 + (O8 Fe8H17C2O7 * 5 Pa8Mt9 (Au7 Si4Pa7 * 5) * 9 Mt) * 8 O7Si3K2N) * 9 O4Ar3H2O99
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
