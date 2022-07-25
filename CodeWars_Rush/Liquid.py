import itertools


def volume(table):
    try:
        counter = 0
        subtract = 0
        findRange = itertools.chain.from_iterable(table)
        findRange = set(findRange)
        shallowest = min(findRange)
        tabDiff = max(findRange) - min(findRange)
        act = False
        for iter in range(0, tabDiff):
            tableTerrace = []
            for row in table:
                row2 = []
                for num in row:
                    if num > shallowest:
                        num = shallowest + 1
                        row2.append(num)
                    elif num < shallowest:
                        num = shallowest
                        row2.append(num)
                        counter += 1
                    else:
                        row2.append(num)
                        counter += 1
                tableTerrace.append(row2)
            edges = [tableTerrace[0], tableTerrace[len(tableTerrace) - 1], [x[0] for x in tableTerrace],
                     [x[len(x) - 1] for x in tableTerrace]]

            for row in edges:
                for index, item in enumerate(row):
                    if item == shallowest:
                        row[index] = shallowest - 1
                        act = True
                        subtract += 1
                    else:
                        pass

            while act:
                act = False
                for index, row2 in enumerate(tableTerrace):
                    for index2, item2 in enumerate(row2):
                        if item2 == shallowest:
                            try:
                                check = [row2[index2 - 1], row2[index2 + 1], tableTerrace[index - 1][index2],
                                         tableTerrace[index + 1][index2]]
                                if shallowest - 1 in check:
                                    row2[index2] = shallowest - 1
                                    act = True
                                    subtract += 1
                                else:
                                    pass
                            except IndexError:
                                act = True
                        else:
                            continue
                if act:
                    pass
                else:
                    pass
            shallowest = shallowest + 1

        answer = counter - subtract
    except UnboundLocalError:
        answer = 0
    return answer


array = [[8, 8, 8, 8, 6, 6, 6, 6],
         [8, 0, 0, 8, 6, 0, 0, 6],
         [8, 0, 0, 8, 6, 0, 0, 6],
         [8, 8, 8, 8, 6, 6, 6, 0]]

print(volume(array))
