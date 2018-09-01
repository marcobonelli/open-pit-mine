#coding: utf-8
import sys
import math
import random
from operator import itemgetter

def findNegP(block, dataB, dataP, posI, reference):
	NegP = []
	if int(dataP[block][1]) == 0:
		return []
	else:
		for collumn in range(0, int(dataP[block][1])):
			if int(dataP[block][2 + collumn]) not in posI:
				NegP.append(int(dataP[block][2 + collumn]))
			if reference[int(dataP[block][2 + collumn])] == []:
				NegP.extend(findNegP(int(dataP[block][2 + collumn]), dataB, dataP, posI, reference))
			else:
				NegP.extend(reference[int(dataP[block][2 + collumn])])
		return NegP

linesB = [line.rstrip('\n') for line in open('newman1.blocks')]
linesP = [line.rstrip('\n') for line in open('newman1.prec')]

dataB = []
dataP = []

for line in range(0, len(linesB)):
    dataB.append(linesB[line].split(' '))
    dataP.append(linesP[line].split(' '))

base = int(dataB[0][0])
topo = int(dataB[9][0])

pos = []
neg = []

for line in range(0, len(dataB)):
	if (float(dataB[line][9]) >= 0):
		pos.append([int(dataB[line][0]), float(dataB[line][9])])
	else:
		neg.append([int(dataB[line][0]), float(dataB[line][9])])

print(pos)
print(neg)

posI = []
for i in range(0, len(pos)):
	posI.append(pos[i][0])

negI = []
for i in range(0, len(neg)):
	negI.append(neg[i][0])

arq = open('newman1.rel', 'w')

NegP = [[] for i in range(len(dataB))]
z = 7
while z > -1:
	for line in posI:
		if int(dataB[line][3]) == z:
			NegP[line].extend(sorted(set(findNegP(line, dataB, dataP, posI, NegP))))
			texto = str(line) + ' ' + str(len(NegP[line])) + ' ' + str(NegP[line]) + '\n'
			arq.writelines(texto)
			print(texto)
	z = z -1

print("c. NegP -> ", NegP)
arq.close()
