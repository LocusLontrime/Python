# accepted on codewars.com


def count_repeats(txt):
    _ch = ''
    i = 0
    counter = 0
    while i < len(txt):
        while i < len(txt) and _ch == txt[i]:
            i += 1
            counter += 1
        if i < len(txt):
            _ch = txt[i]
            i += 1
    return counter


txt1 = 'abbbbc'  # => 'abc'    #  answer: 3
txt2 = 'abbcca'  # => 'abca'   #  answer: 2
txt3 = 'ab cca'  # => 'ab ca'  #  answer: 1

print(f'res -> {count_repeats(txt1)}')
print(f'res -> {count_repeats(txt2)}')
print(f'res -> {count_repeats(txt3)}')
