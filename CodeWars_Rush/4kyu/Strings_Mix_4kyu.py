# accepted on codewars.com
def mix(s1: str, s2: str):  # -> str
    def get_freq_dict(string: str):
        freq_dict = dict()
        for char in string:
            if char != ' ' and char.islower():
                if char in freq_dict.keys():
                    freq_dict[char] += 1
                else:
                    freq_dict[char] = 1
        return freq_dict

    fd1, fd2 = get_freq_dict(s1), get_freq_dict(s2)
    print(f'fd1: {fd1}')
    print(f'fd2: {fd2}')
    result = []

    for key in (s := set(s1 := fd1.keys()).union(set(s2 := fd2.keys()))):
        if key in s1 and key not in s2:
            if (el := fd1[key]) > 1:
                result.append(['1:' + key * el, el])
        elif key not in s1 and key in s2:
            if (el := fd2[key]) > 1:
                result.append(['2:' + key * el, el])
        else:
            if (el := max(el1 := fd1[key], el2 := fd2[key])) > 1:
                if el1 > el2:
                    result.append(['1:' + key * el, el])
                elif el2 > el1:
                    result.append(['2:' + key * el, el])
                else:
                    result.append(['=:' + key * el, el])

    result = sorted(result, key=lambda x: (-x[1], x[0]))
    print(result)

    return "/".join([string[0] for string in result])


mix("A aaaa bb c", "& aaa bbb c d")
mix("Are they here", "yes, they are here")
s = mix("Sadus:cpms>orqn3zecwGvnznSgacs", "MynwdKizfd$lvse+gnbaGydxyXzayp")

print(s)