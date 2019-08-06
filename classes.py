#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools as it
import datetime
import re
import crypt

# import only system from os 
from os import system, name 


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
		self.__history = ''
		self.__max_l = maxl
		self.__min_l = minl
		self.__hash = Hash()
		self.__word = ''

		# пытаемся сконвертировать хеш сначала напрямую, потом из файла
		res = re.split(r'\$', _hash)
		if len(res) > 2:
			self.__hash = Hash(res[1], res[2], res[3])
		else:
			f = open(_hash)
			for line in f:
				res = re.split(r'\$', line.strip())
				if len(res) > 2:
					self.__hash = Hash(res[1], res[2], res[3])
					break;

	def ready(self):
		return True;

	def run(self):
		self.dysplay()
		if self.__wordlist is not None:
			self.bruteforce_by_wordlist()

		self.bruteforce()
		self.dysplay()

	def to_string(self):
		view = '=================================================\n'
		view += self.__hash.to_string()
		view += '\n'
		view += self.__history
		view += self.status()
		view += '\n'
		view += self.__word
		view += '\n'
		return view

	def set_wordlist(self, wordlist):
		self.__wordlist = wordlist

	def iteration(self):
		self.__iterations += 1

	def add_history(self, text):
		today = datetime.datetime.today()
		self.__history += "# {} | {}\n".format(today.strftime("%d-%m-%Y-%H.%M.%S"), text)

	def check(self):
		self.iteration()
		self.dysplay()
		if sha512(self.__word, self.__hash.salt) == self.__hash.to_string():
			self.__status = 1
			self.add_history('Найден пароль: {}'.format(self.__word))
			return True
		else: return False

	def add_symbols(self, symbols):
		self.__symbols += symbols

	# функция перебора по символам в строке symbols
	def bruteforce (self):

		# если пароль найден, ничего не делаем
		if self.__status == 1:
			return False

		if len(self.__symbols) == 0:
			self.add_history('Список символов для перебора пуст. Невозможно запустить цмока')
			return False

		self.__status = 4
		self.add_history('Начинаю подбор пароля по символам из строки {}'.format(self.__symbols))

		for l in range(self.__min_l, self.__max_l + 1):
			all = it.permutations(self.__symbols, l)
			for p in all:
				self.__word = ''.join(p);
				if self.check():
					break;
			if self.__status == 1:
				break;

	def bruteforce_by_wordlist(self):
		# если пароль найден, ничего не делаем
		if self.__status == 1:
			return False

		self.__status = 3
		self.add_history('Начинаю подбор пароля по словарю')

		list = self.__wordlist.read().splitlines()
		for l in list:
			self.__word = l
			if self.check():
				break;

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

	def dysplay(self):
		clear_dysplay()
		print(self.__history)
		print('**********')
		print(self.status())
		print('Всего попыток: {}'.format(self.__iterations))
		colored(self.__word, bcolors.WARNING)

class Hash:
	"""docstring for Hash"""
	def __init__(self, type = '', salt = '', hash = ''):
		self.type = type
		self.salt = salt
		self.hash = hash
	
	def __str__(self):
		return '${}${}${}'.format(self.type, self.salt, self.hash)

	def to_string(self):
		return '${}${}${}'.format(self.type, self.salt, self.hash)

# функция хеширования
def sha512 (word, salt):
	prefix = '$6$'
	return crypt.crypt(word, prefix + salt)

# define our clear function 
def clear_dysplay(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colored(text, color):
	print (color + text + bcolors.ENDC)