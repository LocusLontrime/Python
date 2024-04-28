# accepted on codewars.com
walk = ((0, 1), (1, 0), (0, -1), (-1, 0))


def spaghetti_code(plate: list[list[str]]):
    # shows the plate:
    for row in plate:
        print(f'{row=}')

    j_max, i_max = len(plate), len(plate[0])

    # spaghetti counting and visited cells:
    visited = [[False for _ in range(i_max)] for _ in range(j_max)]
    spaghetti = []

    # finds all the separate spaghetti:
    for j in range(j_max):
        for i in range(i_max):
            if not visited[j][i]:
                if plate[j][i].isalpha() and plate[j][i].isupper():
                    sp_symbs, sp_length = sep_spaghetti(j, i, plate, visited, spaghetti, j_max, i_max, set())

                    # spaghetti finished:
                    spaghetti += [(sp_symbs, sp_length)]
                    print(f'{(sp_symbs, sp_length)} has been finished at {j, i}...')

    print(f'{spaghetti=}')

    symb = sorted(spaghetti, key=lambda x: -x[1])[0][0]

    return (symb - {'S'}).pop() if len(symb) > 1 else 'S'


def sep_spaghetti(j: int, i: int, plate: list[list[str]], visited: list[list[bool]], spaghetti: list, j_max: int,
                  i_max: int, sp_symbs: set):
    """tries to find the whole spaghetti from first visited part"""
    # visiting:
    visited[j][i] = True
    # spaghetti symbols processing:
    sp_symbs |= {plate[j][i]}
    # bfs:
    res = 1
    for dj, di in walk:
        if 0 <= (j_ := j + dj) < j_max and 0 <= (i_ := i + di) < i_max:
            if not visited[j_][i_]:
                if plate[j_][i_].isalpha() and plate[j_][i_].isupper():
                    res += sep_spaghetti(j_, i_, plate, visited, spaghetti, j_max, i_max, sp_symbs)[1]

    return sp_symbs, res


plate1 = [  # answer: 'B'
    [*'SSSSSASS____'],
    [*'____________'],
    [*'SSSSSSBSSSS_'],
    [*'____________'],
    [*'SSSSSC______'],
]

plate2 = [  # answer: 'C'
    [*'SSSSSSSSS      '],
    [*'________S__SSS_'],
    [*' S   S  A    S '],
    [*'_S___S__S____S_'],
    [*' B   S       S '],
    [*'_S___SSSSSCSSS_'],
]

plate3 = [
    [*'SH_SSSS_SSSSSSSSSS__'],
    [*'_S_S___AS___________'],
    [*'_SSS_Q_S_SSSS_______'],
    [*'_______S_S__S_______'],
    [*'SSS___SS____C____SS_'],
    [*'S_SSSSS_SSSSS__SS_S_'],
    [*'S_______S______D__SS'],
    [*'SS______S_JS___SS__S'],
    [*'_S_________S____S__S'],
    [*'_S_________S____S__S'],
    [*'S___S______S____SS_S'],
    [*'SS__S_______SSSR_S_S'],
    [*'_ES_SSF_____S____S_G'],
    [*'__S___S______SSSSS_S'],
    [*'__SSS_S_____SS____SS'],
    [*'____S__SSSSSS_____S_'],
    [*'___SS__S__________S_'],
    [*'___S___S__________S_'],
    [*'___S___S__________S_'],
    [*'___S_SSS_________SS_'],
    [*'__SS_____________S_S'],
    [*'____SSS__________S_S'],
    [*'______S__________S_S'],
    [*'__SVSSS__________SSS'],
]

print(f'res: {spaghetti_code(plate3)}')
