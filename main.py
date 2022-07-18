import sys

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

    # O método isRecognized() é o método responsável por ler uma nova palavra e identificar se ela é reconhecida pelo AFD
    # O loop interno inicia no estado inicial e com a primeira letra da palavra lida
    # e passa para o próximo estado caso encontre uma transição com essa letra
    # Caso nenhuma transição não seja encontrada o AFD iria para o estado de erro, ou seja, o resultado da palavra é "N"

    def isRecognized(self, word): #AFD
        currentState = self.verticeInitial
        letterIndex = 0
        found = False
        currentWordLetter = ''
        restWord = word

        select = 0

        raiz = NodoArvore(self.verticeInitial, restWord)

        for a in self.arestas:
            if a.inicio == currentState and a.letter == currentWordLetter:
                if a.fim is not None:
                    if select == 1:
                        s = raiz.value[1][:0] + raiz.value[1][(0 + 1):]
                        raiz.direita = NodoArvore(a.fim, s)
                    s = raiz.value[1][:0] + raiz.value[1][(0 + 1):]
                    raiz.esquerda = NodoArvore(a.fim, s)
                    select = 1

        while letterIndex < len(word):
            currentWordLetter = word[letterIndex]
            found = False
            for a in self.arestas:
                if a.inicio == currentState and a.letter == currentWordLetter:
                    currentState = a.fim
                    letterIndex = letterIndex + 1
                    found = True
                    break

            if not found:
                return "N"

        if currentState.isFinal:
            return "S"
        else:
            return "N"

    def isRecognized2(self, word): #AFND
        T = [(self.verticeInitial, word)]
        found = False
        end = False
        isFinalState = False
        accepted = False

        while True:
            for t in T:
                if t != None and t[1] != "":
                    for a in self.arestas:
                        letter_size = a.letter.__len__()
                        if a.inicio == t[0] and (a.letter == t[1][0:letter_size] or a.letter == "*"):
                            if a.letter == "*":
                                s = t[1]
                            else:
                                s = t[1][:0] + t[1][(0 + letter_size):]
                            if t[1][0] == "*":
                                k = a.inicio
                            else:
                                k = a.fim
                            T.append((k, s))
                            found = True
                    if found:
                        T.remove(t)
                    else:
                        T.remove(t)
                        T.append(None)

                    for x in T:
                        if x == None or x[1] == "":
                            end = True
                        else:
                            end = False
                            break

            if end == True:
                break

        for t in T:
            if t is not None:
                if t[0].isFinal == True and t[1] == "":
                    accepted = True
                    break

        if accepted:
            return "S"
        else:
            return "N"

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

    ## Entrada transicoes
    #print("Entrada transicoes")

    ######
    # n = 0
    # index = 0
    # part = ""
    # c = 1
    # tcoes1 = ""
    # tcoes2 = ""
    # tcoes3 = ""
    # while n < int(n_transicoes):  ## LEMBRAR DO <=
    #     transicoes = sys.stdin.readline()
    #     l = len(transicoes.rstrip())
    #     for t in transicoes.rstrip():
    #         if t != ' ':
    #             part = part + t
    #         else:
    #             if c == 1:
    #                 tcoes1 = part
    #                 part = ""
    #             if c == 2:
    #                 tcoes2 = part
    #                 part = ""
    #
    #             c = c + 1
    #         index = index + 1
    #
    #         if index == len(transicoes.rstrip()):
    #             tcoes3 = part
    #             part = ""
    #             c = 1
    #
    #     n = n + 1
    #     #print(n)
    #     index = 0
    #     grafo.adicionarAresta(tcoes2, tcoes1, tcoes3)

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

    # Entrada das palavras
    # print("Entrada palavras")
    palavras = sys.stdin.readline()
    cont = 0
    for p in palavras.rstrip():
        if p != ' ':
            word = word + p
        else:
            words.append(word)
            word = ''

        cont = cont + 1

        if cont == len(palavras.rstrip()):
            words.append(word)

    for w in words:
        out.write(grafo.isRecognized3(w) + '\n')
