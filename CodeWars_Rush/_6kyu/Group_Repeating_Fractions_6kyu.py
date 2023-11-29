# accepted on codewars.com

def repeating_fractions(numerator: int, denominator: int):
    quotient = str(numerator / denominator)

    res = ''
    flag = False
    i = 0

    while i < len(quotient):
        ch = quotient[i]
        tmp = i
        if not flag:
            if ch == '.':
                flag = True
            res += ch
            i += 1
        else:
            while i < len(quotient) and quotient[i] == quotient[tmp]:
                i += 1

            res += f'({ch})' if i - tmp > 1 else ch

    return res


