def escape(grid):
    print(f'sizes: {len(grid), len(grid[0])}')
    return []


grid8 = (
    '.c###a.#.b..',
    '#B###..@...#',
    '....##D#.###',
    '.......#A#$.',
    '########.#..',
    '..d......C..'
)

print(f'{escape(grid8)}')
