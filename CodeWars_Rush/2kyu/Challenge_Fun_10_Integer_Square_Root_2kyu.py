import math
import time
from time import sleep

rec_counter: int
SLEEP_FLAG = False


class HugeInt:
    def __init__(self, number):
        if type(number) is list:
            self.number = number.copy()
        elif type(number) is str:
            self.number = []
            for char in number:
                self.number.append(int(char))
        else:
            self.number = []

    def sqrt(self):
        global rec_counter
        rec_counter = 0
        if (length := len(self.number)) == 1:
            return HugeInt([int(math.sqrt(self.number[0]))])
        elif length >= 4:
            borders = self.get_borders()
            return self.bin_search(borders[0], borders[1])
        else:
            return self.bin_search(HugeInt([0]), self)

    def bin_search(self, left_border: 'HugeInt', right_border: 'HugeInt'):
        global rec_counter
        rec_counter += 1
        pivot_element = left_border + right_border
        pivot_element.divide_by_2()
        # print(f'{rec_counter}-th current pivot element equals: {pivot_element} ')
        square = pivot_element * pivot_element
        next_square = square + pivot_element * HugeInt([2]) + HugeInt([1])
        print(f'{rec_counter}-th current pivot element equals: {pivot_element} ')
        if SLEEP_FLAG:
            sleep(0.1)
        if square == self or (square < self < next_square):
            return pivot_element
        elif square > self:
            print(f'-->> left interval')
            return self.bin_search(left_border, pivot_element)
        else:
            print(f'-->> right interval')
            return self.bin_search(pivot_element, right_border)

    def get_borders(self):
        if (length := len(self)) % 2 == 0:
            left_array = [0 for _ in range(length // 2)]
            right_array = [0 for _ in range(length // 2 + 1)]
            left_array[0] = 3
            left_array[1] = 1
            right_array[0] = 1
        else:
            left_array = [0 for _ in range(length // 2 + 1)]
            right_array = [0 for _ in range(length // 2 + 1)]
            left_array[0] = 1
            right_array[0] = 3
            right_array[1] = 2
        left_brd = HugeInt(left_array)
        right_brd = HugeInt(right_array)
        return [left_brd, right_brd]

    def __add__(self, other):
        summa = [0 for _ in range(max(len(self), len(other)) + 1)]
        temporal = 0
        for i in range(len(summa)):
            curr_sum = (self.number[len(self) - i - 1] if len(self) - i - 1 >= 0 else 0) +\
                       (other.number[len(other) - i - 1] if len(other) - i - 1 >= 0 else 0) + temporal
            if curr_sum <= 9:
                summa[len(summa) - i - 1] = curr_sum
                temporal = 0
            else:
                summa[len(summa) - i - 1] = curr_sum % 10
                temporal = 1
        res = HugeInt(summa)
        res.remove_leading_zero()
        return res

    def __mul__(self, other):
        multiplication = HugeInt([0 for _ in range(len(self) + len(other))])
        left = HugeInt(self.number)
        right = HugeInt(other.number)
        while right != HugeInt([0]):
            if right.is_divisible_by_2():
                left += left
                right.divide_by_2()
            else:
                right.subtract_one()
                multiplication += left
        multiplication.remove_leading_zero()
        return multiplication

    def is_divisible_by_2(self):
        return self.number[len(self.number) - 1] % 2 == 0

    def subtract_one(self):
        if len(self) == 1:
            self.number[0] -= 1
        else:
            for i in range(len(self) - 1, -1, -1):
                if self.number[i] != 0:
                    self.number[i] -= 1
                    break
                else:
                    self.number[i] = 9
        self.remove_leading_zero()

    def divide_by_2(self):
        cf = 0
        i = 0
        while i < len(self):
            t = self.number[i] + cf * 10
            self.number[i] = t // 2
            cf = t % 2
            i += 1
        self.remove_leading_zero()

    def remove_leading_zero(self):
        if len(self) > 1 and self.number[0] == 0:
            zeroes_length = 0
            for _ in range(len(self)):
                if self.number[_] == 0:
                    zeroes_length += 1
                else:
                    break
            self.number = self.number[zeroes_length:]

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self.number[i] != other.number[i]:
                return False
        return True

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if len(self) < len(other):
            return True
        elif len(self) > len(other):
            return False
        else:
            for i in range(len(self)):
                if self.number[i] < other.number[i]:
                    return True
                elif self.number[i] == other.number[i]:
                    continue
                else:
                    return False

    def __gt__(self, other):
        return not self < other

    def __len__(self):
        return len(self.number)

    def __int__(self):
        curr_sum = 0
        for i in range(len(self)):
            curr_sum *= 10
            curr_sum += self.number[i]
        return curr_sum

    def __str__(self):
        s = ''
        for digit in self.number:
            s += str(digit)
        return s

    def __repr__(self):
        return str(self)

    def print(self):
        print(f'{str(self)}')


# h_n = HugeInt([1, 2, 3, 4, 5, 6, 7, 8, 9])
# print(f'h_n: {h_n}')
new_huge_int = HugeInt('2323232832321543534534534534345809885675655680940084098098098098080909234324324324324309879963365')
print(f'number length: {len(new_huge_int)}')
start = time.time_ns()
# sqrt = new_huge_int.sqrt()
result = new_huge_int * new_huge_int
finish = time.time_ns()
# print(f'sqrt of {new_huge_int} : {sqrt}')
print(f'res: {result}')
print(f'time elapsed: {(finish - start) // 10 ** 6} milliseconds')

# print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][1:])

huge_int_1 = HugeInt([1, 2, 3])
huge_int_2 = HugeInt([3, 6, 9])
huge_int_3 = HugeInt([1, 0, 0])

# print(f'sum: {huge_int_1 + huge_int_2}')
# huge_int_1.divide_by_2()
# print(f'division by two: {huge_int_1}')
# huge_int_3.subtract_one()
# print(f'one subtraction: {huge_int_3}')
# print(f'mult: {huge_int_1 * huge_int_3}, res: {61 * 99}, 36, 98')


huge_int_with_zeroes = HugeInt([0, 0, 0, 1, 0, 9])
# huge_int_with_zeroes.remove_leading_zero()
# print(f'huge_int_with_zeroes after zeroes elimination: {huge_int_with_zeroes}')


# print(huge_int_1 < huge_int_2)
# print(huge_int_3 > huge_int_2)
# print(HugeInt([1, 1, 0, 9, 2]) < HugeInt([1, 1, 1, 9, 2]))





