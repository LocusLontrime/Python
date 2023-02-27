import controller


class View:

    def __init__(self):
        self.commander = controller.Commander()

    def work(self):
        flag = True
        print('Система учёта животных. Для просмотра команд введите "help"')
        while flag:
            command = input('Ваша команда: ')
            match command:
                case 'help':
                    print('Список доступных команд:\n'
                          '"exit" - выйти из программы\n'
                          '"add" - добавить (завести) новое животное\n'
                          '"info" - получить информацию о животном\n'
                          '"train" - обучить животное новой команде\n'
                          '')
                case 'exit':
                    print('Завершение работы...')
                    flag = False
                case 'add':
                    print('Введите информацию в формате: Имя,дд-мм-гггг,цифра_от_1_до_6\n'
                          'где 1- кот, 2- собака, 3- хомяк, 4- конь, 5- жираф, 6- осел')
                    answer = input('Ответ: ').split(',')
                    self.commander.add_animal(answer[0], answer[1], int(answer[2]))
                case 'info':
                    print('Введите животное, информацию о котором хотите просмотреть, в формате:\n'
                          'Имя,цифра_от_1_до_6\nгде 1- кот, 2- собака, 3- хомяк, 4- конь, 5- жираф, 6- осел')
                    answer = input('Ответ: ').split(',')
                    self.commander.print_list_command(int(answer[1]), answer[0])
                case 'train':
                    print('Введите животное, которого хотите обучить, и команде в формате:\n'
                          'Имя,цифра_от_1_до_6,команда\nгде 1- кот, 2- собака, 3- хомяк')
                    answer = input('Ответ: ').split(',')
                    self.commander.train_pets(int(answer[1]), answer[0], answer[2])
                case _:
                    print('Неверная команда, для просмотра списка команд введите "help"')

