# accepted on codewars.com
def surface_area(skyscrapers_: list[list[int]]):
    w = len(skyscrapers_[0])
    skyscrapers_extended = [[0] * (w + 2)] + [[0] + row + [0] for row in skyscrapers_] + [[0] * (w + 2)]
    for row in skyscrapers_extended:
        print(f'skyscrapers_extended: {row}')
    surface_area_ = 0
    for j in range(1, len(skyscrapers_extended)):
        for i in range(1, len(skyscrapers_extended[0])):
            surface_area_ += (2 if (s := skyscrapers_extended[j][i]) > 0 else 0) + abs(s - skyscrapers_extended[j][i - 1]) + abs(
                s - skyscrapers_extended[j - 1][i])
    return surface_area_


skyscrapers = [
    [1, 3, 4],
    [2, 2, 3],
    [1, 2, 4]
]

skyscrapers_x = [
    [2,1],
    [2,0]
]

print(f'surface_area: {surface_area(skyscrapers_x)}')




