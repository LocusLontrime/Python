from abc import ABC, abstractmethod
from enum import Enum


class ITrainCommands(ABC):

    @abstractmethod
    def train_pets(self, string):
        ...


class Animals(ABC):

    def __init__(self, name, date_fo_birth):
        self.name = name
        self.date_fo_birth = date_fo_birth
        self._list_command = []
        self.type = None


class Pets(Animals, ITrainCommands):

    def __init__(self, name: str, date_fo_birth: str, species: int):
        super().__init__(name, date_fo_birth)
        self.type = AnimalType(species)

    def to_string(self):
        return f'Домашнее животное, вид: {self.type.name}, имя: {self.name}, дата рождения: {self.date_fo_birth}, ' \
               f'подчиняется командам: {self._list_command}'

    def train_pets(self, string):
        self._list_command.append(string)
        print(f'Животное успешно обучено команде: {string}')


class PackAnimals(Animals):

    def __init__(self, name: str, date_fo_birth: str, species: int):
        super().__init__(name, date_fo_birth)
        self.type = AnimalType(species)

    def to_string(self):
        return f'Вьючное животное, вид: {self.type.name}, имя: {self.name}, дата рождения: {self.date_fo_birth}, ' \
               f'подчиняется командам: {self._list_command}'


class ICounterDB(ABC):

    @abstractmethod
    def add_pets_in_db(self, name: str, date_fo_birth: str, species: int):
        ...

    @abstractmethod
    def get_pet(self, animals: int, name: str):
        ...


class AnimalDataBase(ICounterDB):

    def __init__(self):
        self.dict = {
            'CAT': [],
            'DOG': [],
            'HAMSTER': [],
            'HORSE': [],
            'CAMEL': [],
            'DONKEY': []
        }
        self.counter = 0

    def get_pet(self, animals: int, name: str):
        try:
            key = AnimalType(animals).name
        except ValueError:
            print('Таких животных нет')
            return None
        if key in self.dict.keys():
            for pets in self.dict[key]:
                if pets.name == name:
                    return pets
            print('Животного с таким именем не заведено')
            return None

    def get_info(self, animals: int, name: str):
        animal = self.get_pet(animals, name)
        if animal is not None:
            return animal.to_string()

    def add_pets_in_db(self, name: str, date_fo_birth: str, species: int):
        try:
            if 0 < species < 4:
                animals = Pets(name, date_fo_birth, species)
            else:
                animals = PackAnimals(name, date_fo_birth, species)
            if animals.type.name in self.dict.keys():
                self.dict[animals.type.name].append(animals)
                self.counter += 1
            else:
                self.dict[animals.type.name] = []
                self.dict[animals.type.name].append(animals)
                self.counter += 1
            print('Животное успешно добавлено')
        except TypeError:
            print('Необходимые данные введены не полностью или в неправильном виде')


class AnimalType(Enum):
    CAT = 1
    DOG = 2
    HAMSTER = 3
    HORSE = 4
    CAMEL = 5
    DONKEY = 6