# accepted on coderun


class Passenger:
    def __init__(self, a: int, seat: str, row: int, pos: int, st: int):
        self.a = a
        self.seat = seat
        self.row = row
        self.pos = pos
        self.st = st
        self.coord = 0
        self.ready_to_sit_down = False
        self.placed = False

    def move(self, busy_rows: list[list], seats_taken: list, postponed_update: list[int]):
        """tries to move forward in order to reach the row needed"""
        scores = {0: 0, 1: 5, 2: 15}
        if busy_rows[self.coord + 1][0] == 0:
            self.coord += 1
            print(f'self.coord: {self.coord}')
        if self.coord != 0:
            busy_rows[self.coord] = [1, self]
        if self.coord == self.row:
            print(f'READY!!!!! sc, sr: {self.coord, self.row}')
            self.ready_to_sit_down = True
            # print(f'........................................................................................................')
            busy_rows[self.coord][0] += self.a + (
                sc_ := scores[s_ := sum([_[0] for i, _ in enumerate(seats_taken[self.coord][self.pos]) if i < self.st])])
            # print(f'SUM_: {s_}, SCORES: {sc_}')
            if busy_rows[self.coord][0] == 0:
                # print(f'PLACED INSTANTLY AT {self.coord, self.pos, self.st}')
                busy_rows[self.coord][1] = f'N'
                self.placed = True
                seats_taken[self.coord][self.pos][self.st][0] = 1
                seats_taken[self.coord][self.pos][self.st][1] = self.seat
        elif self.coord != 0:
            postponed_update.append(self.coord)

    def do(self, busy_rows: list[list], seats_taken: list, postponed_update: list[int]):
        """the passenger acts"""
        # time.sleep(1)
        if self.ready_to_sit_down:
            if busy_rows[self.coord][0] > 0:
                busy_rows[self.coord][0] -= 1
            if busy_rows[self.coord][0] == 0:
                # print(f'PLACED AT {self.coord, self.pos, self.st}')
                busy_rows[self.coord][1] = f'N'
                self.placed = True
                seats_taken[self.coord][self.pos][self.st][0] = 1
                seats_taken[self.coord][self.pos][self.st][1] = self.seat
        else:
            self.move(busy_rows, seats_taken, postponed_update)

    def __str__(self):
        return f'{self.seat}'  # f'[{self.a}]({self.row}, {self.pos}, {self.st})'

    def __repr__(self):
        return str(self)


class Plane:
    MAX_ROW: int

    def __init__(self, n, passengers):
        self.n = n
        self.passengers = passengers
        print(f'_passengers: {self.passengers}')
        self.parse_passengers()
        print(f'passengers_: {self.passengers}')
        # aux pars:
        self.seats_taken = [[[[0, 'N'], [0, 'N'], [0, 'N']], [[0, 'N'], [0, 'N'], [0, 'N']]] for _ in
                            range(self.MAX_ROW + 1)]  # left and right rows from corridor to illuminator
        self.busy_rows = [[0, f"N"] for _ in range(self.MAX_ROW + 1)]
        self.steps = 0

    def parse_passengers(self):
        self.passengers = [Passenger(int(a), seat, *parse_coords(seat)) for a, seat in self.passengers]
        self.MAX_ROW = max(p.row for p in self.passengers)

    def step(self):
        index_ = 0
        print(f'step: {self.steps}')
        postponed_update = []
        while index_ < len(self.passengers):
            print(f'p_: {self.passengers[index_]}')
            # print(f'busy rows: {self.busy_rows}')
            # print(f'seats taken: {self.seats_taken}')
            self.passengers[index_].do(self.busy_rows, self.seats_taken, postponed_update)
            if (p_ := self.passengers[index_]).placed:
                # print(f'passenger {p_} deleted')
                del self.passengers[index_]
            else:
                index_ += 1
        self.print()
        for ind_ in postponed_update:
            self.busy_rows[ind_][0] -= 1
            self.busy_rows[ind_][1] = f'N'
        self.steps += 1

        if not self.passengers:
            return False
        return True

    def __str__(self):
        d = f'{"-" * (self.MAX_ROW * 4 + 1)}'
        _s = f'{d}\n'
        _s += "\n".join([" | ".join([str(self.seats_taken[row][1][i][1]) for row in range(self.MAX_ROW + 1)]) for i in range(2, -1, -1)])
        s = "  ".join([str(self.busy_rows[_][1]) for _ in range(self.MAX_ROW + 1)])
        s_ = "\n".join([" | ".join([str(self.seats_taken[row][0][i][1]) for row in range(self.MAX_ROW + 1)]) for i in range(2 + 1)])
        s_ += f'\n{d}\n'
        s_ += "   ".join([str(_) for _ in range(self.MAX_ROW + 1)])
        return f'{_s}\n{s}\n{s_}'

    def __repr__(self):
        return str(self)

    def print(self):                                                                  # 36.6 98
        print(f'{self}')


def onboard():
    plane = Plane(*get_pars())
    while plane.step():
        ...
    print(f'steps: {plane.steps - 1}')


def parse_coords(seat: str):
    index_ = 0
    while seat[index_].isdigit():
        index_ += 1
    rn = int(seat[: index_])
    k = ord(seat[index_])
    pos, st = (0, 67 - k) if k < 68 else (1, k - 68)
    return rn, pos, st


def get_pars():
    n = int(input())
    passengers = [input().split() for _ in range(n)]
    return n, passengers


onboard()

# print(f'{ord("A")}')
# print(f'{ord("D")}')
# print(f'res: {parse_coords(f"29A")}')
# print(f'res: {parse_coords(f"28E")}')
# print(f'res: {parse_coords(f"29F")}')
# arr_ = [1, 2, 3, 4, 5]
# ind_ = 0
# while ind_ < len(arr_):
#     print(f'el_: {(el_ := arr_[ind_])}')
#     if el_ % 2 != 0:
#         del arr_[ind_]
#     else:
#         ind_ += 1
# print(f'arr_: {arr_}')
