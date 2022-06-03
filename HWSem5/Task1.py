# 1. Напишите программу, удаляющую из текста все слова содержащие "абв". Используйте знания с последней лекции. Выполните ее в виде функции.

def delete_char_sequence(text: list[str]) -> list:
    return list(filter(lambda x: x.find('абв') == -1, text))


print(delete_char_sequence(['лалалабвло', 'фбтатамв', 'абабавв']))
