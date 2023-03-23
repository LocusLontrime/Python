# -*- coding: utf-8 -*-


# 1. Напишите функцию, которая принимает на вход строку - абсолютный путь до файла.
# Функция возвращает кортеж из трёх элементов: путь, имя файла, расширение файла.
import os


def get_file_info(file_path: str) -> tuple[str, str, str]:
    file_name, extension = os.path.basename(file_path).split(".")
    return os.path.dirname(file_path), file_name, extension


print(f'path, file name, extension: {get_file_info("C:/Users/langr/PycharmProjects/AmberCode/Dive_into_python/HomeWork5/File_path.py")}')


