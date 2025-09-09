# arvore_random.py
import random
import os
from graphviz import Digraph


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, current, value):
        if value < current.value:
            if current.left is None:
                current.left = Node(value)
            else:
                self._insert(current.left, value)
        elif value > current.value:
            if current.right is None:
                current.right = Node(value)
            else:
                self._insert(current.right, value)

    def search(self, value):
        return self._search(self.root, value)

    def _search(self, current, value):
        if current is None:
            return False
        if current.value == value:
            return True
        elif value < current.value:
            return self._search(current.left, value)
        else:
            return self._search(current.right, value)

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, current, value):
        if current is None:
            return current
        if value < current.value:
            current.left = self._delete(current.left, value)
        elif value > current.value:
            current.right = self._delete(current.right, value)
        else:
            if current.left is None and current.right is None:
                return None
            elif current.left is None:
                return current.right
            elif current.right is None:
                return current.left
            else:
                successor = self._min_value_node(current.right)
                current.value = successor.value
                current.right = self._delete(current.right, successor.value)
        return current

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def depth(self, value):
        return self._depth(self.root, value, 0)

    def _depth(self, node, value, d):
        if node is None:
            return -1
        if node.value == value:
            return d
        elif value < node.value:
            return self._depth(node.left, value, d + 1)
        else:
            return self._depth(node.right, value, d + 1)

    def visualize(self, filename):
        dot = Digraph()
        if self.root:
            self._add_nodes(dot, self.root)

        dir_name = os.path.dirname(filename)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        dot.render(filename, format="png", cleanup=True)
        print(f"Árvore gerada em {filename}.png")

    def _add_nodes(self, dot, node):
        if node.left:
            dot.node(str(node.left.value))
            dot.edge(str(node.value), str(node.left.value))
            self._add_nodes(dot, node.left)
        if node.right:
            dot.node(str(node.right.value))
            dot.edge(str(node.value), str(node.right.value))
            self._add_nodes(dot, node.right)


if __name__ == "__main__":
    bst = BinarySearchTree()
    valores = random.sample(range(1, 200), 15)
    for v in valores:
        bst.insert(v)

    print("Árvore aleatória criada:", valores)
    bst.visualize("arvore_random")
    print("Altura inicial da árvore:", bst.height())

    # ----------------------------
    # MENU INTERATIVO
    # ----------------------------
    while True:
        print("\n=== MENU ÁRVORE BINÁRIA RANDOM ===")
        print("1 - Inserir valor")
        print("2 - Buscar valor")
        print("3 - Remover valor")
        print("4 - Calcular altura")
        print("5 - Calcular profundidade de um nó")
        print("6 - Visualizar árvore")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            val = int(input("Digite o valor a ser inserido: "))
            bst.insert(val)
            print(f"Valor {val} inserido.")

        elif opcao == "2":
            val = int(input("Digite o valor a ser buscado: "))
            print("Encontrado!" if bst.search(val) else "Não encontrado.")

        elif opcao == "3":
            val = int(input("Digite o valor a ser removido: "))
            bst.delete(val)
            print(f"Valor {val} removido (se existia).")

        elif opcao == "4":
            print("Altura da árvore:", bst.height())

        elif opcao == "5":
            val = int(input("Digite o valor do nó: "))
            d = bst.depth(val)
            if d == -1:
                print("Nó não encontrado.")
            else:
                print(f"Profundidade do nó {val}: {d}")

        elif opcao == "6":
            nome = input("Nome do arquivo (sem extensão): ")
            bst.visualize(nome)

        elif opcao == "0":
            print("Encerrando programa...")
            break

        else:
            print("Opção inválida, tente novamente.")
