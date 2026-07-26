"""
Tarjan 算法 - 寻找图中的桥（割边）。
桥是指删除该边会导致图的连通性减少的边。
时间复杂度：O(V + E)
空间复杂度：O(V + E)
"""

from collections import defaultdict


class TarjanBridge:
    """
    Tarjan 算法求解桥（割边）。
    
    应用场景：
    - 求解图的桥
    - 构建二连通分量
    - 分析图的结构强度
    """
    
    def __init__(self, num_vertices: int):
        """
        初始化图。
        Args:
            num_vertices: 顶点数量（0 到 num_vertices-1）
        """
        self.num_vertices = num_vertices
        self.adj = defaultdict(list)
        self.discovery = [-1] * num_vertices
        self.low = [-1] * num_vertices
        self.parent = [-1] * num_vertices
        self.bridges = []
        self.timer = [0]
    
    def add_edge(self, u: int, v: int) -> None:
        """
        添加无向边。
        Args:
            u, v: 边的两个端点
        """
        self.adj[u].append(v)
        self.adj[v].append(u)
    
    def find_bridges(self):
        """
        找出图中的所有桥。
        Returns:
            list: 桥的列表，每个桥表示为 (u, v) 对
        """
        for vertex in range(self.num_vertices):
            if self.discovery[vertex] == -1:
                self._dfs_iterative(vertex)
        
        return self.bridges
    
    def _dfs_iterative(self, start: int) -> None:
        """
        使用迭代栈进行 DFS，找出所有桥（避免递归深度限制）。
        Args:
            start: 起始顶点
        """
        stack = [(start, iter(self.adj[start]))]
        self.discovery[start] = self.low[start] = self.timer[0]
        self.timer[0] += 1
        
        while stack:
            vertex, neighbors_iter = stack[-1]
            found_unvisited = False
            
            for neighbor in neighbors_iter:
                if self.discovery[neighbor] == -1:
                    self.parent[neighbor] = vertex
                    self.discovery[neighbor] = self.low[neighbor] = self.timer[0]
                    self.timer[0] += 1
                    stack.append((neighbor, iter(self.adj[neighbor])))
                    found_unvisited = True
                    break
                elif neighbor != self.parent[vertex]:
                    self.low[vertex] = min(self.low[vertex], self.discovery[neighbor])
            
            if not found_unvisited:
                stack.pop()
                if self.parent[vertex] != -1:
                    self.low[self.parent[vertex]] = min(
                        self.low[self.parent[vertex]], self.low[vertex]
                    )
                    if self.low[vertex] > self.discovery[self.parent[vertex]]:
                        self.bridges.append((self.parent[vertex], vertex))


# 保持向后兼容性
Graph = TarjanBridge