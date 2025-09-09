import random
from graphviz import Digraph

# Nó da árvore
class Node:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None

# Árvore Binária
class BinaryTree:
    def __init__(self):
        self.raiz = None

    def inserir(self, valor):
        if self.raiz is None:
            self.raiz = Node(valor)
        else:
            self._inserir_rec(self.raiz, valor)

    def _inserir_rec(self, no, valor):
        if valor < no.valor:
            if no.esquerda is None:
                no.esquerda = Node(valor)
            else:
                self._inserir_rec(no.esquerda, valor)
        else:
            if no.direita is None:
                no.direita = Node(valor)
            else:
                self._inserir_rec(no.direita, valor)

    # Travessias recursivas
    def inorder(self, no=None):
        if no is None:
            no = self.raiz
        return (self.inorder(no.esquerda) if no.esquerda else []) + [no.valor] + \
               (self.inorder(no.direita) if no.direita else [])

    def preorder(self, no=None):
        if no is None:
            no = self.raiz
        return [no.valor] + \
               (self.preorder(no.esquerda) if no.esquerda else []) + \
               (self.preorder(no.direita) if no.direita else [])

    def postorder(self, no=None):
        if no is None:
            no = self.raiz
        return (self.postorder(no.esquerda) if no.esquerda else []) + \
               (self.postorder(no.direita) if no.direita else []) + [no.valor]

    # Visualização com graphviz
    def visualizar(self, nome="arvore"):
        dot = Digraph()
        def add_nodes_edges(no):
            if no:
                dot.node(str(no.valor), str(no.valor))
                if no.esquerda:
                    dot.edge(str(no.valor), str(no.esquerda.valor))
                    add_nodes_edges(no.esquerda)
                if no.direita:
                    dot.edge(str(no.valor), str(no.direita.valor))
                    add_nodes_edges(no.direita)
        add_nodes_edges(self.raiz)
        dot.render(nome, format="png", cleanup=True)
        print(f"Árvore gerada: {nome}.png")

if __name__ == "__main__":
    # Árvore fixa
    valores_fixos = [55, 30, 80, 20, 45, 70, 90]
    arvore1 = BinaryTree()
    for v in valores_fixos:
        arvore1.inserir(v)

    print("\nÁrvore com valores fixos:")
    arvore1.visualizar("arvore_fixa")
    print("Inorder :", arvore1.inorder())
    print("Preorder:", arvore1.preorder())
    print("Postorder:", arvore1.postorder())

    # Perguntar se deseja gerar a árvore randômica
    opcao = input("\nDeseja gerar e visualizar a árvore randômica? (s/n): ").strip().lower()
    if opcao == "s":
        valores_random = random.sample(range(1, 100), 10)
        arvore2 = BinaryTree()
        for v in valores_random:
            arvore2.inserir(v)

        print("\nÁrvore com valores randômicos:", valores_random)
        arvore2.visualizar("arvore_random")
        print("Inorder :", arvore2.inorder())
        print("Preorder:", arvore2.preorder())
        print("Postorder:", arvore2.postorder())
    else:
        print("Árvore randômica não gerada.")
