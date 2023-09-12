def palindromize(number: int) -> str:
    counter = 0
    while (s := str(number)) != (rs := s[::-1]):
        number += int(rs)
        counter += 1
    return f'{counter} {number}'


