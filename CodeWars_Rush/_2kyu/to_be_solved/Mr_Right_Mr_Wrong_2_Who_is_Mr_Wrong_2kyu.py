import re


class Person:
    def __init__(self, name, place=None, left=None, right=None):
        self.name = name
        self.ind = place
        # neighs
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.name}[{self.ind}]'

    def __repr__(self):
        return str(self)

    def placed(self):
        return self.ind is not None


def find_out_mr_wrong(conversation: list[str]):
    mr_wrong = None
    people, conditions, queue_size = scan_conversation(conversation)
    print(f'people: {people}')
    print(f'conditions: ')
    print(f'queue_size: {queue_size}')
    for condition in conditions:
        print(f'{condition}')
    # the main cycle:
    # for name in people:
    #     print(f'name: {name}')
    visited: dict[str, Person] = {}
    indexed: dict[int, Person] = {}
    for condition in conditions:
        a, b = condition
        # if a != name:
        # TODO: check for the possibility of insertion of a non-indexed nodes chain to the queue formed...
        if isinstance(a, str) and isinstance(b, str):
            if a not in visited.keys():
                visited[a] = Person(a)
            if b not in visited.keys():
                visited[b] = Person(b)
            connect(visited[b], visited[a])
            if visited[a].placed():
                l_pass(visited[a], indexed)
            elif visited[b].placed():
                r_pass(visited[b], indexed)
        else:  # it means -> a is str and b is int:
            b = int(b)
            if a not in visited.keys():
                visited[a] = Person(a, b)
            else:
                visited[a].ind = b
            if b not in indexed.keys():
                indexed[b] = visited[a]
            else:
                indexed[b].ind = b
            # merging with neighbouring ones:
            if b != 0:
                # right connection:
                if b - 1 in indexed.keys():
                    print(f'right connection...')
                    connect(visited[a], indexed[b - 1])
            if b != queue_size - 1:
                # left connection:
                if b + 1 in indexed.keys():
                    print(f'left connection... visited[a]: {visited[a]}, indexed[b + 1]: {indexed[b + 1]}')
                    connect(indexed[b + 1], visited[a])
            lr_pass(visited[a], indexed)
    print(f'indexed: {indexed}')
    for name_, person in visited.items():
        print(f'...{person.left}<<--{person}-->>{person.right}')
    # returning result:
    return mr_wrong


def connect(left: Person, right: Person):
    left.right = right
    right.left = left


def l_pass(neigh_: Person, indexed: dict):
    while neigh_.left is not None:
        print(f'neigh_, nl: {neigh_, neigh_.left}')
        i = neigh_.left.ind = neigh_.ind + 1
        indexed[i] = neigh_.left
        neigh_ = neigh_.left


def r_pass(neigh_: Person, indexed: dict):
    while neigh_.right is not None:
        i = neigh_.right.ind = neigh_.ind - 1
        indexed[i] = neigh_.right
        neigh_ = neigh_.right


def lr_pass(neigh_: Person, indexed: dict):
    temp_neigh_ = neigh_
    l_pass(neigh_, indexed)
    r_pass(temp_neigh_, indexed)


def scan_conversation(conversation: list[str]) -> tuple[set[str], list[tuple[str, str | int]], int]:
    data = [c.split(':') for c in conversation]
    names = {c[0] for c in data}
    queue_size = len(names)
    conditions = []
    # print(f'data: {data}')
    # print(f'names: {names}')
    for datum in data:
        name, condition = datum
        res = re.findall(r"\d+", condition)
        num = int(res[0]) if res else None
        print(f'name, condition: {name, condition}')
        print(f'...num found: {num}')
        match condition[:4]:
            case "I'm ":
                conditions.append((name, num))
            case 'The ':
                if condition[8] == 'b':
                    second_name = condition[21:-1]
                    conditions.append((name, second_name))
                else:
                    second_name = condition[26: -1]
                    conditions.append((second_name, name))
            case 'Ther':
                if condition[-10] == 'b':
                    print(f'!!!{name}!!!')
                    conditions.append((name, queue_size - num - 1))
                else:
                    conditions.append((name, num))
            case _:
                raise ValueError(f'WRONG STRING!!! ({condition})')

    return names, conditions, queue_size


conversation_ = ["Wzyhxtwkb:The man in front of me is Itrxwlly.",
                 "Zggyr:The man in front of me is Ynexjb.",
                 "Vgqt:The man behind me is Jvnnp.",
                 "Ynexjb:The man behind me is Zggyr.",
                 "Icrko:The man in front of me is Jvnnp.",
                 "Itrxwlly:The man behind me is Wzyhxtwkb.",
                 "Jvnnp:The man in front of me is Vgqt.",
                 "Bvkmhqbw:The man behind me is Itrxwlly.",
                 "Itrxwlly:The man in front of me is Bvkmhqbw.",
                 "Gbnt:The man in front of me is Wzyhxtwkb.",
                 "Zggyr:The man behind me is Gbnt."]

conv_ = [
    "John:The man in front of me is Igor.",
    "Ron:The man in front of me is James.",
    "Don:I'm in 2nd position.",
    "Ivan:There are 5 people behind me.",
    "Ned:The man behind me is Ivan.",
    "Igor:The man in front of me is Ron.",
    "James:The man in front of me is Don."
]

conv_x = [
    "John:I'm in 1st position.",
    "Peter:I'm in 2nd position.",
    "Tom:I'm in 3st position.",
    'Peter:The man behind me is Tom.'
]

conv_z = [
    "Tom:The man behind me is Bob.",
    "Bob:The man in front of me is Tom.",
    "Bob:The man behind me is Gary.",
    "Gary:The man in front of me is Bob.",
    "Tom:The man in front of me is Fred.",
    "Fred:I'm in 1st position."
]

# expected result: Gbnt
find_out_mr_wrong(conv_)

# r = re.findall(r"\d+", "lala f12x ...?s")
# print(f'{r}')
# some tests
print(f'{Person(f"John")}')

k = Person('a')
x = Person('b')
f = k
k = x
print(f'f: {f}')
print(f'k: {k}')


# lala
