def natural_to_rational(n: int) -> tuple[int, int]:
    return 1, 1


tests: list[int] = [1, 2, 3, 5, 7, 10]

expected: list[tuple[int, int]] = [
    (1, 1), (1, 2), (2, 1), (3, 1), (2, 3), (1, 5)
]

