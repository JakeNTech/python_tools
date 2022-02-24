#!/usr/bin/env python3
import argparse
import zipfile
import itertools
import string

def getargs():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", dest="input_file", help="Name of the zip file to open", metavar="<filename>",required=True)
	parser.add_argument("-w", "--word-list", dest="word_list", help="Name of the word list to open", metavar="<filename>", required=True)
	parser.add_argument("-n","--number",dest="number",help="Define the ammount of numbers to add to the end of the password e.g. 9999", metavar="<integer>",default="0")
	parser.add_argument("-l","--letters",dest="letters",help="Add letters to the end of a password, number specifies how many letters",metavar="<integer>", default="0")
	parser.add_argument("-s","--symbols",dest="symbols",help="Add symbols to the end of a password, number specifies how many symbols",metavar="<integer>",default="0")
	parser.add_argument("-a","--all",dest="all",help="Add letters, numbers and sybmbols to the end of words ",metavar="<integer>",default="0")
	return parser.parse_args()

def extract(zip_file,password):
	try:
		zip_file.extractall(pwd=bytes(password, encoding='utf-8'))
		return password
	except:
		return False

def cracker(zipFile_name,passwordFile_name):
	#Open Zip file using the name that was taken form the command line input
	zipFile = zipfile.ZipFile(zipFile_name)
	passwordFile = open(passwordFile_name)
	#Could load word file into array but that seems in-efficient
	for line in passwordFile.readlines():
		password = line.strip("\n")
		if extract(zipFile,password) != False:
			print("Password Found: ", password)
			exit()
	print("Password not found!")		

def cracker_with_numbers(zipFile_name,passwordFile_name,max_number):
	max_number = int(max_number)
	zipFile = zipfile.ZipFile(zipFile_name)
	passwordFile = open(passwordFile_name)
	for line in passwordFile.readlines():
		password = line.strip("\n")
		for i in range(0,max_number):
			new_password = password + str(i)
			if extract(zipFile,new_password) != False:
				print("Password Found: ", new_password)
				exit()
	print("Password not found!")

def cracker_with_letters(zipFile_name,passwordFile_name,max_letters):
	max_letters = int(max_letters)
	chars = string.ascii_letters
	zipFile = zipfile.ZipFile(zipFile_name)
	passwordFile = open(passwordFile_name)
	for line in passwordFile.readlines():
		password = line.strip("\n")
		for guess in itertools.product(chars, repeat=max_letters):
			guess = ''.join(guess)
			guess = password + guess
			if extract(zipFile,guess) != False:
				print("Password Found: ", guess)
				exit()
	print("Password not found!")

def cracker_with_symbols(zipFile_name,passwordFile_name,max_symbols):
	max_letters = int(max_symbols)
	chars = string.punctuation
	zipFile = zipfile.ZipFile(zipFile_name)
	passwordFile = open(passwordFile_name)
	for line in passwordFile.readlines():
		password = line.strip("\n")
		for guess in itertools.product(chars, repeat=max_letters):
			guess = ''.join(guess)
			guess = password + guess
			if extract(zipFile,guess) != False:
				print("Password Found: ", guess)
				exit()
	print("Password not found!")

def all(zipFile_name,passwordFile_name,max_symbols):
	max_letters = int(max_symbols)
	chars = string.printable
	zipFile = zipfile.ZipFile(zipFile_name)
	passwordFile = open(passwordFile_name)
	for line in passwordFile.readlines():
		password = line.strip("\n")
		for guess in itertools.product(chars, repeat=max_letters):
			guess = ''.join(guess)
			guess = password + guess
			if extract(zipFile,guess) != False:
				print("Password Found: ", guess)
				exit()
	print("Password not found!")

if __name__ == "__main__":
	arguments = getargs()
	if arguments.number != "0" and arguments.letters != "0" and arguments.symbols != "0" and arguments.all != "0":
		print("Sorry! Only one option at a time can be used!")
	elif arguments.letters != "0":
		print("-l Option Selected!")
		cracker_with_letters(arguments.input_file,arguments.word_list, arguments.letters)
	elif arguments.symbols != "0":
		print("-s Option selected!")
		cracker_with_symbols(arguments.input_file,arguments.word_list, arguments.symbols)
	elif arguments.all != "0":
		print("-a Option selected...")
		print("Good luck!")
		all(arguments.input_file,arguments.word_list, arguments.all)
	elif arguments.number != "0":
		print("-n Option Selected!")
		cracker_with_numbers(arguments.input_file,arguments.word_list, arguments.number)
	else:
		print("No additional options added!")
		cracker(arguments.input_file,arguments.word_list)