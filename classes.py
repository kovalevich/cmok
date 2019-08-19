#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools as it
from datetime import datetime
import re
import crypt
import time
import io
from Queue import Queue

# import only system from os 
from os import system, name 


# класс цмока
class Cmok:
	
	def __init__(self, _hash, minl, maxl):
		self.__iterations = 0
		self.__wordlist = None
		self.__symbols = ''
		self.__status = 0
		self.__start_time = datetime.now() 
		self.__end_time = datetime.now()
		self.__log = {}
		self.__max_l = maxl
		self.__min_l = minl
		self.__hash = Hash()
		self.__word = ''
		self.__last_display_time = time.time()
		self.__words = Queue()

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
		self.__add_log("Find hash: {}".format(self.__hash))

	def ready(self):
		self.__status = 3;
		return True;

	def generator(self):
		self.__add_log("Start generator from {}".format(self.__symbols).decode())
		for l in range(self.__min_l, self.__max_l + 1):
			all = it.product(self.__symbols, repeat = l)
			for p in all:
				if self.__status < 3: return True
				if self.__words.qsize() > 1000: time.sleep(1)
				self.__words.put(''.join(p))
		for _ in xrange(30): self.__words.put(None)
		self.__add_log("Generator finish {}".format(self.__timer()))

	def __str__(self):
		view = 'CMOK=================================================\n'
		view += '\n'
		view += self.__history
		view += self.status()
		view += '\n'
		return "{}".format(view)
	
	def __unicode__(self):
		view = '=================================================\n'
		view += str(self.__hash)
		view += '\n'
		view += self.__history
		view += self.status()
		view += '\n'
		return u"{}".format(view)

	def count_words(self):
		return self.__words.qsize()

	def set_wordlist(self, wordlist):
		self.__wordlist = wordlist

	def iteration(self):
		self.__iterations += 1
		
	def logs(self): return self.__log

	def __add_log(self, text):
		self.__log[datetime.now()] = text
		print("# {}".format(text))
	
	def add_log(self, text): self.__add_log(text)

	def check(self, generator):
		while self.__status == 3:
			word = self.__words.get()
			if word == None and not generator.is_alive(): break
			if word == None: continue
			self.iteration()
			self.__word = word
			if sha512(word, self.__hash.salt) == str(self.__hash):
				self.__status = 1
				self.__add_log('PASSWORD: {} find by {}'.format(word, self.__timer()))			
				break
			self.__words.task_done()
		if self.__status > 2: self.__status = 2

	def add_symbols(self, symbols):
		self.__symbols += symbols

	def status(self, flag = False):
		if flag: return self.__status
		if self.__status == 0:
			return 'Поиск не запущен'
		if self.__status == 1:
			return 'Поиск завершен успешно!'
		if self.__status == 2:
			return 'Поиск завершен безуспешно :('
		if self.__status == 3:
			return 'Идет поиск по словарю'

	def display(self):
		if time.time() - self.__last_display_time < 10:
			return False
		colored(self.__word, bcolors.WARNING)
		self.__last_display_time = time.time()
	
	def __timer(self):
		now = datetime.now()
		return now - self.__start_time
		
	def write_log_in_file(self, file_name):
		with io.open(file_name, "a") as out:
			out.write(u"******************************************\n")
			for date, log in self.__log.items():
				#print("{} => {}\n".format(date, log))
				out.write(u"{} => {}\n".format(date, log))

class Hash:
	"""docstring for Hash"""
	def __init__(self, type = '', salt = '', hash = ''):
		self.type = type
		self.salt = salt
		self.hash = hash
	
	def __str__(self):
		return '${}${}${}'.format(self.type, self.salt, self.hash)
	
	def __unicode__(self):
		return u'${}${}${}'.format(self.type, self.salt, self.hash)

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
