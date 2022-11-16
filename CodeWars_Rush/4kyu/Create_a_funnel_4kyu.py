# accepted on codewars.com
class Funnel(object):
    # Coding and coding...

    def __init__(self, size=5):
        # main data structure
        self.funnel_data = [  # can be upgraded with comprehension
            [' '],
            [' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ']]

    def get_weight(self, coordinates: tuple[int, int]) -> int:  # (j, i) -> coordinates' tuple
        aggregated_weight = 0
        for j in range(coordinates[0] + 1, len(self.funnel_data)):
            for i in range(coordinates[1], coordinates[1] + coordinates[0] + 1 - j + 2):
                if self.funnel_data[j][i] != ' ':
                    aggregated_weight += 1
        return aggregated_weight

    def fill(self, *args) -> None:
        for arg in args:
            flag_of_changing = False
            for j in range(len(self.funnel_data)):
                if flag_of_changing:
                    break
                for i in range(len(self.funnel_data[j])):
                    if self.funnel_data[j][i] == ' ':
                        self.funnel_data[j][i] = arg
                        flag_of_changing = True
                        break

            if not flag_of_changing:
                print(f'Arg: {arg} cannot be placed, the funnel is full')
                break

    # recursive drip
    def drip(self):
        dripped_value = self.funnel_data[0][0]

        if dripped_value == ' ':
            return None

        def rec_seeker(j: int, i: int):
            if j < len(self.funnel_data) - 1:
                if self.funnel_data[j + 1][i] == self.funnel_data[j + 1][i + 1] == ' ':
                    self.funnel_data[j][i] = ' '
                    return
                elif self.funnel_data[j + 1][i] == ' ':
                    self.funnel_data[j][i] = self.funnel_data[j + 1][i + 1]
                    rec_seeker(j + 1, i + 1)
                elif self.funnel_data[j + 1][i + 1] == ' ':
                    self.funnel_data[j][i] = self.funnel_data[j + 1][i]
                    rec_seeker(j + 1, i)
                else:
                    left_weight = self.get_weight((j + 1, i))
                    right_weight = self.get_weight((j + 1, i + 1))

                    if left_weight >= right_weight:
                        self.funnel_data[j][i] = self.funnel_data[j + 1][i]
                        rec_seeker(j + 1, i)
                    else:
                        self.funnel_data[j][i] = self.funnel_data[j + 1][i + 1]
                        rec_seeker(j + 1, i + 1)
            else:
                self.funnel_data[j][i] = ' '

        rec_seeker(0, 0)
        return dripped_value

    def __str__(self):
        k = self.funnel_data
        # can be easily rewritten with for
        s = f"\\{k[4][0]} {k[4][1]} {k[4][2]} {k[4][3]} {k[4][4]}/\n \\{k[3][0]} {k[3][1]} {k[3][2]} {k[3][3]}/\n  \\{k[2][0]} {k[2][1]} {k[2][2]}/\n   \\{k[1][0]} {k[1][1]}/\n    \\{k[0][0]}/"
        return s


fun = ("\\         /\n" +
       " \\  7   9/\n" +
       "  \\4 5 6/\n" +
       "   \\2 3/\n" +
       "    \\1/")

print(fun)
print(366)

new_funnel = Funnel()
print(new_funnel)

new_funnel.fill(4, 0, 0)
print(new_funnel)

new_funnel.fill(3, 6, 6)
new_funnel.fill(3, 9, 4)
print(new_funnel)

# new_funnel.fill(1, 2, 3, 4, 5)
# print(new_funnel)
#
# new_funnel.drip()
# print(new_funnel)
#
# new_funnel.fill(6, 7, 8, 9)
# print(new_funnel)
#
# new_funnel.fill(10, 11, 12, 13, 14, 15, 16, 17, 18)
# print(new_funnel)
#
# new_funnel.drip()
# print(new_funnel)


