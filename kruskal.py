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

def kruskals(graph):
    mst_edges = []
    total_weight = 0
    
    all_edges = []
    seen_pairs = set()
    
    for node in graph:
        for neighbor, weight in graph[node]:
            pair_key = tuple(sorted((node, neighbor)))
            if pair_key not in seen_pairs:
                all_edges.append((node, neighbor, weight))
                seen_pairs.add(pair_key)

    all_edges.sort(key=lambda x: x[2])
    
    print("Sorted Edges (Kruskal's Priority):")
    print(all_edges)
    print("\n--- Processing Edges ---")

    # union find
    parent = {node: node for node in graph}

    def find(node):
        # recursively find the root representative of the node
        if parent[node] != node:
            parent[node] = find(parent[node]) # path compression
        return parent[node]

    def union(node1, node2):
        # connect two sets together
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            parent[root1] = root2
            return True 
        return False 

    for u, v, w in all_edges:
        if union(u, v):
            print(f" Accepting Edge: ({u}, {v}) Weight: {w}")
            mst_edges.append((u, v))
            total_weight += w
        else:
            print(f" Rejecting Edge: ({u}, {v}) Weight: {w} (Creates Cycle)")

    return mst_edges, total_weight

if __name__ == '__main__':
    edges, total = kruskals(graph)
    print("\n=============================")
    print("MST edges:", edges)
    print("Total weight:", total)