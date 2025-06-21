# accepted on codewars.com

def luxhouse(houses):

    max_el = 0
    floors_added = [0 for _ in range(len(houses))]

    for i in range(len(houses) - 1, -1, -1):
        floors_added[i] = k if (k := max_el - houses[i] + 1) > 0 else 0
        max_el = max(max_el, houses[i])

    return floors_added


test_case = [1, 2, 3, 1, 2]

print(f'res: {luxhouse(test_case)}')
