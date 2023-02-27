import controller


class View:

    def __init__(self):
        self.commander = controller.Commander()

    def work(self):
        flag = True
        print('������� ����� ��������. ��� ��������� ������ ������� "help"')
        while flag:
            command = input('���� �������: ')
            match command:
                case 'help':
                    print('������ ��������� ������:\n'
                          '"exit" - ����� �� ���������\n'
                          '"add" - �������� (�������) ����� ��������\n'
                          '"info" - �������� ���������� � ��������\n'
                          '"train" - ������� �������� ����� �������\n'
                          '')
                case 'exit':
                    print('���������� ������...')
                    flag = False
                case 'add':
                    print('������� ���������� � �������: ���,��-��-����,�����_��_1_��_6\n'
                          '��� 1- ���, 2- ������, 3- �����, 4- ����, 5- �����, 6- ����')
                    answer = input('�����: ').split(',')
                    self.commander.add_animal(answer[0], answer[1], int(answer[2]))
                case 'info':
                    print('������� ��������, ���������� � ������� ������ �����������, � �������:\n'
                          '���,�����_��_1_��_6\n��� 1- ���, 2- ������, 3- �����, 4- ����, 5- �����, 6- ����')
                    answer = input('�����: ').split(',')
                    self.commander.print_list_command(int(answer[1]), answer[0])
                case 'train':
                    print('������� ��������, �������� ������ �������, � ������� � �������:\n'
                          '���,�����_��_1_��_6,�������\n��� 1- ���, 2- ������, 3- �����')
                    answer = input('�����: ').split(',')
                    self.commander.train_pets(int(answer[1]), answer[0], answer[2])
                case _:
                    print('�������� �������, ��� ��������� ������ ������ ������� "help"')

