import os
from tabulate import tabulate
from search import plan  

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

        # encontra mínimos por linha
        min_visitados = min(r["Visitados"] for r in resultados.values())
        min_tamanho   = min(r["Tamanho"] for r in resultados.values())
        min_custo     = min(r["Custo"] for r in resultados.values())

        def colorir(valor, minimo):
            return f"\033[92m{valor}\033[0m" if valor == minimo else str(valor)

        # monta tabela com cores
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

        # identifica os melhores para cada critério
        melhores_visitados = [nome for nome, r in resultados.items() if r["Visitados"] == min_visitados]
        melhores_tamanho   = [nome for nome, r in resultados.items() if r["Tamanho"] == min_tamanho]
        melhores_custo     = [nome for nome, r in resultados.items() if r["Custo"] == min_custo]

        # melhor geral considerando: menor custo, depois menor caminho, depois menor nós visitados
        melhor_geral_valor = min(
            resultados.items(),
            key=lambda item: (item[1]["Custo"], item[1]["Tamanho"], item[1]["Visitados"])
        )[1]
        melhores_geral = [nome for nome, r in resultados.items() 
                          if (r["Custo"], r["Tamanho"], r["Visitados"]) == 
                             (melhor_geral_valor["Custo"], melhor_geral_valor["Tamanho"], melhor_geral_valor["Visitados"])]

        print("\nMelhor em cada critério:")
        print(f" - Menor número de visitados: {', '.join(melhores_visitados)}")
        print(f" - Menor tamanho de caminho: {', '.join(melhores_tamanho)}")
        print(f" - Menor custo: {', '.join(melhores_custo)}")
        print(f" - Melhor geral: {', '.join(melhores_geral)}\n")

if __name__ == "__main__":
    mapas = carregar_mapas(PASTA_MAPAS)

    mapa_especifico = None  # mapanumero ou None, exemplo: "mapa10"

    if mapa_especifico:
        # Procura o arquivo que comece com o nome informado
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