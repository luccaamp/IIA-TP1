import heapq
from math import sqrt
from collections import deque

WALL = 'X'
START_STATE = 'S'
GOAL_STATE  = 'G'

def plan(map, algorithm='bfs', heuristic=None):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """
    #print(map)
    #print("Algorithm:", algorithm)
    #print("Heuristic:", heuristic)

    # Load the level from the file
    level = parse_level(map)

    # Retrieve the source and destination coordinates from the level.
    start = level['start']
    goal = level['goal']

    # Search for and display the path from src to dst.
    path = []
    visited = {}

    if algorithm == 'bfs':
        path, visited = bfs(start, goal, level, transition_model)
    elif algorithm == 'dfs':
        path, visited = dfs(start, goal, level, transition_model)
    elif algorithm == 'ucs':
        path, visited = ucs(start, goal, level, transition_model)
    elif algorithm == 'greedy':
        if heuristic == 'euclidian':
            path, visited = greedy_best_first(start, goal, level, transition_model, h_euclidian)
        elif heuristic == 'manhattan':
            path, visited = greedy_best_first(start, goal, level, transition_model, h_manhattan)
    elif algorithm == 'astar':
        if heuristic == 'euclidian':
            path, visited = a_star(start, goal, level, transition_model, h_euclidian)
        elif heuristic == 'manhattan':
            path, visited = a_star(start, goal, level, transition_model, h_manhattan)

    return path, path_cost(path, level), visited

def parse_level(map):
    """ Parses a level from a string.

    Args:
        level_str: A string containing a level.

    Returns:
        The parsed level (dict) containing the locations of walls (set), the locations of spaces 
        (dict), and a mapping of locations to waypoints (dict).
    """
    start = None
    goal = None
    walls = set()
    spaces = {}

    for j, line in enumerate(map.split('\n')):
        for i, char in enumerate(line):
            if char == '\n':
                continue
            elif char == WALL:
                walls.add((i, j))
            elif char == START_STATE:
                start = (i, j)
                spaces[(i, j)] = 1.
            elif char == GOAL_STATE:
                goal = (i, j) 
                spaces[(i, j)] = 1.
            elif char.isnumeric():
                spaces[(i, j)] = float(char)

    level = {'walls': walls, 'spaces': spaces, 'start': start, 'goal': goal}

    return level

def path_cost(path, level):
    """ Returns the cost of the given path.

    Args:
        path: A list of cells from the source to the goal.
        level: A loaded level, containing walls, spaces, and waypoints.

    Returns:
        The cost of the given path.
    """
    cost = 0
    for i in range(len(path) - 1):
        cost += cost_function(level, path[i], path[i + 1], 
                              level['spaces'][path[i]], 
                              level['spaces'][path[i + 1]])

    return cost

# =============================
# Transition Model
# =============================

def cost_function(level, state1, state2, cost1, cost2):
    """ Returns the cost of the edge joining state1 and state2.

    Args:
        state1: A source location.
        state2: A target location.

    Returns:
        The cost of the edge joining state1 and state2.
    """

    # distância euclidiana
    dist = sqrt((state1[0] - state2[0])**2 + (state1[1] - state2[1])**2)
    
    # custo médio ponderado entre os dois estados
    avg_cost = (cost1 + cost2) / 2.0

    return dist * avg_cost

def transition_model(level, state1):
    """ Provides a list of adjacent states and their respective costs from the given state.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        state: A target location.

    Returns:
        A list of tuples containing an adjacent sates's coordinates and the cost of 
        the edge joining it and the originating state.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    adj_states = {}

    # Movimentos possíveis: horizontal, vertical e diagonal
    movimentos = [
        (-1, -1), (0, -1), (1, -1),
        (-1,  0),         (1,  0),
        (-1,  1), (0,  1), (1,  1)
    ]

    for dx, dy in movimentos:
        vizinho = (state1[0] + dx, state1[1] + dy)

        # Verifica se o vizinho é um espaço válido (não é parede)
        if vizinho in level['spaces']:
            # Obtém o custo dos estados
            cost1 = level['spaces'][state1]
            cost2 = level['spaces'][vizinho]

            # Calcula o custo da transição
            custo = cost_function(level, state1, vizinho, cost1, cost2)

            # Adiciona à lista de vizinhos
            adj_states[vizinho] = custo

    return adj_states.items()
    #return sorted(adj_states.items(), key=lambda x: (x[0][0], x[0][1]))

# =============================
# Uninformed Search Algorithms
# =============================

def bfs(s, g, level, adj):
    """ Searches for a path from the source to the goal using the Breadth-First Search algorithm.

    Args:
        s: The source location.
        g: The goal location.
        level: The level containing the locations of walls, spaces, and waypoints.
        adj: A function that returns the adjacent cells and their respective costs from the given cell.

    Returns:
        A list of tuples containing cells from the source to the goal, and a dictionary 
        containing the visited cells and their respective parent cells.
    """
    visited = {s: None}
    
    fila = deque([s])

    while fila:
        atual = fila.popleft()

        # se chegamos no objetivo, para
        if atual == g:
            break

        # percorre os vizinhos do estado atual
        for vizinho, _ in adj(level, atual):
            if vizinho not in visited:  # só visita uma vez
                visited[vizinho] = atual  # guarda quem é o pai
                fila.append(vizinho)

    # reconstrução do caminho se chegamos no objetivo
    path = []
    if g in visited:
        atual = g
        while atual is not None:
            path.append(atual)
            atual = visited[atual]
        path.reverse()

    return path, visited

def dfs(s, g, level, adj):
    """ Searches for a path from the source to the goal using the Depth-First Search algorithm.
    Args:
        s: The source location.
        g: The goal location.
        level: The level containing the locations of walls, spaces, and waypoints.
        adj: A function that returns the adjacent cells and their respective costs from the given cell.
    
    Returns:
        A list of tuples containing cells from the source to the goal, and a dictionary containing the visited cells and their respective parent cells.
    """
    visited = {s: None}
    pilha = [s]  # pilha LIFO

    while pilha:
        atual = pilha.pop()  # pega o último inserido (profundidade)

        if atual == g:
            break  # encontramos o objetivo

        # percorre vizinhos
        for vizinho, _ in adj(level, atual):
            if vizinho not in visited:  # só visita uma vez
                visited[vizinho] = atual  # guarda quem é o pai
                pilha.append(vizinho)

    # reconstrução do caminho
    path = []
    if g in visited:
        atual = g
        while atual is not None:
            path.append(atual)
            atual = visited[atual]
        path.reverse()

    return path, visited

def ucs(start, goal, level, adj):
    """ Searches for a path from the source to the goal using the Uniform-Cost Search algorithm.

    Args:
        s: The source location.
        g: The goal location.
        level: The level containing the locations of walls, spaces, and waypoints.
        adj: A function that returns the adjacent cells and their respective costs from the given cell.

    Returns:
        A list of tuples containing cells from the source to the goal, and a dictionary containing the visited cells and their respective parent cells.
    """
    # Contador para o critério de desempate (FIFO)
    counter = 0
    
    # A fronteira agora armazena (custo, contador, nó)
    frontier = [(0, counter, start)]
    visited = {start: (0, None)}
    
    while frontier:
        # Desempacota os três valores
        current_cost, _, current_node = heapq.heappop(frontier)
        
        if current_cost > visited[current_node][0]:
            continue
        
        if current_node == goal:
            break
        
        for neighbor, cost in adj(level, current_node):
            new_cost = current_cost + cost
            
            if neighbor not in visited or new_cost < visited[neighbor][0]:
                visited[neighbor] = (new_cost, current_node)
                # Incrementa o contador a cada inserção
                counter += 1
                heapq.heappush(frontier, (new_cost, counter, neighbor))
    
    path = []
    if goal in visited:
        current = goal
        while current is not None:
            path.append(current)
            current = visited[current][1]
        path.reverse()
    
    simple_visited = {node: parent for node, (cost, parent) in visited.items()}

    #print(f"\nCaminho: {path}")
    
    return path, simple_visited


# ======================================
# Informed (Heuristic) Search Algorithms
# ======================================
def greedy_best_first(s, g, level, adj, h):
    """ Searches for a path from the source to the goal using the Greedy Best-First Search algorithm.
    
    Args:
        s: The source location.
        g: The goal location.
        level: The level containing the locations of walls, spaces, and waypoints.
        adj: A function that returns the adjacent cells and their respective costs from the given cell.
        h: A heuristic function that estimates the cost from the current cell to the goal.

    Returns:
        A list of tuples containing cells from the source to the goal, and a dictionary containing the visited cells and their respective parent cells.
    """
    visited = {s: None}

    # Fronteira como fila de prioridade, ordenada por h(n)
    frontier = [(h(s, g), s)]

    # Conjunto de nós já expandidos
    expanded = set()

    while frontier:
        _, current = heapq.heappop(frontier)

        if current in expanded:
            continue
        expanded.add(current)

        # Chegamos no objetivo
        if current == g:
            break

        # Explora vizinhos
        for neighbor, _ in adj(level, current):
            if neighbor not in visited:
                visited[neighbor] = current
                heapq.heappush(frontier, (h(neighbor, g), neighbor))

    # Reconstrução do caminho
    path = []
    if g in visited:
        node = g
        while node is not None:
            path.append(node)
            node = visited[node]
        path.reverse()

    return path, visited

def a_star(s, g, level, adj, h):
    """ Searches for a path from the source to the goal using the A* algorithm.

    Args:
        s: The source location.
        g: The goal location.
        level: The level containing the locations of walls, spaces, and waypoints.
        adj: A function that returns the adjacent cells and their respective costs from the given cell.
        h: A heuristic function that estimates the cost from the current cell to the goal.
    
    Returns:
        A list of tuples containing cells from the source to the goal, and a dictionary containing the visited cells and their respective parent cells.
    """
    frontier = [(h(s, g), s)]
    visited = {s: None}
    g_scores = {s: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == g:
            break

        for neighbor, cost in adj(level, current):
            new_g_score = g_scores[current] + cost

            if neighbor not in g_scores or new_g_score < g_scores[neighbor]:
                g_scores[neighbor] = new_g_score
                visited[neighbor] = current
                f_score = new_g_score + h(neighbor, g)
                heapq.heappush(frontier, (f_score, neighbor))

    path = []
    if g in visited:
        node = g
        while node is not None:
            path.append(node)
            node = visited[node]
        path.reverse()
    
    return path, visited

# ======================================
# Heuristic functions
# ======================================
def h_euclidian(s, g):
    """ Estimates the cost from the current cell to the goal using the Euclidian distance.

    Args:
        s: The current location.
        g: The goal location.
    
    Returns:
        The estimated cost from the current cell to the goal.    
    """

    ################################
    # 3.1 INSIRA SEU CÓDIGO AQUI
    ################################

    return sqrt((s[0] - g[0])**2 + (s[1] - g[1])**2)

def h_manhattan(s, g):
    """ Estimates the cost from the current cell to the goal using the Manhattan distance.
    
    Args:
        s: The current location.
        g: The goal location.
    
    Returns:
        The estimated cost from the current cell to the goal.
    """

    ################################
    # 3.1 INSIRA SEU CÓDIGO AQUI
    ################################

    return abs(s[0] - g[0]) + abs(s[1] - g[1])