"""
最大流算法：支持边信息查询的 Dinic 算法实现。

时间复杂度：O(V² * E)

特性：
- 支持添加和查询边的流量信息
- 提供最小割查询
- 边的容量和流量可以修改
"""

from collections import deque
from typing import List, Dict, Any


class Edge:
    """流网络中的边。"""
    
    def __init__(self, to: int, rev: int, cap: int):
        self.to = to
        self.rev = rev
        self.cap = cap


class MaxFlow:
    """
    最大流类。
    
    特点：
    - 支持边的增删查改
    - 支持最小割计算
    - 支持流量查询
    """
    
    def __init__(self, n: int):
        """
        初始化。
        
        Args:
            n: 顶点个数
        """
        self.n = n
        self.graph: List[List[Edge]] = [[] for _ in range(n)]
        self.edges: List[tuple] = []  # 记录原始边的位置信息
    
    def add_edge(self, from_: int, to: int, cap: int) -> int:
        """
        添加边，返回边的编号。
        
        Args:
            from_: 起点
            to: 终点
            cap: 容量
            
        Returns:
            边的编号（用于后续查询）
        """
        edge_id = len(self.edges)
        self.edges.append((from_, len(self.graph[from_])))
        
        self.graph[from_].append(Edge(to, len(self.graph[to]), cap))
        self.graph[to].append(Edge(from_, len(self.graph[from_]) - 1, 0))
        
        return edge_id
    
    def get_edge(self, edge_id: int) -> Dict[str, Any]:
        """
        获取边的信息。
        
        Args:
            edge_id: 边的编号
            
        Returns:
            包含 from, to, cap, flow 的字典
        """
        from_, idx = self.edges[edge_id]
        edge = self.graph[from_][idx]
        reverse_edge = self.graph[edge.to][edge.rev]
        
        return {
            'from': from_,
            'to': edge.to,
            'cap': edge.cap + reverse_edge.cap,
            'flow': reverse_edge.cap
        }
    
    def change_edge(self, edge_id: int, new_cap: int, new_flow: int) -> None:
        """
        修改边的容量和流量。
        
        Args:
            edge_id: 边的编号
            new_cap: 新容量
            new_flow: 新流量
        """
        assert 0 <= new_flow <= new_cap
        
        from_, idx = self.edges[edge_id]
        edge = self.graph[from_][idx]
        reverse_edge = self.graph[edge.to][edge.rev]
        
        edge.cap = new_cap - new_flow
        reverse_edge.cap = new_flow
    
    def max_flow(self, s: int, t: int, flow_limit: int = float('inf')) -> int:
        """
        计算最大流。
        
        Args:
            s: 源点
            t: 汇点
            flow_limit: 流量限制（默认无限）
            
        Returns:
            最大流的值
        """
        total_flow = 0
        
        while total_flow < flow_limit:
            # BFS 构建分层图
            self.level = [-1] * self.n
            self.level[s] = 0
            queue = deque([s])
            
            while queue:
                v = queue.popleft()
                for edge in self.graph[v]:
                    if edge.cap > 0 and self.level[edge.to] < 0:
                        self.level[edge.to] = self.level[v] + 1
                        if edge.to == t:
                            break
                        queue.append(edge.to)
            
            if self.level[t] < 0:
                break
            
            # DFS 找增广路
            self.iter = [0] * self.n
            while total_flow < flow_limit:
                flow = self._dfs(s, t, flow_limit - total_flow)
                if flow == 0:
                    break
                total_flow += flow
        
        return total_flow
    
    def _dfs(self, v: int, t: int, up: int) -> int:
        """
        DFS 沿分层图找增广路。
        
        Args:
            v: 当前顶点
            t: 汇点
            up: 可推送的最大流量
            
        Returns:
            实际推送的流量
        """
        if v == t:
            return up
        
        res = 0
        while self.iter[v] < len(self.graph[v]):
            edge = self.graph[v][self.iter[v]]
            
            if (self.level[v] < self.level[edge.to] and 
                edge.cap > 0):
                
                flow = self._dfs(edge.to, t, min(up - res, edge.cap))
                if flow > 0:
                    edge.cap -= flow
                    self.graph[edge.to][edge.rev].cap += flow
                    res += flow
                    if res == up:
                        return res
            
            self.iter[v] += 1
        
        self.level[v] = self.n
        return res
    
    def min_cut(self, s: int) -> List[tuple]:
        """
        求最小割。
        
        Args:
            s: 源点
            
        Returns:
            割边列表 [(u, v), ...]
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
                if not visited[edge.to]:
                    cut_edges.append((v, edge.to))
        
        return cut_edges
    
    def all_edges(self) -> List[Dict[str, Any]]:
        """获取所有边的信息。"""
        result = []
        for i in range(len(self.edges)):
            result.append(self.get_edge(i))
        return result


# ==================== 测试 ====================

def test_simple_flow():
    """测试简单流。"""
    mf = MaxFlow(4)
    mf.add_edge(0, 1, 10)
    mf.add_edge(0, 2, 10)
    mf.add_edge(1, 3, 10)
    mf.add_edge(2, 3, 10)
    
    flow = mf.max_flow(0, 3)
    assert flow == 20, f"Expected 20, got {flow}"
    print("✓ test_simple_flow passed")


def test_bottleneck():
    """测试瓶颈边。"""
    mf = MaxFlow(3)
    mf.add_edge(0, 1, 10)
    mf.add_edge(1, 2, 5)
    
    flow = mf.max_flow(0, 2)
    assert flow == 5, f"Expected 5, got {flow}"
    print("✓ test_bottleneck passed")


def test_complex():
    """测试复杂网络。"""
    mf = MaxFlow(6)
    mf.add_edge(0, 1, 16)
    mf.add_edge(0, 2, 13)
    mf.add_edge(1, 2, 10)
    mf.add_edge(1, 3, 12)
    mf.add_edge(2, 1, 9)
    mf.add_edge(2, 4, 14)
    mf.add_edge(3, 2, 9)
    mf.add_edge(3, 5, 20)
    mf.add_edge(4, 3, 7)
    mf.add_edge(4, 5, 4)
    
    flow = mf.max_flow(0, 5)
    assert flow == 23, f"Expected 23, got {flow}"
    print("✓ test_complex passed")


if __name__ == "__main__":
    test_simple_flow()
    test_bottleneck()
    test_complex()
    print("\n所有 MaxFlow 测试通过! ✓")
