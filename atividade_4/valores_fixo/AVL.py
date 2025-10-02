import sys

class No:
    """Representa um nó na Árvore AVL."""
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None
        self.altura = 1

class AVLTree:
    """
    Implementa uma árvore de busca auto-balanceada (AVL).
    """
    def obter_altura(self, no):
        """Retorna a altura de um nó; 0 se o nó for nulo."""
        if not no:
            return 0
        return no.altura

    def calcular_fator_balanceamento(self, no):
        """Calcula o fator de balanceamento de um nó."""
        if not no:
            return 0
        return self.obter_altura(no.esquerda) - self.obter_altura(no.direita)

    def _rotacao_direita(self, z):
        """Realiza uma rotação simples para a direita."""
        y = z.esquerda
        T3 = y.direita
        y.direita = z
        z.esquerda = T3
        z.altura = 1 + max(self.obter_altura(z.esquerda), self.obter_altura(z.direita))
        y.altura = 1 + max(self.obter_altura(y.esquerda), self.obter_altura(y.direita))
        return y

    def _rotacao_esquerda(self, z):
        """Realiza uma rotação simples para a esquerda."""
        y = z.direita
        T2 = y.esquerda
        y.esquerda = z
        z.direita = T2
        z.altura = 1 + max(self.obter_altura(z.esquerda), self.obter_altura(z.direita))
        y.altura = 1 + max(self.obter_altura(y.esquerda), self.obter_altura(y.direita))
        return y

    def inserir(self, raiz, chave):
        """Insere uma chave e rebalanceia a árvore."""
      
        if not raiz:
            return No(chave)
        elif chave < raiz.chave:
            raiz.esquerda = self.inserir(raiz.esquerda, chave)
        else:
            raiz.direita = self.inserir(raiz.direita, chave)

       
        raiz.altura = 1 + max(self.obter_altura(raiz.esquerda), self.obter_altura(raiz.direita))

       
        balance = self.calcular_fator_balanceamento(raiz)

       
        if balance > 1 and chave < raiz.esquerda.chave:
            print(f"-> Rotação Simples à Direita em torno do nó {raiz.chave}")
            return self._rotacao_direita(raiz)

        
        if balance < -1 and chave > raiz.direita.chave:
            print(f"-> Rotação Simples à Esquerda em torno do nó {raiz.chave}")
            return self._rotacao_esquerda(raiz)

        
        if balance > 1 and chave > raiz.esquerda.chave:
            print(f"-> Rotação Dupla (Esquerda-Direita) em torno do nó {raiz.chave}")
            raiz.esquerda = self._rotacao_esquerda(raiz.esquerda)
            return self._rotacao_direita(raiz)

        
        if balance < -1 and chave < raiz.direita.chave:
            print(f"-> Rotação Dupla (Direita-Esquerda) em torno do nó {raiz.chave}")
            raiz.direita = self._rotacao_direita(raiz.direita)
            return self._rotacao_esquerda(raiz)

        return raiz

    def visualizar_arvore(self, no, nivel=0, prefixo="Raiz:"):
        """Imprime a estrutura da árvore de forma visual."""
        if no is not None:
            print(" " * (nivel * 4) + prefixo + str(no.chave) + f" (h={no.altura}, fb={self.calcular_fator_balanceamento(no)})")
            if no.esquerda is not None or no.direita is not None:
                self.visualizar_arvore(no.esquerda, nivel + 1, "E---")
                self.visualizar_arvore(no.direita, nivel + 1, "D---")


if __name__ == "__main__":
    print("======================================================")
    print("DEMONSTRAÇÃO 1: ROTAÇÃO SIMPLES (Inserindo 10, 20, 30)")
    print("======================================================")
    
    arvore_simples = AVLTree()
    raiz_simples = None
    chaves_simples = [10, 20, 30]

    for chave in chaves_simples:
        print(f"\n--- Inserindo {chave} ---")
        raiz_simples = arvore_simples.inserir(raiz_simples, chave)
        arvore_simples.visualizar_arvore(raiz_simples)
        print("-" * 20)

    print("\n\n======================================================")
    print("DEMONSTRAÇÃO 2: ROTAÇÃO DUPLA (Inserindo 10, 30, 20)")
    print("======================================================")

    arvore_dupla = AVLTree()
    raiz_dupla = None
    chaves_duplas = [10, 30, 20]

    for chave in chaves_duplas:
        print(f"\n--- Inserindo {chave} ---")
        raiz_dupla = arvore_dupla.inserir(raiz_dupla, chave)
        arvore_dupla.visualizar_arvore(raiz_dupla)
        print("-" * 20)
