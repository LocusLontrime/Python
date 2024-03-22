# accepted on codewars.com

def bump_counter(ants):
    collisions, saved, d = ['' for _ in range(len(ants))], 0, {('L', 'R'): -1, ('R', 'L'): 1}
    for i, x in enumerate(zip(ants, 'L' * (rc := ants.count('L')) + 'R' * (len(ants) - rc))):
        cc = 2 * saved + d.get(x, 0)
        collisions[i], saved = f'{cc}', cc - saved
    return ' '.join(collisions)


ants_ = "RRLRL"

print(f'res: {bump_counter(ants_)}')
