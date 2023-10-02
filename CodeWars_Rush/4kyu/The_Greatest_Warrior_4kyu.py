# accepted on codewars.com
class Warrior:
    RANKS = ["Pushover", "Novice", "Fighter", "Warrior", "Veteran", "Sage", "Elite", "Conqueror", "Champion", "Master",
             "Greatest"]
    MAX_EXP = 10_000
    EXP_PER_LVL = 100

    def __init__(self):
        self.experience = 100
        self.level = 1
        self.rank = self.RANKS[0]
        self.achievements = []

    def battle(self, enemy_lvl: int) -> str:
        if not (1 <= enemy_lvl <= 100):
            return "Invalid level"
        lvl_delta = self.level - enemy_lvl
        if lvl_delta >= 2:
            exp = 0
            res = f"Easy fight"
        elif lvl_delta == 1:
            exp = 5
            res = f"A good fight"
        elif lvl_delta == 0:
            exp = 10
            res = f"A good fight"
        elif enemy_lvl // 10 == self.level // 10 or abs(lvl_delta) < 5:
            exp = 20 * lvl_delta ** 2
            res = f"An intense fight"
        else:
            exp = 0
            res = f"You've been defeated"
        self._process_exp(exp)
        return res

    def training(self, args: list) -> str:
        achievement, exp, lvl_req = args
        if self.level >= lvl_req:
            self._process_exp(exp)
            self.achievements.append(achievement)
            return achievement
        return "Not strong enough"

    def _process_exp(self, exp: int):
        if exp > 0:
            if self.experience < self.MAX_EXP:
                self.experience = (self.experience + exp) if self.experience + exp <= self.MAX_EXP else self.MAX_EXP
                self.level = self.experience // self.EXP_PER_LVL
                self.rank = self.RANKS[self.level // 10]


bruce_lee = Warrior()
print(f'bruce_lee.level: {bruce_lee.level}')         # => 1
print(f'bruce_lee.experience: {bruce_lee.experience}')    # => 100
print(f'bruce_lee.rank: {bruce_lee.rank}')         # => "Pushover"
print(f'bruce_lee.achievements: {bruce_lee.achievements}')  # => []
print(f'training res: {bruce_lee.training(["Defeated Chuck Norris", 9000, 1])}')  # => "Defeated Chuck Norris"
print(f'bruce_lee.experience: {bruce_lee.experience}')    # => 9100
print(f'bruce_lee.level: {bruce_lee.level}')         # => 91
print(f'bruce_lee.rank: {bruce_lee.rank}')         # => "Master"
bruce_lee.battle(90)    # => "A good fight"
print(f'bruce_lee.experience: {bruce_lee.experience}')    # => 9105
print(f'bruce_lee.achievements: {bruce_lee.achievements}')  # => ["Defeated Chuck Norris"]
print(f'training res: {bruce_lee.training(["Boxing with Rambo", 5000, 89])}')
print(f'bruce_lee.experience: {bruce_lee.experience}')
print(f'bruce_lee.level: {bruce_lee.level}')
print(f'bruce_lee.rank: {bruce_lee.rank}')
print(f'bruce_lee.achievements: {bruce_lee.achievements}')





















print(f'res: {9 // 10}')


























