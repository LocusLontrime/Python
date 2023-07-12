# accepted on coderun
import sys


def jewelry_stone():
    jewelry = input()
    stones = input()
    print(sum(1 for _ in stones if _ in jewelry))


def main():
    jewelry_stone()

