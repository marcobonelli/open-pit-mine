#coding: utf-8
import sys
import math
import random
from gurobipy import *

allB = [2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 15, 16, 21, 22, 23, 28]

R = [0, 1, 2]

B = [[] for i in range(len(R))]
B[0] = [7, 8, 9, 14, 15, 16, 21, 22, 23, 28]
B[1] = [5, 6, 13]
B[2] = [2, 3, 4, 11]

K = [0]

A = [[] for i in range(29)]
A[2] = []
A[3] = []
A[4] = []
A[5] = []
A[6] = []
A[7] = []
A[8] = []
A[9] = []
A[11] = [2, 3, 4]
A[13] = [5, 6, 7]
A[14] = [7, 8]
A[15] = [8, 9]
A[16] = [9]
A[21] = [14, 15]
A[22] = [15, 16]
A[23] = [22]
A[28] = [21, 23]

v = [0, 0, +2, -3, +1, +5, -2, -2, +4, -6, 0, +1, 0, +2, +3, +1, +4, 0, 0, 0, 0, +6, +1, +3, 0, 0, 0, 0, +1]

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
