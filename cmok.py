#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from classes import Cmok
import logging
from classes import Bot

TOKEN = '983511418:AAHNxHWuQvJfAxvmDelinu5F8lGJXo1ryVc'

bot = Bot(TOKEN)

parser = argparse.ArgumentParser(description='Скрипт для брутфорса хешей sha-512')
parser.add_argument('hash', metavar='HASH', help='Хеш искомого пароля в кавычках, или путь к файлу с хешем')
parser.add_argument('-w', metavar='word_list',
                    help='Путь к словарю. Если указать словарь, подбор будет только по словарю. Не указывайте, если нужен полный перебор по символам.')
parser.add_argument('-min', metavar='min_length', type=int, help='Минимальная длина пароля для подбора', default=1)
parser.add_argument('-max', metavar='max_length', type=int, help='Максимальная длина пароля для подбора', default=4)
parser.add_argument('-l', action='store_true', help='Пароль содержит буквы', default=False)
parser.add_argument('-u', action='store_true', help='Пароль содержит буквы верхнего регистра', default=False)
parser.add_argument('-n', action='store_true', help='Пароль содержит цифры', default=False)
parser.add_argument('-m', help='Пользовательский набор символов', default='')

args = parser.parse_args()

cmok = Cmok(args.hash, bot, args.min, args.max)

# начало работы программы
if cmok.ready():

    # настраиваем стек символов для подбора в зависимости от передынных параметров
    symbols = ''
    symbols += 'qwertyuiopasdfghjklzxcvbnm' if args.l else ''
    symbols += 'QWERTYUIOPASDFGHJKLZXCVBNM' if args.u else ''
    symbols += '1234567890' if args.n else ''
    symbols += args.m
    cmok.add_symbols(symbols)

    if args.w is not None:
        wordlist = open(args.w)
        cmok.set_wordlist(wordlist)

    cmok.run()
    logging.info(cmok)
