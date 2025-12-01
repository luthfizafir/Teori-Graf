"""
    (A)
   /   \
  3     4
 /       \
(B)---2---(C)
    1
    |
   (D)
   

        A
      /   \
    2       3
   B--- 7 ---CD
   | \     / |
   4  1   5  6
   D--2--E-3-F

"""
# graph = {
#     'A': [('B', 3), ('C', 4)],
#     'B': [('A', 3), ('C', 2), ('D', 1)],
#     'C': [('A', 4), ('B', 2)],
#     'D': [('B', 1)]
# }

# graph = {
#     'A': [('B', 2), ('C', 3)],
#     'B': [('A', 2), ('C', 7), ('D', 4), ('E', 1)],
#     'C': [('A', 3), ('B', 7), ('E', 5), ('F', 6)],
#     'D': [('B', 4), ('E', 2)],
#     'E': [('B', 1), ('C', 5), ('D', 2), ('F', 3)],
#     'F': [('C', 6), ('E', 3)]
# }

graph = {
    0: [(1, 1), (2, 2)],
    1: [(0, 1), (3, 3), (2, 5)],
    2: [(0, 2), (1, 5), (4, 4)],
    3: [(1, 3), (4, 6), (5, 1)],
    4: [(2, 4), (3, 6), (5, 1)],
    5: [(3, 1), (4, 1)]
}

# Total edge weight
def total_edge_weight(graph):
    total = 0
    for node in graph:
        for neighbor, weight in graph[node]:
            total += weight
    return total // 2 

# Find odd-degree nodes
def odd_degree_nodes(graph):
    odd = []
    for node in graph:
        degree = len(graph[node])
        if degree % 2 == 1:
            odd.append(node)
    return odd

# Djikstra
def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    visited = {node: False for node in graph}
    dist[start] = 0

    while True:
        min_node = None
        min_dist = float('inf')
        for node in graph:
            if not visited[node] and dist[node] < min_dist:
                min_dist = dist[node]
                min_node = node

        if min_node is None: 
            break

        visited[min_node] = True

        for neighbor, weight in graph[min_node]:
            if dist[min_node] + weight < dist[neighbor]:
                dist[neighbor] = dist[min_node] + weight

    return dist

# Minimum weight
def min_weight_matching(odd_nodes, dist_matrix):
    if not odd_nodes:
        return 0, []

    best_cost = float('inf')
    best_pairs = []

    def helper(nodes, current_pairs, current_cost):
        nonlocal best_cost, best_pairs
        if not nodes:
            if current_cost < best_cost:
                best_cost = current_cost
                best_pairs = current_pairs.copy()
            return

        first = nodes[0]
        for i in range(1, len(nodes)):
            second = nodes[i]
            pair_cost = dist_matrix[first][second]
            if current_cost + pair_cost >= best_cost:
                continue
            remaining = nodes[1:i] + nodes[i+1:]
            current_pairs.append((first, second))
            helper(remaining, current_pairs, current_cost + pair_cost)
            current_pairs.pop()

    helper(odd_nodes, [], 0)
    return best_cost, best_pairs

if __name__ == '__main__': 
    print("===== Chinese Postman Problem =====\n")

    total_weight = total_edge_weight(graph)
    print(f"1) Total edge weight of graph: {total_weight}\n")

    odd_nodes = odd_degree_nodes(graph)
    print(f"2) Odd-degree nodes: {odd_nodes}\n")

    print("3) Shortest paths between odd nodes:")
    dist_matrix = {}
    for node in odd_nodes:
        dists = dijkstra(graph, node)
        dist_matrix[node] = {}
        for other in odd_nodes:
            dist_matrix[node][other] = dists[other]
            if node != other:
                print(f"   {node} → {other} = {dists[other]}")
    print()

    extra_cost, best_pairing = min_weight_matching(odd_nodes, dist_matrix)
    print(f"4) Best pairing of odd nodes: {best_pairing}")
    print(f"   Extra cost to make all degrees even: {extra_cost}\n")

    cpp_total = total_weight + extra_cost
    print(f"5) Chinese Postman Problem total length = {cpp_total}")
    print("=====================================================================")


    
    
