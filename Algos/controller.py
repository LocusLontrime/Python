import model


class Commander:

    def __init__(self):
        self.db = model.AnimalDataBase()

    def add_animal(self, name: str, date_fo_birth: str, species: int):
        self.db.add_pets_in_db(name, date_fo_birth, species)

    def print_list_command(self, species: int, name: str):
        animal = self.db.get_info(animals=species, name=name)
        print(animal)

    def train_pets(self, species: int, name: str, command: str):
        pets = self.db.get_pet(species, name)
        pets.train_pets(command)

