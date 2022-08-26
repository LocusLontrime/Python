import sys


def knights_tour(start, size):
    MOVES = [(-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2)]

    def genNeighs(pos):
        return ((pos[0] + dx, pos[1] + dy) for dx, dy in MOVES if (pos[0] + dx, pos[1] + dy) in Warnsdorf_DP)

    def travel(pos):
        neighs = sorted((Warnsdorf_DP[n], n) for n in genNeighs(pos))
        for nSubNeighs, neigh in neighs:
            del Warnsdorf_DP[neigh]
            path.append(neigh)
            subNeighs = list(genNeighs(neigh))
            for n in subNeighs: Warnsdorf_DP[n] -= 1
            travel(neigh)
            if not Warnsdorf_DP:
                break
            else:
                for n in subNeighs: Warnsdorf_DP[n] += 1
                Warnsdorf_DP[path.pop()] = nSubNeighs

    path, Warnsdorf_DP = [start], {(x, y): 0 for x in range(size) for y in range(size) if (x, y) != start}
    for pos in Warnsdorf_DP: Warnsdorf_DP[pos] = sum(1 for _ in genNeighs(pos))
    travel(start)

    return path


sys.setrecursionlimit(1000000)

print(knights_tour((0, 0), 43))
