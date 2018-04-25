#coding: utf-8
import TemplatePD as tpd
import sys
import math
import random
import numpy 
from numpy.random import standard_normal, normal
from numpy import array, zeros, sqrt, shape
from pylab import *
from leitorXML import *
class ProblemaOPM(tpd.Problema):
  # criar a classe problema
  # puxar dados do xml
  ''' Classe com os parametros que definem a instancia do problema
      Objetivo: Gerenciar a instância do problema
      Métodos Obrigatórios: 
               - Leitura
               - ImprimeResultados
               - SalvaResultados
      Variáveis Obrigatórias:
               - Arquivo de entrada
               - Nome da Instância            
  '''
  def __init__(self, InstPar):
    '''
       Construtor
       \par InstPar - Lista de parametros das instancia
       DEVE SER SOBRESCRITO 

    '''
    Leitura(InstPar.InstArq)  
    return 0

  def Leitura(self, ArqEntrada):
    '''
        Metodo para carregamento de dados das instancias
        \par ArqEntrada  - Nome do arquivo de entrada
        DEVE SER SOBRESCRITO
    '''
    Instancia = LerXML(args.InstArq)
    dadosIn =  Instancia["Incerteza"]
    dadosMin = Instancia["Mina"]
    dadosSim = Instancia["Simulador"]
    [self.B,self.P,self.N] = CriaBloco(dadosMin['Arqblocos'],dadosMin['Arqprec'],dadosMin['Arqupit']) 
    self.p0 = dadosIn['p0']
    self.precomedio = dadosIn['precomedio']
    self.desviopreco = dadosIn['desviopreco']
    self.H = dadosIn['H']
    self.dt = dadosIn['dt']
    return 0

  def CriaBloco(self, ArqBloco, ArqPrecedncia, ArqUpit):
    # Fazer leitura do ArqUpit

    linesP = [line.rstrip('\n') for line in open('r_instance.prec')]
    linesB = [line.rstrip('\n') for line in open('r_instance.blocks')]

    dataP = []
    dataB = []

    for line in range(0, len(linesP)):
        dataP.append(linesP[line].split(' '))
        dataB.append(linesB[line].split(' '))
        print(dataB[line])

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

    return [dataB,dataP,neighbors]

  def ImprimeResultados(self):
    '''
        Metodo para impressao de resultados da analise
        DEVE SER SOBRESCRITO
    '''
    return 0 

  def SalvaResultados(self, ArqSaida):
    '''
        Metodo para escrita detalhada de resultados da analise
        \par ArqSaida  - Nome do arquivo de saida
        DEVE SER SOBRESCRITO
    '''
    return 0 
class GeraIncerteza(tpd.GeraIncerteza):
  ''' Classe que gera a incerteza do problema
      Objetivos: 1) Gerar incerteza
      Métodos Obrigatórios: 
                - geracao()
                - CalcValor(self): 
      Variáveis Obrigatórias:
                
                 
  '''

  def __init__(self, vEstado, vDecisao,vEstagio,ParInc):
    '''
       Construtor
       \par vEstado - instancia da classe Estado
       \par vDecisao - instancia da classe Decisao
       \par vEstagio - inteiro com a informação do estagio atual
       \par ParInc - lista com parâmetros para realizacao da incerteza
       ParInc[0] = p_inicial
       ParInc[1] = H
       ParInc[2] = dt
       ParInc[3] = sigma
       ParInc[4] = mu
       **ParInc[5] = nSimu

       DEVE SER SOBRESCRITO
    ''' 

    self.p_inicial = ParInc[0] 
    self.H = ParInc[1]       
    self.dt = ParInc[2]     
    self.sigma = ParInc[3]     
    self.mu = ParInc[4]     
    self.nSimu = 100  
    return 0

  def incertezaPrecoMinerio():   

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

  def incertezasVizinhos(self, Estado):
    #arquivo = open ('/Users/matheusteixeira/Google Drive/UFOP/8º Periodo/Programacao Dinamica/estruturaprecedencia.txt', 'w')

    expected = []

    for line in range(0, len(dataB)):
        expected.append([])
        for collumn in neighbors[line]:
            expected[line].append(int(dataB[collumn][9]))

    # for line in range(0, len(dataB)):
        # print("bloco {}: {}".format(line, expected[line]))

    desvio = []
    media = []
    normaldistribution = []
    for line in range(0, len(dataB)):
        desvio.append(std(expected[line]))
        media.append(mean(expected[line]))
        if desvio[line] != 0:
            normaldistribution.append(normal(media[line], desvio[line]))
        else:
            normaldistribution.append(media[line])
        # print("bloco {}: {}".format(line, normaldistribution[line]))

    for line in range(0, len(dataP)):
        for collumn in range(0, len(dataP)):
            if (int(dataP[line][1]) == 0):
                normaldistribution[line] = int(dataB[line][9])

    return normaldistribution


  def geracao(self, Estado):

    '''
       Metodo que gera incerteza propriamente dita
       DEVE SER SOBRESCRITO

    '''
    self.concentracao = incertezasVizinhos()
    self.preco = incertezaPrecoMinerio()
    # print(vizinhos,preco,tons)

    # print(vizinhos)

    self.beneficiototal = [0 for i in range(len(tons))]

    for i in range(len(tons)):
        self.beneficiototal[i] = float(format(self.concentracao[i]*self.preco*float(Estado.B[]), '.2f'))

    # print(preco)
    print(self.beneficiototal)

    # return self.beneficiototal

  def CalcValor(self):
    '''
       Calcula Valor dos custos apos a realizacao da incerteza
       DEVE SER SOBRESCRITO
    '''
    return ret 
class EstadoOPM(tpd.Estado):
  #criar as variáveis de estado
  #criar o construtor
  #criar o imprime

  def __init__(self, ParEst):
    '''
       Construtor
       \par ParEst - Lista de parametros para inicializacao do estado

        ** ParEst[0] - Rd: lista de blocos agregados  
        ParEst[1] - B: Blocos com possibilidade de serem explorados 
        ** ParEst[2] - Br: Blocos agregados com possibilidade de serem explorados
        ParEst[3] - e: Estimativa da relacao esteril/minerio
        ParEst[4] - p: Preco do minerio no mercado
        ** ParEst[5] - v: Beneficio do bloco extraido
        ParEst[6] - precedence: Precedencia dos blocos 

       DEVE SER SOBRESCRITO
    '''  
    self.B = ParEst[0]
    self.precedence = ParEst[1] 
    self.neighbors = ParEst[2]     
    self.p = ParEst[3]

    return 0

  def imprime(self):
    '''
       Metodo que imprime as informacoes do estado
       DEVE SER SOBRESCRITO

    '''
    return 0

  def transicao(self,Dec,ParInc):

    '''
       Metodo que realiza a transicao do estado
       \par Dec - Instancia da classe decisao
       \par ParInc - Lista de parametros para geracao de incerteza
       \return ValorAfterUpdate
       NAO PODE SER SOBRESCRITO
    '''  
    Incerteza = GeraIncerteza(self,Dec,self.estagio,ParInc)
    Incerteza.geracao()
    # Passagem de estagio
    self.estagio = self.estagio+1
    ValorAfterUpdate = self.Atualizar(Incerteza)
    return ValorAfterUpdate


  def Atualizar(self,Incerteza):
    '''
       Metodo que atualiza as informacoes do estado apos a geracao de incerteza dentro do processo de transicao
       \par Incerteza - Instancia da classe incerteza apos a geracao
       \return ValorAfterUpdate
       DEVE SER SOBRESCRITO
    '''  
    self.beneficiototal = beneficiototal
    return 0

