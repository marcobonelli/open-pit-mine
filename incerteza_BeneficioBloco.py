#coding: utf-8
import sys
import math
import random
from numpy.random import standard_normal
from numpy import array, zeros, sqrt, shape
from pylab import *

def incertezaPrecoMinerio():
    p_inicial = 120.35		
    H = 1				
    dt = 0.01			
    sigma = 3.49			
    mu = 6.38			
    nSimu = 100			

    passos = round(H / dt); 
    S = zeros([nSimu, passos], dtype = float)
    x = range(0, int(passos), 1)
    price = []

    for j in range(0, nSimu, 1):
        S[j, 0] = p_inicial
        for i in x[:-1]:
            if S[j, i] < 50:
                mu /= 2
            elif S[j, i] > 150:
                mu /= 2
            S[j, i + 1] = S[j, i] * math.exp((mu - 0.5 * math.pow(sigma, 2)) * dt + sigma * math.sqrt(dt) * standard_normal())

    for j in range(0, len(S[0]), 1):
        somatorio = 0
        for i in range(0, len(S), 1):
            somatorio += S[i][j]
        price.append(somatorio / len(S))
    # print(price[1])
    return price[1]    
    # plot(x, price)
    # title('Simulacao com %d dias e Preco Inicial de %.2f' % (int(passos), p_inicial))
    # xlabel('Dias')
    # ylabel('Preco da Acao')
    # show()

def incertezasVizinhos():
    #arquivo = open ('/Users/matheusteixeira/Google Drive/UFOP/8º Periodo/Programacao Dinamica/estruturaprecedencia.txt', 'w')

    linesP = [line.rstrip('\n') for line in open('r_instance.prec')]
    linesB = [line.rstrip('\n') for line in open('r_instance.blocks')]

    dataP = []
    dataB = []

    for line in range(0, len(linesP)):
        dataP.append(linesP[line].split(' '))
        dataB.append(linesB[line].split(' '))
        # print(dataB[line])

    for line in range(0, len(dataP)):
        for collumn in range(0, len(dataP[line])):
            dataP[line][collumn] = int(dataP[line][collumn])

    neighbors = []

    for line in range(0, len(dataP)):
        neighbors.append([])
        neighbors[line].append(line)
        
        for collumn in range(2, len(dataP[line])):
            neighbors[line].append(dataP[line][collumn])
            
        for lineN in range(0, len(dataP)):
            for collumn in range(2, len(dataP[lineN])):
                if dataP[lineN][collumn] == line:
                    neighbors[line].append(dataP[lineN][0])

    for line in range(0, len(dataB)):
        for collumn in range(0, 4):
            dataB[line][collumn] = int(dataB[line][collumn])

        for collumn in range(5, 10):
            dataB[line][collumn] = float(dataB[line][collumn])

        dataB[line][10] = int(dataB[line][10])

    blocks = dataB

    aux = [0 for i in range(len(dataB))]

    value = []
    # print(neighbors[10])
    for line in range(0, len(blocks)):
        for collumn in range(0, len(dataP)):
            if(dataP[line][1] == 0):
                aux[line] = dataB[line][9]
            else:
                expected = 0
                for block in neighbors[line]:
                    expected += blocks[block][9]
                expected /= len(neighbors[line])
                aux[line] = expected 

    # print(aux)
    return aux
        # value.append([line, expected])

    # for line in range(0, len(value)):
    #     print(value[line])

def Toneladas():

    linesP = [line.rstrip('\n') for line in open('r_instance.prec')]
    linesB = [line.rstrip('\n') for line in open('r_instance.blocks')]

    dataP = []
    dataB = []

    for line in range(0, len(linesP)):
        dataP.append(linesP[line].split(' '))
        dataB.append(linesB[line].split(' '))
        # print(dataB[line])

    for line in range(0, len(dataP)):
        for collumn in range(0, len(dataP[line])):
            dataP[line][collumn] = int(dataP[line][collumn])

    neighbors = []

    for line in range(0, len(dataP)):
        neighbors.append([])
        neighbors[line].append(line)
        
        for collumn in range(2, len(dataP[line])):
            neighbors[line].append(dataP[line][collumn])
            
        for lineN in range(0, len(dataP)):
            for collumn in range(2, len(dataP[lineN])):
                if dataP[lineN][collumn] == line:
                    neighbors[line].append(dataP[lineN][0])

    for line in range(0, len(dataB)):
        for collumn in range(0, 4):
            dataB[line][collumn] = int(dataB[line][collumn])

        for collumn in range(5, 10):
            dataB[line][collumn] = float(dataB[line][collumn])

        dataB[line][10] = int(dataB[line][10])

    tons = [0 for i in range(len(dataB))]

    for line in range(0, len(dataB)):
        for collumn in range(0, len(dataB)):
            tons[collumn] = dataB[line][6] 

    return tons

def Beneficio():

    vizinhos = incertezasVizinhos()
    preco = incertezaPrecoMinerio()
    tons = Toneladas()
    # print(vizinhos,preco,tons)

    beneficiototal = [0 for i in range(len(vizinhos))]

    for i in range(len(vizinhos)):
        beneficiototal[i] = vizinhos[i]*preco*tons[i]

    # print(preco)
    print(beneficiototal)

    return beneficiototal

Beneficio()