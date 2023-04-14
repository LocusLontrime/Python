# accepted on codewars.com
def parse_molecule(formula: str):
    l_ = len(formula)
    print(f'formula: {formula}')

    # core recursive parsing method:
    def rec_parser(ind: int):
        # dictionary for molecule's parsing:
        atoms: dict[str, int] = dict()
        i = ind
        while i < l_:
            temp_ind = i
            if formula[i].isupper():
                i += 1
                while i < l_ and formula[i].isalpha() and formula[i].islower():
                    i += 1
                elem = formula[temp_ind: i]
                print(f'elem found: {elem}')
                temp_ind = i
                while i < l_ and formula[i].isdigit():
                    i += 1
                num = int(formula[temp_ind: i]) if temp_ind != i else 1
                print(f'num for {elem}: {num}')
                if elem in atoms.keys():
                    atoms[elem] += num
                else:
                    atoms[elem] = num
            if i < l_ and formula[i] in '{[(':
                print(f'opening...')
                i, inner_atoms = rec_parser(i + 1)
                temp_ind = i
                while i < l_ and formula[i].isdigit():
                    i += 1
                num = int(formula[temp_ind: i]) if i != temp_ind else 1
                print(f'outer num: {num}')
                for key in inner_atoms.keys():
                    val = inner_atoms[key] * num
                    if key in atoms.keys():
                        atoms[key] += val
                    else:
                        atoms[key] = val
                print(f'inner_atoms: {inner_atoms}')
                print(f'atoms_: {atoms}')
                print(f'i: {i}')
            elif i < l_ and formula[i] in ')]}':
                print(f'closing... ind: {ind=} {i=}')
                return i + 1, atoms
        return atoms
    atoms_ = rec_parser(0)
    return atoms_


print(f'easy parsing: {parse_molecule("{H2O}2")}')
print(f'parsing: {parse_molecule("K4[ON(SO3)2]2")}')
print(f'parsing: {parse_molecule("Mg(OH)2")}')
print(f'diff parsing: {parse_molecule("As2{Be4C5[BCo3(CO2)3]2}4Cu5")}')

print(f'strange parsing: {parse_molecule("(C5H5)Fe(CO)2CH3")}')

print(f'great parsing: {parse_molecule("Au11{Cu5Au17OH4(Ag7Pt6Zi8)7(H2[AuBe5]4Be2O3)5(Be23Ti17Ag7[IrO3]3[Mt7H3O24Pt8]2[Cu8C{Ca7K8CO7(O8Mg6Fe[COH3Tl8Pb3]3)2OH17}O5]7Fe3H8)7}Se7Ca11(H2O3Fe5)2Be3")}')






























