# accepted on coderun


class NumberFormat:
    def __init__(self, pattern: str):
        dash_parsing = pattern.split('-')
        self.country_operator = dash_parsing[1][1:]
        index_ = 1
        while dash_parsing[0][index_] != ' ':
            index_ += 1
        self.country_code = dash_parsing[0][1:index_]
        index_ += 2
        temp = index_
        while dash_parsing[0][index_] != ')':
            index_ += 1
        self.operator_code = dash_parsing[0][temp:index_]
        index_ += 2
        self.personal_number = dash_parsing[0][index_:len(dash_parsing[0]) - 1]
        self.pn_nums = ''.join([ch for ch in self.personal_number if ch.isdigit()])
        self.ccl = len(self.country_code)
        self.ocl = len(self.operator_code)
        self.pnl = len(self.pn_nums)

    def __str__(self):
        return f'+{self.country_code} ({self.operator_code}) {self.personal_number} - {self.country_operator}'

    def __repr__(self):
        return str(self)

    def match(self, phone_num: str) -> bool:
        # length match:
        if len(phone_num) != self.ccl + self.ocl + len(self.personal_number):
            return False
        # cc match:
        if phone_num[:self.ccl] != self.country_code:
            return False
        # oc match:
        if phone_num[self.ccl:self.ccl + self.ocl] != self.operator_code:
            return False
        # pn match:
        if phone_num[self.ccl + self.ocl:self.ccl + self.ocl + self.pnl] != self.pn_nums:
            return False
        # matching!
        return True

    def validate_num(self, phone_num: str) -> str:
        return f'+{phone_num[:self.ccl]} ({phone_num[self.ccl: self.ccl + self.ocl]}) {phone_num[self.ccl + self.ocl:]} - {self.country_operator}'


def process_nums():
    n, phones, m, patterns = get_pars()
    for phone_ in phones:
        for pattern_ in patterns:
            if pattern_.match(phone_):
                print(f'{pattern_.validate_num(phone_)}')
                break


def process_num(phone_num: str):
    return ''.join([ch for ch in phone_num if ch.isdigit()])


def get_pars():
    n = int(input())
    phones = [process_num(input()) for _ in range(n)]
    m = int(input())
    patterns = [NumberFormat(input()) for _ in range(m)]
    return n, phones, m, patterns


process_nums()



























