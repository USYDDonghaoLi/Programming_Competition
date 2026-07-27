"""
Dinic 最大流算法（优化版本 - Capacity Scaling）

改进的 Dinic 算法变体，通过容量缩放或二进制缩放来处理大容量边。

相比标准 Dinic O(V² E)，缩放版可在某些情况下达到：
- O(V E log max_capacity) - 容量缩放
- O(E√V) - 单位容量网络
- 对于稀疏图或特殊结构可显著加速

核心优化思想：
1. 按容量的二进制位数，从高位到低位逐位处理
2. 在每个阶段只考虑"足够大"的容量边
3. 可减少 BFS 轮数，从而加速总体流程

应用场景：
- 大容量网络（C > 10^6）
- 稀疏图或二部图
- 单位容量特殊情况

参考文献：
- Scaling Max Flow (King, Rao, Tarjan)
- Binary Scaling Dinic
"""

from collections import deque
from typing import List, Tuple


class Edge:
    """流网络中的边。"""
    
    def __init__(self, to: int, cap: int, rev: int):
        self.to = to
        self.cap = cap
        self.rev = rev


class DinicScaling:
    """
    Dinic 最大流 - 容量缩放优化版。
    
    通过二进制缩放处理不同大小的容量，减少 BFS 轮数。
    """
    
    def __init__(self, n: int):
        """初始化流网络。"""
        self.n = n
        self.graph: List[List[Edge]] = [[] for _ in range(n)]
        self.max_cap = 0
    
    def add_edge(self, u: int, v: int, cap: int) -> None:
        """添加有向边 u -> v，容量为 cap。"""
        self.graph[u].append(Edge(v, cap, len(self.graph[v])))
        self.graph[v].append(Edge(u, 0, len(self.graph[u]) - 1))
        self.max_cap = max(self.max_cap, cap)
    
    def _bfs_with_threshold(self, s: int, t: int, threshold: int) -> bool:
        """
        BFS 构建分层图，只考虑容量 >= threshold 的边。
        
        Args:
            s: 源点
            t: 汇点
            threshold: 容量阈值
            
        Returns:
            汇点是否可达
        """
        self.level = [-1] * self.n
        self.level[s] = 0
        queue = deque([s])
        
        while queue:
            v = queue.popleft()
            for edge in self.graph[v]:
                if edge.cap >= threshold and self.level[edge.to] < 0:
                    self.level[edge.to] = self.level[v] + 1
                    queue.append(edge.to)
        
        return self.level[t] >= 0
    
    def _dfs_with_threshold(self, v: int, t: int, pushed: int, threshold: int) -> int:
        """
        DFS 在分层图中找增广路，只使用容量 >= threshold 的边。
        
        Args:
            v: 当前顶点
            t: 汇点
            pushed: 可推送的流量
            threshold: 容量阈值
            
        Returns:
            实际推送的流量
        """
        if v == t or pushed == 0:
            return pushed
        
        while self.iter[v] < len(self.graph[v]):
            edge = self.graph[v][self.iter[v]]
            
            if edge.cap < threshold or self.level[v] + 1 != self.level[edge.to]:
                self.iter[v] += 1
                continue
            
            flow = self._dfs_with_threshold(edge.to, t, min(pushed, edge.cap), threshold)
            
            if flow > 0:
                edge.cap -= flow
                self.graph[edge.to][edge.rev].cap += flow
                return flow
            
            self.iter[v] += 1
        
        return 0
    
    def max_flow_scaling(self, s: int, t: int) -> int:
        """
        使用容量缩放的 Dinic 算法。
        
        从高位到低位逐个二进制位处理容量，可减少整体轮数。
        
        复杂度：O(V E log max_capacity)
        
        Args:
            s: 源点
            t: 汇点
            
        Returns:
            最大流值
        """
        if self.max_cap == 0:
            return 0
        
        # 从最高二进制位开始
        threshold = 1 << (self.max_cap.bit_length() - 1)
        total_flow = 0
        
        while threshold > 0:
            # 在当前阈值下反复构建分层图并查找增广路
            while self._bfs_with_threshold(s, t, threshold):
                self.iter = [0] * self.n
                while True:
                    pushed = self._dfs_with_threshold(s, t, float('inf'), threshold)
                    if pushed == 0:
                        break
                    total_flow += pushed
            
            threshold >>= 1  # 降低阈值到下一个二进制位
        
        return total_flow
    
    def max_flow(self, s: int, t: int) -> int:
        """
        标准 Dinic 流程（不使用缩放）。
        
        复杂度：O(V² E)
        """
        self.level = [-1] * self.n
        total_flow = 0
        
        while self._bfs_with_threshold(s, t, 1):  # threshold=1 等同于标准 Dinic
            self.iter = [0] * self.n
            while True:
                pushed = self._dfs_with_threshold(s, t, float('inf'), 1)
                if pushed == 0:
                    break
                total_flow += pushed
        
        return total_flow
    
    def min_cut(self, s: int) -> Tuple[int, List[Tuple[int, int]]]:
        """
        求最小割。
        
        Returns:
            (割值, 割边列表)
        """
        # BFS 找所有可达顶点
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
        cut_value = 0
        
        for u in range(self.n):
            if visited[u]:
                for i, edge in enumerate(self.graph[u]):
                    if not visited[edge.to]:
                        # 原边在 u -> edge.to
                        cut_edges.append((u, edge.to))
                        # 割值 = 原边容量
                        if i < len(self.graph[u]):
                            # 从反向边恢复原容量
                            rev_edge = self.graph[edge.to][edge.rev]
                            original_cap = edge.cap + rev_edge.cap
                            cut_value += original_cap
        
        return cut_value, cut_edges


# ======================== 测试 ========================

def test_scaling_dinic():
    """测试容量缩放 Dinic"""
    # 简单测试
    g = DinicScaling(6)
    edges = [
        (0, 1, 16), (0, 2, 13),
        (1, 2, 10), (1, 3, 12),
        (2, 1, 9), (2, 4, 14),
        (3, 2, 9), (3, 5, 20),
        (4, 3, 7), (4, 5, 4)
    ]
    
    for u, v, cap in edges:
        g.add_edge(u, v, cap)
    
    # 使用缩放版
    flow_scaling = g.max_flow_scaling(0, 5)
    
    # 创建新图用标准 Dinic 验证
    g2 = DinicScaling(6)
    for u, v, cap in edges:
        g2.add_edge(u, v, cap)
    
    flow_standard = g2.max_flow(0, 5)
    
    assert flow_scaling == 23, f"Expected 23, got {flow_scaling}"
    assert flow_standard == 23, f"Expected 23, got {flow_standard}"
    print("✓ test_basic passed (flow = 23)")
    
    # 大容量测试
    g3 = DinicScaling(4)
    g3.add_edge(0, 1, 1000000)
    g3.add_edge(0, 2, 1000000)
    g3.add_edge(1, 3, 1000000)
    g3.add_edge(2, 3, 1000000)
    
    flow = g3.max_flow_scaling(0, 3)
    assert flow == 2000000, f"Expected 2000000, got {flow}"
    print("✓ test_large_capacity passed (scaling 处理大容量高效)")
    
    # 单位容量
    g4 = DinicScaling(5)
    edges_unit = [(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1), (3, 4, 2)]
    for u, v, cap in edges_unit:
        g4.add_edge(u, v, cap)
    
    flow = g4.max_flow_scaling(0, 4)
    assert flow == 2, f"Expected 2, got {flow}"
    print("✓ test_unit_capacity passed")


if __name__ == "__main__":
    test_scaling_dinic()
    print("\n所有 Dinic 优化版测试通过！✓")
    print("\n性能对比:")
    print("- 标准 Dinic: O(V² E)")
    print("- 容量缩放: O(VE log C) 其中 C 是最大容量")
    print("- 单位容量: O(E√V)")
