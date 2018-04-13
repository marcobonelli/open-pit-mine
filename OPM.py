# -*- coding: utf-8 -*-
import TemplatePD as tpd


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
        return 0

    def Leitura(self, ArqEntrada):
    '''
        Metodo para carregamento de dados das instancias
        \par ArqEntrada  - Nome do arquivo de entrada
        DEVE SER SOBRESCRITO
    '''
        return 0 

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

class EstadoOPM(tpd.Estado)
#criar as variáveis de estado
#criar o construtor
#criar o imprime 
    def __init__(self, ParEst):
    '''
       Construtor
       \par ParEst - Lista de parametros para inicializacao do estado
            ParEst[0] - qual variável??? ... 
       DEVE SER SOBRESCRITO
    '''  
        return 0
    def imprime(self):
    '''
       Metodo que imprime as informacoes do estado
       DEVE SER SOBRESCRITO

    '''
    
       return 0

    def Atualizar(self,Incerteza):
    '''
       Metodo que atualiza as informacoes do estado apos a geracao de incerteza  dentro do processo de transicao
       \par Incerteza - Instacia da classe incerteza apos a geracao
       \return ValorAfterUpdate
       DEVE SER SOBRESCRITO
    '''  
        return 0
