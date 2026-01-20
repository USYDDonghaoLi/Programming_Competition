from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def find_bridges(self):
        bridges = []
        discovery = [-1] * self.V
        low = [-1] * self.V
        parent = [-1] * self.V
        stack = []

        # Timer for the discovery time
        time = [0]

        for i in range(self.V):
            if discovery[i] == -1:
                stack.append((i, iter(self.graph[i])))
                while stack:
                    node, neighbors = stack[-1]
                    if discovery[node] == -1:
                        discovery[node] = low[node] = time[0]
                        time[0] += 1

                    for neighbor in neighbors:
                        if discovery[neighbor] == -1:
                            parent[neighbor] = node
                            stack.append((neighbor, iter(self.graph[neighbor])))
                            break
                        elif neighbor != parent[node]:
                            low[node] = min(low[node], discovery[neighbor])
                    else:
                        if parent[node] != -1:
                            low[parent[node]] = min(low[parent[node]], low[node])
                            if low[node] > discovery[parent[node]]:
                                bridges.append((parent[node], node))
                        stack.pop()

        return bridges