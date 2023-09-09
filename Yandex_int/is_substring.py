def is_substring(first_string: str, second_string: str):
    fi, si = 0, 0
    while fi < (l1 := len(first_string)) and si < len(second_string):
        if first_string[fi] == second_string[si]:
            fi += 1
        si += 1
    return fi == l1


s1 = 'abc'
s2 = 'mnagbcd'
print(f'res: {is_substring(s1, s2)}')
