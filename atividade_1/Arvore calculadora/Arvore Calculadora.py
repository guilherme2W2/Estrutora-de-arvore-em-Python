from graphviz import Digraph


class No:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None


def arvore(no, Nivel=0):
    if no is not None:
        if Nivel == 0:
            print( str(no.valor))
            print()
        else:
            print(" " * (Nivel - 1) * 4 + str(no.valor))

        if no.esquerda is not None:
            arvore(no.esquerda, Nivel + 1, "Esquerda ")
        if no.direita is not None:
            arvore(no.direita, Nivel + 1, "Direita ")


def desenhar_arvore_png(raiz, nome_arquivo="arvore"):
    dot = Digraph(comment="Árvore Binária")
    dot.attr('node', shape='circle') 

    def add(n, pai=None):
        if n is None:
            return
        nid = str(id(n))  
        dot.node(nid, str(n.valor))  
        if pai is not None:
            dot.edge(str(id(pai)), nid)  
        add(n.esquerda, n)
        add(n.direita, n)

    add(raiz)  
    
    dot.render(nome_arquivo, format="png", cleanup=True)
    print(f"Árvore salva como {nome_arquivo}.png")


if __name__ == "__main__":
    
    n7 = No(7)
    n3 = No(3)
    n5 = No(5)
    n2 = No(2)

    # Nós internos (operadores)
    soma = No('+')
    soma.esquerda = n7
    soma.direita = n3

    subtracao = No('-')
    subtracao.esquerda = n5
    subtracao.direita = n2

    raiz = No('*')
    raiz.esquerda = soma
    raiz.direita = subtracao


    
    arvore(raiz)

 
    desenhar_arvore_png(raiz, "arvore")