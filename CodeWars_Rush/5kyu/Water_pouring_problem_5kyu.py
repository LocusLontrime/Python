import math
import sys
import threading
sys.setrecursionlimit(500000)
# increase the stack size

water_memoized: set[tuple[int, int]]
flag = True
result = []
counter = 0


class Wpp:

    def __init__(self, a, b, n):
        self.a = a
        self.b = b
        self.n = n

    def __call__(self):
        global water_memoized, result
        water_memoized = set()

        if self.n < 0 or self.n > self.b:
            return result

        def rec_seeker(curr_a, curr_b, path_done: list[tuple[int, int]]):
            global flag, result, counter
            counter += 1
            print(f'counter: {counter}, length of memo table: {len(water_memoized)}')
            if self.n in [curr_a, curr_b]:
                flag = False
                print(f'Final water volumes: {curr_a, curr_b}')
                print(f'memo table: {water_memoized}')
                result = path_done + [(curr_a, curr_b)]
            elif (curr_a, curr_b) not in water_memoized and flag:
                new_path_done = [] + path_done
                new_path_done.append((curr_a, curr_b))
                print(f'counter: {counter}, curr_a, curr_b: {curr_a, curr_b}')
                # print(f'water_memoized: {water_memoized}')
                water_memoized.add((curr_a, curr_b))
                # step 1:
                rec_seeker(0, curr_b, new_path_done)
                rec_seeker(curr_a, 0, new_path_done)
                # step 2:
                rec_seeker(self.a, curr_b, new_path_done)
                rec_seeker(curr_a, self.b, new_path_done)
                # step 3 & 4:
                # 1: a -->> b:

                if self.b - curr_b < curr_a:
                    rec_seeker(curr_a - (self.b - curr_b), self.b, new_path_done)
                else:
                    rec_seeker(0, curr_b + curr_a, new_path_done)
                # 2: b -->> a:
                if self.a - curr_a < curr_b:
                    rec_seeker(self.a, curr_b - (self.a - curr_a), new_path_done)
                else:
                    rec_seeker(curr_a + curr_b, 0, new_path_done)

        rec_seeker(0, 0, [])

        res = result[1:]

        print(f'res: {res}')

        return res


threading.stack_size(0x8000000)
t = threading.Thread(target=Wpp(11357, 13560, 11851))
t.start()
t.join()

print(f'GCD: {math.gcd(86350, 99999)}')


# print(f'path done: {wpp(33, 51, 45000)}')
# print(f'path done: {Wpp.wpp(86350, 99999, 52607)}')
# print(f'water_memoized_len: {len(water_memoized)}')


# table = {(0, 0)}
# table.add((98, 989))
# table.add((0, 0))
#
# print(table)





