import re
from collections import defaultdict as d


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
    wrongs_counter = 0
    people, conditions, queue_size = scan_conversation(conversation)
    print(f'people: {people}')
    print(f'conditions: ')
    print(f'queue_size: {queue_size}')
    for condition in conditions:
        print(f'{condition}')
    # the main cycle:
    for i, name in enumerate(people, 1):
        print(f'{i}th name: {name}')
        visited: dict[str, Person] = {}
        indexed: dict[int, Person] = {}
        flag = True
        for condition in conditions:
            speaker, a, b = condition
            if speaker != name:
                print(f'...a, b: {a, b}')
                # TODO: check for the possibility of insertion of a non-indexed nodes chain to the queue formed...
                # TODO: decide how to process the liar's condition...
                # TODO: check for negative indices possibilities!!!
                if isinstance(a, str) and isinstance(b, str):
                    if a == b:
                        flag = False
                        print(f'err(a == b)')
                        break
                    if a not in visited.keys():
                        visited[a] = Person(a)
                    if b not in visited.keys():
                        visited[b] = Person(b)
                    if visited[a].left is not None and visited[a].left != visited[b] or visited[b].right is not None and \
                            visited[b].right != visited[a]:
                        flag = False
                        print(
                            f'visited[a], visited[a].left: {visited[a], visited[a].left} | visited[b], visited[b].right: {visited[b], visited[b].right}')
                        print(f'err(1)')
                        break
                    connect(visited[b], visited[a])
                    if visited[a].placed() and visited[b].placed():
                        # check for error:
                        if visited[b].ind != visited[a].ind + 1:
                            flag = False
                    elif visited[a].placed():
                        print(f'l_pass...')
                        flag = l_pass(visited[a], indexed, queue_size)
                    elif visited[b].placed():
                        print(f'r_pass...')
                        flag = r_pass(visited[b], indexed, queue_size)
                    if not flag:
                        print(f'err(2)')
                        break
                else:  # it means -> a is str and b is int:
                    b = int(b)
                    if a not in visited.keys():
                        visited[a] = Person(a, b)
                    else:
                        visited[a].ind = b
                    if visited[a].placed() and visited[a].ind != b:
                        flag = False
                        print(f'err(3)')
                        break
                    if b in indexed.keys() and indexed[b] != visited[a]:
                        print(f'indexed[b] != visited[a] -->> {indexed[b]} != {visited[a]}')
                        flag = False
                        print(f'err(4)')
                        break
                    if b not in indexed.keys():
                        indexed[b] = visited[a]
                    else:
                        indexed[b].ind = b
                    # indexation:
                    print(f'lr_pass...')
                    flag = lr_pass(visited[a], indexed, queue_size)
                    if not flag:
                        print(f'err(5)')
                        break
                    # merging with neighbouring ones:
                    if b != 1:
                        # right connection:
                        if b - 1 in indexed.keys():
                            # print(f'right connection...')
                            connect(visited[a], indexed[b - 1])
                    if b != queue_size:
                        # left connection:
                        if b + 1 in indexed.keys():
                            # print(f'left connection... visited[a]: {visited[a]}, indexed[b + 1]: {indexed[b + 1]}')
                            connect(indexed[b + 1], visited[a])
        if flag:
            print(f'...THERE HAVE BEEN NO ERRORS')
        else:
            print(f'ERROR OCCURRED -->> {name} is not Mr.Wong!!!')
            continue
            # raise ValueError(f'...ERROR OCCURRED!!!')
        print(f'...indexed: {indexed}')
        for name_, person in visited.items():
            print(f'......{person.left}<<--{person}-->>{person.right}')
        queue = [0 for _ in range(queue_size)]
        interim_flag = True
        for key in indexed.keys():
            # print(f'key: {key}, val: {indexed[key]}')
            if key < 1 or key > queue_size:
                interim_flag = False
                break
            queue[key - 1] = 1
        if not interim_flag:
            print(f'ERROR OCCURRED -->> {name} is not Mr.Wong!!!')
            continue
        print(f'...queue: {queue}')
        segments = d(int)
        used = set()
        interim_flag = True
        for key, val in visited.items():
            print(f'key, val: {key, val}')
            if not val.placed() and val not in used:
                node_ = val
                used.add(val)
                counter = 1
                while node_.left is not None:
                    if counter > len(visited):
                        interim_flag = False
                        break
                    counter += 1
                    node_ = node_.left
                    used.add(node_)
                node_ = val
                while node_.right is not None:
                    if counter > len(visited):
                        interim_flag = False
                        break
                    counter += 1
                    node_ = node_.right
                    used.add(node_)
                segments[counter] += 1
            if not interim_flag:
                break
        if not interim_flag:
            print(f'ERROR OCCURRED -->> {name} is not Mr.Wong!!!')
            continue
        if name not in visited.keys():
            segments[1] += 1
        print(f'...segments: {segments}')
        # backtracking:
        res = backtrack(0, queue, segments)
        print(f'...VERDICT -->> {name} is Mr.Wrong: {res}')
        if res is not None:
            if wrongs_counter == 0:
                mr_wrong = name
                wrongs_counter += 1
            else:
                return None
    # returning result:
    return mr_wrong


def backtrack(j: int, queue: list[int], segments: dict[int, int]):
    print(f'j: {j}')
    # base cases:
    if j == len(queue):
        print(f'SOLUTION FOUND')
        print(f'segments: {segments}')
        return True
    if queue[j] == 1:
        # placed Person:
        return backtrack(j + 1, queue, segments)
    # body of recursion:
    res = False
    for key, val in segments.items():
        if val > 0:
            print(f'LALA!')
            if not all(queue[j: j + key]):
                segments[key] -= 1
                res = res or backtrack(j + key, queue, segments)
                # backtracking:
                segments[key] += 1
                if res:
                    return res


def connect(left: Person, right: Person):
    left.right = right
    right.left = left


def l_pass(neigh_: Person, indexed: dict, size: int) -> bool:
    counter = 0
    while neigh_.left is not None:
        if counter > size:
            return False
        # print(f'neigh_, nl: {neigh_, neigh_.left}')
        if neigh_.ind + 1 in indexed.keys():
            if indexed[neigh_.ind + 1] != neigh_.left:
                return False
        i = neigh_.left.ind = neigh_.ind + 1
        indexed[i] = neigh_.left
        neigh_ = neigh_.left
        counter += 1
    return True


def r_pass(neigh_: Person, indexed: dict, size: int) -> bool:
    counter = 0
    while neigh_.right is not None:
        if counter > size:
            return False
        # print(f'neigh_, nr: {neigh_, neigh_.right}')
        if neigh_.ind - 1 in indexed.keys():
            if indexed[neigh_.ind - 1] != neigh_.right:
                return False
        i = neigh_.right.ind = neigh_.ind - 1
        indexed[i] = neigh_.right
        neigh_ = neigh_.right
        counter += 1
    return True


def lr_pass(neigh_: Person, indexed: dict, size: int) -> bool:
    temp_neigh_ = neigh_
    return l_pass(neigh_, indexed, size) and r_pass(temp_neigh_, indexed, size)


def scan_conversation(conversation: list[str]) -> tuple[set[str], list[tuple[str, str, str | int]], int]:
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
                conditions.append((name, name, num))
            case 'The ':
                if condition[8] == 'b':
                    second_name = condition[21:-1]
                    conditions.append((name, name, second_name))
                else:
                    second_name = condition[26: -1]
                    conditions.append((name, second_name, name))
            case 'Ther':
                if condition[-10] == 'b':
                    print(f'!!!{name}!!!')
                    conditions.append((name, name, queue_size - num))
                else:
                    conditions.append((name, name, num + 1))
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
    "Tom:I'm in 1st position.",
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

conv_xyz = [
    "John:The man in front of me is Ron.",
    "Ron:The man in front of me is Don.",
    "Don:The man behind me is Ron.",
    "Ivan:The man in front of me is Igor.",
    "Igor:The man in front of me is Ned.",
    "Ned:The man behind me is Igor.",
    "James:The man behind me is Fred.",
    "Fred:The man in front of me is James.",
    "Bred:I'm in 8st position.",
    "Bred:The man behind me is Kevin.",
    "Dag:The man behind me is Bred.",
    "Kevin:The man in front of me is Bred.",
    "Peter:I'm in 3nd position.",
    # "Bred:The man in front of me is Peter."
]

conv_big = [
    'Czyooyt:There are 5 people in front of me.',
    'Mrepaytu:There are 10 people in front of me.',
    'Qoigzse:The man behind me is Jeaiky.',
    'Etaxt:The man in front of me is Hrye.',
    'Hujyu:The man in front of me is Froujioe.',
    'Aouisyrz:There are 5 people behind me.',
    'Exwhao:There are 25 people in front of me.',
    'Oqma:There are 33 people behind me.',
    'Nsjkaxn:There are 7 people in front of me.',
    'Oiiikue:The man in front of me is Fudu.',
    "Oqma:I'm in 7th position.",
    'Oiiikue:There are 36 people in front of me.',
    'Oaivj:The man behind me is Wodboaa.',
    'Exwhao:The man in front of me is Cedezmes.',
    "Fudu:I'm in 36th position.",
    "Ypurk:I'm in 22th position.",
    'Muion:There are 38 people behind me.',
    'Ewvwecagb:There are 12 people behind me.',
    'Fgviom:The man behind me is Froujioe.',
    'Jevbdybau:The man in front of me is Ewvwecagb.',
    'Egoigregs:There are 2 people in front of me.',
    'Froujioe:The man behind me is Hujyu.',
    'Aouvgxfz:The man behind me is Mrepaytu.',
    'Lweipytec:There are 39 people behind me.',
    'Aouvgxfz:There are 30 people behind me.',
    "Ipieemp:I'm in 40th position.",
    'Iimharu:There are 23 people behind me.',
    'Igxyfgsn:There are 17 people in front of me.',
    'Luuhabiij:There are 22 people in front of me.',
    'Oqma:The man behind me is Nsjkaxn.',
    'Qoigzse:There are 36 people behind me.',
    'Cuowumg:The man behind me is Cedezmes.',
    'Lweipytec:There are 0 people in front of me.',
    "Aaaae:I'm in 27th position.",
    'Hujyu:The man behind me is Ypurk.',
    'Wodboaa:The man in front of me is Oaivj.',
    "Wtpe:I'm in 14th position.",
    'Jeaiky:There are 4 people in front of me.',
    'Rego:There are 15 people in front of me.',
    'Aouisyrz:The man behind me is Fudu.',
    'Oaivj:There are 11 people in front of me.',
    'Djxohlr:The man behind me is Aaaae.',
    'Egoigregs:The man in front of me is Muion.',
    "Luuhabiij:I'm in 23th position.",
    'Ipieemp:There are 39 people in front of me.',
    'Sgidivo:The man behind me is Aouisyrz.',
    'Igxyfgsn:The man behind me is Fgviom.',
    'Wtpe:There are 26 people behind me.',
    "Ejzqi:I'm in 15th position.",
    'Jeaiky:The man in front of me is Qoigzse.',
    "Dfadk:I'm in 39th position.",
    'Hyzdeexk:There are 8 people in front of me.',
    'Fgviom:There are 18 people in front of me.',
    "Oaivj:I'm in 12th position.",
    "Oiiikue:I'm in 37th position.",
    'Jevbdybau:There are 11 people behind me.',
    'Gbuiu:There are 7 people behind me.',
    'Ypurk:The man behind me is Luuhabiij.',
    'Jeaiky:The man behind me is Czyooyt.',
    "Djxohlr:I'm in 26th position.",
    'Fudu:There are 35 people in front of me.',
    'Rego:The man in front of me is Ejzqi.',
    'Wodboaa:The man behind me is Wtpe.',
    'Aaaae:The man in front of me is Exwhao.',
    'Igxyfgsn:The man in front of me is Iimharu.',
    'Dfadk:There are 38 people in front of me.',
    'Dfadk:The man in front of me is Ojtangexg.',
    "Ojtangexg:I'm in 38th position.",
    "Muion:I'm in 2nd position.",
    'Ewvwecagb:There are 27 people in front of me.',
    'Czyooyt:The man in front of me is Jeaiky.',
    'Nsjkaxn:There are 32 people behind me.',
    'Iimharu:The man behind me is Igxyfgsn.',
    'Fudu:There are 4 people behind me.',
    'Mrepaytu:The man behind me is Oaivj.',
    'Egoigregs:There are 37 people behind me.',
    'Hrye:The man behind me is Etaxt.',
    'Cedezmes:There are 15 people behind me.',
    'Luuhabiij:The man in front of me is Ypurk.',
    "Lweipytec:I'm in 1st position.",
    'Ejzqi:The man behind me is Rego.',
    'Mrepaytu:The man in front of me is Aouvgxfz.',
    'Ejzqi:There are 14 people in front of me.',
    'Ypurk:The man in front of me is Hujyu.',
    'Cuowumg:There are 23 people in front of me.',
    'Nsjkaxn:The man behind me is Hyzdeexk.',
    'Cuowumg:The man in front of me is Luuhabiij.',
    'Ojtangexg:The man behind me is Dfadk.'  # Djxohlr
]

conv_zzz = [
    "Ivjoyulu:I'm in 2nd position.",
    'Avief:The man in front of me is Ohdub.',
    'Jaasa:The man in front of me is Iqra.',
    "Rece:I'm in 29th position.",
    'Snae:There are 32 people in front of me.',
    'Ohdub:There are 12 people behind me.',
    'Ukwiiesao:There are 37 people behind me.',
    'Hngoee:There are 29 people in front of me.',
    'Iueqa:There are 7 people behind me.',
    'Oeuenidmh:The man in front of me is Rsgprw.',
    'Afak:There are 27 people behind me.',
    'Iqra:The man behind me is Jaasa.',
    'Opqean:There are 30 people in front of me.',
    'Rece:There are 10 people behind me.',
    'Nxpsui:There are 14 people behind me.',
    "Ueievc:I'm in 35th position.",
    'Nlui:There are 36 people in front of me.',
    'Gcegegyi:The man in front of me is Uqalyf.',
    'Luff:There are 18 people behind me.',
    'Ulaergv:There are 5 people in front of me.',
    'Swdu:The man behind me is Rsgprw.',
    'Iqra:There are 32 people behind me.',
    'Afak:There are 11 people in front of me.',
    'Ivjoyulu:The man in front of me is Snae.',
    "Fkgpmayu:I'm in 20th position.",
    'Roatuu:There are 38 people in front of me.',
    'Pwisodylu:There are 24 people behind me.',
    'Rsgprw:The man in front of me is Swdu.',
    'Ohdub:The man in front of me is Ixuiuoisj.',
    'Ixuiuoisj:The man in front of me is Nxpsui.',
    'Ujuabgo:The man in front of me is Mwswwaot.',
    'Redypne:There are 0 people in front of me.',
    'Ivjoyulu:The man behind me is Ivjoyulu.',
    'Iwoeegf:The man behind me is Raka.',
    'Iwoeegf:The man in front of me is Luff.',
    'Fdprprv:There are 5 people behind me.',
    'Ulaergv:There are 33 people behind me.',
    'Mwswwaot:The man behind me is Ujuabgo.',
    'Ohdub:The man behind me is Avief.',
    'Pwisodylu:The man behind me is Swdu.',
    'Gcegegyi:There are 10 people in front of me.',
    'Ovoe:The man behind me is Ivjoyulu.',
    'Fkgpmayu:The man behind me is Luff.',
    'Olvg:The man in front of me is Oeuenidmh.',
    'Iitfe:There are 15 people behind me.',
    'Rsgprw:There are 22 people behind me.',
    'Swdu:There are 15 people in front of me.',
    "Ixuiuoisj:I'm in 26th position.",
    'Ukwiiesao:The man in front of me is Redypne.',
    'Ujuabgo:The man behind me is Uooy.',
    'Ovoe:There are 26 people behind me.',
    'Raka:There are 22 people in front of me.',
    'Uqalyf:There are 9 people in front of me.',
    'Qeiseo:There are 8 people in front of me.',
    'Ueievc:There are 4 people behind me.',
    "Iueqa:I'm in 32th position.",
    'Qeiseo:There are 30 people behind me.',
    "Nxpsui:I'm in 25th position.",
    'Iueqa:The man in front of me is Opqean.',
    'Luff:The man in front of me is Fkgpmayu.',
    'Ovoe:There are 12 people in front of me.',
    'Snae:The man in front of me is Iueqa.',
    'Roatuu:The man in front of me is Tuwev.',
    'Uooy:There are 4 people in front of me.',
    'Ulaergv:The man behind me is Iqra.',
    "Iwoeegf:I'm in 22th position.",
    'Opqean:There are 8 people behind me.',
    'Ujuabgo:There are 35 people behind me.',
    'Roatuu:There are 0 people behind me.',
    'Olvg:There are 18 people in front of me.',
    'Raka:There are 16 people behind me.',
    'Caehgvyeg:There are 35 people in front of me.',
    'Mwswwaot:There are 2 people in front of me.',
    "Iqra:I'm in 7th position.",
    'Fkgpmayu:The man in front of me is Olvg.',
    'Caehgvyeg:The man in front of me is Ueievc.',
    "Tuwev:I'm in 38th position.",
    'Pwisodylu:There are 14 people in front of me.',
    'Iitfe:The man behind me is Nxpsui.',
    "Uqalyf:I'm in 10th position.",
    'Nxpsui:The man in front of me is Iitfe.',
    "Snae:I'm in 33th position."  # Ivjoyulu
]

conversation_zz = [
    'Bndj:There are 14 people behind me.',
    "Zrsnubg:I'm in 22th position.",
    'Piwiapo:There are 10 people behind me.',
    'Knekaiezc:There are 20 people behind me.',
    'Rvem:The man behind me is Ltoao.',
    'Oplotoae:The man behind me is Oqeu.',
    'Lpkjqya:There are 5 people behind me.',
    "Yoaeoot:I'm in 38th position.",
    "Oqeu:I'm in 15th position.",
    'Ymiex:The man behind me is Cdiyw.',
    "Ifjge:I'm in 12th position.",
    'Yoaeoot:There are 0 people behind me.',
    'Eyzrhiuuw:There are 0 people in front of me.',
    'Youalouzy:There are 31 people in front of me.',
    'Eppkve:There are 33 people behind me.',
    'Okocof:There are 13 people in front of me.',
    'Oyybageya:There are 16 people in front of me.',
    "Eyzrhiuuw:I'm in 1st position.",
    'Cdiyw:There are 34 people behind me.',
    "Cnwcvompy:I'm in 7th position.",
    'Oqeu:The man behind me is Gdjp.',
    'Okocof:The man in front of me is Iediu.',
    'Oaueuqjzp:The man behind me is Yoaeoot.',
    'Oyybageya:The man in front of me is Gdjp.',
    'Lvpeaa:The man behind me is Oaueuqjzp.',
    'Gdjp:There are 22 people behind me.',
    'Kseyiada:There are 27 people behind me.',
    'Bndj:There are 23 people in front of me.',
    'Newyoih:The man behind me is Abjemu.',
    'Iiufooae:There are 5 people in front of me.',
    'Etgo:The man in front of me is Bndj.',
    "Efebce:I'm in 19th position.",
    'Oaueuqjzp:There are 36 people in front of me.',
    'Zrsnubg:The man behind me is Erpumieul.',
    'Faouyoi:There are 3 people behind me.',
    'Newyoih:There are 9 people behind me.',
    'Euaw:The man in front of me is Ltoao.',
    'Ilhdhxr:There are 12 people behind me.',
    'Euaw:There are 9 people in front of me.',
    'Erpumieul:There are 22 people in front of me.',
    'Azhnufko:There are 4 people behind me.',
    'Piwiapo:There are 27 people in front of me.',
    'Youalouzy:There are 6 people behind me.',
    "Lvpeaa:I'm in 36th position.",
    'Oqeu:The man in front of me is Okocof.',
    'Rqiasi:There are 36 people behind me.',
    'Efebce:The man behind me is Eesb.',
    'Kseyiada:The man behind me is Ifjge.',
    'Zrsnubg:The man in front of me is Ebjjriyx.',
    'Cnwcvompy:The man in front of me is Iiufooae.',
    "Ilhdhxr:I'm in 26th position.",
    'Oyybageya:The man behind me is Knekaiezc.',
    'Rvem:There are 7 people in front of me.',
    'Oaueuqjzp:The man in front of me is Lvpeaa.',
    'Knekaiezc:The man behind me is Efebce.',
    'Rqiasi:The man behind me is Ymiex.',
    'Ifjge:There are 26 people behind me.',
    'Piwiapo:The man behind me is Newyoih.',
    "Eypei:I'm in 31th position.",
    'Faouyoi:The man in front of me is Azhnufko.',
    'Lvpeaa:There are 35 people in front of me.',
    "Bndj:I'm in 24th position.",
    'Yoaeoot:The man in front of me is Oaueuqjzp.',
    'Cnwcvompy:The man behind me is Rvem.',
    'Eesb:There are 18 people behind me.',
    'Eypei:The man behind me is Youalouzy.',
    'Oplotoae:There are 28 people in front of me.',
    'Abjemu:There are 29 people in front of me.',
    "Iediu:I'm in 13th position.",
    "Etgo:I'm in 25th position.",
    "Abjemu:I'm in 30th position.",
    'Oplotoae:The man in front of me is Zrsnubg.',
    "Iiufooae:I'm in 6th position.",
    'Faouyoi:The man behind me is Lvpeaa.',
    'Euaw:There are 28 people behind me.',
    'Ilhdhxr:The man behind me is Oplotoae.',
    'Ebjjriyx:The man in front of me is Eesb.',
    'Ltoao:There are 8 people in front of me.',
    "Youalouzy:I'm in 32th position.",
    'Eyzrhiuuw:There are 37 people behind me.',
    'Ebjjriyx:The man behind me is Zrsnubg.',
    'Iiufooae:There are 32 people behind me.',
    'Okocof:The man behind me is Oqeu.'  # Oplotoae
]

conv_q = [
    'Xeolox:There are 9 people in front of me.',
    'Izdxi:There are 16 people behind me.',
    'Ssezkd:There are 27 people in front of me.',
    'Jyuogw:The man in front of me is Izdxi.',
    'Ardr:The man behind me is Zmuircws.',
    'Xojudao:There are 5 people in front of me.',
    "Tudiz:I'm in 18th position.",
    'Mxtequck:The man in front of me is Ianddeov.',
    'Emgjzqeq:There are 25 people in front of me.',
    'Foeyexj:There are 21 people behind me.',
    'Ueigi:There are 8 people behind me.',
    "Eaxo:I'm in 13th position.",
    'Egucuti:The man behind me is Xpogflw.',
    "Zxnn:I'm in 39th position.",
    'Hreabi:The man in front of me is Xpogflw.',
    'Lognisoua:The man in front of me is Xeolox.',
    "Atyeyazo:I'm in 37th position.",
    'Mxtequck:There are 4 people behind me.',
    'Oeol:The man behind me is Kotroerin.',
    'Xpogflw:The man behind me is Hreabi.',
    'Uhrezsf:There are 33 people behind me.',
    'Pdly:There are 7 people behind me.',
    'Kotwcvao:There are 13 people behind me.',
    'Egucuti:The man in front of me is Ssezkd.',
    'Xeolox:The man behind me is Lognisoua.',
    'Oeol:The man in front of me is Ohgjoue.',
    'Izdxi:The man behind me is Paavuo.',
    'Tudiz:There are 22 people behind me.',
    "Pqapxo:I'm in 23th position.",
    'Fvvs:There are 35 people behind me.',
    'Ianddeov:There are 5 people behind me.',
    "Mxtequck:I'm in 36th position.",
    'Lognisoua:The man behind me is Vdnexy.',
    'Ueigi:There are 31 people in front of me.',
    'Oeol:There is 1 people in front of me.',
    'Saawioo:The man in front of me is Vhazyxtkh.',
    'Vhazyxtkh:The man behind me is Saawioo.',
    "Uhrezsf:I'm in 7th position.",
    'Xpogflw:There are 29 people in front of me.',
    "Oooniaeyi:I'm in 38th position.",
    'Ypaa:The man in front of me is Kotroerin.',
    'Rdquyje:There are 16 people in front of me.',
    'Obtwtmko:There are 21 people in front of me.',
    'Zmuircws:The man in front of me is Ardr.',
    'Zmuircws:The man behind me is Xeolox.',
    'Xojudao:The man behind me is Uhrezsf.',
    'Foeyexj:The man in front of me is Tudiz.',
    'Audicsr:There are 20 people in front of me.',
    'Eaxo:The man behind me is Vhazyxtkh.',
    'Hreabi:The man behind me is Ueigi.',
    'Eaxo:There are 12 people in front of me.',
    'Zxnn:There is 1 people behind me.',
    'Atyeyazo:The man in front of me is Mxtequck.',
    "Paavuo:I'm in 25th position.",
    'Atyeyazo:There are 3 people behind me.',
    'Ohgjoue:There are 39 people behind me.',
    'Xeolox:The man in front of me is Zmuircws.',
    'Ypaa:The man behind me is Fvvs.',
    'Izdxi:There are 23 people in front of me.',
    'Zmuircws:There are 31 people behind me.',
    'Kotroerin:The man behind me is Ypaa.',
    'Xojudao:There are 34 people behind me.',
    'Vdnexy:The man behind me is Eaxo.',
    'Fijf:The man behind me is Ianddeov.',
    'Hqcea:The man behind me is Audicsr.',
    "Ohgjoue:I'm in 1st position.",
    'Foeyexj:There are 18 people in front of me.',
    "Xkaeaidmv:I'm in 40th position.",
    'Fvvs:There are 4 people in front of me.',
    "Egucuti:I'm in 29th position.",
    'Kotwcvao:There are 26 people in front of me.',
    "Lognisoua:I'm in 11th position.",
    "Jyuogw:I'm in 25th position.",
    'Pqapxo:There are 17 people behind me.',
    'Kotroerin:The man in front of me is Oeol.',
    "Audicsr:I'm in 21th position.",
    'Audicsr:The man behind me is Obtwtmko.',
    'Tudiz:The man behind me is Foeyexj.',
    "Ardr:I'm in 8th position.",
    'Ardr:There are 32 people behind me.',
    "Vdnexy:I'm in 12th position.",
    'Ohgjoue:The man behind me is Oeol.',
    'Fvvs:The man behind me is Xojudao.',
    'Jyuogw:There are 24 people in front of me.',
    "Saawioo:I'm in 15th position.",
    'Kotroerin:There are 2 people in front of me.',
    'Paavuo:There are 24 people in front of me.'  # Jyuogw
]

conv_l = [
    'Odycyq:There are 20 people in front of me.',
    'Elgywe:There are 17 people in front of me.',
    "Tevipmu:I'm in 35th position.",
    "Duoiaae:I'm in 34th position.",
    "Ljywyxek:I'm in 29th position.",
    'Okgs:The man behind me is Uehduwf.',
    'Alemoxjk:The man in front of me is Ljywyxek.',
    "Elgywe:I'm in 18th position.",
    "Tynize:I'm in 32th position.",
    'Ebnee:The man in front of me is Tevipmu.',
    'Aawhum:There are 39 people behind me.',
    'Dlju:There are 29 people behind me.',
    'Lxaa:There are 27 people behind me.',
    "Uehduwf:I'm in 24th position.",
    'Duoiaae:There are 6 people behind me.',
    'Apdqnved:There are 11 people in front of me.',
    'Dlju:The man behind me is Apdqnved.',
    'Buamcbcet:The man behind me is Xluy.',
    'Eeenx:There are 36 people behind me.',
    'Eeenx:The man behind me is Uvyewkp.',
    'Sliotve:There are 38 people behind me.',
    'Sliotve:There is 1 people in front of me.',
    'Uehduwf:The man behind me is Htouglar.',
    'Noioao:There are 36 people in front of me.',
    'Cqtqqueuc:There are 19 people in front of me.',
    'Ectici:There are 37 people behind me.',
    'Uexa:The man behind me is Dlju.',
    'Ljywyxek:The man behind me is Alemoxjk.',
    'Iyeoxro:There are 23 people behind me.',
    'Itioaukcy:There are 15 people in front of me.',
    'Ectici:There are 2 people in front of me.',
    'Uyphp:There are 39 people in front of me.',
    'Ljywyxek:There are 11 people behind me.',
    'Uyphp:The man in front of me is Xluy.',
    'Odycyq:The man behind me is Ugxvov.',
    'Qegjoavqy:The man in front of me is Nkqeapeip.',
    'Htouglar:The man behind me is Ilioqay.',
    'Tevipmu:The man behind me is Ebnee.',
    'Aawhum:There are 0 people in front of me.',
    'Uehduwf:The man in front of me is Okgs.',
    'Exiipckhy:The man behind me is Uexa.',
    'Dlju:The man in front of me is Uexa.',
    'Duoiaae:There are 33 people in front of me.',
    'Xluy:There is 1 people behind me.',
    'Iyeoxro:The man behind me is Elgywe.',
    'Noioao:The man in front of me is Ebnee.',
    'Ugxvov:There are 18 people behind me.',
    "Lxaa:I'm in 13th position.",
    'Apdqnved:There are 28 people behind me.',
    'Uvyewkp:There are 4 people in front of me.',
    'Zxioeapc:There are 26 people in front of me.',
    'Exiipckhy:There are 34 people behind me.',
    "Blplauvlo:I'm in 19th position.",
    'Xluy:There are 38 people in front of me.',
    'Ilioqay:The man in front of me is Htouglar.',
    'Alemoxjk:The man behind me is Exiipckhy.',
    "Alemoxjk:I'm in 30th position.",
    'Apdqnved:The man in front of me is Dlju.',
    'Eeenx:The man in front of me is Ectici.',
    'Okgs:The man in front of me is Ugxvov.',
    'Tynize:The man behind me is Wbqqy.',
    'Xluy:The man in front of me is Buamcbcet.',
    'Nyjvfya:The man behind me is Itioaukcy.',
    'Htouglar:There are 15 people behind me.',
    'Nkqeapeip:There are 33 people behind me.',
    'Uexa:There are 9 people in front of me.',
    'Itioaukcy:There are 24 people behind me.',
    'Exiipckhy:There are 16 people in front of me.',
    'Blplauvlo:The man behind me is Cqtqqueuc.',
    'Lxaa:The man in front of me is Apdqnved.',
    'Nkqeapeip:There are 6 people in front of me.',
    'Ezowe:There are 26 people behind me.',
    'Ebnee:There are 4 people behind me.',
    'Dvok:The man behind me is Nkqeapeip.',
    'Buamcbcet:There are 2 people behind me.',
    'Tevipmu:The man in front of me is Duoiaae.',
    "Eezewh:I'm in 9th position.",
    'Wbqqy:The man in front of me is Tynize.',
    'Uexa:There are 30 people behind me.',
    'Uyphp:There are 0 people behind me.',
    'Nyjvfya:There are 14 people in front of me.',
    'Nbfvafi:The man behind me is Ljywyxek.'  # Exiipckhy
]

conv_trouble = [
    "Tom:The man behind me is Bob.",
    "Bob:The man in front of me is Tom.",
    "Bob:The man behind me is Gary.",
    "Gary:The man in front of me is Bob.",
    "Fred:I'm in 1st position."  # Fred
]

conv_short_1 = [
    "Enoapqg:I'm in 1st position.",
    'Deuekaeq:There are 2 people in front of me.',
    'Kvzatz:The man behind me is Vaaeok.',
    'Vaaeok:There are 0 people behind me.'
]

conv_short_2 = [
    "Huqdafek:I'm in 2nd position.",
    'Owjfamoy:The man behind me is Owjfamoy.',
    "Waxgcric:I'm in 1st position.",
    'Yaqou:There are 0 people behind me.'
]

secret_conv = [
    'Cevsc:The man in front of me is Oweee.',
    "Rafieshe:I'm in 6th position.",
    'Oxvsehb:There are 0 people in front of me.',
    'Ivbcikuya:The man in front of me is Zweaxs.',
    'Heqq:There are 2 people in front of me.',
    "Kaunistoz:I'm in 9th position.",
    'Heqq:The man behind me is Ivbcikuya.',
    'Deeuiaa:The man in front of me is Oxvsehb.',
    'Zweaxs:The man in front of me is Ivbcikuya.',
    'Oxvsehb:The man behind me is Deeuiaa.',
    'Kaunistoz:There are 0 people behind me.',
    'Rafieshe:There are 3 people behind me.',
    "Oweee:I'm in 7th position.",
    'Deeuiaa:There is 1 people in front of me.'
]

conv_k = [
    'Vpyeepoz:The man in front of me is Veeoioqg.',
    'Encjiutz:The man in front of me is Ekzauwkk.',
    'Ekzauwkk:The man in front of me is Orjsd.',
    'Orjsd:The man behind me is Ekzauwkk.',
    'Orjsd:The man in front of me is Ewxejuc.',
    'Zxleoaqka:The man in front of me is Ieboaec.',
    'Ieboaec:The man in front of me is Vpyeepoz.',
    'Ekzauwkk:The man behind me is Encjiutz.',
    'Veeoioqg:The man behind me is Vpyeepoz.',
    'Rvioeb:The man behind me is Orjsd.',
    'Ewxejuc:The man in front of me is Zxleoaqka.'
]  # liar's condition check!!!

conv_n = [
    'Bqbfne:There are 2 people in front of me.',
    'Oodri:There are 3 people in front of me.',
    'Smidbao:The man in front of me is Eoaod.',
    'Eoaod:The man in front of me is Bqbfne.'
]

conv_nn = [
    'Vgwkwoe:The man in front of me is Zoauax.',
    'Ejpqyitt:The man in front of me is Zoauax.',
    'Iosvmyr:The man in front of me is Ejpqyitt.',
    'Zoauax:There is 1 people behind me.'
]

conv_nnn = [
    'Sslxecy:There are 3 people in front of me.',
    "Iaquzyt:I'm in 12th position.",
    'Iymauoyda:The man behind me is Mdmxecr.',
    'Hgjee:There are 7 people in front of me.',
    'Mdmxecr:The man in front of me is Iymauoyda.',
    'Eeypbemj:The man in front of me is Aqfauldi.',
    'Stwa:The man in front of me is Xeie.',
    'Stwa:There are 6 people behind me.',
    'Sslxecy:There are 8 people behind me.',
    'Mdmxecr:The man behind me is Sslxecy.',
    'Aqfauldi:The man in front of me is Iaquzyt.',
    "Sslxecy:I'm in 4th position.",
    'Aqfauldi:There are 2 people behind me.',
    'Iymauoyda:There are 10 people behind me.',
    'Chnoobbie:There are 11 people behind me.',
    "Chnoobbie:I'm in 1st position.",
    'Aqfauldi:There are 9 people in front of me.',
    "Iymauoyda:I'm in 2nd position.",
    'Eeypbemj:There is 1 people behind me.',
    'Gxev:There are 5 people behind me.',
    "Mdmxecr:I'm in 3rd position.",
    "Xeie:I'm in 5th position.",
    'Xeie:There are 7 people behind me.',
    'Owedme:The man in front of me is Eeypbemj.',
    'Eeypbemj:There are 10 people in front of me.',
    'Chnoobbie:The man behind me is Iymauoyda.'
]

# expected result: Gbnt
RES = find_out_mr_wrong(conv_nnn)
print(f'RES: {RES}')

# segments_ = {7: 1, 5: 1, 3: 3, 2: 2, 1: 1}
# ones = {11, 12, 13, 14, 15, 29, 30, 33, 34, 35}
# queue_ = [1 if _ in ones else 0 for _ in range(36)]
# print(f'queue_: {queue_}')
# print(f'segments_: {segments_}')
# res_ = backtrack(0, queue_, segments_)
# print(f'res_: {res_}')

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

dict_ = d(int)
dict_[1] += 1
dict_[98] += 1
print(f'dict_: {dict_}')
dict_[98] -= 1
print(f'dict_: {dict_}')

# lala
