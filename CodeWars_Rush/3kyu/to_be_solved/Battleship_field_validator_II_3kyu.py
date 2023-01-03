def validate_battlefield(battlefield):
    # write your code
    return True


battlefield_x = [
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 0, 1, 1, 1, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

print(validate_battlefield(battlefield_x))



