#coding: utf-8
import numpy as np


def dfsPath(listaBlocos,i,j,start = 0):

	if not start:
		for v in listaBlocos[i].listaP:
			if (v == j):
				return True
			else:
				res = dfsPath(listaBlocos,v,j)
				if res:
					return True
	else:
		Pmj = [k for k in listaBlocos[i].listaP if k !=j]
		for v in Pmj:
			res = dfsPath(listaBlocos,v,j)
			if res:
				return True
	return False




class Bloco(object):

	def __init__(self,idi,listaP,valor,vol):

		self.listaP = listaP
		self.id = idi
#		self.lbid = idi # index na lista de blocos, inicialmente igual ao id
		self.valor = valor
		self.volume = vol
		self.compactado = False
#		self.idcomp = -1
#		self.listaOriginal = []
		self.listaSucessor = []
		self.excluido = 0
		self.agregados = []
	def calcSucessores(self,listaBlocos):

		for b in listaBlocos:
			if(self.id in b.listaP):
				self.listaSucessor = self.listaSucessor + [b.id]

	def __str__(self):
		saida  = '###### Bloco {}: \n\t excluido: {} \n\t predecessores: {}\n\t sucessores: {}\n\t agredados: {} \n\t ###################'.format(self.id,self.excluido,str(self.listaP),str(self.listaSucessor),str(self.agregados))
		return saida 

	def candAgregacao(self,listaBlocos,cap):
		for p in self.listaP:
			print p
			print self.id
			if not dfsPath(listaBlocos,self.id,p,1):
				print 'dfs - ok'
				print np.sign(self.valor)
				print np.sign(listaBlocos[p].valor)	
				if (np.sign(self.valor) == np.sign(listaBlocos[p].valor)):
					print 'sign ok'
					print self.volume
					print listaBlocos[p].volume
					if self.volume + listaBlocos[p].volume<= cap:
						print 'vol ok'
						return p
		return -1
				

def agregaIJ(listaBlocos, i, j):
	# j precede i
	listaBlocos[j].excluido = 1
	listaBlocos[i].agregados.append(j)
	listaBlocos[i].listaP.remove(j)
	listaBlocos[i].listaP = listaBlocos[i].listaP + listaBlocos[j].listaP
	for v in listaBlocos[j].listaSucessor:
		if v !=i:
			listaBlocos[v].listaP.remove(j) # remove j da lista de predecessores de seu sucessor
			listaBlocos[v].listaP = listaBlocos[v].listaP + [i] # adiciona o i na lista de predecessores do sucessor de j
			listaBlocos[i].listaSucessor = listaBlocos[i].listaSucessor + [v] # adiciona o sucessor de j na lista de sucessores de i
	listaBlocos[i].volume = listaBlocos[i].volume + listaBlocos[j].volume
	listaBlocos[i].valor = listaBlocos[i].valor + listaBlocos[j].valor 

'''def criaListaBlocosAgregados(listaBlocos):
	1) para todo no que não tiver sido excluido
	2) busca candidato a agregação (func candAgregacao)
	3) agregar
	4) limpar todos os blocos excluidos
	5) o id na nova lista vai ser diferente do id anterior **** 
	6) criar um mapa (id, posição) de indices e passar a usar o mapa para a lista de blocos agregados
	7) Buscar na internet estrutura ou função do python específica para mapeamento
'''		
def crialistaBlocos(listaB,listaP,valor):

	listaBlocos = []

	for b in listaB:
		idb = listaB.index(b)
		listaBlocos.append(Bloco(idb,listaP[idb],valor[idb],1))

	return listaBlocos

def criaSucessores(listaBlocos):

	for b in listaBlocos:
		b.calcSucessores(listaBlocos)

def imprimir(listaBlocos):
	for b in listaBlocos:
		print(b)

if __name__=="__main__":

	blocos = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]
	valor = [-1,-2,2,-3,1,5,-2,-2,4,-6,-2,1,-1,2,3,1,4,5,2,4,-5,6,1,3,2,2,-1,3,1,-4,2,-3,2,2,-2,5,-2,4,8,6]
	prec = [[],[],[],[],[],[],[],[],[],[],[0,1,2],[2,3,4],[4,5],[5,6,7],[7,8],[8,9],[9],[10,11],[11,12],[12,13],[13,14],[14,15],[15,16],[22],[17,18],[18,19],[19,20],[20,21],[21,23],[23],[24],[24,25],[25,26],[26,27],[27,28,29],[30,31,32],[32,33,34],[33,34],[35,36,37],[36,37]]
	B = crialistaBlocos(blocos,prec,valor)
	criaSucessores(B)
	imprimir(B)

	print dfsPath(B,17,8,start = 1)
	print B[10].candAgregacao(B,2)
	agregaIJ(B, 21, 14)
	print(B[14])
	print(B[20])
	print(B[21])
# 	1) copiar (deep cpy) a lista de blocos
