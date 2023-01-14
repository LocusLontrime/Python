class User:
    def __init__(self, id_: int, user_name: str, hash_password: int, card_number: int):
        self.__id = id_
        self.__user_name = user_name
        self.__hash_password = hash_password
        self.__card_number = card_number

    def __str__(self):
        return f'Client {"{"} id: {self.__id}, user name: {self.__user_name}, card number: {self.__card_number} {"}"}'

    def __eq__(self, other):
        if other is None or type(other) != type(self):
            return False
        else:
            return self.__id == other.__id and self.__user_name == other.__user_name and \
                self.__card_number == other.__card_number and self.__hash_password == other.__hash_password

    def __hash__(self):
        return hash((self.__id, self.__user_name, self.__hash_password, self.__card_number))

    def get_id(self) -> int:
        return self.__id

    def get_user_name(self) -> str:
        return self.__user_name

    def get_hash_password(self) -> int:
        return self.__hash_password

    def get_card_number(self) -> int:
        return self.__card_number

