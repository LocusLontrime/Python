# accepted on codewars.com
from collections import Counter


def score(dice: list[int]):
    scores_dicts = {1: 1000, 6: 600, 5: 500, 4: 400, 3: 300, 2: 200}, {1: 100, 5: 50}
    counter = Counter(dice)
    scores = 0
    for j, scores_dict in enumerate(scores_dicts):
        for i, v in scores_dict.items():
            while counter[i] >= (k := 3 - 2 * j):
                counter[i] -= k
                scores += v
    return scores


dice_ = [1, 1, 1, 3, 1]
score(dice_)



