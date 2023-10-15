# accepted on codewars.com
def maximize_points(team1: list[int], team2: list[int]) -> int:
    team1 = sorted(team1, key=lambda x: -x)
    team2 = sorted(list(enumerate(team2)), key=lambda x: -x[1])

    points = 0
    i1, i2 = 0, 0
    while i2 < len(team2):
        if team2[i2][1] >= team1[i1]:
            i2 += 1
        else:
            points += 1
            i1, i2 = i1 + 1, i2 + 1

    return points
