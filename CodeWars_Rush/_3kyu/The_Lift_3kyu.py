# accepted on codewars.com
from collections import deque as deq


class Dinglemouse(object):
    dirs = (1, -1)

    def __init__(self, queues: tuple, capacity: int):
        self.queues, self.points_of_int, self.counter = self.init_queues(queues)
        self.cap = capacity
        self.floor = 0  # starting floor is always 0
        self.passengers_in = []  # passengers in the lift at the time being...
        self.dir_ind = 0  # at the very beginning the lift is going up...

    @property
    def pass_rem(self):
        """passengers remained in the lift at the moment"""
        return self.cap - len(self.passengers_in)

    @property
    def queue(self):
        """queue of passengers waiting on the current floor and heading the same direction the lift is"""
        return self.queues[self.floor][self.dir_ind]

    def move(self, floor: int):
        """changes the floor the lift on"""
        self.floor = floor

    def next_stop(self) -> bool:
        """finds the next possible stop in the direction the lift goes and makes the lift move towards it"""
        # a. passengers heading to the same dir:
        if self.dir_ind == 0:
            if higher_fl := [x for x in self.points_of_int[self.dir_ind] | set(self.passengers_in) if x > self.floor]:
                self.move(min(higher_fl))
                return True
        else:
            if lower_fl := [x for x in self.points_of_int[self.dir_ind] | set(self.passengers_in) if x < self.floor]:
                self.move(max(lower_fl))
                return True
        # b. border passengers right before the dir change:
        if self.dir_ind == 0 and self.points_of_int[1] and (highest_down := max(self.points_of_int[1])) > self.floor:
            self.move(highest_down)
            return True
        if self.dir_ind == 1 and self.points_of_int[0] and (lowest_up := min(self.points_of_int[0])) < self.floor:
            self.move(lowest_up)
            return True
        # c. if nothing been changed:
        return False

    def change_dir(self) -> None:
        """changes the direction the lift goes"""
        self.dir_ind = (self.dir_ind + 1) % len(self.dirs)

    def get_on(self) -> None:
        """embark passengers"""
        ql = len(self.queue)
        while self.pass_rem > 0 and self.queue:
            passenger_ = self.queue.popleft()
            self.passengers_in.append(passenger_)
        if not self.queue and ql:
            self.points_of_int[self.dir_ind].remove(self.floor)

    def get_off(self) -> None:
        """disembark passengers"""
        pq = len(self.passengers_in)
        self.passengers_in = [p for p in self.passengers_in if p != self.floor]
        self.counter -= pq - len(self.passengers_in)

    @staticmethod
    def init_queues(queues: tuple) -> tuple[list[list[deq[int]], deq[int]], tuple[set[int], set[int]], int]:
        """initialization shadow mechanisms"""
        counter = sum([len(q) for q in queues])
        qs = [[deq([x for x in q if x > i]), deq([x for x in q if x < i])] for i, q in enumerate(queues)]
        poi = {i for i, q in enumerate(qs) if q[0]}, {i for i, q in enumerate(qs) if q[1]}
        return qs, poi, counter

    def the_lift(self) -> list[int]:
        # cycling while there are any passengers in the lift:
        floors_visited = []
        while self.counter:
            # passengers gets on and off...
            self.get_off()
            self.get_on()
            # lift moving...
            if self.next_stop():
                # moving in the direction chosen:
                floors_visited.append(self.floor)
            else:
                # dir change:
                self.change_dir()
        return [0] + floors_visited + ([0] if floors_visited and floors_visited[-1] else [])


queues_, cap_ = ((4, 5, 6), (5,), (1, 3), (1, 6, 7), (2, 2, 2, 7), (7, 7), (1, 2, 3, 4, 5, 5, 7), (0, 0, 1, 6)), 7
queues_1, cap_1 = ((), (), (5, 5, 5), (), (), (), ()), 5
queues_2, cap_2 = ((), (), (1, 1), (), (), (), ()), 5
queues_3, cap_3 = ((), (3,), (4,), (), (5,), (), ()), 5
queues_4, cap_4 = ((), (0,), (), (), (2,), (3,), ()), 5
# lift = Dinglemouse(queues_2, cap_2)
# lift = Dinglemouse(queues_3, cap_3)
lift = Dinglemouse(queues_4, cap_4)
print(f'floors visited: {lift.the_lift()}')
print(f'counter: {lift.counter}')
