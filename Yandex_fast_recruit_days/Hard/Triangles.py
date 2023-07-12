# accepted on coderun
import sys
import math
from collections import defaultdict as d


def isosceles_triangles():
    n, triangles = get_pars()
    print(f'n, triangles: {n, triangles}')
    counter = 0
    equilateral_triangles: set[tuple[tuple[int, ...], ...]] = set()
    for j in range(n):
        sides = d(list[tuple[int, ...]])
        print(f'J: {j}..................')
        for i in range(n):
            print(f'i: {i}')
            if j != i:
                distance_ = euclidian_distance(triangles[j], triangles[i])
                print(f'distance_: {distance_}')
                sides[distance_].append(triangles[i])
        print(f'{triangles[j]}: {sides}')
        for distance_ in sides.keys():
            for j_ in range(length := len(sides[distance_])):
                for i_ in range(j_ + 1, length):
                    if euclidian_distance(sides[distance_][j_], sides[distance_][i_]) == distance_:
                        t = sorted([triangles[j], triangles[j_], triangles[i_]], key=lambda x: (x[0], x[1]))
                        equilateral_triangles.add(tuple(t))
            length = len(sides[distance_])
            counter += length * (length - 1) // 2
    counter -= 2 * len(equilateral_triangles)
    print(f'{counter}')


def get_pars() -> tuple[int, list[tuple[int, ...]]]:
    return (n := int(input())), [tuple(int(_) for _ in input().split(' ') if _.isdigit() or _[0] == '-' and _[1:].isdigit()) for _ in range(n)]


def euclidian_distance(p1: tuple[int, ...], p2: tuple[int, ...]) -> float:
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


isosceles_triangles()



