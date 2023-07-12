# accepted on coderun
from collections import defaultdict as d


def ivan():
    n, m, q, black_dirs, library_files, queries = get_pars()
    files_to_be_removed = []
    for library_file_ in library_files:
        for black_dir_ in black_dirs:
            if library_file_.startswith(black_dir_):
                files_to_be_removed.append((library_file_, library_file_.split('/')[-1].split('.')[1]))
                break
    print(f'files_to_be_removed: ')
    for f_ in files_to_be_removed:
        print(f'{f_}')
    for query_ in queries:
        file_container = d(int)
        for f_, ext_ in files_to_be_removed:
            if f_.startswith(query_):
                file_container[ext_] += 1
        print(f'{len(file_container)}')
        for key_ in file_container.keys():
            print(f'.{key_}: {file_container[key_]}')


def get_pars():
    n = int(input())
    black_dirs = [input().strip() for _ in range(n)]
    m = int(input())
    library_files = [input().strip() for _ in range(m)]
    q = int(input())
    queries = [input().strip() for _ in range(q)]
    return n, m, q, black_dirs, library_files, queries


ivan()


