import os
import sys


sys.setrecursionlimit(100_000)


def flood(curr_path: str, name: str = 'TopSecret', depth: int = 1, depth_: int = 1, multiplier: int = 2, ind: int = 1):
    if depth_ <= depth:

        curr_path_ = f'{curr_path}/{name}[D{depth_}_N{ind}]'
        os.mkdir(curr_path_)

        for i, _ in enumerate(range(multiplier), 1):
            flood(curr_path_, name, depth, depth_ + 1, multiplier, i)


# flood('d:/', depth=16)
# flood('d:/', depth=36_665, multiplier=1)

# os.mkdir("hello")
# os.mkdir("c://somedir")
