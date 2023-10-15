# accepted on codewars.com


def build_matches_table(teams: int) -> list[list[(int, int)]]:
    matrix = []
    rounds = teams - 1 if teams % 2 == 0 else teams
    team_nums = [_ for _ in range(1, rounds + 2)]
    for j in range(0, rounds):
        matrix.append([])
        for i in range((teams + 1) // 2):
            if teams + 1 not in [l_ := team_nums[i], r_ := team_nums[-i - 1]]:
                matrix[j].append((l_, r_))
        team_nums.remove(rounds - j + 1)
        team_nums.insert(1, rounds - j + 1)
    return matrix


m = build_matches_table(10)
for row in m:
    print(f'{row}')
