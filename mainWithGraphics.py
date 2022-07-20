import sys
import random
import string
import time
import scipy.optimize as so
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class NodoArvore:
    def __init__(self, state, restWord, esquerda=None, direita=None):
        self.value = (state, restWord)
        self.esquerda = esquerda
        self.direita = direita


class Aresta:

    # Classe Aresta com atributos de letra da transição, vértice de inicio e vértice de fim

    def __init__(self, letter, inicio, fim, desempilha, empilha):
        self.letter = letter
        self.inicio = inicio
        self.fim = fim
        self.desempilha = desempilha
        self.empilha = empilha

class Vertice:
    # Classe Vertice com atributos de dado (nome do estado), se é inicial e se é final.

    isInitial = False
    isFinal = False

    def __init__(self, dado):
        self.dado = dado


class Grafo:

    # Classe Grafo com atributos de lista de vertices, listas de arestas e vertice inicial.

    def __init__(self):
        self.verticeInitial = None
        self.arestas = []
        self.vertices = []

    def adicionarVertice(self, dado):
        vertice = Vertice(dado)
        self.vertices.append(vertice)

    def adicionarAresta(self, letter, dadoInicio, dadoFim, desempilha, empilha):
        inicio = self.getVertice(dadoInicio)
        fim = self.getVertice(dadoFim)

        aresta = Aresta(letter, inicio, fim, desempilha, empilha)

        self.arestas.append(aresta)

    def getVertice(self, dado):
        for v in self.vertices:
            if v.dado == dado:
                return v

    def setInitial(self, dado):
        for v in self.vertices:
            if v.dado == dado:
                v.isInitial = True
                self.verticeInitial = v
                break

    def setFinal(self, dado):
        for v in self.vertices:
            if v.dado == dado:
                v.isFinal = True
                break

    def isRecognized3(self, word): #APND
        T = [(self.verticeInitial, word, "")]
        found = False
        end = False
        accepted = False

        while True:
            for t in T:
                if t != None:
                    if t[1] == "*" and t[0].isInitial and t[0].isFinal:
                        end = True
                        break
                    for a in self.arestas:
                        if (a.inicio == t[0] and (a.letter == t[1][0:1] or a.letter == "*")) or (a.inicio == t[0] and t[1] == "*"):
                            if a.letter == "*":
                                restWord = t[1]
                            else:
                                restWord = t[1][:0] + t[1][(0 + 1):]

                            pilha = t[2]
                            desempilha_size = a.desempilha.__len__()

                            if t[2] == "" and a.desempilha != "*":
                                continue
                            elif t[2] == "" and a.desempilha == "*":
                                pilha = t[2]
                            elif t[2] != "" and a.desempilha == "*":
                                pilha = t[2]
                            elif a.desempilha == t[2][0:desempilha_size]:
                                #Desempilha
                                pilha = t[2][:0] + t[2][(0 + desempilha_size):]
                            else:
                                continue

                            if a.empilha != "*":
                                # Empilha
                                pilha = a.empilha + pilha
                            nextState = a.fim

                            T.append((nextState, restWord, pilha))
                            found = True
                    if found:
                        T.remove(t)
                    else:
                        T.remove(t)

                    if T.__len__() != 0:
                        haveLambdaTransition = False
                        for x in T:
                            for a in self.arestas:
                                if x[2] != '':
                                    if a.inicio == x[0] and a.letter == "*" and a.desempilha == x[2][0]:
                                        haveLambdaTransition = True
                                        break
                            if (x is None or x[1] == "" or x[1] == "*") and haveLambdaTransition is False:
                                end = True
                            else:
                                end = False
                                break
                    else:
                        end = True

                    if end is True:
                        break

                for t in T:
                    if t is not None:
                        if t[0].isFinal == True and (t[1] == "" or t[1] == "*") and t[2] == "":
                            accepted = True
                            break

                if accepted:
                    return "S"

            if end is True:
                break #

        for t in T:
            if t is not None:
                if t[0].isFinal == True and (t[1] == "" or t[1] == "*") and t[2] == "":
                    accepted = True
                    break

        if accepted:
            return "S"
        else:
            return "N"

    def specific_string(self, length, s_string):
        sample_string = s_string  # define the specific string
        # define the condition for random string
        result = ''.join((random.choice(sample_string)) for x in range(length))
        return result

if __name__ == '__main__':

    grafo = Grafo()

    alfabeto = []
    alfabetoPilha = []
    word = ''
    words = []
    out = sys.stdout

    # Entrada de estados
    # print("Entrada de estados")
    estados = sys.stdin.readline()
    for s in estados.rstrip():
        if s != ' ':
            grafo.adicionarVertice(s)

    # Entrada do alfabeto
    # print("Entrada do alfabeto")
    alfabeto = sys.stdin.readline()
    for a in alfabeto:
        if a != ' ':
            alfabeto = alfabeto + a

    # Entrada do alfabeto de pilha
    # print("Entrada do alfabeto de pilha")
    alfabetoPilha = sys.stdin.readline()
    for a in alfabetoPilha:
        if a != ' ':
            alfabeto = alfabetoPilha + a

    # Entrada do numero de transicoes
    # print("Entrada do numero de transicoes")
    n_transicoes = sys.stdin.readline().rstrip()

    # Entrada transicoes
    # print("Entrada transicoes")
    n = 0
    while n < int(n_transicoes): ## LEMBRAR DO <=
        transicoes = sys.stdin.readline()
        if transicoes.rstrip() != '':
            n = n + 1
            empilha = transicoes[8:transicoes.rstrip().__len__()]
            grafo.adicionarAresta(transicoes[2], transicoes[0], transicoes[6], transicoes[4], empilha)

    # Entrada do estado inicial
    # print("Estado inicial")
    estado_inicial = sys.stdin.readline()
    grafo.setInitial(estado_inicial.rstrip())

    # Entrada de estados finais
    # print("Entrada estados finais")
    estados_finais = sys.stdin.readline()
    for s in estados_finais.rstrip():
        if s != ' ':
            grafo.setFinal(s)

    #########################

    results_list = []

    wa = 'aaaaa'
    wb = 'bbbbb'
    input_list = []

    i = 0

    for i in range(300):
        sustenido = "#"
        w = wa + wb
        input_list.append(w)
        # roda
        wa = wa + 'aaaaaaaaaaaaaaaaaaaa'
        wb = wb + 'bbbbbbbbbbbbbbbbbbbb'

    #print(input_list)

    # input_list = ['ab','aabb','aaaabbbb','aaaaabbbbb','aaaaaaaaabbbbbb','aaaaaaaaaaaaaaaabbbbbbbbbbbbbb','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbb']
    input_list_size = []
    execution_time_list = []
    i = 0
    while i < input_list.__len__():
        words.append(input_list[i])
        i = i + 1

    for w in words:
        inicio = time.time()
        results_list.append(grafo.isRecognized3(w))
        fim = time.time()
        execution_time_list.append((fim-inicio))

    print(execution_time_list)
    print(results_list)

    i = 0
    while i < input_list.__len__():
        input_list_size.append(input_list[i].__len__())
        i = i + 1

    print(input_list_size)

    x = np.array(input_list_size)
    y = np.array(execution_time_list)

    mod_linear = np.polyfit(x, y, 1)
    print(mod_linear)
    print(mod_linear[0])

    a = float(mod_linear[0])
    b = float(mod_linear[1])

    y_mod = a * x + b

    plt.plot(input_list_size, execution_time_list, "o", label="Execuções de palavras")
    plt.plot(x,y_mod, "-r", label="Regressão Linear")
    plt.xlabel("Quantidade de caracteres da palavra de entrada")
    plt.ylabel("Tempo de execução (em segundos)")
    plt.title("Análise de execução do AP")
    plt.legend()
    plt.show()
