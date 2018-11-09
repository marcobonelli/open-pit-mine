# coding: utf-8
import sys
import math
import random
import matplotlib
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from gurobipy import *
from mpl_toolkits.mplot3d import Axes3D

def CriaMina(tx,ty,tz,sigmin,sigmax,numero_de_clusters):

	X = [i for i in range(0,tx)]
	Y = [i for i in range(0,ty)]
	Z = [i for i in range(0,tz)]

	ID = [i for i in range(len(X)*len(Y)*len(Z))]
	blocosescolhidos = random.sample(ID, numero_de_clusters)

	cluster_mu = []
	cluster_sigma = []

	for c in range(numero_de_clusters):
		cluster_mu.append([random.uniform(0,tx),random.uniform(0,ty),random.uniform(0,tz)])
		cluster_sigma.append([tx/random.uniform(sigmin,sigmax),ty/random.uniform(sigmin,sigmax),tz/random.uniform(sigmin,sigmax)])

	blocos_coord = [(a,b,c) for a in X for b in Y for c in Z]

	dens = [0 for b in range(len(blocos_coord))]

	for c in range(numero_de_clusters):
		cov_matrix = np.diag(cluster_sigma[c])
		for b in range(len(blocos_coord)):
			dens[b] = dens[b] + st.multivariate_normal.pdf(blocos_coord[b],cluster_mu[c],np.diag(cluster_sigma[c]))

	return [blocos_coord,dens]

def precList(b, Blocos,xmax,ymax,zmax):
	prec = []
	for dx in (-1,0,1):
		if((b[0]+dx>=0) and(b[0]+dx<xmax)):
			for dy in (-1,0,1):
				if((b[1]+dy>=0) and(b[1]+dy<ymax)):
					if(b[2]-1>=0):
						prec.append(Blocos.index((b[0]+dx,b[1]+dy,b[2]-1)))
	return prec

def criaPrecList(blocos_coord,tx,ty,tz):
	PrecList = []
	for b in range(len(blocos_coord)):
		prec = precList(blocos_coord[b], blocos_coord,tx,ty,tz)
		PrecList.append(prec)
	return PrecList

def criaArqPrec(nfile,blocos_coord,pList):
	with open(nfile, 'w') as prec_file:
		for b in range(len(blocos_coord)):
			prec = pList[b]
			prec_file.write('{}\t{}\t'.format(b,len(prec)))
			for p in prec:
				prec_file.write('{}\t'.format(p))
			prec_file.write('\n')

def criaAPP(blocos_coord,dens,mxb,mnb,mxc):
	dmin = min(dens)
	dmax = max(dens)
	benef = random.uniform(mnb,mxb)
	benefList = [benef*((dens[b] - dmin)/(dmax-dmin)) for b in range(len(dens))]
	ap_process = [-random.uniform(0,mxc)+benefList[b] for b in range(len(benefList))]
	return ap_process

def criaArqBloco(nfile,blocos_coord,ap_process):
	with open(nfile, 'w') as bfile:
		for b in blocos_coord:
			bid = blocos_coord.index(b) 
			bfile.write('{}\t{}\t{}\t{}\t0\t0\t0\t0\t0\t0\t{}\n'.format(bid,b[0],b[1],b[2],ap_process[bid]))

def UPIT(blocos_coord,value,pList):
	upitList = []
	precValue =[]

	m = Model()
	n = len(blocos_coord) # number of blocks

	# Indicator variable for each block
	x = []
	for i in range(n):
		x.append(m.addVar(vtype=GRB.BINARY, name="x%d" % i))

	m.update()

	# Set objective
	m.setObjective(quicksum(value[i]*x[i] for i in range(n)), GRB.MAXIMIZE)

	# Add constraints
	for b in range(n):
		for bp in pList[b]:
			m.addConstr(x[b] <= x[bp])

	m.optimize()

	for b in range(n):
		if (x[b].x == 1):
			upitList.append(blocos_coord[b])
			precValue.append(value[b])
	print(len(upitList), len(precValue))
	

	m.write('upit.lp')
	m.write('upit.mps')

	return upitList,precValue

def scatter3d(arqName,mina, upit,csmina,csupit, plot = 0, colorsMap='RdYlGn'):
	cm = plt.get_cmap(colorsMap)
	cNorm = matplotlib.colors.Normalize(vmin=min(csmina), vmax=max(csmina))
	scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
	fig = plt.figure(figsize=(19.20, 10.8), dpi=200)

	ax = fig.add_subplot(1,2,1,projection = '3d')
	ax.set_title("Original Mine")
	ax.scatter(mina[0], mina[1], mina[2], c=scalarMap.to_rgba(csmina),marker = 'o', edgecolors = 'none')
	print ax.azim
	ax.view_init(elev=-150,azim = 60)
	scalarMap.set_array(csmina)
	fig.colorbar(scalarMap)
	#ax.scatter(x, y, z, c=scalarMap.to_rgba(cs),marker = 'o')

	ax = fig.add_subplot(1,2,2,projection = '3d')
	ax.set_title("Ultimate PIT")
	ax.scatter(upit[0], upit[1], upit[2], c=scalarMap.to_rgba(csupit),marker = 'o', edgecolors = 'none')
	ax.view_init(elev=-150,azim = 60)

	scalarMap.set_array(csupit)
	fig.colorbar(scalarMap)
	plt.subplots_adjust(bottom=0.05, left= 0.05, right=0.95, top=0.95, wspace=0.1)
	plt.savefig(arqName) #, bbox_inches='tight')
	if plot:
		plt.show()


