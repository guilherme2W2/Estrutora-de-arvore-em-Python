class No:
    """
    Representa um nó na Árvore AVL.
    Cada nó armazena uma chave, referências para os filhos e sua altura.
    """
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None
        self.altura = 1 # A altura de um novo nó (folha) é sempre 1

class ArvoreAVL:
    """
    Implementa a estrutura e as operações de uma Árvore AVL.
    """
    def __init__(self):
        self.raiz = None

    # ===============================================================
    # TAREFA 0: IMPLEMENTAR MÉTODOS AUXILIARES E ROTAÇÕES
    # ===============================================================

    def obter_altura(self, no):
        """
        Calcula a altura de um nó. Se o nó for nulo, a altura é 0.
        """
        if not no:
            return 0
        return no.altura

    def obter_fator_balanceamento(self, no):
        """
        Calcula o fator de balanceamento de um nó (altura da subárvore esquerda - altura da subárvore direita).
        """
        if not no:
            return 0
        return self.obter_altura(no.esquerda) - self.obter_altura(no.direita)

    def _atualizar_altura(self, no):
        """
        Atualiza a altura de um nó com base na altura máxima de seus filhos.
        A altura é 1 + max(altura(esquerda), altura(direita)).
        """
        if not no:
            return
        no.altura = 1 + max(self.obter_altura(no.esquerda), self.obter_altura(no.direita))

    def obter_no_valor_minimo(self, no):
        """
        Encontra o nó com o menor valor em uma subárvore (o nó mais à esquerda).
        """
        if no is None or no.esquerda is None:
            return no
        return self.obter_no_valor_minimo(no.esquerda)

    def _rotacao_direita(self, no_pivo):
        """
        Realiza uma rotação para a direita em torno do no_pivo.
        """
        nova_raiz = no_pivo.esquerda
        filho_direita_da_nova_raiz = nova_raiz.direita
        
        # Realiza a rotação
        nova_raiz.direita = no_pivo
        no_pivo.esquerda = filho_direita_da_nova_raiz
        
        # Atualiza as alturas
        self._atualizar_altura(no_pivo)
        self._atualizar_altura(nova_raiz)
        
        return nova_raiz

    def _rotacao_esquerda(self, no_pivo):
        """
        Realiza uma rotação para a esquerda em torno do no_pivo.
        """
        nova_raiz = no_pivo.direita
        filho_esquerda_da_nova_raiz = nova_raiz.esquerda

        # Realiza a rotação
        nova_raiz.esquerda = no_pivo
        no_pivo.direita = filho_esquerda_da_nova_raiz

        # Atualiza as alturas
        self._atualizar_altura(no_pivo)
        self._atualizar_altura(nova_raiz)

        return nova_raiz

    # ===============================================================
    # TAREFA 1: IMPLEMENTAR INSERÇÃO E DELEÇÃO COM BALANCEAMENTO
    # ===============================================================

    def inserir(self, chave):
        """Método público para inserir uma chave na árvore."""
        self.raiz = self._inserir_recursivo(self.raiz, chave)

    def _inserir_recursivo(self, no_atual, chave):
        # Passo 1: Realiza a inserção padrão de uma BST.
        if not no_atual:
            return No(chave)
        elif chave < no_atual.chave:
            no_atual.esquerda = self._inserir_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._inserir_recursivo(no_atual.direita, chave)
        else:
            # Chaves duplicadas não são permitidas
            raise ValueError("Chave duplicada não permitida na Árvore AVL.")

        # Passo 2: Atualiza a altura do nó atual (ancestral) após a inserção.
        self._atualizar_altura(no_atual)

        # Passo 3: Calcula o fator de balanceamento para verificar se o nó ficou desbalanceado.
        fator_balanceamento = self.obter_fator_balanceamento(no_atual)

        # Passo 4: Verifica se o nó ficou desbalanceado e aplica as rotações corretas.
        # Caso 1: Desbalanceamento à Esquerda-Esquerda (Rotação Simples à Direita)
        if fator_balanceamento > 1 and chave < no_atual.esquerda.chave:
            return self._rotacao_direita(no_atual)

        # Caso 2: Desbalanceamento à Direita-Direita (Rotação Simples à Esquerda)
        if fator_balanceamento < -1 and chave > no_atual.direita.chave:
            return self._rotacao_esquerda(no_atual)

        # Caso 3: Desbalanceamento à Esquerda-Direita (Rotação Dupla)
        if fator_balanceamento > 1 and chave > no_atual.esquerda.chave:
            no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
            return self._rotacao_direita(no_atual)

        # Caso 4: Desbalanceamento à Direita-Esquerda (Rotação Dupla)
        if fator_balanceamento < -1 and chave < no_atual.direita.chave:
            no_atual.direita = self._rotacao_direita(no_atual.direita)
            return self._rotacao_esquerda(no_atual)
        
        return no_atual

    def deletar(self, chave):
        """Método público para deletar uma chave da árvore."""
        self.raiz = self._deletar_recursivo(self.raiz, chave)

    def _deletar_recursivo(self, no_atual, chave):
        # Passo 1: Realiza a deleção padrão de uma BST.
        if not no_atual:
            return no_atual # Nó não encontrado

        if chave < no_atual.chave:
            no_atual.esquerda = self._deletar_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._deletar_recursivo(no_atual.direita, chave)
        else: # Nó encontrado
            # Caso 1: Nó com um filho ou nenhum filho.
            if no_atual.esquerda is None:
                temp = no_atual.direita
                no_atual = None
                return temp
            elif no_atual.direita is None:
                temp = no_atual.esquerda
                no_atual = None
                return temp
            
            # Caso 2: Nó com dois filhos.
            # Encontra o sucessor em ordem (menor nó da subárvore direita)
            sucessor = self.obter_no_valor_minimo(no_atual.direita)
            no_atual.chave = sucessor.chave # Copia a chave do sucessor
            # Deleta o sucessor
            no_atual.direita = self._deletar_recursivo(no_atual.direita, sucessor.chave)

        # Se a árvore tinha apenas um nó, retorna
        if no_atual is None:
            return no_atual

        # Passo 2: Atualiza a altura do nó atual.
        self._atualizar_altura(no_atual)

        # Passo 3: Calcula o fator de balanceamento.
        fator_balanceamento = self.obter_fator_balanceamento(no_atual)

        # Passo 4: Verifica o desbalanceamento e aplica as rotações.
        # Rotação Simples à Direita (Esquerda-Esquerda)
        if fator_balanceamento > 1 and self.obter_fator_balanceamento(no_atual.esquerda) >= 0:
            return self._rotacao_direita(no_atual)

        # Rotação Simples à Esquerda (Direita-Direita)
        if fator_balanceamento < -1 and self.obter_fator_balanceamento(no_atual.direita) <= 0:
            return self._rotacao_esquerda(no_atual)

        # Rotação Dupla Esquerda-Direita
        if fator_balanceamento > 1 and self.obter_fator_balanceamento(no_atual.esquerda) < 0:
            no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
            return self._rotacao_direita(no_atual)

        # Rotação Dupla Direita-Esquerda
        if fator_balanceamento < -1 and self.obter_fator_balanceamento(no_atual.direita) > 0:
            no_atual.direita = self._rotacao_direita(no_atual.direita)
            return self._rotacao_esquerda(no_atual)

        return no_atual

    # ===============================================================
    # TAREFA 2 E 3: IMPLEMENTAR BUSCAS
    # ===============================================================

    def encontrar_nos_intervalo(self, chave_min, chave_max):
        """
        Encontra e retorna uma lista com todas as chaves no intervalo [chave_min, chave_max].
        """
        resultado = []
        self._encontrar_nos_intervalo_recursivo(self.raiz, chave_min, chave_max, resultado)
        return resultado

    def _encontrar_nos_intervalo_recursivo(self, no, chave_min, chave_max, resultado):
        if not no:
            return

        # Se a chave do nó atual for maior que a chave mínima, pode haver chaves no intervalo na subárvore esquerda
        if chave_min < no.chave:
            self._encontrar_nos_intervalo_recursivo(no.esquerda, chave_min, chave_max, resultado)
        
        # Se a chave do nó atual estiver dentro do intervalo, adicione-a ao resultado
        if chave_min <= no.chave <= chave_max:
            resultado.append(no.chave)
            
        # Se a chave do nó atual for menor que a chave máxima, pode haver chaves no intervalo na subárvore direita
        if chave_max > no.chave:
            self._encontrar_nos_intervalo_recursivo(no.direita, chave_min, chave_max, resultado)

    def obter_profundidade_no(self, chave):
        """
        Calcula a profundidade (nível) de um nó com uma chave específica.
        A raiz está no nível 0. Se o nó não for encontrado, retorna -1.
        """
        no_atual = self.raiz
        profundidade = 0
        while no_atual is not None:
            if chave == no_atual.chave:
                return profundidade
            elif chave < no_atual.chave:
                no_atual = no_atual.esquerda
            else:
                no_atual = no_atual.direita
            profundidade += 1
        return -1 # Nó não encontrado

    # --- Função auxiliar para visualização ---
    def percurso_em_ordem(self):
        """Retorna uma lista com as chaves em ordem."""
        resultado = []
        self._percurso_em_ordem_recursivo(self.raiz, resultado)
        return resultado

    def _percurso_em_ordem_recursivo(self, no, resultado):
        if no:
            self._percurso_em_ordem_recursivo(no.esquerda, resultado)
            resultado.append(no.chave)
            self._percurso_em_ordem_recursivo(no.direita, resultado)

# --- Bloco de Teste e Demonstração da Atividade AVL ---
if __name__ == "__main__":
    arvore_avl = ArvoreAVL()
    
    print("\n--- ATIVIDADE PRÁTICA: ÁRVORE AVL ---")
    
    print("\n--- 1. Inserindo nós ---")
    chaves_para_inserir = [9, 5, 10, 0, 6, 11, -1, 1, 2]
    try:
        for chave in chaves_para_inserir:
            arvore_avl.inserir(chave)
        print("Inserção concluída (sem erros).")
        print(f"Árvore em ordem após inserção: {arvore_avl.percurso_em_ordem()}")
    except Exception as e:
        print(f"\nERRO DURANTE A INSERÇÃO: {e}")

    print("\n--- 2. Deletando nós ---")
    try:
        chaves_para_deletar = [10, 11]
        for chave in chaves_para_deletar:
            arvore_avl.deletar(chave)
        print("Deleção concluída (sem erros).")
        print(f"Árvore em ordem após deleção: {arvore_avl.percurso_em_ordem()}")
    except Exception as e:
        print(f"\nERRO DURANTE A DELEÇÃO: {e}")

    print("\n--- 3. Buscando nós no intervalo [1, 9] ---")
    try:
        nos_no_intervalo = arvore_avl.encontrar_nos_intervalo(1, 9)
        if nos_no_intervalo is not None:
            print(f"Nós encontrados: {sorted(nos_no_intervalo)}")
        else:
            print("Método `encontrar_nos_intervalo` ainda não implementado.")
    except Exception as e:
        print(f"\nERRO DURANTE A BUSCA POR INTERVALO: {e}")

    print("\n--- 4. Calculando profundidade do nó 6 ---")
    try:
        profundidade = arvore_avl.obter_profundidade_no(6)
        if profundidade is not None:
            if profundidade != -1:
                print(f"O nó 6 está no nível/profundidade: {profundidade}")
            else:
                print("O nó 6 não foi encontrado.")
        else:
            print("Método `obter_profundidade_no` ainda não implementado.")
    except Exception as e:
        print(f"\nERRO DURANTE O CÁLCULO DE PROFUNDIDADE: {e}")