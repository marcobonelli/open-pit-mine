# -*- coding: utf-8 -*-
import argparse
from leitorXML import *
from instGen import *

parser = argparse.ArgumentParser(description='OPMS_instGen')
parser.add_argument('InstArq', help='Arquivo com os parâmetros da instância')
args = parser.parse_args()

Configuracao = LerXMLGen(args.InstArq)

nomeArqBloco = "{}.bloc".format(Configuracao["ArqName"].encode('utf-8'))
nomeArqPrec =  "{}.prec".format(Configuracao["ArqName"].encode('utf-8'))
figName = "{}.png".format(Configuracao["ArqName"].encode('utf-8'))
Mina = Configuracao["Mina"]
Valor = Configuracao["Valor"]
 
tx = Mina["Tx"]
ty = Mina["Ty"]
tz = Mina["Tz"]
sigmin = Mina["SigmaMin"]
sigmax = Mina["SigmaMax"]
numero_de_clusters = Mina["NumeroClusters"]

print "\n"
print args.InstArq
print Configuracao["ArqName"].encode('utf-8')
print nomeArqBloco
print nomeArqPrec
print numero_de_clusters

[B,dens] = CriaMina(tx,ty,tz,sigmin,sigmax,numero_de_clusters)

mxb = Valor["BeneficioMax"]
mnb = Valor["BeneficioMin"]
mxc = Valor["CustoMax"]

print "\n"
print mxb
print mnb
print mxc

approc = criaAPP(B,dens,mxb,mnb,mxc)

criaArqBloco(nomeArqBloco,B,approc)
pList = criaPrecList(B,tx,ty,tz)
criaArqPrec(nomeArqPrec,B,pList)
upitList,precValue = UPIT(B,approc,pList)
pList2 = criaPrecList(upitList,tx,ty,tz)

b1x = [b[0] for b in B]
b1y = [b[1] for b in B]
b1z = [b[2] for b in B]

mina = [b1x,b1y,b1z]


b2x = [b[0] for b in upitList]
b2y = [b[1] for b in upitList]
b2z = [b[2] for b in upitList]

upit = [b2x,b2y,b2z]
scatter3d(figName,mina,upit,approc,precValue)

