def experience():  # runtime: O(n^2) in the worst case and O(n) in the best one, but in common something between O(n) and O(n^2):
    queries, n = parse()
    colleagues: dict[str, list] = {}
    team_exp = 0
    curr_team = set()
    max_exp_name, max_exp = None, 0
    for i, [s, t] in enumerate(queries):
        flag_ = True  # flag of not removing the max exp teammate (if flag_=True)...
        t = int(t)  # casting time from str to int
        # growing overall team's experience, O(1) at the every step of for-cycle:
        if i > 0:
            team_exp += (t - int(queries[i - 1][1])) * len(curr_team)
        # Ops with teammates:
        if s not in colleagues:
            # first meet with teammate s (first join):
            colleagues[s] = [0, t, True]
            curr_team.add(s)
        else:
            _e, _t, flag = colleagues[s]
            if flag:
                # teammate leaves the team:
                colleagues[s] = [_e + t - _t, 0, False]
                curr_team.remove(s)
                team_exp -= colleagues[s][0]
                # if the teammate to be removed has the max experience in the team -> we must calculate the new max exp teammate...
                if s == max_exp_name:
                    # most intense in terms of performance part, O(n) at the every step of for-cycle:
                    max_exp_name = max(curr_team, key=lambda x: (-(colleagues[x][0] + t - colleagues[x][1]), x))
                    max_exp = colleagues[max_exp_name][0]
                    flag_ = False
            else:
                # teammate joins the team AGAIN:
                colleagues[s] = [_e, t, True]
                curr_team.add(s)
                team_exp += _e
        if max_exp_name is None:
            # if there is no max exp teammate at the moment:
            max_exp_name = s
            max_exp = 0
        else:
            # checks if the new teammate is the max exp one, O(1) at the every step of for-cycle...
            max_exp_curr_moment, candidate = max_exp + t - colleagues[max_exp_name][1], colleagues[s][0]
            if flag_ and (max_exp_curr_moment < candidate or (max_exp_curr_moment == candidate and max_exp_name > s)):
                max_exp_name = s
                max_exp = candidate
        # printing the local answer:
        print(f'{max_exp_name} {team_exp - 2 * (max_exp + (t - colleagues[max_exp_name][1]))}')


def parse():
    n = int(input())
    queries = [input().split(' ') for _ in range(n)]
    return queries, n


if __name__ == '__main__':
    experience()










































