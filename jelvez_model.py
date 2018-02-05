#coding: utf-8
import sys
import math
import random
from gurobipy import *
# Universidade Federal De Ouro Preto - Joao Monlevade - ICEA
# Aluno: Matheus Correia Teixeira - 14.1.8375

try:
    # Criação de um novo modelo
    m = Model("modelo jelvez")

    # Criação de Variaveis
    x = []
    for j in R:
        for i in B[j]:
            x[i] = m.addVar(vtype = GRB.BINARY, name = "x")

    y = []
    for i in R:
        y[i] = m.addVar(vtype = GRB.BINARY, name = "y")

    M = []
    for i in R:
        M[i] = m.addVar(vtype = GRB.BINARY, name = "M")

    # Integração das Variaveis
    m.update()

    # Função Objetivo
    m.setObjective(quicksum(p * v[i] * x[i] for r in R for i in B[r]), GRB.MAXIMIZE)

    # Criação das Restrições

    # (2)
    for r in R:
        for i in B[r]:
            m.addConstr(x[i] <= y[r])

    # (3)
    for [i, j] in A:
        m.addConstr(x[i] <= x[j])


    # (4)
    for k in K:
        m.addConstr(quicksum(a[i][k] * x[i] for r in R for i in B[r]) <= cUpperBound[k])

    # (5)
    for k in K:
        m.addConstr(quicksum(a[i][k] * x[i] for r in R for i in B[r]) >= cLowerBound[k])

    # (6)
    m.addConstr(quicksum(y[r] for r in R) <= 1 + quicksum(M[r] for r R))

    # (7)
    for r in R:
        m.addConstr(M[r] <= quicksum(x[i] for i in B[r]) / len(B[r]))

    m.optimize()
    
except GurobiError:
    print 'Error reported'
