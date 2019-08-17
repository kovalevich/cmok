#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from classes import Cmok 
import datetime
import threading
import time

# ======================= settings

# количество потоков
COUNT_THREADS = 10
# файл для записи логов
LOG_FILE_NAME = "logs.txt"
 
parser = argparse.ArgumentParser(description='Скрипт для брутфорса хешей sha-512')
parser.add_argument('hash', metavar='HASH', help='Хеш искомого пароля в кавычках, или путь к файлу с хешем')
parser.add_argument('-w', metavar='word_list', help='Путь к словарю. Если указать словарь, подбор будет только по словарю. Не указывайте, если нужен полный перебор по символам.')
parser.add_argument('-min', metavar='min_length', type=int, help='Минимальная длина пароля для подбора', default=1)
parser.add_argument('-max', metavar='max_length', type=int, help='Максимальная длина пароля для подбора', default=4)
parser.add_argument('-l', action='store_true', help='Пароль содержит буквы', default=False)
parser.add_argument('-u', action='store_true', help='Пароль содержит буквы верхнего регистра', default=False)
parser.add_argument('-n', action='store_true', help='Пароль содержит цифры', default=False)
parser.add_argument('-m', help='Пользовательский набор символов', default='')


def main():

	global COUNT_THREADS;
	
	# получаем параметры из коммандной строки
	args = parser.parse_args()

	cmok = Cmok(args.hash, args.min, args.max)
	symbols = ''
	symbols += 'qwertyuiopasdfghjklzxcvbnm' if args.l else ''
	symbols += 'QWERTYUIOPASDFGHJKLZXCVBNM' if args.u else ''
	symbols += '1234567890' if args.n else ''
	symbols += args.m
	cmok.add_symbols(symbols)
	cmok.ready()

	threads = []

	thread_generator = threading.Thread(target=cmok.generator)
	thread_generator.start()

	# создаем необходимое количество потоков
	for i in xrange(COUNT_THREADS):
		thread_ = threading.Thread(target=cmok.check, args = (thread_generator, ))
		thread_.start()
		threads.append(thread_)
		cmok.add_history("Запускаю перебор в потоке #{}".format(i))

	cmok.display()

	while threading.active_count() > 1:
		cmok.display()
		if cmok.status() == 1: 
			for t in threads:
				t.join()
		time.sleep(1)

	cmok.display()

def check(name):
	print('thread {} start'.format(name))
	time.sleep(2)
	print('thread {} fin'.format(name))

def log(text):
	return True

main()