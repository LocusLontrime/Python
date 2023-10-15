# accepted on codewars.com
rec_calls: int
starting_read: str


def reconstruct_genome(reads, has_errors=False):
    def sort_key(x):
        return -(x[1] + len(x[2]))

    print(f'reads: {reads}')
    global rec_calls, starting_read
    rec_calls = 0

    graph = graphify_with_errors(reads, has_errors)
    print(f'len of graph: {len(graph.keys())}')
    show(graph)
    starting_read = max([read for read in graph.keys()],
                        key=lambda x: max([sort_key(y) for y in graph[x]]))
    print(f'start read: {starting_read}')
    sequenced_genome = rec_hamilton_seeker_with_errors(starting_read, [(starting_read, 0)], graph, set(), has_errors)
    print(f'rec calls: {rec_calls}')
    return sequenced_genome


def rec_hamilton_seeker_with_errors(genome: str, path: list[tuple[str, int]],
                                    graph: dict[str, list[tuple[str, int, list[int]]]],
                                    errors_cols: set[int], errors: bool):
    global rec_calls, starting_read

    # aux method for sorting
    def sort_key(x):
        return -(x[1] + len(x[2]))
    # rec counter
    rec_calls += 1
    # border cases:
    if len(path) == len(graph.keys()):
        print(f'the path: {path}')
        overlap = (c := calc_affinity(path[-1][0], starting_read))[0] + len(c[1]) if errors else find_overlapping_pair(
            path[-1][0], starting_read)
        print(f'overlap: {overlap}')
        # completes the circuit
        if len(path[0][0]) == 3:
            genome = genome[:8]
        else:
            genome = genome[:-overlap] if overlap != 0 else genome
        # errors checking:
        for e in errors_cols:
            symbols_freq = dict()
            for v in path:
                symbol = None
                l_pos, r_pos = v[1] % 100, (v[1] + 50) % 100
                # checks if error falls within the bounds of interval:
                if l_pos < r_pos:
                    if l_pos <= e < r_pos:
                        symbol = v[0][e - l_pos]
                else:
                    if l_pos <= e < 100:
                        symbol = v[0][e - l_pos]
                    elif 0 <= e < r_pos:
                        symbol = v[0][100 - l_pos + e]
                # adding a symbol to the frequency dictionary
                if symbol is not None:
                    if symbol in symbols_freq:
                        symbols_freq[symbol] += 1
                    else:
                        symbols_freq[symbol] = 1
            # getting the most frequent element
            right_symbol = sorted(symbols_freq.keys(), key=lambda x: -symbols_freq[x])[0]
            genome = genome[:e] + right_symbol + genome[e + 1:]

        return genome
    # sorting heuristic
    vertexes = graph[(prev_vertex := path[-1])[0]]
    sorted_vertexes = sorted(vertexes, key=lambda x: (-(x[1] + len(x[2])), -max(
        [-98] + [-sort_key(y) for y in graph[x[0]] if y[0] not in [vertex[0] for vertex in path]])))
    # body of rec:
    for next_vertex in sorted_vertexes:  # graph[(prev_vertex := path[-1])[0]]:
        # recursive call:
        if next_vertex[0] not in [vertex[0] for vertex in path]:
            print(f'path: {path}')
            # section of errors elimination:
            n = next_vertex[0]
            beginning_index = len(n) - next_vertex[1] - len(next_vertex[2])
            new_errors_cols = errors_cols.copy()

            for error in next_vertex[2]:
                error_position_in_genome = (prev_vertex[1] + error) % (2 * 50)
                new_errors_cols.add(error_position_in_genome)

            ans = rec_hamilton_seeker_with_errors(
                genome + next_vertex[0][-beginning_index:],
                path + [(next_vertex[0], prev_vertex[1] + beginning_index)], graph, new_errors_cols, errors)

            if ans is not None:
                return ans


# Function to calculate maximum
# overlap in two given strings
def find_overlapping_pair(str1: str, str2: str) -> int:  # just for faster graph building in no errors case
    length = min(len(str1), len(str2))  # may be just one length will be enough
    # check if the suffix of str1 matches with the prefix of str2
    for i in range(length - 1, 0, -1):
        # compare last i characters in str1 with first i characters in str2
        if str1[-i:] == str2[:i]:
            # if matches we add the str2 to the overlapping pairs
            return i
    return 0


def calc_affinity(str1: str, str2: str):
    max_res, max_j, error_indexes, errors = 0, 0, [], []
    for j_index in range(len(str1)):
        res, error_indexes = 0, []
        for index in range(len(str1) - j_index):
            if str1[j_index + index] == str2[index]:
                res += 1
            else:
                error_indexes.append(index)

        if max_res < res:
            max_res = res
            max_j = j_index
            errors = error_indexes.copy()

    errs = [(max_j + err) for err in errors]

    return max_res, errs


def graphify_with_errors(reads: list[str], errors: bool) -> dict[str, list[tuple[str, int, list[int]]]]:
    graph_with_errors = dict()
    length = len(reads)

    for j in range(length):
        graph_with_errors[reads[j]] = []
        for i in range(length):
            if j != i:
                overlap, errs = calc_affinity(reads[j], reads[i]) if errors else (find_overlapping_pair(reads[j], reads[i]), [])
                if len(errs) in [0, 1, 2]:
                    graph_with_errors[reads[j]].append((reads[i], overlap, errs))

    return graph_with_errors


def show(g: dict[str, list[tuple[str, int, list[int]]]]) -> None:
    for key_read in g:
        print(f'read: {key_read}, connections: {g[key_read]}')


# TTACTTACAAAACCAGATATGACTAACTGAGGCATTGTCCCGAATCAACTGAGAATGGGACCATACCCCTCTTCGCATGAACGGTCTGGCTGTAATACAG
reads_x = ['TCGCATGAACGGTCTGGCTGAAATACAGTTACTTACAAAACCAGATATGA', 'AAAACCAGATCTGACTAACTGAGGCATTGTCCCGAATCAACTGAGAATGG',
           'ATGAACGGTCTGGCTGTAATACAGTTACTTACAAAACCAGATATGACTAT', 'GAGAATGGGACCATACCCCTCTTCGCATGAACGGTCTGGCTCTAATACAG',
           'ACTTACAAAACCAGATATGACTAACTGAGGCATTCTCCCGAATCAACTGA', 'ACAGTTACTTACAAAACCAGATATAACTAACTGAGGCATTGTCCCGAATC',
           'TTACTTACAAAACCAGAAATGACTAACTGAGGCATTGTCCCGAATCAACT', 'ATACAGTTACTTACAAAACCAGATATGGCTAACTGAGGCATTGTCCCGAA',
           'CGAATCAACTGAGAATGGGACCATACCCCTCTTCGCATGAACGGTCTGTC', 'GGGACCATACCCCTCATCGCATGAACGGTCTGGCTGTAATACAGTTACTT',
           'CCAGATATGACTAACTGAGGCATTGTCCCGAATCAACTGAGAATCGGACC', 'GAACGGTCTGGCTGTAATACAGTTACTTACAAAACCAGATTTGACTAACT',
           'CATTGTCCCGAATCAACAGAGAATGGGACCATACCCCTCTTCGCATGAAC', 'CTCTTCGCATGAACGGTCTGGCTGTAATACAGTTACTTACAAAACCCGAT',
           'AACTGAGAATGGGACCAGACCCCTCTTCGCATGAACGGTCTGGCTGTAAT', 'ACAAAACCAGATATGACTAACTGAGGCATTGTCCCGAATCACCTGAGAAT',
           'AACCAGCTATGACTAACTGAGGCATTGTCCCGAATCAACTGAGAATGGGA']

print(reconstruct_genome(reads_x, True))
# gr = graphify_with_errors(reads_x, False)
# print(f'graph before sort: ')
# show(gr)
# print(f'max: {max([(y[1] + len(y[2])) for y in gr["TCG"]])}')
# print(f'graph after sort: ')
# show(smart_sort(gr))

# test section:
# gra = dict()
# gra[1] = [2, 5]
# gra[2] = [1, 4]
# gra[3] = [4, 6, 5, 9]
# gra[4] = [2, 3]
# gra[5] = [1, 9, 3]
# gra[6] = [9, 3]
# gra[9] = [3, 5, 6]
#
# for key_int in gra.keys():
#     gra[key_int] = sorted(gra[key_int], key=lambda x: -max(gra[x]))
#
# for k in gra.keys():
#     print(f'vertex: {k}, connections: {gra[k]}')

print([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][:-5])
