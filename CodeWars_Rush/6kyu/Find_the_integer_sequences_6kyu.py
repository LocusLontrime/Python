# accepted on codewars.com


def find_sequences(n):
    result_list = []
    ri, li = 1, 1
    sum_ = 1
    while ri < n - 1:
        if sum_ + ri + 1 > n:
            sum_ -= li
            li += 1
        else:
            ri += 1
            sum_ += ri
            if sum_ == n:
                result_list.append([_ for _ in range(li, ri + 1)])
    return sorted(result_list, key=lambda x: len(x))


n_ = 4_369_000
sequences = find_sequences(n_)
print(f'sequences: ')
for i, sequence in enumerate(sequences, 1):
    print(f'{i}th: {sequence}')
