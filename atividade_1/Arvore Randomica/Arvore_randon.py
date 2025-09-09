import random
from graphviz import Digraph

class Node:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None

def gerar_expressao():
    operadores = ["+", "-", "*", "/"]
    num_operadores = random.randint(2, 4)  
    operando_inicial = str(random.randint(1, 10))

    formula = operando_inicial
    for i in range(num_operadores):
        formula += " " + random.choice(operadores) + " " + str(random.randint(1, 10))

    return formula

def construir_arvore(formula):
    tokens = formula.split()
    transmissao = []
    operador = []
    comando = {"+": 1, "-": 1, "*": 2, "/": 2}

    for token in tokens:
        if token.isdigit():
            transmissao.append(Node(int(token)))
        elif token in comando:
            while (operador and operador[-1] in comando and comando[operador[-1]] >= comando[token]):
                no = Node(operador.pop())
                no.direita = transmissao.pop()
                no.esquerda = transmissao.pop()
                transmissao.append(no)
            operador.append(token)

    while operador:
        no = Node(operador.pop())
        no.direita = transmissao.pop()
        no.esquerda = transmissao.pop()
        transmissao.append(no)

    return transmissao[0] if transmissao else None

def desenhar_arvore(node, nome_arquivo="arvore"):
    dot = Digraph()
    
    def adicionar_no(no):
        if no:
            dot.node(str(id(no)), str(no.valor))
            if no.esquerda:
                dot.edge(str(id(no)), str(id(no.esquerda)))
                adicionar_no(no.esquerda)
            if no.direita:
                dot.edge(str(id(no)), str(id(no.direita)))
                adicionar_no(no.direita)

    adicionar_no(node)
    dot.render(nome_arquivo, format="png", cleanup=True)
    print(f"Árvore salva como {nome_arquivo}.png")

if __name__ == '__main__':
    expressao = gerar_expressao()
    print(f"Expressão gerada: {expressao}")
    arvore = construir_arvore(expressao)
    desenhar_arvore(arvore, "Arvore_randomica")
