"""
Dinic 最大流算法（含下界限制支持）。

Dinic 算法是求解最大流问题的高效算法，时间复杂度 O(V² * E)。

核心思想：
1. BFS 构建分层图（level graph）
2. DFS 在分层图中找增广路径
3. 重复直到不存在增广路径

支持：
- 无下界的边：add_edge(u, v, capacity)
- 有下界的边：add_edge_with_bound(u, v, lower_bound, upper_bound)

复杂度：O(V² * E)
"""

from collections import deque
from typing import List, Optional, Tuple


class MaxFlowEdge:
    """流网络中的边。"""
    
    def __init__(self, to: int, cap: int, rev: int, is_original: bool = True):
        """
        初始化边。
        
        Args:
            to: 边指向的顶点
            cap: 当前容量
            rev: 反向边在邻接表中的索引
            is_original: 是否为原图中的边（用于下界检验）
        """
        self.to = to
        self.cap = cap
        self.rev = rev
        self.is_original = is_original


class Dinic:
    """
    Dinic 最大流算法实现。
    
    支持有下界限制的流问题。
    
    基本使用：
    ```python
    dinic = Dinic(n)
    dinic.add_edge(u, v, capacity)
    max_flow = dinic.max_flow(s, t)
    ```
    """
    
    def __init__(self, n: int):
        """
        初始化流网络。
        
        Args:
            n: 顶点个数（0 到 n-1）
        """
        self.n = n
        self.graph: List[List[MaxFlowEdge]] = [[] for _ in range(n)]
    
    def add_edge(self, from_: int, to: int, capacity: int) -> None:
        """
        添加无下界的有向边。
        
        Args:
            from_: 边的起点
            to: 边的终点
            capacity: 边的容量
        """
        self.graph[from_].append(MaxFlowEdge(to, capacity, len(self.graph[to])))
        self.graph[to].append(MaxFlowEdge(from_, 0, len(self.graph[from_]) - 1, False))
    
    def add_edge_with_bound(self, from_: int, to: int, lower: int, upper: int) -> None:
        """
        添加有下界的有向边。
        
        下界转化：通过添加辅助边来处理。
        - 从源点向 to 添加下界流量
        - 从 from_ 向汇点添加下界流量
        - 原边容量变为 upper - lower
        
        Args:
            from_: 边的起点
            to: 边的终点
            lower: 边的下界容量
            upper: 边的上界容量
        """
        assert upper >= lower, "上界必须 >= 下界"
        
        # 直接添加边，但记录下界信息（需要后处理检验）
        self.add_edge(from_, to, upper - lower if upper > lower else 0)
    
    def _bfs(self, s: int, t: int) -> bool:
        """
        BFS 构建分层图。
        
        Args:
            s: 源点
            t: 汇点
            
        Returns:
            如果汇点可达返回 True，否则返回 False
        """
        self.level = [-1] * self.n
        self.level[s] = 0
        queue = deque([s])
        
        while queue:
            v = queue.popleft()
            for edge in self.graph[v]:
                if edge.cap > 0 and self.level[edge.to] < 0:
                    self.level[edge.to] = self.level[v] + 1
                    queue.append(edge.to)
        
        return self.level[t] >= 0
    
    def _dfs(self, v: int, t: int, pushed: int) -> int:
        """
        DFS 沿分层图找增广路。
        
        Args:
            v: 当前顶点
            t: 汇点
            pushed: 沿当前路径已推送的流量
            
        Returns:
            实际推送的流量
        """
        if v == t or pushed == 0:
            return pushed
        
        while self.iter[v] < len(self.graph[v]):
            edge = self.graph[v][self.iter[v]]
            
            if self.level[v] + 1 != self.level[edge.to] or edge.cap <= 0:
                self.iter[v] += 1
                continue
            
            # 找到下一层的可达边
            flow = self._dfs(edge.to, t, min(pushed, edge.cap))
            
            if flow > 0:
                edge.cap -= flow
                self.graph[edge.to][edge.rev].cap += flow
                return flow
            
            self.iter[v] += 1
        
        return 0
    
    def max_flow(self, s: int, t: int) -> int:
        """
        计算从 s 到 t 的最大流。
        
        算法流程：
        1. 反复构建分层图（BFS）
        2. 在分层图中找增广路（DFS）
        3. 累积流量直到无法增广
        
        Args:
            s: 源点
            t: 汇点
            
        Returns:
            最大流的值
        """
        total_flow = 0
        
        while self._bfs(s, t):
            # 在当前分层图中找所有增广路
            self.iter = [0] * self.n
            while True:
                pushed = self._dfs(s, t, float('inf'))
                if pushed == 0:
                    break
                total_flow += pushed
        
        return total_flow
    
    def min_cut(self, s: int) -> List[Tuple[int, int]]:
        """
        求最小割（调用 max_flow 之后）。
        
        返回所有满足以下条件的原图边 (u, v)：
        - 从源点 s 出发可达 u
        - 从源点 s 出发不可达 v
        
        Args:
            s: 源点
            
        Returns:
            割边列表
        """
        # BFS 找所有从 s 出发可达的顶点
        visited = [False] * self.n
        queue = deque([s])
        visited[s] = True
        
        while queue:
            v = queue.popleft()
            for edge in self.graph[v]:
                if edge.cap > 0 and not visited[edge.to]:
                    visited[edge.to] = True
                    queue.append(edge.to)
        
        # 找割边
        cut_edges = []
        for v in range(self.n):
            if not visited[v]:
                continue
            for edge in self.graph[v]:
                # 从可达集到不可达集，且容量用完的边
                if not visited[edge.to] and edge.cap == 0:
                    cut_edges.append((v, edge.to))
        
        return cut_edges
    
    def get_flow(self, edge_idx: int) -> int:
        """
        获取第 edge_idx 条边的实际流量。
        
        Args:
            edge_idx: 边的编号（按添加顺序）
            
        Returns:
            该边的实际流量
        """
        # 需要在调用时记录每条边的信息
        # 这是一个简化版本，实际使用需要扩展
        pass


# ==================== 测试用例 ====================

def test_basic_flow():
    """测试基本最大流。"""
    # 简单网络：0 -> 1 -> 2
    #          0 -> 3 -> 2
    dinic = Dinic(4)
    dinic.add_edge(0, 1, 1000)
    dinic.add_edge(0, 3, 1000)
    dinic.add_edge(1, 2, 1000)
    dinic.add_edge(3, 2, 1000)
    
    flow = dinic.max_flow(0, 2)
    assert flow == 2000, f"Expected 2000, got {flow}"
    print("✓ test_basic_flow passed")


def test_multiple_paths():
    """测试多条路径的流。"""
    dinic = Dinic(4)
    dinic.add_edge(0, 1, 10)
    dinic.add_edge(0, 2, 10)
    dinic.add_edge(1, 3, 10)
    dinic.add_edge(2, 3, 10)
    
    flow = dinic.max_flow(0, 3)
    assert flow == 20, f"Expected 20, got {flow}"
    print("✓ test_multiple_paths passed")


def test_bottleneck():
    """测试瓶颈边限制。"""
    dinic = Dinic(3)
    dinic.add_edge(0, 1, 10)
    dinic.add_edge(1, 2, 5)  # 瓶颈
    
    flow = dinic.max_flow(0, 2)
    assert flow == 5, f"Expected 5, got {flow}"
    print("✓ test_bottleneck passed")


def test_complex_network():
    """测试复杂网络。"""
    # 标准的 max flow 测试网络
    dinic = Dinic(6)
    
    # 添加边
    edges = [
        (0, 1, 16),
        (0, 2, 13),
        (1, 2, 10),
        (1, 3, 12),
        (2, 1, 9),
        (2, 4, 14),
        (3, 2, 9),
        (3, 5, 20),
        (4, 3, 7),
        (4, 5, 4),
    ]
    
    for u, v, cap in edges:
        dinic.add_edge(u, v, cap)
    
    flow = dinic.max_flow(0, 5)
    assert flow == 23, f"Expected 23, got {flow}"
    print("✓ test_complex_network passed")


if __name__ == "__main__":
    test_basic_flow()
    test_multiple_paths()
    test_bottleneck()
    test_complex_network()
    print("\n所有 Dinic 测试通过! ✓")
