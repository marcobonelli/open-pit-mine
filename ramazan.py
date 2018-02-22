#coding: utf-8
import sys
import math
import random
from operator import itemgetter
from gurobipy import *

def atualizacao(f):
    NegP = [[] for i in range(len(linesB))]
    for line in posI:
	for collumn in NegP_past[line]:
	    if f[line, collumn].x != 0.0:
		NegP[line].append(collumn)

    PosN = [[] for i in range(len(linesB))]
    for line in posI:
	for collumn in range(0, len(NegP[line])):
	    PosN[NegP[line][collumn]].append(line)

    C_aux = [[i, 0] for i in range(0, len(linesB))]
    for line in posI:
        C_aux[line][0] = line
        C_aux[line][1] = V[line]
        for collumn in NegP[line]:
	    C_aux[line][1] += V[collumn]

    C_aux = sorted(C_aux, key = itemgetter(1), reverse = True)

    ranking = 1
    for line in range(0, len(linesB)):
        if C_aux[line][0] in posI:
            C_aux[line][1] = ranking
            ranking += 1

    C_aux = sorted(C_aux, key = itemgetter(0))

    C = [0 for i in range(len(linesB))]
    for line in range(0, len(C_aux)):
        C[line] = C_aux[line][1]

    return NegP,PosN,C

linesB = [line.rstrip('\n') for line in open('r_instance.blocks')]
linesP = [line.rstrip('\n') for line in open('r_instance.txt')]

for line in range(0, len(linesB)):
    linesB[line] = linesB[line].split(' ')

for line in range(0, len(linesP)):
    linesP[line] = linesP[line].split(' ')

NegP = [[] for i in range(len(linesB))]
for line in linesP:
    for collumn in range(2, int(line[1]) + 2):
        NegP[int(line[0])].append(int(line[collumn]))

pos = []
neg = []

for line in range(0, len(linesB)):
    if (float(linesB[line][9]) > 0):
	pos.append([line, float(linesB[line][9])])
    elif (float(linesB[line][9]) < 0):
	neg.append([line, float(linesB[line][9])])

posI = []
for i in range(0, len(pos)):
    posI.append(pos[i][0])

negI = []
for i in range(0, len(neg)):
    negI.append(neg[i][0])

PosN = [[] for i in range(len(linesB))]
for line in posI:
    for collumn in range(0, len(NegP[line])):
	PosN[NegP[line][collumn]].append(line)

V = []
for line in range(0, len(linesB)):
    V.append(float(linesB[line][9]))

C_aux = [[i, 0] for i in range(0, len(linesB))]
for line in posI:
    C_aux[line][0] = line
    C_aux[line][1] = V[line]
    for collumn in NegP[line]:
	C_aux[line][1] += V[collumn]

print(C_aux)

C_aux = sorted(C_aux, key = itemgetter(1), reverse = True)

ranking = 1
for line in range(0, len(linesB)):
    if C_aux[line][0] in posI:
        C_aux[line][1] = ranking
        ranking += 1

C_aux = sorted(C_aux, key = itemgetter(0))

C = [0 for i in range(len(linesB))]
for line in range(0, len(C_aux)):
    C[line] = C_aux[line][1]

C = [0, 0, 0, 0, 3, 2, 1, 0, 0, 4, 0, 0, 5, 6, 0, 0, 7]
# C = [0, 0, 0, 0, 2, 1, 3, 0, 0, 4, 0, 0, 5, 6, 0, 0, 7]

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

print('Obj:', model.objVal)

NegP_past = NegP

[NegP, PosN, C] = atualizacao(f)

for i in posI:
    for j in NegP[i]:
        print("bloco {} agregado ao bloco {}".format(i, j))
