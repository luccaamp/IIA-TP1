import os
import pytest
from search import parse_level, cost_function, transition_model, bfs, path_cost, dfs, ucs, h_euclidian, h_manhattan, greedy_best_first, a_star

MAPS_BASIC = "maps_basic"
MAPS = "maps"

TESTES_COST_FUNCTION = {
    "1": [
        {"state1": (1,1), "state2": (2,1), "esperado": 2.0},
        {"state1": (1,1), "state2": (1,2), "esperado": 5.0},
        {"state1": (1,1), "state2": (2,2), "esperado": 7.78}
    ],
    "2": [
        {"state1": (2,1), "state2": (2,2), "esperado": 1.5},
        {"state1": (1,2), "state2": (1,1), "esperado": 4.0},
        {"state1": (1,2), "state2": (2,1), "esperado": 2.83},
        {"state1": (1,2), "state2": (2,2), "esperado": 2.5}
    ],
    "3": [
        {"state1": (1,1), "state2": (2,2), "esperado": 3.53}
    ]
}

TESTES_TRANSITION_MODEL = {
    "1": [{"state": (1,1), "esperados": {(2,1): 2.0, (1,2): 5.0, (2,2): 7.78}}],
    "2": [{"state": (1,2), "esperados": {(1,1): 4.0, (2,1): 2.83, (2,2): 2.5}}],
    "4": [{"state": (6,2), "esperados": {(5,1): 5.66, (6,1): 3.50, (7,1): 4.24, (5,2): 4.50, (7,2): 2.50, (5,3): 1.41, (6,3): 1.50, (7,3): 2.83}}],
    "5": [{"state": (3,2), "esperados": {(3,1): 5.0, (4,1): 2.83, (2,3): 1.41, (4,3): 3.54}}],
}

TESTES_BFS = {
    "mapa1_aberto": { "esperado": {"Visitados": 434, "Tamanho": 31, "Custo": 35.38}},
    "mapa3_barreira": { "esperado": {"Visitados": 658, "Tamanho": 44, "Custo": 46.31}},
    "mapa7_custo": { "esperado": {"Visitados": 296, "Tamanho": 9, "Custo": 31.11}}
}

TESTES_DFS = {
    "mapa1_aberto": {"esperado": {"Visitados": 98, "Tamanho": 31, "Custo": 35.38}},
    "mapa3_barreira": {"esperado": {"Visitados": 677, "Tamanho": 340, "Custo": 351.42}},
    "mapa7_custo": {"esperado": {"Visitados": 234, "Tamanho": 99, "Custo": 131.32}},
}

TESTES_UCS = {
    "mapa1_aberto": { "esperado": {"Visitados": 434, "Tamanho": 31, "Custo": 35.38}},
    "mapa3_barreira": { "esperado": {"Visitados": 607, "Tamanho": 44, "Custo": 44.65}},
    "mapa7_custo": { "esperado": {"Visitados": 328, "Tamanho": 15, "Custo": 15.65}}
}

TESTES_HEURISTICAS = [
    {"s": (1, 1), "g": (4, 5), "euclidian": 5.0, "manhattan": 7},
    {"s": (2, 3), "g": (2, 3), "euclidian": 0.0, "manhattan": 0},
    {"s": (0, 0), "g": (3, 4), "euclidian": 5.0, "manhattan": 7},
    {"s": (100, 200), "g": (300, 800), "euclidian": 632.46, "manhattan": 800},
]

TESTES_GREEDY = {
    "mapa1_aberto": {"heuristica": "euclidian", "esperado": {"Visitados": 98, "Tamanho": 31, "Custo": 35.38}},
    "mapa3_barreira": {"heuristica": "euclidian", "esperado": {"Visitados": 454, "Tamanho": 50, "Custo": 54.79}},
    "mapa7_custo": {"heuristica": "euclidian", "esperado": {"Visitados": 30, "Tamanho": 9, "Custo": 22.0}},
}

TESTES_A_STAR = {
    "mapa1_aberto": {"heuristica": "euclidian", "esperado": {"Visitados": 319, "Tamanho": 31, "Custo": 35.38}},
    "mapa3_barreira": {"heuristica": "euclidian", "esperado": {"Visitados": 582, "Tamanho": 44, "Custo": 44.65}},
    "mapa7_custo": {"heuristica": "euclidian", "esperado": {"Visitados": 165, "Tamanho": 15, "Custo": 15.65}},
}

# --------------------------
#          Testes 
# --------------------------

@pytest.mark.parametrize("nome, testes", TESTES_COST_FUNCTION.items())
def test_cost_function(nome, testes):
    path_arquivo = os.path.join(MAPS_BASIC, f"{nome}.txt")
    if not os.path.exists(path_arquivo):
        pytest.skip(f"Mapa {nome} não encontrado")

    with open(path_arquivo, "r") as f:
        mapa_str = f.read()

    print(f"\nTestando {nome}...")
    level = parse_level(mapa_str)
    print("Spaces:", level['spaces'])

    for teste in testes:
        s1, s2, esperado = teste["state1"], teste["state2"], teste["esperado"]
        cost1, cost2 = level['spaces'][s1], level['spaces'][s2]
        resultado = cost_function(level, s1, s2, cost1, cost2)

        if abs(resultado - esperado) < 0.01:
            print(f"PASS ✅: custo {s1} -> {s2} = {resultado:.2f}")
        else:
            print(f"FAIL ❌: custo {s1} -> {s2} = {resultado:.2f}, esperado {esperado:.2f}")
        # Mantém o assert para o pytest registrar falha formalmente
        assert abs(resultado - esperado) < 0.01


@pytest.mark.parametrize("nome, testes", TESTES_TRANSITION_MODEL.items())
def test_transition_model(nome, testes):
    path_arquivo = os.path.join(MAPS_BASIC, f"{nome}.txt")
    if not os.path.exists(path_arquivo):
        pytest.skip(f"Mapa {nome} não encontrado")

    with open(path_arquivo, "r") as f:
        mapa_str = f.read()

    print(f"\nTestando {nome}...")
    level = parse_level(mapa_str)

    for teste in testes:
        state = teste["state"]
        esperados = teste["esperados"]
        vizinhos = dict(transition_model(level, state))

        status_global = "PASS ✅"
        for viz, custo in vizinhos.items():
            custo_esperado = esperados.get(viz)
            if custo_esperado is not None and abs(custo - custo_esperado) >= 0.01:
                status_global = "FAIL ❌"

        print(f"{status_global}")
        print(f"state: {state}")
        print("vizinhos:")

        for viz, custo in vizinhos.items():
            custo_esperado = esperados.get(viz)
            if custo_esperado is not None:
                if abs(custo - custo_esperado) < 0.01:
                    print(f"    {viz}: {custo:.2f}")
                else:
                    print(f"    {viz}: {custo:.2f}, esperado {custo_esperado:.2f}")
            else:
                print(f"    {viz}: {custo:.2f} (não definido no teste esperado)")

        # Mantém asserts para pytest registrar falha
        for viz, custo_esperado in esperados.items():
            assert viz in vizinhos, f"{viz} não encontrado em {state}"
            assert abs(vizinhos[viz] - custo_esperado) < 0.01, \
                f"{state}->{viz}: {vizinhos[viz]:.2f} != {custo_esperado:.2f}"


@pytest.mark.parametrize("nome, dados", TESTES_BFS.items())
def test_bfs(nome, dados):
    caminho_arquivo = os.path.join(MAPS, f"{nome}.txt")
    if not os.path.exists(caminho_arquivo):
        print(f"Mapa {nome}.txt não encontrado, pulando...")
        pytest.skip(f"Mapa {nome} não encontrado")

    with open(caminho_arquivo, "r") as f:
        mapa_str = f.read()

    level = parse_level(mapa_str)
    start, goal = level['start'], level['goal']

    # Rodando BFS diretamente
    path, visited = bfs(start, goal, level, transition_model)
    cost = path_cost(path, level)

    resultados = {
        "Visitados": len(visited),
        "Tamanho": len(path),
        "Custo": cost
    }

    esperado = dados["esperado"]

    #print(f"\nTeste {nome}:")
    print("\nVisitados:", resultados["Visitados"], "| Esperado:", esperado["Visitados"])
    print("Tamanho caminho:", resultados["Tamanho"], "| Esperado:", esperado["Tamanho"])
    print("Custo:", resultados["Custo"], "| Esperado:", esperado["Custo"])

    # Critérios de validação
    visitados_ok = resultados["Visitados"] <= esperado["Visitados"]
    tamanho_ok = resultados["Tamanho"] == esperado["Tamanho"]
    custo_ok = abs(resultados["Custo"] - esperado["Custo"]) <= 0.01

    if visitados_ok and tamanho_ok and custo_ok:
        print("PASS ✅")
    else:
        print("FAIL ❌")
        if not visitados_ok:
            print(f"  Visitados maior que o esperado ({resultados['Visitados']} > {esperado['Visitados']})")
        if not tamanho_ok:
            print(f"  Tamanho do caminho diferente do esperado ({resultados['Tamanho']} != {esperado['Tamanho']})")
        if not custo_ok:
            print(f"  Custo fora do limite permitido ({resultados['Custo']} vs {esperado['Custo']})")

    # Mantém os asserts para pytest registrar falha formalmente
    assert visitados_ok, f"Visitados {resultados['Visitados']} > {esperado['Visitados']}"
    assert tamanho_ok, f"Tamanho {resultados['Tamanho']} != {esperado['Tamanho']}"
    assert custo_ok, f"Custo {resultados['Custo']:.2f} != {esperado['Custo']:.2f}"


@pytest.mark.parametrize("nome, dados", TESTES_DFS.items())
def test_dfs(nome, dados):
    caminho_arquivo = os.path.join(MAPS, f"{nome}.txt")
    if not os.path.exists(caminho_arquivo):
        print(f"Mapa {nome}.txt não encontrado, pulando...")
        pytest.skip(f"Mapa {nome} não encontrado")

    with open(caminho_arquivo, "r") as f:
        mapa_str = f.read()

    level = parse_level(mapa_str)
    start, goal = level['start'], level['goal']

    # Rodando DFS diretamente
    path, visited = dfs(start, goal, level, transition_model)
    cost = path_cost(path, level)

    resultados = {
        "Visitados": len(visited),
        "Tamanho": len(path),
        "Custo": cost
    }

    esperado = dados["esperado"]

    print(f"\nTeste {nome}:")
    print("Visitados:", resultados["Visitados"], "| Esperado:", esperado["Visitados"])
    print("Tamanho caminho:", resultados["Tamanho"], "| Esperado:", esperado["Tamanho"])
    print("Custo:", resultados["Custo"], "| Esperado:", esperado["Custo"])

    # Critérios de validação
    visitados_ok = resultados["Visitados"] <= esperado["Visitados"]
    tamanho_ok = resultados["Tamanho"] == esperado["Tamanho"]
    custo_ok = abs(resultados["Custo"] - esperado["Custo"]) <= 0.01

    if visitados_ok and tamanho_ok and custo_ok:
        print("PASS ✅")
    else:
        print("FAIL ❌")
        if not visitados_ok:
            print(f"  Visitados maior que o esperado ({resultados['Visitados']} > {esperado['Visitados']})")
        if not tamanho_ok:
            print(f"  Tamanho do caminho diferente do esperado ({resultados['Tamanho']} != {esperado['Tamanho']})")
        if not custo_ok:
            print(f"  Custo fora do limite permitido ({resultados['Custo']} vs {esperado['Custo']})")

    # Mantém os asserts para pytest registrar falha formalmente
    assert visitados_ok, f"Visitados {resultados['Visitados']} > {esperado['Visitados']}"
    assert tamanho_ok, f"Tamanho {resultados['Tamanho']} != {esperado['Tamanho']}"
    assert custo_ok, f"Custo {resultados['Custo']:.2f} != {esperado['Custo']:.2f}"


@pytest.mark.parametrize("nome, dados", TESTES_UCS.items())
def test_ucs(nome, dados):
    caminho_arquivo = os.path.join(MAPS, f"{nome}.txt")
    if not os.path.exists(caminho_arquivo):
        print(f"Mapa {nome}.txt não encontrado, pulando...")
        pytest.skip(f"Mapa {nome} não encontrado")

    with open(caminho_arquivo, "r") as f:
        mapa_str = f.read()

    level = parse_level(mapa_str)
    start, goal = level['start'], level['goal']

    # Rodando UCS diretamente
    path, visited = ucs(start, goal, level, transition_model)
    cost = path_cost(path, level)

    resultados = {
        "Visitados": len(visited),
        "Tamanho": len(path),
        "Custo": cost
    }

    esperado = dados["esperado"]

    # Impressão no estilo do teste manual
    print(f"\nTeste {nome}:")
    print("Visitados:", resultados["Visitados"], "| Esperado:", esperado["Visitados"])
    print("Tamanho caminho:", resultados["Tamanho"], "| Esperado:", esperado["Tamanho"])
    print("Custo:", round(resultados["Custo"], 2), "| Esperado:", esperado["Custo"])

    # Critérios de validação
    visitados_ok = resultados["Visitados"] <= esperado["Visitados"]
    tamanho_ok = resultados["Tamanho"] == esperado["Tamanho"]
    custo_ok = abs(resultados["Custo"] - esperado["Custo"]) <= 0.01

    if visitados_ok and tamanho_ok and custo_ok:
        print("PASS ✅")
    else:
        print("FAIL ❌")
        if not visitados_ok:
            print(f"  Visitados maior que o esperado ({resultados['Visitados']} > {esperado['Visitados']})")
        if not tamanho_ok:
            print(f"  Tamanho do caminho diferente do esperado ({resultados['Tamanho']} != {esperado['Tamanho']})")
        if not custo_ok:
            print(f"  Custo fora do limite permitido ({resultados['Custo']} vs {esperado['Custo']})")

    # Mantém asserts para pytest registrar falha formalmente
    assert visitados_ok, f"Visitados {resultados['Visitados']} > {esperado['Visitados']}"
    assert tamanho_ok, f"Tamanho {resultados['Tamanho']} != {esperado['Tamanho']}"
    assert custo_ok, f"Custo {resultados['Custo']:.2f} != {esperado['Custo']:.2f}"


@pytest.mark.parametrize("teste", TESTES_HEURISTICAS)
def test_heuristicas(teste):
    s, g = teste["s"], teste["g"]

    resultado_e = h_euclidian(s, g)
    resultado_m = h_manhattan(s, g)

    ok_e = abs(resultado_e - teste["euclidian"]) < 0.01
    ok_m = abs(resultado_m - teste["manhattan"]) < 0.01

    print(f"\nDe {s} até {g}:")
    print(f"  Euclidian: {resultado_e:.2f} | Esperado: {teste['euclidian']:.2f} -> {'PASS ✅' if ok_e else 'FAIL ❌'}")
    print(f"  Manhattan: {resultado_m:.2f} | Esperado: {teste['manhattan']:.2f} -> {'PASS ✅' if ok_m else 'FAIL ❌'}")

    # Asserts formais para pytest registrar
    assert ok_e, f"h_euclidian({s}, {g}) = {resultado_e:.2f}, esperado {teste['euclidian']:.2f}"
    assert ok_m, f"h_manhattan({s}, {g}) = {resultado_m:.2f}, esperado {teste['manhattan']:.2f}"


@pytest.mark.parametrize("nome, dados", TESTES_GREEDY.items())
def test_greedy_best_first(nome, dados):
    caminho_arquivo = os.path.join(MAPS, f"{nome}.txt")
    if not os.path.exists(caminho_arquivo):
        pytest.skip(f"Mapa {nome} não encontrado")

    with open(caminho_arquivo, "r") as f:
        mapa_str = f.read()

    level = parse_level(mapa_str)
    start, goal = level['start'], level['goal']

    # Escolhe a heurística
    heuristica = h_euclidian if dados["heuristica"] == "euclidian" else h_manhattan

    # Executa Greedy Best-First
    path, visited = greedy_best_first(start, goal, level, transition_model, heuristica)
    cost = path_cost(path, level)

    resultados = {
        "Visitados": len(visited),
        "Tamanho": len(path),
        "Custo": cost
    }

    esperado = dados["esperado"]

    print(f"\nTeste {nome} (Greedy Best-First):")
    print("Visitados:", resultados["Visitados"], "| Esperado:", esperado["Visitados"])
    print("Tamanho caminho:", resultados["Tamanho"], "| Esperado:", esperado["Tamanho"])
    print("Custo:", round(resultados["Custo"], 2), "| Esperado:", esperado["Custo"])

    # Critérios de validação
    visitados_ok = resultados["Visitados"] <= esperado["Visitados"]
    tamanho_ok = resultados["Tamanho"] == esperado["Tamanho"]
    custo_ok = abs(resultados["Custo"] - esperado["Custo"]) <= 0.01

    if visitados_ok and tamanho_ok and custo_ok:
        print("PASS ✅")
    else:
        print("FAIL ❌")
        if not visitados_ok:
            print(f"  Visitados maior que o esperado ({resultados['Visitados']} > {esperado['Visitados']})")
        if not tamanho_ok:
            print(f"  Tamanho do caminho diferente do esperado ({resultados['Tamanho']} != {esperado['Tamanho']})")
        if not custo_ok:
            print(f"  Custo fora do limite permitido ({resultados['Custo']} vs {esperado['Custo']})")

    # Mantém asserts para pytest
    assert visitados_ok, f"Visitados {resultados['Visitados']} > {esperado['Visitados']}"
    assert tamanho_ok, f"Tamanho {resultados['Tamanho']} != {esperado['Tamanho']}"
    assert custo_ok, f"Custo {resultados['Custo']:.2f} != {esperado['Custo']:.2f}"


@pytest.mark.parametrize("nome, dados", TESTES_A_STAR.items())
def test_a_star(nome, dados):
    caminho_arquivo = os.path.join(MAPS, f"{nome}.txt")
    if not os.path.exists(caminho_arquivo):
        pytest.skip(f"Mapa {nome} não encontrado")

    with open(caminho_arquivo, "r") as f:
        mapa_str = f.read()

    level = parse_level(mapa_str)
    start, goal = level['start'], level['goal']

    # Escolhe a heurística
    heuristica = h_euclidian if dados["heuristica"] == "euclidian" else h_manhattan

    # Executa A*
    path, visited = a_star(start, goal, level, transition_model, heuristica)
    cost = path_cost(path, level)

    resultados = {
        "Visitados": len(visited),
        "Tamanho": len(path),
        "Custo": cost
    }

    esperado = dados["esperado"]

    print(f"\nTeste {nome} (A*):")
    print("Visitados:", resultados["Visitados"], "| Esperado:", esperado["Visitados"])
    print("Tamanho caminho:", resultados["Tamanho"], "| Esperado:", esperado["Tamanho"])
    print("Custo:", round(resultados["Custo"], 2), "| Esperado:", esperado["Custo"])

    # Critérios de validação
    visitados_ok = resultados["Visitados"] <= esperado["Visitados"]
    tamanho_ok = resultados["Tamanho"] == esperado["Tamanho"]
    custo_ok = abs(resultados["Custo"] - esperado["Custo"]) <= 0.01

    if visitados_ok and tamanho_ok and custo_ok:
        print("PASS ✅")
    else:
        print("FAIL ❌")
        if not visitados_ok:
            print(f"  Visitados maior que o esperado ({resultados['Visitados']} > {esperado['Visitados']})")
        if not tamanho_ok:
            print(f"  Tamanho do caminho diferente do esperado ({resultados['Tamanho']} != {esperado['Tamanho']})")
        if not custo_ok:
            print(f"  Custo fora do limite permitido ({resultados['Custo']} vs {esperado['Custo']})")

    # Mantém asserts para pytest
    assert visitados_ok, f"Visitados {resultados['Visitados']} > {esperado['Visitados']}"
    assert tamanho_ok, f"Tamanho {resultados['Tamanho']} != {esperado['Tamanho']}"
    assert custo_ok, f"Custo {resultados['Custo']:.2f} != {esperado['Custo']:.2f}"

