# Начиная с числа 1 и двигаясь дальше вправо по часовой
# стрелке, образуется следующая спираль 5 на 5:

# 21 22 23 24 25
# 20  7  8  9 10
# 19  6  1  2 11
# 18  5  4  3 12
# 17 16 15 14 13

# Можно убедиться, что сумма чисел в диагоналях равна 101. (1+3+5+7+9+13+17+21+25)
# Какова сумма чисел в диагоналях спирали 1001 на 1001, образованной таким же способом?


def get_diagonal_spiral_sum(length: int) -> int:
    iterations = (length - 1) // 2
    return (16 * iterations ** 3 + 30 * iterations ** 2 + 26 * iterations + 3) // 3  # elementary math, at first polynomials for all 4th diagonal elements are found then they are added


print(get_diagonal_spiral_sum(10000000000000000000000000000000000000000000000000000000000000000000000000001))
