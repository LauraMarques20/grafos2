import os
import grafoPonderado as gp
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import re
filtroAno = input("Digite o ano desejado: ")
filtroPartido = input("Digite os partidos que deseja analisar, separado por virgulas: ")
threshold = input("Digite o threshold: ")

#retirar os espaços
filtroPartido = filtroPartido.replace(" ", "")

#separar os partidos
filtroPartido = filtroPartido.split(",")


# Caminho para os arquivos
caminho_arquivo_graph = os.path.join("datasets", f"graph{filtroAno}.txt")
caminho_arquivo_politicians = os.path.join("datasets", f"politicians{filtroAno}.txt")

if os.path.exists(caminho_arquivo_graph):
    with open(caminho_arquivo_graph, "r", encoding="utf-8", errors="replace") as arquivo:
        conteudo_graph = arquivo.read()
    
else:
    print("O arquivo não foi encontrado.")

if os.path.exists(caminho_arquivo_politicians):
    with open(caminho_arquivo_politicians, "r", encoding="utf-8", errors="replace") as arquivo:
        conteudo_politicians = arquivo.read()
else:
    print("O arquivo não foi encontrado.")


# Pega os deputados dos partidos desejados
deputados = []
for linha in conteudo_politicians.split("\n"):
    partes = linha.strip().split(";")
    if len(partes) >= 2 and partes[1] in filtroPartido:
        deputados.append(partes[0])


#pegar as votações em comum entre os deputados
votacoes = []
for linha in conteudo_graph.split("\n"):
    partes = linha.strip().split(";")
    if len(partes) >= 2 and partes[0] in deputados and partes[1] in deputados:
        votacoes.append(linha)

#normalizar os pesos
votacoesDeputados = {}
for linha in conteudo_politicians.split("\n"):
    partes = linha.strip().split(";")
    if len(partes) >= 2 and partes[0] in deputados:
        votacoesDeputados[partes[0]] = {'total': partes[2], 'partido': partes[1]}

votNormalizadas = []
for votos in votacoes:
    partes = votos.strip().split(";")
    valor1 = votacoesDeputados[partes[0]]['total']
    valor2 = votacoesDeputados[partes[1]]['total']
    novoPeso = int(partes[2]) / min(int(valor1), int(valor2))
    votos = "(" + votacoesDeputados[partes[0]]['partido'] + ") " + partes[0] + ";" +  "(" + votacoesDeputados[partes[1]]['partido'] + ") " + partes[1] + ";" + str(novoPeso)
    votNormalizadas.append(votos)
votacoesNormalizadas = sorted(votNormalizadas)

#muda os deputados para o formato (partido) nome
dep2 = []
for linha in conteudo_politicians.split("\n"):
    partes = linha.strip().split(";")
    if len(partes) >= 2 and partes[1] in filtroPartido:
        dep2.append("(" + partes[1] + ") " + partes[0])

deputados2 = sorted(dep2)

grafoNormalizado = gp.GrafoPonderado()
grafoNormalizado.adiciona_nos(deputados2)
#adicionar as arestas
for l in votacoesNormalizadas:
    partes = l.strip().split(";")
    grafoNormalizado.adicionar_aresta(partes[0], partes[1], partes[2])


#threshold
votacoesThreshold = []
for votos in votacoesNormalizadas:
    partes = votos.strip().split(";")
    if float(partes[2]) >= float(threshold):
        votacoesThreshold.append(votos)

#inversao de pesos 
votacoesInversao = []
for votos in votacoesThreshold:
    partes = votos.strip().split(";")
    novoPeso = 1 - float(partes[2])
    votos = partes[0] + ";" + partes[1] + ";" + str(novoPeso)
    votacoesInversao.append(votos)


# Cria o grafo threshold
grafo = gp.GrafoPonderado()
grafo.adiciona_nos(deputados2) 
#adicionar as arestas
for linha in votacoesInversao:
    partes = linha.strip().split(";")
    grafo.adicionar_aresta(partes[0], partes[1], partes[2])


# #calcular centralidade
G = nx.Graph()
for node in grafo.lista_adj:
    G.add_node(node)

for node, neighbors in grafo.lista_adj.items():
    for neighbor, weight_str in neighbors.items():
        weight = float(weight_str)
        G.add_edge(node, neighbor, weight=weight)

# centralidade = nx.betweenness_centrality(G, weight='weight')
# #ordenar a centralidade
# centralidade = {k: v for k, v in sorted(centralidade.items(), key=lambda item: item[1], reverse=True)}

# #plotar o gráfico
# plt.figure(figsize=(10, 10))

# plt.title(f"Centralidade de intermediação dos deputados do {filtroPartido} no ano de {filtroAno}")
# plt.bar(centralidade.keys(), centralidade.values(), color='b')
# plt.xlabel("Deputados")
# plt.ylabel("Centralidade de intermediação")
# plt.xticks(rotation=90, fontsize=6)
# plt.tight_layout()
# # plt.savefig(f"centralidade{filtroAno}.png")
# # plt.show()

#heatmap
# nodes = list(grafoNormalizado.lista_adj.keys())
# node_indices = {node: i for i, node in enumerate(nodes)}
# num_nodes = len(nodes)
# heatmap_data = np.zeros((num_nodes, num_nodes))
# for source_node, connections in grafoNormalizado.lista_adj.items():
#     for target_node, value in connections.items():
#         source_idx = node_indices[source_node]
#         target_idx = node_indices[target_node]
#         heatmap_data[source_idx][target_idx] = value


# plt.figure(figsize=(8, 6))
# plt.title(f"Mapa de calor das votações dos deputados do {filtroPartido} no ano de {filtroAno}")
# plt.imshow(heatmap_data, cmap='hot', interpolation='nearest')
# plt.xticks(np.arange(num_nodes), nodes, rotation=90, fontsize=4)
# plt.yticks(np.arange(num_nodes), nodes, fontsize=4)


# plt.colorbar()
# plt.tight_layout()
# # plt.savefig(f"heatmap{filtroAno}.png")
# plt.show()



#grafo 
party_colors = {
    'PSDB': 'blue',
    'PT': 'red',
    'PSB': 'green',
    'PSOL': 'purple'
}

def extract_party(node_name):
    match = re.search(r'\((.*?)\)', node_name)
    if match:
        return match.group(1)
    return None
pos = nx.spring_layout(G)
node_colors = [party_colors[extract_party(node)] for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_size=1000, node_color=node_colors, font_size=10, font_color='black', font_weight='bold')
plt.show()




