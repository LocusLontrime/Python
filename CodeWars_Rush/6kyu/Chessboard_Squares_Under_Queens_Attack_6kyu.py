# accepted on codewars.com
shifts = [[-1, -1], [-1, 1], [1, 1], [1, -1]]  # (j, i)


def chessboard_squares_under_queen_attack(a: int, b: int):
    aggregated_value = 0
    for j in range(a):
        for i in range(b):
            aggregated_value += count_cells_under_attack(a, b, j, i)
    return aggregated_value - 4 * a * b


# Levi Gin method
def count_cells_under_attack(a: int, b: int, start_j: int, start_i: int):
    ans = 0
    if 0 <= start_j < a and 0 <= start_i < b:
        ans += a + b - 2
        for shift in shifts:
            j, i = start_j, start_i
            while a > j >= 0 and b > i >= 0:
                ans += 1
                j += shift[0]
                i += shift[1]
        return ans
    else:
        return -1


def ultra_fast_one(a: int, b: int):
    x = min(a, b)
    y = max(a, b)

    return x * (9 * x * y - 2 * x ** 2 + 3 * y ** 2 - 12 * y + 2) // 3


# print(ultra_fast_one(2, 3))
# print(ultra_fast_one(2, 2))
print(ultra_fast_one(2500000000000000000000000000000000, 2500000000000000000000000000000000000000))  # 320

print(chessboard_squares_under_queen_attack(5, 5))
