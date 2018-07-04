# -*- coding: utf-8 -*-
import argparse
from leitorXML import *
import csv
from OPM import *
from time import time


parser = argparse.ArgumentParser(description='OPMS_instance')
parser.add_argument('InstArq', help='Arquivo com os parâmetros da instância')
args = parser.parse_args()

P= ProblemaOPM(args);
print P.B
print P.P
print P.N

Estado = P.CriaEstado()

Estado.imprime()


