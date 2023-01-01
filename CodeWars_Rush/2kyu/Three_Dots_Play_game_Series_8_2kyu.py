def three_dots(game_map):
    pass


s = ["+------------+\n"
     + "|R    *******|\n"
     + "|G    *******|\n"
     + "|Y    *******|\n"
     + "|            |\n"
     + "|           r|\n"
     + "|******     g|\n"
     + "|******     y|\n"
     + "+------------+"]


print(f'game map: ')
for string in s:
    print(f'{string}')

print(f'solution: {three_dots(s)}')

