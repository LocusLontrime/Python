import os


def files_renaming(desired_file_name: str, digits_num: int, extension_in: str, extension_out: str, name_range: tuple[int, int]):
    files = os.listdir()
    print(f'{files=}')
    _m, m_ = name_range
    for ind, file in enumerate(files):
        name, ext = file.split('.')
        if ext != 'py':
            if len(s := str(ind)) > digits_num:
                raise ValueError('The sequence number is out of range!!!')
            sequence_num = '0' * (digits_num - len(s)) + str(s)
            if ext == extension_in:
                os.rename(file, (name[_m: m_ + 1] if _m <= len(name) <= m_ else name) + desired_file_name + sequence_num + f'.{extension_out}')


files_renaming('file', 3, 'txt', 'dll', (2, 4))


