class Carrier:
    def __init__(self, id_: int, card_number: int):
        self.__id = id_
        self.__card_number = card_number
        self.__zones = []  # must be initialized somehow

    def get_id(self) -> int:
        return self.__id

    def get_card_number(self) -> int:
        return self.__card_number


