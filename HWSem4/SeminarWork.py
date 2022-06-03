# Seminar work

# Получить рандомный полином степени n

from HWSem4.Polynomial import Polynomial  # 36 366 98 989


p1 = Polynomial.get_random_pol(100, 100)
p1.print()

with open("Pol_random.txt", "w") as file:
    file.write(str(p1))





