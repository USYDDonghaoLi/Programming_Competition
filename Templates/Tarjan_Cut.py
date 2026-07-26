"""
Tarjan 算法 - 寻找图中的割点（切点/关键点）。
割点是指删除该节点会导致图的连通性减少的节点。
时间复杂度：O(V + E)
空间复杂度：O(V + E)
"""


class TarjanCut:
    """
    Tarjan 算法求解割点（切点）。
    
    原理：
    - 对于根节点：如果至少有两个子树，则根是割点
    - 对于非根节点 v：如果存在子树中的节点 u，使得 low[u] >= disc[v]，则 v 是割点
    
    应用场景：
    - 求解图的割点
    - 分析图的脆弱性
    - 构建分块图
    """
    
    def __init__(self, num_vertices: int):
        """
        初始化图。
        Args:
            num_vertices: 顶点数量（0 到 num_vertices-1）
        """
        self.num_vertices = num_vertices
        self.adj = [[] for _ in range(num_vertices)]
        self.ids = [-1] * num_vertices
        self.low = [0] * num_vertices
        self.visited = [False] * num_vertices
        self.is_articulation = [False] * num_vertices
        self.timer = 0
    
    def add_edge(self, u: int, v: int) -> None:
        """
        添加无向边。
        Args:
            u, v: 边的两个端点
        """
        self.adj[u].append(v)
        self.adj[v].append(u)
    
    def find_articulation_points(self):
        """
        找出图中的所有割点。
        Returns:
            list: 割点的列表
        """
        for vertex in range(self.num_vertices):
            if not self.visited[vertex]:
                self._dfs_iterative(vertex)
        
        return [i for i, is_ap in enumerate(self.is_articulation) if is_ap]
    
    def _dfs_iterative(self, root: int) -> None:
        """
        使用迭代栈进行 DFS，找出所有割点（避免递归深度限制）。
        Args:
            root: 起始顶点
        """
        # 栈存储：(parent, current, neighbors_iter, out_edge_count)
        stack = [(root, root, iter(self.adj[root]), 0)]
        self.ids[root] = self.low[root] = self.timer
        self.timer += 1
        self.visited[root] = True
        
        while stack:
            parent, current, neighbors_iter, out_edge_count = stack[-1]
            found_unvisited = False
            
            for neighbor in neighbors_iter:
                # 跳过回边指向父节点
                if neighbor == parent:
                    continue
                
                if not self.visited[neighbor]:
                    # 未访问，递归下降
                    self.visited[neighbor] = True
                    self.ids[neighbor] = self.low[neighbor] = self.timer
                    self.timer += 1
                    
                    # 如果当前是根，统计子树数
                    if current == root:
                        out_edge_count += 1
                    
                    stack[-1] = (parent, current, neighbors_iter, out_edge_count)
                    stack.append((current, neighbor, iter(self.adj[neighbor]), 0))
                    found_unvisited = True
                    break
                else:
                    # 已访问，更新 low 值（回边）
                    self.low[current] = min(self.low[current], self.ids[neighbor])
            
            if not found_unvisited:
                # 所有邻接顶点都已处理，回溯
                parent, current, _, out_edge_count = stack.pop()
                
                if current != root:
                    # 非根节点：检查是否为割点
                    if parent != -1:
                        self.low[parent] = min(self.low[parent], self.low[current])
                        if self.ids[parent] <= self.low[current]:
                            self.is_articulation[parent] = True
                else:
                    # 根节点：至少有两个子树时是割点
                    if out_edge_count > 1:
                        self.is_articulation[root] = True


# 保持向后兼容性
Tarjan = TarjanCut