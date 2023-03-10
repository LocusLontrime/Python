import decimal


class ATM:
    # constants:
    TAKE_OFF_TAX = 1.5 / 100
    REFINANCE_RATE = 3.0 / 100
    LOWER_BOUND, UPPER_BOUND = 30, 600
    TOTAL_LIMIT = 5_000_000
    WEALTH_TAX = 10 / 100
    LCM = 50
    Q = 3  # every Q operation the something happens

    def __init__(self, prec=35):
        # account section:
        self.sum_ = 0
        self.prec = prec
        self.operations_counter = 0
        # bank section:
        self._bank_income = 0
        self.exit_flag = False

    def take_off(self, amount_of_money: int) -> bool:
        ...

    def put(self, amount_of_money: int) -> bool:

        if amount_of_money % ATM.LCM != 0:
            return False
        # operation successful:
        self.operations_counter += 1
        amount = amount_of_money * (1 - ATM.WEALTH_TAX) if self.wealth else amount_of_money
        self.sum_ += amount
        if self.is_divisible_by_q:
            self.sum_ += amount_of_money * ATM.REFINANCE_RATE
        print(f'current sum: {self}')

    @property
    def wealth(self) -> bool:
        return self.sum_ > ATM.TOTAL_LIMIT

    @property
    def is_divisible_by_q(self) -> bool:
        return self.operations_counter % ATM.Q == 0

    def __str__(self):
        return f'account money: {self.sum_}'

    def __repr__(self):
        return str(self)

    def exit(self) -> None:
        self.exit_flag = True
        print(f'Session aborted')


def main():
    atm = ATM(prec=36)
    while not atm.exit_flag:
        command = input(f'Enter your request: ')
        match command:
            case 'take off':
                amount = input(f'Enter amount of money to be taken off: ')
                atm.take_off(int(amount))  # condition
            case 'put':
                amount = input(f'Enter amount of money to be put: ')
                atm.put(int(amount))
            case 'exit':
                atm.exit()
            case _:
                ...


main()


