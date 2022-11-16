# accepted on codewars.com, should be optimized and refactored

import operator
signs = {'*':  operator.mul, '/': operator.floordiv , '+': operator.add, '--': operator.add, '-': operator.sub}


def solve_runes(runes):
    parts = runes.split('=')
    print(f'parts: {parts}')

    left_part = parts[0]
    right_part = parts[1]
    print(f'l_p: {left_part}, r_p: {right_part}')

    for sing in signs:
        if sing in left_part[1:]:
            a_and_b = left_part.split(sing)
            if left_part[0] == sing == '-':
                a = '-' + a_and_b[1]
                b = a_and_b[2]
            else:
                a = a_and_b[0]
                b = a_and_b[1]

            print(f'a: {a}, b: {b}, c: {right_part}')

            if a == '' or b == '' or right_part == '':
                return -1

            for i in range(10):
                if (j := str(i)) not in a and j not in b and j not in right_part:
                    if signs[sing](int(a.replace('?', str(i))), int(b.replace('?', str(i)))) == int((r_p := right_part.replace('?', str(i)))):
                        if not (len(r_p) > 1 and (r_p[0] == '0' or (r_p[0] == '-' and r_p[1] == '0'))):
                            print(f'the key-number is: {i}')
                            return i

            return -1


print(solve_runes("123*45?=5?088"))  # --> answer is '6'
print(solve_runes("-5?*-1=5?"))  # --> answer is '0'
print(solve_runes("19--45=5?"))

print(solve_runes("?*11=??"))
print(solve_runes("-8593-533??=-?1959"))




print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][1:])
