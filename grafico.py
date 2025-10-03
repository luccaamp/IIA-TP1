import os
from tabulate import tabulate
from search import plan  
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

PASTA_MAPAS = "maps"

algoritmos = [
    ("BFS", "bfs", None),
    ("DFS", "dfs", None),
    ("UCS", "ucs", None),
    ("Greedy Euclidiana", "greedy", "euclidian"),
    ("Greedy Manhattan", "greedy", "manhattan"),
    ("A* Euclidiana", "astar", "euclidian"),
    ("A* Manhattan", "astar", "manhattan")
]

def carregar_mapas(pasta):
    mapas = {}
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".txt"):
            caminho = os.path.join(pasta, arquivo)
            with open(caminho, "r") as f:
                mapas[arquivo] = f.read()
    return mapas

def comparar_desempenho(mapas, algoritmos):
    resultados_por_mapa = {}
    
    for nome_mapa, mapa in mapas.items():
        resultados = {}

        # roda todos os algoritmos no mapa
        for nome_algo, algo, heur in algoritmos:
            path, custo, visited = plan(mapa, algorithm=algo, heuristic=heur)
            tamanho = len(path) if path else float("inf")
            nos_visitados = len(visited)

            resultados[nome_algo] = {
                "Visitados": nos_visitados,
                "Tamanho": tamanho,
                "Custo": round(custo, 2) if path else float("inf")
            }

        resultados_por_mapa[nome_mapa] = resultados

        # tabela colorida
        min_visitados = min(r["Visitados"] for r in resultados.values())
        min_tamanho   = min(r["Tamanho"] for r in resultados.values())
        min_custo     = min(r["Custo"] for r in resultados.values())

        def colorir(valor, minimo):
            return f"\033[92m{valor}\033[0m" if valor == minimo else str(valor)

        headers = [""] + [nome_algo for nome_algo, _, _ in algoritmos]
        tabela = [
            ["Visitados"] + [colorir(resultados[nome_algo]["Visitados"], min_visitados) for nome_algo, _, _ in algoritmos],
            ["Tamanho"]   + [colorir(resultados[nome_algo]["Tamanho"],   min_tamanho)   for nome_algo, _, _ in algoritmos],
            ["Custo"]     + [colorir(resultados[nome_algo]["Custo"],     min_custo)     for nome_algo, _, _ in algoritmos],
        ]

        print("\n" + "="*60)
        print(f" {nome_mapa} ".center(60, "="))
        print("="*60)
        print(tabulate(tabela, headers=headers, tablefmt="grid"))

    # plota heatmaps para todas as métricas
    plotar_heatmaps(resultados_por_mapa, algoritmos)

def plotar_heatmaps(resultados_por_mapa, algoritmos):
    metricas = ["Visitados", "Custo", "Tamanho"]
    mapas = list(resultados_por_mapa.keys())
    algoritmos_nomes = [nome for nome, _, _ in algoritmos]

    # cria pasta "imagens" se não existir
    if not os.path.exists("imagens"):
        os.makedirs("imagens")

    for metrica in metricas:
        # cria matriz de valores: linhas = mapas, colunas = algoritmos
        matriz = []
        for mapa in mapas:
            linha = [resultados_por_mapa[mapa][algo][metrica] for algo in algoritmos_nomes]
            matriz.append(linha)
        matriz = np.array(matriz)

        plt.figure(figsize=(10, 6))
        sns.heatmap(matriz, annot=True, fmt=".2f", xticklabels=algoritmos_nomes, yticklabels=mapas, cmap="YlGnBu")
        plt.title(f"Heatmap - {metrica}")
        plt.xlabel("Algoritmos")
        plt.ylabel("Mapas")
        plt.tight_layout()

        # salva o gráfico
        plt.savefig(f"imagens/heatmap_{metrica}.png")
        plt.close()

if __name__ == "__main__":
    mapas = carregar_mapas(PASTA_MAPAS)

    mapa_especifico = None  # mapanumero ou None, exemplo: "mapa10"

    if mapa_especifico:
        mapa_encontrado = None
        for arquivo in mapas:
            if arquivo.startswith(mapa_especifico):
                mapa_encontrado = arquivo
                break

        if mapa_encontrado:
            comparar_desempenho({mapa_encontrado: mapas[mapa_encontrado]}, algoritmos)
        else:
            print(f"Nenhum mapa começando com '{mapa_especifico}' foi encontrado na pasta {PASTA_MAPAS}.")
    else:
        comparar_desempenho(mapas, algoritmos)
