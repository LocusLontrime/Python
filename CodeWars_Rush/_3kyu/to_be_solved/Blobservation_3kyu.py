class Blobservation:
    def __init__(self, h: int, w: int = None):
        # initial pars:
        self.h = h
        self.w = h if w is None else w
        # core pars:
        self.blobs = []
        self.turn = 0
        # aux pars:
        self.smallest_blob = None
        self.blobs_ = dict()  # ???

    def populate(self, population: list[dict[str, int]]) -> None:
        for new_blob in population:
            if (new_blob['y'], new_blob['x']) in self.blobs_.keys():
                ...
            else:
                ...
        ...

    def move(self, moves: int = 1) -> None:
        for i in range(moves):
            for blob in self.blobs_:
                blob.move()

    def print_state(self) -> list[list[int, int, int]]:
        ...


class Blob:
    def __init__(self, y: int, x: int, size: int):
        self.y = y
        self.x = x
        self.size = size

    def move(self):
        ...

    def fuse(self, other):
        ...

    def consume(self, other):
        ...

    def find_prey(self):
        ...

    def choose_dir(self):
        ...

    def __str__(self):
        ...

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x and self.size == other.size

    def __del__(self):
        ...

