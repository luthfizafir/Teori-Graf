"""
        (A)
       / | \
     4   2   5
     /    \    \
   (B)--1--(C)--3--(F)
     \      |      /
      6     8     7
       \    |    /
         (D)--4--(E)
"""

graph = {
    'A': [('B', 4), ('C', 2), ('F', 5)],
    'B': [('A', 4), ('C', 1), ('D', 6)],
    'C': [('A', 2), ('B', 1), ('F', 3), ('D', 8)],
    'D': [('B', 6), ('C', 8), ('E', 4)],
    'E': [('D', 4), ('F', 7)],
    'F': [('A', 5), ('C', 3), ('E', 7)]
}

def prims(graph, start):
    visited = []
    mst_edges = []
    total_weight = 0

    visited.append(start)
    while len(visited) < len(graph):
        min_edge = None
        min_weight = 0

        # Prims logic
        for node in visited:
            print (f'--{visited}-- Node: {node}')
            print ('The available edges are: ')

            # Printing available edges
            for neighbor, weight in graph[node]:
                if neighbor not in visited:
                    edges = (node, neighbor, weight)
                    print(f'\t{edges}')
            print(f'')

            # Picking the minimum weight
            for neighbor, weight in graph[node]:
                if neighbor not in visited and (min_weight == 0 or min_weight > weight):
                    min_edge = (node, neighbor)
                    min_weight = weight
        print('=============================\n')
        mst_edges.append(min_edge)
        total_weight += min_weight
        visited.append(min_edge[1])

    return mst_edges, total_weight

if __name__ == '__main__':
    edges, total = prims(graph, 'A')
    print("MST edges:", edges)
    print("Total weight:", total)



