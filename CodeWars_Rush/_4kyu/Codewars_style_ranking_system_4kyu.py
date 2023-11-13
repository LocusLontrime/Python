class User:
    ranks = [-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]
    ranks_possible = {v: i for i, v in enumerate(ranks)}

    def __init__(self):
        self.rank = -8
        self.progress = 0

    def inc_progress(self, rank):
        # validity check:
        if type(rank) != int or rank < -8 or rank > 8 or rank == 0:
            raise ValueError(f"task's ranges must fits the following values: {self.ranks}")
        # checks user's rank for ability to grow progress:
        if self.rank < 8:
            # re_calcs ranks in a convenient way:
            rank_, self_rank_ = self.ranks_possible[rank], self.ranks_possible[self.rank]
            # estimates progress increase and applies it:
            if rank_ == self_rank_:
                self.progress += 3
            elif rank_ == self_rank_ - 1:
                self.progress += 1
            elif rank_ > self_rank_:
                d = rank_ - self_rank_
                self.progress += 10 * d * d
            # processes progress and user's rank:
            if self.progress >= 100:
                delta_ranks = self.progress // 100
                new_user_rank = self_rank_ + delta_ranks
                if new_user_rank < len(self.ranks) - 1:
                    self.rank = self.ranks[new_user_rank]
                    self.progress = self.progress - 100 * delta_ranks
                else:
                    self.rank = 8
                    self.progress = 0

    def __str__(self):
        return f'rank: {self.rank}, progress: {self.progress}'


# -8 -8 -4 -1 8 6 6 8 4 8
user = User()
user.inc_progress(-8)
print(f'{user}')
user.inc_progress(-8)
print(f'{user}')
user.inc_progress(-4)
print(f'{user}')
user.inc_progress(-1)
print(f'{user}')
user.inc_progress(8)
print(f'{user}')
user.inc_progress(6)
print(f'{user}')
user.inc_progress(6)
print(f'{user}')
user.inc_progress(8)
print(f'{user}')
user.inc_progress(4)
print(f'{user}')
user.inc_progress(8)
print(f'{user}')

