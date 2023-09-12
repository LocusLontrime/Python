# accepted on codewars.com
import heapq as hq
import math

walk = ((-1, 0), (0, 1), (1, 0), (0, -1))


class Height:
    def __init__(self, j: int, i: int, height: int):
        self.j, self.i = j, i
        self.val = height

    def __lt__(self, other):
        return self.val < other.val


def volume(heightmap) -> int:
    # sizes:
    jm, im = len(heightmap), len(heightmap[0])
    # adding border heights to the min_heap:
    heights = []
    visited = [[False for _ in range(im)] for _ in range(jm)]
    hq.heapify(heights)
    for j in range(0, jm):
        hq.heappush(heights, Height(j, 0, heightmap[j][0]))
        hq.heappush(heights, Height(j, im - 1, heightmap[j][im - 1]))
        visited[j][0] = True
        visited[j][im - 1] = True
    for i in range(1, im - 1):
        hq.heappush(heights, Height(0, i, heightmap[0][i]))
        hq.heappush(heights, Height(jm - 1, i, heightmap[jm - 1][i]))
        visited[0][i] = True
        visited[jm - 1][i] = True
    # main cycle:
    max_height_val = - math.inf
    water_drops = 0
    while heights:
        # current min height in the heap:
        height_ = hq.heappop(heights)
        max_height_val = max(max_height_val, height_.val)
        # let us visit the nearest neighs:
        for dj, di in walk:
            j_, i_ = height_.j + dj, height_.i + di
            if validate(j_, i_, jm, im):
                if not visited[j_][i_]:
                    neigh_ = Height(j_, i_, heightmap[j_][i_])
                    visited[j_][i_] = True
                    if neigh_.val < max_height_val:
                        water_drops += max_height_val - neigh_.val
                    hq.heappush(heights, neigh_)
    return water_drops


def validate(j: int, i: int, jm: int, im: int) -> bool:
    return 0 <= j < jm and 0 <= i < im


water_matrix = [
    [8, 8, 8, 8, 6, 6, 6, 6],
    [8, 0, 0, 8, 6, 0, 0, 6],
    [8, 0, 0, 8, 6, 0, 0, 6],
    [8, 8, 8, 8, 6, 6, 6, 0]
]

print(f'water drops: {volume(water_matrix)}')


