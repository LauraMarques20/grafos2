import os
import grafoPonderado as gp
# import matplotlib.pyplot as plt

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

# print(deputados)

# Cria o grafo
grafo = gp.GrafoPonderado()
grafo.adiciona_nos(deputados)

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
        votacoesDeputados[partes[0]] = partes[2]

votacoesNormalizadas = []
for votos in votacoes:
    partes = votos.strip().split(";")
    valor1 = votacoesDeputados[partes[0]]
    valor2 = votacoesDeputados[partes[1]]
    novoPeso = int(partes[2]) / min(int(valor1), int(valor2))
    votos = partes[0] + ";" + partes[1] + ";" + str(novoPeso)
    votacoesNormalizadas.append(votos)

print(votacoesNormalizadas)

#threshold
votacoesThreshold = []
for votos in votacoesNormalizadas:
    partes = votos.strip().split(";")
    if float(partes[2]) >= float(threshold):
        votacoesThreshold.append(votos)

print(votacoesThreshold)

#inversao de pesos 
votacoesInversao = []
for votos in votacoesThreshold:
    partes = votos.strip().split(";")
    novoPeso = 1 - float(partes[2])
    votos = partes[0] + ";" + partes[1] + ";" + str(novoPeso)
    votacoesInversao.append(votos)

print(votacoesInversao)


# for linha in votacoes:
#     partes = linha.strip().split(";")
#     grafo.adicionar_aresta(partes[0], partes[1], partes[2])

# print(grafo.lista_adj)

# deputados_psdb = []
# for linha in linhas:
#     partes = linha.strip().split(';')
#     if partes[1] == 'PSDB':
#         deputados_psdb.append(partes[0])




