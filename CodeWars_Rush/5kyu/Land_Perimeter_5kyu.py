# accepted on codewars.com
def land_perimeter(arr: list[str]):
    xsQuantity = 0
    bridgesQuantity = 0

    for j in range(0, len(arr)):
        for i in range(0, len(arr[0])):

            if arr[j][i] == 'X':
                xsQuantity += 1

            if i != len(arr[0]) - 1:
                if arr[j][i] == 'X' and arr[j][i + 1] == 'X':
                    bridgesQuantity += 1

            if j != len(arr) - 1:
                if arr[j][i] == 'X' and arr[j + 1][i] == 'X':
                    bridgesQuantity += 1

    return f'Total land perimeter: {4 * xsQuantity - 2 * bridgesQuantity}'


print(land_perimeter(["OXOOOX", "OXOXOO", "XXOOOX", "OXXXOO", "OOXOOX", "OXOOOO", "OOXOOX", "OOXOOO", "OXOOOO", "OXOOXX"]))

print(len("lalala"))
