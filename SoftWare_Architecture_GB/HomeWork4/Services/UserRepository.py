from AmberCode.SoftWare_Architecture_GB.HomeWork4.Models.User import User
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Interfaces.IUserRepo import IUserRepo


class UserRepository:
    __client_repository = None

    def __init__(self):
        self.__clients = []
        self.__clients.append(User(1, "Ivan", hash("1111"), 2))
        self.__clients.append(User(2, "Vasiliy", hash("2222"), 3))
        self.__clients.append(User(3, "Fedor", hash("3333"), 4))
        self.__clients.append(User(4, "Grigoriy", hash("4444"), 5))

    @staticmethod
    def get_client_repository():
        if UserRepository.__client_repository is None:
            UserRepository.__client_repository = UserRepository()
        return UserRepository.__client_repository

    def create(self, user_name: str, password_hash: int, card_number: int) -> int:
        id_ = len(self.__clients)
        client = User(id_, user_name, password_hash, card_number)
        for curr_client in self.__clients:
            if curr_client.get_id() == client.get_id():
                raise Exception(f'A client already exists')
        self.__clients.append(client)

        return client.get_id()

    def read(self, info: int or str) -> User:
        if type(info) == int:  # id case
            for client in self.__clients:
                if client.get_id() == info:
                    return client
            raise Exception(f'A client with this ID not found')
        elif type(info) == str:  # username case
            for client in self.__clients:
                if client.get_user_name() == info:
                    return client
            raise Exception(f'A client with this username not found')

    def read_all(self) -> list[User]:
        if not self.__clients:
            raise Exception(f'List of clients is empty')
        return self.__clients

    def update(self, client: User) -> bool:
        for curr_client in self.__clients:
            if curr_client.get_id() == client.get_id():
                self.__clients.remove(curr_client)
                self.__clients.append(client)
                return True
        return False

    def delete(self, client: User) -> bool:
        for curr_client in self.__clients:
            if curr_client == client:
                self.__clients.remove(curr_client)
                return True
        return False



