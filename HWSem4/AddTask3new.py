# Вот вам файл с английскими именами. https://cloud.mail.ru/public/J7aq/iHnLspVJR
# Начните с сортировки в алфавитном порядке. Затем подсчитайте алфавитные значения каждого имени и умножьте это значение на
# порядковый номер имени в отсортированном списке для получения количества очков имени.
# Например, если список отсортирован по алфавиту, имя COLIN (алфавитное значение которого 3 + 15 + 12 + 9 + 14 = 53)
# является 938-м в списке. Поэтому, имя COLIN получает 938 × 53 = 49714 очков.
# Какова сумма очков имен в файле?


def get_scores():
    names_dictionary = dict([(chr(i), i - 65) for i in range(65, 91)])  # 36 98 989
    names = []
    result_scores = 0

    def get_name_score(curr_name: str):
        result_sum = 0
        for character in curr_name:
            result_sum += names_dictionary[character]
        return result_sum

    with open("english_names.txt", "r") as file:
        str_names = file.readline()
        names_quote = str_names.split(',')
        for name in names_quote:
            names.append(name.strip('"'))
    names = sorted(names)

    for name_index in range(len(names)):
        result_scores += name_index * get_name_score(names[name_index])

    return result_scores


print(get_scores())

