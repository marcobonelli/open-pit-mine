#coding: utf-8

# funcao que realiza a leitura do arquivo de blocos e retorna todos os dados, em formato de lista
def ler_blocos(ArqBloco):

	database = [line.rstrip('\n') for line in open(ArqBloco.encode('utf-8'))]
	
	for i in range(0, len(database)):
		database[i] = database[i].split(' ')
		for j in [0, 1, 2, 3, 10]:
			database[i][j] = int(database[i][j])
		for j in [5, 6, 7, 8, 9]:
			database[i][j] = float(database[i][j])

	return database

# funcao que realiza a leitura do arquivo contendo o upit e retorna somente os blocos pertencentes ao upit, em formato de lista
def ler_upit(ArqUpit):

	database = [line.rstrip('\n') for line in open(ArqUpit.encode('utf-8'))]
	
	upit = []
	for i in range(len(database)):
		database[i] = database[i].split(' ')
		database[i] = [int(database[i][0]), float(database[i][1])]
		upit.append(database[i][0])

	return upit

# funcao que realiza a leitura do arquivo de precedencia de blocos e retorna todos os dados, em formato de lista
def ler_precedencia(ArqPrecedncia):

	database = [line.rstrip('\n') for line in open(ArqPrecedncia.encode('utf-8'))]

	for i in range(0, len(database)):
		database[i] = database[i].split(' ')
		for j in range(0, len(database[i])):
			database[i][j] = int(database[i][j])

	return database

# funcao que retorna todos os dados referentes ao blocos que pertencem ao upit, em formato de lista
def gerar_blocos_upit(ArqBloco, ArqUpit):

	blocos = ler_blocos(ArqBloco)
	upit = ler_upit(ArqUpit)

	database = []
	for i in upit:
		database.append(blocos[i])

	return database

# funcao que retorna todos os dados referentes ao blocos precedentes que pertencem ao upit, em formato de lista
def gerar_precedentes_upit(ArqPrecedncia,ArqUpit):

	precedencia = ler_precedencia(ArqPrecedncia)
	upit = ler_upit(ArqUpit)

	for k in range(len(precedencia) - len(upit)):
		for i in range(len(precedencia)):
			for j in range(2, 2 + precedencia[i][1]):
				if precedencia[i][j] not in upit:
					precedencia[i].remove(precedencia[i][j])
					precedencia[i][1] = precedencia[i][1] - 1
					break 

	database = []
	for i in upit:
		database.append(precedencia[i])

	return database

# funcao que retorna todos os dados referentes aos blocos vizinhos pertencentes ao upit, em formato de lista
def gerar_vizinhos_upit(ArqPrecedncia,ArqUpit):
	
	blocos = ler_precedencia(ArqPrecedncia)
	upit = ler_upit(ArqUpit)

	for i in range(len(blocos)):
		blocos[i].remove(blocos[i][1])

	for i in range(len(blocos)):
		for j in range(len(blocos)):
			if i != j and i in blocos[j]:
				blocos[i].append(blocos[j][0])
		blocos[i] = sorted(set(blocos[i]))

	for k in range(len(blocos) - len(upit)):
		for i in range(len(blocos)):
			for j in range(len(blocos)):
				if blocos[i][j] not in upit:
					blocos[i].remove(blocos[i][j])
					break 

	database = []
	for i in upit:
		database.append(blocos[i])
	
	return database

'''if __name__ == '__main__':

	print('leitura das informacoes sobre blocos iniciada:')
	blocos = gerar_blocos_upit()
	print('\t--> concluido.\n')

	print('leitura das precedencias dos blocos iniciada:')
	precedentes = gerar_precedentes_upit()
	print('\t--> concluido.\n')

	print('leitura das vizinhancas dos blocos iniciada:')
	vizinhos = gerar_vizinhos_upit()
	print('\t--> concluido.\n')
'''
