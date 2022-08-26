# accepted on codewars.com
def n_queen(n):
    rem = n % 6

    if n in [2, 3]:
        return []
    elif rem == 2:
        evens = list(range(1, n, 2))
        odds = list(range(2, n, 2))
        odds[1] = 0
        odds.append(4)
    elif rem == 3:
        evens = list(range(3, n, 2)) + [1]
        odds = list(range(4, n, 2))
        odds += [0, 2]
    else:
        evens = list(range(1, n, 2))
        odds = list(range(0, n, 2))

    res = evens + odds
    return [res[i] for i in range(n)]


print(n_queen(5))
print(n_queen(6))

print(n_queen(14))

