#coding: utf-8
import sys
import math
import random
from gurobipy import *
# Universidade Federal De Ouro Preto - Joao Monlevade - ICEA
# Aluno: Matheus Correia Teixeira - 14.1.8375

R = [1,2,3]
B = [[1,2,3],[4,5,6],[7,8,9,10,11,12]]
A = [(7,0),(7,1),(7,2),(7,5),(7,6),
     (8,4),(8,5),(8,1),(8,2),(8,3),
     (11,0),(11,1),(11,2),(11,3),(11,4),(11,5),(11,6),(11,9),(11,10)]
K = [3,3,3,3,3,3,3,3,3,3,3,3]
v = [[0,3,0],[0,3,2],[1,1,2,5,7,8]]
p = 0.3
a = [1,2,3,1,2,3,1,2,3,1,2,3]
cUpperBound = [6,6,6,6,6,6,6,6,6,6,6,6]
cLowerBound = [1,1,1,1,1,1,1,1,1,1,1,1]

try:
    # Criação de um novo modelo
    m = Model("modeloexato")

    # Criação de Variaveis
    x = []
    for j in range(len(R)):
        for i in range(len(B[j])):
            x.append(m.addVar(vtype = GRB.BINARY, name = "x"))

    y = []
    for j in range(len(R)):
        for i in range(len(B[j])):
            y.append(m.addVar(vtype = GRB.BINARY, name = "y"))

    M = []
    for i in range(len(R)):
        M.append(m.addVar(vtype = GRB.BINARY, name = "M"))

    # Integração das Variaveis
    m.update()

    # Função Objetivo
    m.setObjective(quicksum(p * v[r][i] * x[i] for r in range(len(R)) for i in range(len(B[r]))), GRB.MAXIMIZE)

    # Criação das Restrições

    # (2)
    for r in range(len(R)):
        for i in range(len(B[r])):
            m.addConstr(x[i] <= y[r])

    # (3)
    for (i,j) in A:
        m.addConstr(x[i] <= x[j])

    # (4)
    for k in range(len(K)):
        m.addConstr(quicksum(a[i] * x[i] for r in range(len(R)) for i in range(len(B[r]))) <= cUpperBound[k])

    # (5)
    for k in range(len(K)):
        m.addConstr(quicksum(a[i] * x[i] for r in range(len(R)) for i in range(len(B[r]))) >= cLowerBound[k])

    # (6)
    m.addConstr(quicksum(y[r] for r in range(len(R))) <= 1 + quicksum(M[r] for r in range(len(R))))

    # (7)
    for r in range(len(R)):
        m.addConstr(M[r] <= quicksum(x[i] for i in range(len(B[r]))) / len(B[r]))

    m.optimize()
    for v in m.getVars():
        print v.varName, v.x

    print 'Obj:', m.objVal
    
except GurobiError:
    print 'Error reported'
