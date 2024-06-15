def missing(s: str) -> int:
    for el_len in range(1, len(s) // 2):
        errs_counter, i = 0, 0
        while i + 2 * el_len <= len(s):
            # compare curr and next nums:
            el, el_, el__ = s[i: i + el_len], s[i + el_len: i + 2 * el_len], s[i + el_len: i + 2 * el_len + 1]
            _el_len = el_len
            if int(el) + 1 == int(el_):
                ...
            elif int(el) + 2 == int(el_):
                errs_counter += 1
                missing_el = int(el) + 1
            elif int(el) + 1 == int(el__):
                el_len += 1
            elif int(el) + 2 == int(el__):
                el_len += 1
                errs_counter += 1
                missing_el = int(el) + 1
            else:
                break
            if errs_counter > 1:
                break
            i += _el_len
        else:
            if errs_counter:
                return missing_el
    return -1

print(f'res: {missing("900001900002900004900005900006")}')  # -> 900003               # 36 366 98 989 98989 LL
# print(f'res: {missing("9899101102")}')  # -> 100

