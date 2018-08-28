#coding: utf-8

import TemplatePD as tpd
import sys
import math
import random
import numpy
import copy as c
from numpy.random import standard_normal, normal
from numpy import array, zeros, sqrt, shape
from pylab import *
from leitorXML import *
from gurobipy import *

import leitor_instancia as instancia

class ProblemaOPM(tpd.Problema):
  # criar a classe problema
  # puxar dados do xml
  ''' Classe com os parametros que definem a instancia do problema
	  Objetivo: Gerenciar a instância do problema
	  Métodos Obrigatórios: 
			   - Leitura
			   - ImprimeResultados
			   - SalvaResultados
	  Variáveis Obrigatórias:
			   - Arquivo de entrada
			   - Nome da Instância            
  '''
  def __init__(self, InstPar):
	'''
	   Construtor
	   \par InstPar - Lista de parametros das instancia
	   DEVE SER SOBRESCRITO 

	'''
	self.Leitura(InstPar.InstArq)  
	#return 0

  def Leitura(self, ArqEntrada):
	'''
		Metodo para carregamento de dados das instancias
		\par ArqEntrada  - Nome do arquivo de entrada
		DEVE SER SOBRESCRITO
	'''
	Instancia = LerXML(ArqEntrada)
	dadosIn =  Instancia["Incerteza"]
	dadosMin = Instancia["Mina"]
	dadosSim = Instancia["Simulador"]
	[self.B, self.P, self.N] = self.CriaBloco(dadosMin['Arqblocos'], dadosMin['Arqprec'], dadosMin['Arqupit']) 
	self.p0 = dadosIn['p0']
	self.precomedio = dadosIn['precomedio']
	self.desviopreco = dadosIn['desviopreco']
	self.H = dadosIn['H']
	self.dt = dadosIn['dt']
	return 0

  def CriaBloco(self, ArqBloco, ArqPrecedncia, ArqUpit):

	print('leitura das informacoes sobre blocos iniciada:')
	blocos = instancia.gerar_blocos_upit(ArqBloco, ArqUpit)
	print('\t--> concluido.\n')

	print('leitura das precedencias dos blocos iniciada:')
	precedentes = instancia.gerar_precedentes_upit(ArqPrecedncia, ArqUpit)
	print('\t--> concluido.\n')

	print('leitura das vizinhancas dos blocos iniciada:')
	vizinhos = instancia.gerar_vizinhos_upit(ArqPrecedncia, ArqUpit)
	print('\t--> concluido.\n')
	
	return [blocos, precedentes, vizinhos]

  def ImprimeResultados(self):
	'''
		Metodo para impressao de resultados da analise
		DEVE SER SOBRESCRITO
	'''
	return 0 

  def SalvaResultados(self, ArqSaida):
	'''
		Metodo para escrita detalhada de resultados da analise
		\par ArqSaida  - Nome do arquivo de saida
		DEVE SER SOBRESCRITO
	'''
	return 0 

  def CriaEstado(self):

	vEstado = EstadoOPM([self.B,self.P,self.N,self.p0])
	vEstado.imprime()
	return vEstado

class GeraIncerteza(tpd.GeraIncerteza):
  ''' Classe que gera a incerteza do problema
	  Objetivos: 1) Gerar incerteza
	  Métodos Obrigatórios: 
				- geracao()
				- CalcValor(self): 
	  Variáveis Obrigatórias:
				 
  '''

  def __init__(self,vDecisao,ParInc):
	'''
	   Construtor
	   \par vEstado - instancia da classe Estado
	   \par vDecisao - instancia da classe Decisao
	   \par vEstagio - inteiro com a informação do estagio atual
	   \par ParInc - lista com parâmetros para realizacao da incerteza
	   ParInc[0] = p_inicial
	   ParInc[1] = H
	   ParInc[2] = dt
	   ParInc[3] = sigma
	   ParInc[4] = mu
	   **ParInc[5] = nSimu

	   DEVE SER SOBRESCRITO
	''' 

	self.p_inicial = ParInc[0] 
	self.H = ParInc[1]       
	self.dt = ParInc[2]     
	self.sigma = ParInc[3]     
	self.mu = ParInc[4]     
	self.nSimu = 100  
	

  def incertezaPrecoMinerio():   

	N = round(self.H / self.dt); 
	t = numpy.linspace(0, T, N)
	W = standard_normal(size = N)
	W = numpy.cumsum(W)*numpy.sqrt(dt) ### standard brownian motion ###
	X = (self.mu-0.5*self.sigma**2)*t + self.sigma*W 
	S = self.p_inicial*numpy.exp(X) ### geometric brownian motion ###
	#plot(t, S)
	#show()

	return S[1]    

  def incertezasVizinhos(self, vEstado, vDecisao):
	#arquivo = open ('/Users/matheusteixeira/Google Drive/UFOP/8º Periodo/Programacao Dinamica/estruturaprecedencia.txt', 'w')

	for r in vDecisao.removidos:
		vEstado.removeBlock(r)

	expected = []
	dataB = vEstado.B # copy?
	dataP = vEstado.precedence
	neighbors = vEstado.N

	for line in range(0, len(dataB)):
		expected.append([])
		for collumn in neighbors[line]:
			expected[line].append(int(dataB[collumn][9]))

	# for line in range(0, len(dataB)):
		# print("bloco {}: {}".format(line, expected[line]))

	desvio = []
	media = []
	normaldistribution = []
	for line in range(0, len(dataB)):
		desvio.append(std(expected[line]))
		media.append(mean(expected[line]))
		if desvio[line] != 0:
			normaldistribution.append(normal(media[line], desvio[line]))
		else:
			normaldistribution.append(media[line])
		# print("bloco {}: {}".format(line, normaldistribution[line]))

	for line in range(0, len(dataP)):
		if (int(dataP[line][1]) == 0):
			normaldistribution[line] = int(dataB[line][9])

	return normaldistribution


  def geracao(self, vEstado, vDecisao):

	'''
	   Metodo que gera incerteza propriamente dita
	   DEVE SER SOBRESCRITO

	'''

	self.concentracao = incertezasVizinhos(self, vEstado, vDecisao)
	self.preco = incertezaPrecoMinerio(self, vEstado.estagio)

	# print(vizinhos,preco,tons)

	# print(vizinhos)


	#return self.beneficiototal
 
class EstadoOPM(tpd.Estado):
  #criar as variáveis de estado
  #criar o construtor
  #criar o imprime

  def __init__(self, ParEst):
	'''
	   Construtor
	   \par ParEst - Lista de parametros para inicializacao do estado

		** ParEst[0] - Rd: lista de blocos agregados  
		ParEst[1] - B: Blocos com possibilidade de serem explorados 
		** ParEst[2] - Br: Blocos agregados com possibilidade de serem explorados
		ParEst[3] - e: Estimativa da relacao esteril/minerio
		ParEst[4] - p: Preco do minerio no mercado
		** ParEst[5] - v: Beneficio do bloco extraido
		ParEst[6] - precedence: Precedencia dos blocos 

	   DEVE SER SOBRESCRITO
	'''  
	self.B = ParEst[0]
	self.precedence = ParEst[1] 
	self.neighbors = ParEst[2]     
	self.p = ParEst[3]
	self.Bjunior = range(len(self.B))
	self.beneficiototal = [0 for i in range(len(self.Bjunior))]

   

  def CalcValor(self,vDecisao,vIncerteza):
	'''
	   Calcula Valor dos custos apos a realizacao da incerteza
	   DEVE SER SOBRESCRITO
	'''


  def removeBlock(self,idb):
	sucessores = [i for i in self.neighbors[idb] if i not in self.precedence[idb]]
	for s in sucessores:
		a = self.precedence[s][0:2]
		b = self.precedence[s][2:]
		b.remove(idb)
		a[1] = a[1] -1
		self.precedence[s] = a+b
	self.Bjunior = 	self.Bjunior.remove(idb)

  def imprime(self):
	'''
	   Metodo que imprime as informacoes do estado
	   DEVE SER SOBRESCRITO

	'''
	print "blocos: ", self.B, "\n" 
	print "precedentes: ", self.precedence , "\n"
	print "vizinhos: ", self.neighbors  , "\n"   
	print "preço inicial: ", self.p, "\n" 
	print "Bonelli Júnior: ",self.Bjunior , "\n"
	print "Benefício Total: ",self.beneficiototal, "\n"
	

  def transicao(self,Dec,ParInc):

	'''
	   Metodo que realiza a transicao do estado
	   \par Dec - Instancia da classe decisao
	   \par ParInc - Lista de parametros para geracao de incerteza
	   \return ValorAfterUpdate
	   NAO PODE SER SOBRESCRITO
	'''  
	Incerteza = GeraIncerteza(self,Dec,self.estagio,ParInc)
	Incerteza.geracao()
	# Passagem de estagio
	self.estagio = self.estagio+1
	self.Atualizar(Incerteza)
	ValorAfterUpdate = CalcValor(self,Dec,Incerteza)
	
	return ValorAfterUpdate


  def Atualizar(self,Incerteza):
	'''
	   Metodo que atualiza as informacoes do estado apos a geracao de incerteza dentro do processo de transicao
	   \par Incerteza - Instancia da classe incerteza apos a geracao
	   \return ValorAfterUpdate
	   DEVE SER SOBRESCRITO


	'''  

	for i in range(len(beneficiototal)):
		idb = vEstado.Bjunior[i]
		self.beneficiototal[i] = float(format(Incerteza.concentracao[i]*Incerteza.preco*float(vEstado.B[idb][6]), '.2f'))

	# print(preco)
	print(self.beneficiototal)

	return 0

class PoliticaOPM(tpd.Politica):
	''' Classe que representa uma politica apra a solucao do problema
		Objetivos: 1) Resolver o subproblema
				   2) Realizar o trainamento se necessário
		Métodos Obrigatórios: 
				  - solver() 
		Variáveis Obrigatórias:
				   
	'''    
	def __init__(self, ParPol):
		''' 
			Construtor
			\par ParPol - lista com parâmetros para a politica
			DEVE SER SOBRESCRITO
		''' 
	def Agrega(self,linesB,linesP):
		'''
			Método de agregação de blocos "ADAPTADO DE RAMAZAN"
			\par linesB - conjunto de blocos
			\par linesP - conjunto de blocos
			\return conjunto de blocos agregados	    
		''' 
		E = float(0.0001) 

		model = Model("Fundamental_Tree_Algorithm")

		f = model.addVars(posI, negI, vtype = GRB.CONTINUOUS, name = 'f')

		model.setObjective(quicksum(C[i] * f[i, j] for i in posI for j in NegP[i]), GRB.MINIMIZE)

		model.update()

		model.addConstrs((quicksum(f[i, j] for i in PosN[j]) == -V[j] + E for j in negI), name = 'negativo')
		model.addConstrs((quicksum(f[i, j] for j in NegP[i]) <= V[i] for i in posI), name = 'positivo')

		model.write('ramazan.lp') 
		model.write('ramazan.mps') 

		model.optimize()

		blocosagregados = []

		for i in posI:
		  blocosagregados.append([])
		  for j in NegP[i]:
			blocosagregados[i].append(j)
			print("bloco {} agregado ao bloco {}".format(i, j))

		return blocosagregados

	def solver(self,estX):
		'''
			Método de solução do sub problema, modelo adaptado de Jelvez et al.
			\par estX - Estado
			\return objeto da classe decisão
		'''

		K = [0]

		p = 0.15

		cLowerBound = [[] for i in range(len(K))]
		cLowerBound[0] = 5

		cUpperBound = [[] for i in range(len(K))]
		cUpperBound[0] = 10

		model = Model("Open_Pit_Mine_Production_Scheduling")

		x = model.addVars(allB, vtype = GRB.BINARY, name = 'x')
		y = model.addVars(R, vtype = GRB.BINARY, name = 'y')
		M = model.addVars(R, vtype = GRB.BINARY, name = 'M')

		model.update()

		model.setObjective(quicksum(p * v[i] * x[i] for i in allB), GRB.MAXIMIZE)

		model.addConstrs((x[i] <= y[r] for r in R for i in B[r]), name = 'R2')
		model.addConstrs((x[i] <= x[j] for i in allB for j in A[i] if len(A[i]) != 0), name = 'R3')
		model.addConstrs((quicksum(x[i] for i in allB) >= cLowerBound[k] for k in K), name = 'R4') # falta adicionar o peso [a] do processo
		model.addConstrs((quicksum(x[i] for i in allB) <= cUpperBound[k] for k in K), name = 'R5') # falta adicionar o peso [a] do processo
		model.addConstr((quicksum(y[r1] for r1 in R) <= 1 + quicksum(M[r2] for r2 in R)), name = 'R6')
		model.addConstrs((M[r] <= quicksum(x[i] for i in B[r]) / len(B[r]) for r in R), name = 'R7')

		model.write('jelvez.lp') 
		model.write('jelvez.mps') 

		model.optimize()

		for i in allB:
			if x[i].x == 1:
				print("o bloco {} foi extraído".format(i))
			else:
				print("o bloco {} não foi extraído".format(i))

		print("")

		for r in R:
			if y[r] .x == 1:
				print("o bloco agregado {} foi explorado".format(r))
			else:
				print("o bloco agregado {} não foi explorado".format(r))

		return y,x

class DecisaoOPM(tpd.Decisao):
	''' Classe que organiza a decisão tomada pela politica
		Objetivos: 1) padronizar o formato da decisao
		Métodos Obrigatórios: 
				  - def imprime()
		Variáveis Obrigatórias:
				   
	'''

	def __init__(self, ParDec):
		'''
			Construtor
			@par ParDec - Lista de parametros resultantes do metodo de solucao
			@par ParDec[0] - Lista de Ids dos blocos removidos
			DEVE SER SOBRESCRITO
		'''  
		self.removidos = ParDec[0]
		return 0 
	def imprime(self):
		'''
			Metodo que imprime as informacoes da decisao
			DEVE SER SOBRESCRITO
		'''
		return 0 


