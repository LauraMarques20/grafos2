import os
import grafoPonderado as gp
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import re
import random
import scipy as sp
import sys
filtroAno = input("Digite o ano desejado: ")
filtroPartido = input("Digite os partidos que deseja analisar, separado por virgulas: ")
threshold = input("Digite o threshold: ")

if filtroPartido != '':
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
    sys.exit()

if os.path.exists(caminho_arquivo_politicians):
    with open(caminho_arquivo_politicians, "r", encoding="utf-8", errors="replace") as arquivo:
        conteudo_politicians = arquivo.read()
else:
    print("O arquivo não foi encontrado.")
    sys.exit()

print("Arquivos carregados com sucesso. Aguarde...")

# Pega os deputados dos partidos desejados
deputados = []
for linha in conteudo_politicians.split("\n"):
    partes = linha.strip().split(";")
    if filtroPartido != '':
        if len(partes) >= 2 and partes[1] in filtroPartido:
            deputados.append(partes[0])
    else:
        if len(partes) >= 2:
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
    if filtroPartido != '':
        if len(partes) >= 2 and partes[1] in filtroPartido:
            dep2.append("(" + partes[1] + ") " + partes[0])
    else:
        if len(partes) >= 2:
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

centralidade = nx.betweenness_centrality(G)
#ordenar a centralidade
centralidade = {k: v for k, v in sorted(centralidade.items(), key=lambda item: item[1], reverse=True)}

#plotar o gráfico
plt.figure(figsize=(10, 10))

if filtroPartido != '':
    plt.title(f"Centralidade de intermediação dos deputados do {filtroPartido} no ano de {filtroAno}")
else:
    plt.title(f"Centralidade de intermediação dos deputados no ano de {filtroAno}")
plt.bar(centralidade.keys(), centralidade.values(), color='b')
plt.xlabel("Deputados")
plt.ylabel("Centralidade de intermediação")
plt.xticks(rotation=90, fontsize=6)
plt.tight_layout()
if filtroPartido != '':
    plt.savefig(f"betwenness{filtroPartido}{filtroAno}.png")
else:
    plt.savefig(f"betwenness{filtroAno}.png")
plt.close()

# #heatmap
nodes = list(grafoNormalizado.lista_adj.keys())
node_indices = {node: i for i, node in enumerate(nodes)}
num_nodes = len(nodes)
heatmap_data = np.zeros((num_nodes, num_nodes))
for source_node, connections in grafoNormalizado.lista_adj.items():
    for target_node, value in connections.items():
        source_idx = node_indices[source_node]
        target_idx = node_indices[target_node]
        heatmap_data[source_idx][target_idx] = value


plt.figure(figsize=(8, 6))
if filtroPartido != '':
    plt.title(f"Mapa de calor das votações dos deputados do {filtroPartido} no ano de {filtroAno}")
else:
    plt.title(f"Mapa de calor das votações dos deputados no ano de {filtroAno}")
plt.imshow(heatmap_data, cmap='hot', interpolation='nearest')
plt.xticks(np.arange(num_nodes), nodes, rotation=90, fontsize=4)
plt.yticks(np.arange(num_nodes), nodes, fontsize=4)


plt.colorbar()
plt.tight_layout()
if filtroPartido != '':
    plt.savefig(f"heatmap{filtroAno}{filtroPartido}.png")
else:
    plt.savefig(f"heatmap{filtroAno}.png")
plt.close()

#pegar todos os partidos 
partidos = []
for linha in conteudo_politicians.split("\n"):
    partes = linha.strip().split(";")
    if len(partes) >= 2 and partes[1] not in partidos:
        partidos.append(partes[1])

#grafo 
cores_partido = {partido: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for partido in partidos}

def extrair_partido(node_name):
    match = re.search(r'\((.*?)\)', node_name)
    if match:
        return match.group(1)
    return None
pos = nx.spring_layout(G)
node_colors = [cores_partido[extrair_partido(node)] for node in G.nodes()]
plt.figure(figsize=(10, 15))
nx.draw(G, pos=pos, with_labels=True, node_size=70, node_color=node_colors, font_size=6, font_color='black', font_weight='bold', width=0.5, edge_color='grey')
legend_labels = []
for partido, color in cores_partido.items():
    if any(extrair_partido(node) == partido for node in G.nodes()):
        legend_labels.append(plt.Line2D([0], [0], color=color, lw=4, label=partido))
plt.legend(handles=legend_labels, loc='upper right', fontsize=8)
if filtroPartido != '':
    plt.title(f"Grafo dos deputados do {filtroPartido} no ano de {filtroAno}")
else:
    plt.title(f"Grafo dos deputados do {filtroPartido}")
if filtroPartido != '':
    plt.savefig(f"graph{filtroAno}{filtroPartido}.png")
else:
    plt.savefig(f"graph{filtroAno}.png")
plt.close()

print ("Os arquivos foram salvos em formato png")
if filtroPartido != '':
    print(f"betwenness{filtroPartido}{filtroAno}.png")
    print(f"heatmap{filtroAno}{filtroPartido}.png")
    print(f"graph {filtroAno}{filtroPartido}.png")
else:
    print(f"betwenness{filtroAno}.png")
    print(f"heatmap{filtroAno}.png")
    print(f"graph{filtroAno}.png")



