class Tarjan:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.graph = [[] for _ in range(num_vertices)]
        self.ids = [-1] * num_vertices
        self.low = [0] * num_vertices
        self.visited = [False] * num_vertices
        self.is_articulation = [False] * num_vertices
        self.id = 0

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def find_articulation_points(self):
        for i in range(self.num_vertices):
            if not self.visited[i]:
                self.dfs(i)
        return [i for i, is_ap in enumerate(self.is_articulation) if is_ap]

    def dfs(self, root):
        stack = [(root, root, iter(self.graph[root]))]
        self.ids[root] = self.low[root] = self.id
        self.id += 1
        self.visited[root] = True
        out_edge_count = 0

        while stack:
            parent, current, neighbors = stack[-1]
            finished = True
            for neighbor in neighbors:
                if neighbor == parent:
                    continue
                if not self.visited[neighbor]:
                    stack.append((current, neighbor, iter(self.graph[neighbor])))
                    self.visited[neighbor] = True
                    self.ids[neighbor] = self.low[neighbor] = self.id
                    self.id += 1
                    if current == root:
                        out_edge_count += 1
                    finished = False
                    break
                else:
                    self.low[current] = min(self.low[current], self.ids[neighbor])
            if finished:
                if current != root:
                    self.low[parent] = min(self.low[parent], self.low[current])
                    if self.ids[parent] <= self.low[current]:
                        self.is_articulation[parent] = True
                stack.pop()

        if out_edge_count > 1:
            self.is_articulation[root] = True