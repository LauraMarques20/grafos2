import os
filtroAno = input("Digite o ano desejado: ")
filtroPartido = input("Digite os partidos que deseja analisar, separado por virgulas: ")

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
deputados = {}
for linha in conteudo_politicians.split("\n"):
    partes = linha.strip().split(";")
    if len(partes) >= 2 and partes[1] in filtroPartido:
        deputados[partes[0]] = partes[1]

print(deputados)

# deputados_psdb = []
# for linha in linhas:
#     partes = linha.strip().split(';')
#     if partes[1] == 'PSDB':
#         deputados_psdb.append(partes[0])




