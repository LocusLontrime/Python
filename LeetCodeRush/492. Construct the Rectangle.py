import math


# area = 96

def process_web_page(area: int) -> tuple[int, int]:  # -> L, W

    difference = area
    l, w = -1, -1

    for i in range(1, int(math.sqrt(area) + 1)):
        print(f'{i = }')
        if area % i == 0:
            print(f'i, area//i: {i, area // i}')
            if abs(i - area // i) < difference:
                l, w = area // i, i

    return l, w


area_ = 1024
print(f'L, W of area = {area_}: {process_web_page(area_)}')
