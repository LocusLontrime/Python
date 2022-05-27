# Определите функцию, которая удаляет весь текст, следующий за любым из переданных маркеров комментариев. Любые пробелы в конце строки также должны быть удалены.
# Пример:
# Входные данные:
# «apples, pears # and bananas
# grapes
# bananas !apples          »
# Выходные данные:
# «apples, pears
# grapes
# bananas»
# Функция может вызываться вот так:
# result = function("apples, pears # and bananas\ngrapes\nbananas !apples", ["#", "!"])


def remove_comments(text: str, list_of_symbols: list) -> str:
    strs = text.split('\n')
    result = ''
    for curr_str in strs:
        flag = False
        for char in curr_str:
            if char in list_of_symbols:
                curr_str = curr_str[:curr_str.find(char)]
                # print(f'curr_str = {curr_str}')
                result += curr_str + '\n'
                flag = True
        if not flag:
            result += curr_str + '\n'
    result = result[:len(result) - 1]
    return result

s = 'Ruslan is hacking: GeekBrains now'

s = s[: s.find(":")]

print(s)

print(remove_comments("apples, pears # and bananas\ngrapes\nbananas !apples", ["#", "!"]))

