from datetime import datetime


class Ticket:
    def __init__(self, route_number: int, place: int, price: int, date: datetime, is_valid: bool):
        self.__route_number = route_number
        self.__place = place
        self.__price = price
        self.__date = date
        self.__is_valid = is_valid
        self.__zone_start, self.__zone_stop = None, None

    def __str__(self):
        return f'Ticket Route Number {self.__route_number}, place: {self.__place}, Price: {self.__price} rub.,' \
               f' Date: {self.__date}, {"Free" if self.__is_valid else "Busy"}'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.__date) ^ (self.__route_number + self.__place + self.__price)

    def __eq__(self, other):
        if other is None or type(other) != type(self):
            return False
        else:
            return self.__route_number == other.__route_number and self.__date == other.__date and \
                self.__place == other.__place and self.__price == other.__price and hash(self) == hash(other)

    def get_route_number(self) -> int:
        return self.__route_number

    def get_place(self) -> int:
        return self.__place

    def get_price(self) -> int:
        return self.__price

    def get_date(self) -> datetime:
        return self.__date

    def get_valid(self) -> bool:
        return self.__is_valid

    def set_valid(self, flag: bool) -> None:
        self.__is_valid = flag

    def set_zone_start(self, zone_start: int) -> None:
        self.__zone_start = zone_start

    def set_zone_stop(self, zone_stop: int) -> None:
        self.__zone_stop = zone_stop


