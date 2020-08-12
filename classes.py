#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools as it
import re
import crypt
import logging

# import only system from os 
from os import system, name


class Hash:
    """Класс хэш"""

    def __init__(self, type_, salt, hash_):
        self.type = type_
        self.salt = salt
        self.hash = hash_

    def __str__(self):
        return '${}${}${}'.format(self.type, self.salt, self.hash)


class Color:

    """Класс для колеровки текста в терминале"""

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def warning(cls, text: str) -> str:
        return cls.WARNING + text + cls.ENDC

    @classmethod
    def fail(cls, text: str) -> str:
        return cls.FAIL + text + cls.ENDC

    @classmethod
    def ok(cls, text: str) -> str:
        return cls.OKGREEN + text + cls.ENDC

    @classmethod
    def info(cls, text: str) -> str:
        return cls.OKBLUE + text + cls.ENDC


# класс цмока
class Cmok():
    """docstring for Cmok"""

    def __init__(self, _hash, minl, maxl):
        self.__iterations = 0
        self.__status = 0
        self.__wordlist = None
        self.__symbols = ''
        self.__start_time = ''
        self.__end_time = ''
        self.__max_l = maxl
        self.__min_l = minl
        self.__hash = None
        self.__word = ''

        # настройки логирования
        logging.basicConfig(filename='cmok.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.DEBUG)

        # пытаемся сконвертировать хеш сначала напрямую, потом из файла
        res = _hash.split('$')
        if len(res) > 2:
            self.__hash = Hash(res[1], res[2], res[3])
        else:
            f = open(_hash)
            for line in f:
                res = re.split(r'\$', line.strip())
                if len(res) > 2:
                    self.__hash = Hash(res[1], res[2], res[3])
                    break

    def ready(self):
        return True if self.__hash is not None else False

    def run(self):
        logging.info(f'Начало работы по {self.__hash}')
        self.display()
        if self.__wordlist is not None:
            self.bruteforce_by_wordlist()

        self.bruteforce()
        self.display()

    def __str__(self):
        return f'Cmok: symbols({self.__symbols})'

    def set_wordlist(self, wordlist):
        self.__wordlist = wordlist

    def iteration(self):
        self.__iterations += 1

    def check(self):
        self.iteration()
        self.display()
        if sha512(self.__word, self.__hash.salt) == str(self.__hash):
            self.__status = 1
            logging.info('Найден пароль: {}'.format(self.__word))
            return True
        else:
            return False

    def add_symbols(self, symbols):
        self.__symbols += symbols

    # функция перебора по символам в строке symbols
    def bruteforce(self):

        # если пароль найден, ничего не делаем
        if self.__status == 1:
            return False

        if len(self.__symbols) == 0:
            logging.warning('Список символов для перебора пуст. Невозможно запустить цмока')
            return False

        self.__status = 4
        logging.info('Начинаю подбор пароля по символам из строки {}'.format(self.__symbols))

        for pass_len in range(self.__min_l, self.__max_l + 1):
            set_words = it.permutations(self.__symbols, pass_len)
            for word in set_words:
                self.__word = ''.join(word)
                if self.check():
                    break
            if self.__status == 1:
                break

    def bruteforce_by_wordlist(self):
        # если пароль найден, ничего не делаем
        if self.__status == 1:
            return False

        self.__status = 3
        logging.info(f'Начинаю подбор пароля по словарю')

        list_ = self.__wordlist.read().splitlines()
        for word in list_:
            self.__word = word
            if self.check():
                break

    def status(self):
        if self.__status == 0:
            return 'Поиск не запущен'
        if self.__status == 1:
            return 'Поиск завершен успешно!'
        if self.__status == 2:
            return 'Поиск завершен безуспешно :('
        if self.__status == 3:
            return 'Идет поиск по словарю'
        if self.__status == 4:
            return 'Идет поиск перебором по символам {}'.format(self.__symbols)

    def display(self):
        """Метод отображает состояние в консоль"""
        clear_display()
        print(f'Поиск для {Color.info(str(self.__hash))}\n'
              f'************\n'
              f'{self.status()}\nВсего попыток: {self.__iterations}\n{Color.warning(self.__word)}')


# функция хеширования
def sha512(word, salt):
    prefix = '$6$'
    return crypt.crypt(word, prefix + salt)


# define our clear function 
def clear_display():
    # for windows 
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
