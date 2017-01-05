from ged import GED
from data_base import Data_Base
from table import Table
import os
import sys
import random


class BufferPool(object):
    """Buffer Pool"""
    paginas = [] #vetor de páginas (bFrames)
    politicaSubistituicao = 0
    politicas = {
        0: 'random',
        1: 'ultimoUsado',
        2: 'maisRecente'
    }

    #recebe como parametro a quantidade de páginas, o tamanho delas e a politica de subistituicao
    def __init__(self,politicaSubistituicao,qtdPaginas=10, tamanhoPaginas = 1024):
        for i in range(0,qtdPaginas):
            self.paginas.append(bFrame(tamanhoPaginas))
        self.politicaSubistituicao = politicaSubistituicao
        self.posicaoMaisRecente = 0

    def substituir (self,content):
        if(self.politicas[politicaSubistituicao] == 'random'):
            indice = random.randint(0,len(self.paginas))
            paginaEscolhida = self.paginas[indice]
            if(paginaEscolhida.dirty):
                paginaEscolhida.salvarNoDisco()
            paginaEscolhida.freeSpace()
            paginaEscolhida.insertContent(content)
            self.posicaoMaisRecente = indice

        if(self.politicas[politicaSubistituicao] == 'maisRecente'):
            paginaEscolhida = self.paginas[self.posicaoMaisRecente]
            if(paginaEscolhida.dirty):
                paginaEscolhida.salvarNoDisco()
            paginaEscolhida.freeSpace()
            paginaEscolhida.insertContent(content)
        return True

    #retorna o indice da próxima pagina vazia, ou -1 caso não exista
    def getPaginaVazia(self):
        for i in range(0,len(self.paginas)):
            if(self.paginas[i].isEmpty()):
                return i
        return -1

    #tenta inserir na próxima página vazia, caso não exista substitui
    def inserirConteudo(self,conteudo):
        indiceVazia = self.getPaginaVazia
        if(indiceVazia != -1):
            self.paginas[indiceVazia].insertContent(conteudo)
            self.posicaoMaisRecente = indiceVazia
        else:
            self.substituir(conteudo)


class bFrame(object):
    #passa como parâmetro o tamanho da página
    def __init__(self,tamanhoPagina = 1024):
        self.tamanho = tamanhoPagina
        self.espacoLivre = tamanhoPagina
        self.conteudo = []
        self.dirty = False #a pagina fica suja quando há uma modificação nela
        self.maisRecenteUsado = 0 #página mais recente

    #Retorna true se couber tudo nesta página, caso contráio retorna false
    def checkInsert (self,content):
        return(len(content)>espacoLivre)

    #limpa a página
    def freeSpace (self):
        self.conteudo = []
        return True

    #retorna true se estiver vazia
    def isEmpty (self):
        return (self.conteudo == [])

    def insertContent (self,content):
        if(self.checkInsert(contetn)):
            for charactere in content:
                self.contudo.append(charactere)
            self.espacoLivre -= len(content)
            return True
        return False

    #salva a página direto no disco
    #Como neste trabalho não tem alteração isso não foi implementado
    def salvarNoDisco(self):
        return True

    #concatena tudo que tem no conteudo e retorna a string dele
    def read(self):
        return ''.join(map(str,self.conteudo))
