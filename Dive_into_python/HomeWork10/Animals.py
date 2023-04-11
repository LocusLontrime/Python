class Animal:
    DIVISOR = 20

    def __init__(self, name: str, age: int, weight: int):
        self.name = name
        self.age = age
        self.weight = weight

    def sound(self):
        print(f'{self.name}!..')

    def __str__(self):
        return f'{self.name, self.age, self.weight}'

    def __repr__(self):
        return str(self)

    def give_birth(self, other: 'Animal'):
        return Animal(f'{self.name}_{other.name}', 0, (self.weight + other.weight) // (2 * Animal.DIVISOR))


class Fish(Animal):
    def __init__(self, name: str, age: int, weight: int, fins_q: int):
        super().__init__(name, age, weight)
        self.fins_q = fins_q
        self.swim()

    def swim(self):
        print(f'{self.name}: I am swimming!..')


class Mammal(Animal):
    def __init__(self, name: str, age: int, weight: int, legs_q: int):
        super().__init__(name, age, weight)
        self.legs_q = legs_q
        self.run()

    def run(self):
        print(f'{self.name}: I am running!..')


class Bird(Animal):
    def __init__(self, name: str, age: int, weight: int, flyable: bool):
        super().__init__(name, age, weight)
        self.flyable = flyable
        self.fly()

    def fly(self):
        if self.flyable:
            print(f'{self.name}: I am flying!..')


class Factory:
    args_ = None

    def __init__(self, *args):
        Factory.args_ = args

    def __new__(cls, *args):
        return args[0](*args[1:])


f = Factory(Bird, 'Ovip Lokos', 10, 10, True)
print(f'f: {f}')






