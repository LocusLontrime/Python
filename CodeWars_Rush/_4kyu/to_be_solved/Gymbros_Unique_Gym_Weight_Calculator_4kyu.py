import re
SIZE = (40 - 2 * 3) // 2
pattern = r'\d+'
MIN_PLATE_WIDTH = 5
BAR_WEIGHT = 0.5
BARS_WEIGHT = 20


def configure_bar(w, ap):
    print(f'len: {len(ap)}, w: {w}')
    print(f'SIZE: {SIZE}')
    weight = w - BARS_WEIGHT
    print(f'weight: {weight}')
    plates = [[], [], []]
    for plate in ap:
        plate_weight = int(re.search(pattern, plate)[0])
        plates[(l_ := len(plate)) - MIN_PLATE_WIDTH].append(plate_weight - BAR_WEIGHT * l_)
    for i, row in enumerate(plates):
        plates[i].sort()
        print(f'{i + MIN_PLATE_WIDTH} hyphens plates: {row} kg...')
    ...


w_, ap_ = (
    254,
    [
        '|78kg|', '|153kg|', '|83kg|',
        '|150kg|', '|151kg|', '|2kg|',
        '|104kg|', '|95kg|', '|156kg|',
        '|153kg|', '|142kg|', '|35kg|',
        '|130kg|', '|74kg|', '|41kg|',
        '|4kg|', '|4kg|'
    ]
)  # ans: "--|74kg||35kg||2kg|--|4kg||41kg||95kg|--"

print(f'conf: {configure_bar(w_, ap_)}')
s = '|999kg|'

# print(f'res: {re.search(pattern, s)[0]}')
# 17 -> 5 + 5 + 5, 5 + 5 + 6, 5 + 5 + 7, 5 + 6 + 6

