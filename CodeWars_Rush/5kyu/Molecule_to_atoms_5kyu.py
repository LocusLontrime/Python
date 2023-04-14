# accepted on codewars.com
from collections import defaultdict


def parse_molecule(formula: str):
    l_ = len(formula)
    print(f'formula: {formula}')

    # core recursive parsing method:
    def rec_parser(ind: int, depth: int):
        tab = "    " * depth
        print(f'{tab}{depth}th depth: ')
        # dictionary for molecule's parsing:
        atoms = defaultdict(int)
        i = ind
        while i < l_:
            temp_ind = i
            if formula[i].isupper():
                i += 1
                while i < l_ and formula[i].isalpha() and formula[i].islower():
                    i += 1
                elem = formula[temp_ind: i]
                temp_ind = i
                while i < l_ and formula[i].isdigit():
                    i += 1
                num = int(formula[temp_ind: i]) if temp_ind != i else 1
                print(f'{tab}elem found: {elem} {num}')
                atoms[elem] += num
            if i < l_ and (symb := formula[i]) in '{[(':
                print(f'{tab}-->> opening bracket {symb}... ind: {ind=} {i=}')
                i, inner_atoms = rec_parser(i + 1, depth + 1)
                temp_ind = i
                while i < l_ and formula[i].isdigit():
                    i += 1
                num = int(formula[temp_ind: i]) if i != temp_ind else 1
                print(f'{tab}x{num}')
                for key in inner_atoms.keys():
                    val = inner_atoms[key] * num
                    atoms[key] += val
            elif i < l_ and (symb := formula[i]) in ')]}':
                print(f'{"    " * (depth - 1)}<<-- closing bracket ...{symb} ind: {ind=} {i=}')
                return i + 1, atoms
        return atoms
    return rec_parser(0, 0)


# print(f'easy parsing: {parse_molecule("{H2O}2")}')
# print(f'parsing: {parse_molecule("K4[ON(SO3)2]2")}')
# print(f'parsing: {parse_molecule("Mg(OH)2")}')
# print(f'diff parsing: {parse_molecule("As2{Be4C5[BCo3(CO2)3]2}4Cu5")}')
#
# print(f'strange parsing: {parse_molecule("(C5H5)Fe(CO)2CH3")}')
#
print(f'great parsing: {parse_molecule("Au11{Cu5Au17OH4(Ag7Pt6Zi8)7(H2[AuBe5]4Be2O3)5(Be23Ti17Ag7[IrO3]3[Mt7H3O24Pt8]2[Cu8C{Ca7K8CO7(O8Mg6Fe[COH3Tl8Pb3]3)2OH17}O5]7Fe3H8)7}Se7Ca11(H2O3Fe5[Mg17Au3Be7]3SeH3)2Mg8(FeSe7)5Be3")}')
#





























