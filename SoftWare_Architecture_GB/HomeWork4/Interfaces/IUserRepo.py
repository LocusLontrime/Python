from abc import ABC, abstractmethod
from AmberCode.SoftWare_Architecture_GB.HomeWork4.Models.User import User


class IUserRepo(ABC):
    @abstractmethod
    def create(self, user_name, password_hash, card_number) -> int:
        ...

    @abstractmethod
    def read(self, user_name) -> User:
        ...

    @abstractmethod
    def read_all(self) -> list[User]:
        ...

    @abstractmethod
    def update(self, client: User) -> bool:
        ...

    @abstractmethod
    def delete(self, client: User) -> bool:
        ...

