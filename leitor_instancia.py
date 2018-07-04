#coding: utf-8

def ler_blocos():

	database = [line.rstrip('\n') for line in open('newman1.blocks')]

	return 0

def ler_upit():

	database = [line.rstrip('\n') for line in open('newman1.upit')]
	
	upit = []
	for i in range(len(database)):
		database[i] = database[i].split(' ')
		database[i] = [int(database[i][0]), float(database[i][1])]
		upit.append(database[i][0])

	return upit

def ler_precedencia():

	database = [line.rstrip('\n') for line in open('newman1.prec')]

	return 0

ler_upit()
