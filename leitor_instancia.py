#coding: utf-8

# realiza a leitura do arquivo de blocos e retorna todos os dados, em formato de lista
def ler_blocos():

	database = [line.rstrip('\n') for line in open('newman1.blocks')]
	
	for i in range(0, len(database)):
		database[i] = database[i].split(' ')
		for j in [0, 1, 2, 3, 10]:
			database[i][j] = int(database[i][j])
		for j in [5, 6, 7, 8, 9]:
			database[i][j] = float(database[i][j])

	return database

# realiza a leitura do arquivo contendo o upit e retorna somente os blocos pertencentes ao upit, em formato de lista
def ler_upit():

	database = [line.rstrip('\n') for line in open('newman1.upit')]
	
	upit = []
	for i in range(len(database)):
		database[i] = database[i].split(' ')
		database[i] = [int(database[i][0]), float(database[i][1])]
		upit.append(database[i][0])

	return upit

# realiza a leitura do arquivo de precedencia de blocos e retorna todos os dados, em formato de lista
def ler_precedencia():

	database = [line.rstrip('\n') for line in open('newman1.prec')]

	for i in range(0, len(database)):
		database[i] = database[i].split(' ')
		for j in range(0, len(database[i])):
			database[i][j] = int(database[i][j])

	return database

# retorna todos os dados referentes ao blocos que pertencem ao upit, em formato de lista
def gerar_blocos_upit():

	blocos = ler_blocos()
	upit = ler_upit()

	database = []
	for i in upit:
		database.append(blocos[i])

	return database
