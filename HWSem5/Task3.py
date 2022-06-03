#  Вот вам текст:
# «Ну, вышел я, короче, из подъезда. В общем, короче говоря, шел я, кажется, в магазин.
# Ну, эээ, в общем, было лето, кажется. Как бы тепло. Солнечно, короче. Иду я, иду, в общем,
# по улице, а тут, короче, яма. Я, эээээ…. Упал в нее. И снова вышел, короче, из подъезда.
# Ясен пень, в магазин. В общем, лето на дворе, жарко, солнечно, птицы, короче, летают.
# Кстати, иду я по улице, иду, а тут, короче, яма. Ну, я в нее упал, в общем. Вышел из подъезда, короче.
# Лето на дворе, ясен пень. Птицы поют, короче, солнечно. В общем, в магазин мне надо.
# Что-то явно не так, короче. «Рекурсия», - подумал я. Ээээ...короче, в общем, пошел другой дорогой
# и не упал в эту… ээээ… яму. Хлеба купил».

# Отфильтруйте его, чтобы эту фигню можно было прочесть. Предусмотрите вариант, что мусорные слова могли быть написаны без использования запятых.

def filter_text(file_path: str) -> None:
    filler_words = ['короче говоря', 'короче', 'кстати', 'эээээ', 'ээээ', 'эээ', 'кажется', 'ясен пень', 'в общем', 'ну', 'как бы']

    with open(file_path, "r", encoding='utf-8') as file:
        test_line = file.readline().lower()
        print(test_line)
        for filler_word in filler_words:
            test_line = test_line.replace(', ' + filler_word, '')
        for filler_word in filler_words:
            test_line = test_line.replace(' ' + filler_word, '')
        for filler_word in filler_words:
            test_line = test_line.replace(filler_word, '')

    while test_line[1] == ',' or test_line[1] == ' ' or test_line[1] == '...':
        test_line = test_line[1:]

    test_line = '«' + test_line

    with open(file_path, "w", encoding='utf-8') as file:
        file.write(test_line)


filter_text('Хлебная_Дичь.txt')
