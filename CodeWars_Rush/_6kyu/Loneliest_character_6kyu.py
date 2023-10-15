# accepted on codewars.com
def loneliest(strng: str):
    s = strng.strip()
    length = len(s)
    i = 0
    bests = []
    max_length = 0
    left_spaces = 0
    while i < length:
        temp = i
        i += 1
        while i < length and s[i] == ' ':
            i += 1
        right_spaces = i - temp - 1
        if (l_ := right_spaces + left_spaces) > max_length:
            max_length = l_
            bests = [s[temp]]
        elif l_ == max_length:
            bests.append(s[temp])
        left_spaces = right_spaces
    return bests


s1 = "a b  c"  # -->  ["b"]
s2 = "a bcs           d k"  # -->  ["d"]
s3 = "    a b  sc     p     t   k"  # -->  ["p"]
s4 = "a  b  c  de"  # -->  ["b", "c"]
s5 = "     a  b  c de        "  # -->  ["b"]
s6 = "abc"  # -->  ["a", "b", "c"]

print(f'res: {loneliest(s1)}')
print(f'res: {loneliest(s2)}')
print(f'res: {loneliest(s3)}')
print(f'res: {loneliest(s4)}')
print(f'res: {loneliest(s5)}')
print(f'res: {loneliest(s6)}')