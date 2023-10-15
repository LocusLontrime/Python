# accepted on codewars.com
digits = '0123456789'


def increment_string(string):
    i, res = 0, ''
    while i < (length := len(string)):
        start, end = '', ''
        while i < length and (s := string[i]) not in digits:
            start += s
            i += 1
        while i < length and (s := string[i]) in digits:
            end += s
            i += 1
        if i == length and end:
            length_before = len(str(e := int(end)))
            zeroes_quantity = len(end) - length_before
            s = str(e + 1)
            end = '0' * (zeroes_quantity - (1 if len(s) > length_before else 0)) + s
        elif not end:
            end = '1'
        res += start + end
    return res if string else '1'


print(increment_string("foobar099"))
print(increment_string('foo'))
print(increment_string('foobar001'))
print(increment_string(''))
