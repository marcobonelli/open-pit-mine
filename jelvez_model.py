#coding: utf-8
import sys
import math
import random
from gurobipy import *

allB = [0,1,10,17,24,30,31,35,37,38,39]

R = [0, 1, 2]

B = [[] for i in range(len(R))]
B[0] = [0,1,10,17,24,30,31,35,38]
B[1] = [37]
B[2] = [39]

A = [[] for i in range(40)]

A[10] = [0,1]
A[17] = [10]
A[24] = [17]
A[30] = [24]
A[31] = [24]
A[35] = [30,31]
A[38] = [35]
A[39] = [37]

linesB = [line.rstrip('\n') for line in open('aux4.blocks')]

dataB = []
for line in range(0, len(linesB)):
    dataB.append(linesB[line].split(' '))

v = [0 for i in range(40)]
for i in range(len(allB)):
    for line in range(0, len(dataB)):
    # v[int(dataB[line][11])] = float(dataB[line][9])
        if(int(dataB[line][11]) == allB[i]):
            v[allB[i]] = float(dataB[line][9])
print(v)
# v = [-122.4, -244.81,0, -367.21,0,0,0,0,0,0, 349.28, 937.87,0,0,0,0,0, 755.1, 162.41,0,0,0,0,0, 495.52, 51.69, 367.21, 367.21, 392.15,0, 248.13, 290.22,0, 533.12,0, 231.73]

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