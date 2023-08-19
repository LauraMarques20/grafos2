class GrafoPonderado:
    
    def __init__(self) -> None:
        self.lista_adj = {}
        self.num_nos = 0
        self.num_arestas = 0

    def adicionar_no(self, no):
        if no in self.lista_adj:
            print(f"AVISO: No {no} ja existe")
            return
        self.lista_adj[no] = {}
        self.num_nos += 1

    def adicionar_aresta(self, no1, no2, peso):
        try:
            self.lista_adj[no1][no2] = peso
            self.num_arestas += 1
        except KeyError as e:
            print(f"AVISO: No {e} não existe")

    def adiciona_nos(self, nos):
        for no in nos:
            self.adicionar_no(no)

    def adicionar_aresta_bidirecional(self, no1, no2, peso):
        self.adicionar_aresta(no1, no2, peso)
        self.adicionar_aresta(no2, no1, peso)

    def remove_aresta(self, no1, no2):
        try:
          self.lista_adj[no1].pop(no2)
          self.num_arestas -= 1
        except KeyError as e:
            print(f"AVISO: Aresta {no1} -> {no2} não existe")

    def verifica_aresta(self, no1, no2):
        try:
            if self.lista_adj[no1][no2] != None:
                return True
        except KeyError as e:
            return False
        
    def verifica_aresta_bidirecional(self, no1, no2):
        return self.verifica_aresta(no1, no2) and self.verifica_aresta(no2, no1)
    
    def soma_um_peso(self, no1, no2):
        if self.verifica_aresta(no1, no2):
            peso_atual = self.lista_adj[no1][no2]
            self.lista_adj[no1][no2] = peso_atual + 1
        else:
            print(f"AVISO: Aresta {no1} -> {no2} não existe")
    
    