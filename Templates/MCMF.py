"""
最小费用最大流（Minimum Cost Maximum Flow）。

使用势函数（Potential Function）优化的 SPFA + Dijkstra 混合算法。

特点：
- 支持获取流量随费用变化的曲线（slope）
- 时间复杂度：O(F * E * log V)，其中 F 是最大流
- 空间复杂度：O(V + E)

应用场景：
- 运输问题（运输最少费用）
- 路由问题（寻找最低成本路径）
- 匹配问题（最优分配）
"""

from heapq import heappush, heappop
from typing import List, Dict, Any, Tuple


class MCMFEdge:
    """最小费用最大流中的边。"""
    
    def __init__(self, to: int, rev: int, cap: int, cost: int):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.cost = cost


class MinCostMaxFlow:
    """
    最小费用最大流类。
    
    核心算法：
    1. 使用势函数维护可行性条件
    2. 用 Dijkstra 找新的增广路（所有边权都非负）
    3. 更新势函数
    4. 重复直到达到流量限制或无法增广
    """
    
    def __init__(self, n: int):
        """
        初始化。
        
        Args:
            n: 顶点个数
        """
        self.n = n
        self.graph: List[List[MCMFEdge]] = [[] for _ in range(n)]
        self.edge_list: List[Tuple[int, int]] = []
    
    def add_edge(self, from_: int, to: int, cap: int, cost: int) -> int:
        """
        添加一条边。
        
        Args:
            from_: 边的起点
            to: 边的终点
            cap: 边的容量
            cost: 边的费用（权重）
            
        Returns:
            边的编号（用于查询）
        """
        edge_id = len(self.edge_list)
        self.edge_list.append((from_, len(self.graph[from_])))
        
        self.graph[from_].append(MCMFEdge(to, len(self.graph[to]), cap, cost))
        self.graph[to].append(MCMFEdge(from_, len(self.graph[from_]) - 1, 0, -cost))
        
        return edge_id
    
    def get_edge(self, edge_id: int) -> Dict[str, Any]:
        """
        获取边的信息。
        
        Args:
            edge_id: 边的编号
            
        Returns:
            包含 from, to, cap, flow, cost 的字典
        """
        from_, idx = self.edge_list[edge_id]
        edge = self.graph[from_][idx]
        reverse_edge = self.graph[edge.to][edge.rev]
        
        return {
            'from': from_,
            'to': edge.to,
            'cap': edge.cap + reverse_edge.cap,
            'flow': reverse_edge.cap,
            'cost': edge.cost
        }
    
    def all_edges(self) -> List[Dict[str, Any]]:
        """获取所有边的信息。"""
        return [self.get_edge(i) for i in range(len(self.edge_list))]
    
    def max_flow(self, s: int, t: int, flow_limit: int = float('inf')) -> Tuple[int, int]:
        """
        计算最小费用最大流（完整版本）。
        
        Args:
            s: 源点
            t: 汇点
            flow_limit: 流量限制
            
        Returns:
            (最大流的值, 对应的最小费用)
        """
        result = self.slope(s, t, flow_limit)
        if result:
            return result[-1]
        return (0, 0)
    
    def slope(self, s: int, t: int, flow_limit: int = float('inf')) -> List[Tuple[int, int]]:
        """
        计算流量-费用曲线（Pareto 前沿）。
        
        返回一系列 (flow, cost) 的点，表示在达到该流量时的最小费用。
        
        Args:
            s: 源点
            t: 汇点
            flow_limit: 流量限制
            
        Returns:
            [(flow, cost), ...] 按流量递增排列，费用也递增
        """
        assert 0 <= s < self.n
        assert 0 <= t < self.n
        assert s != t
        
        INF = 10**18
        
        # 势函数：维持所有边的约化费用非负
        # 约化费用 = cost + potential[from] - potential[to]
        potential = [0] * self.n
        
        total_flow = 0
        total_cost = 0
        result = [(0, 0)]
        
        while total_flow < flow_limit:
            # Dijkstra：在所有约化费用非负的条件下找最短路
            dist = [INF] * self.n
            pv = [-1] * self.n  # 前驱顶点
            pe = [-1] * self.n  # 前驱边的索引
            
            dist[s] = 0
            heap = [(0, s)]
            
            while heap:
                d, v = heappop(heap)
                
                if d > dist[v]:
                    continue
                
                for i, edge in enumerate(self.graph[v]):
                    if edge.cap > 0:
                        # 约化费用
                        reduced_cost = edge.cost + potential[v] - potential[edge.to]
                        new_dist = dist[v] + reduced_cost
                        
                        if new_dist < dist[edge.to]:
                            dist[edge.to] = new_dist
                            pv[edge.to] = v
                            pe[edge.to] = i
                            heappush(heap, (new_dist, edge.to))
            
            # 无法到达汇点
            if dist[t] == INF:
                break
            
            # 更新势函数
            for v in range(self.n):
                if dist[v] < INF:
                    potential[v] += dist[v]
            
            # 沿增广路推送流量
            push_flow = flow_limit - total_flow
            v = t
            while v != s:
                push_flow = min(push_flow, self.graph[pv[v]][pe[v]].cap)
                v = pv[v]
            
            # 更新边的容量和流量
            v = t
            while v != s:
                pv_node = pv[v]
                pe_idx = pe[v]
                edge = self.graph[pv_node][pe_idx]
                rev_edge = self.graph[v][edge.rev]
                
                edge.cap -= push_flow
                rev_edge.cap += push_flow
                v = pv_node
            
            # 更新流量和费用
            total_flow += push_flow
            total_cost += push_flow * potential[t]
            
            # 避免重复的 (flow, cost) 对
            if result[-1][1] != total_cost:
                result.append((total_flow, total_cost))
        
        return result


# ==================== 测试用例 ====================

def test_simple_mcmf():
    """测试简单的最小费用最大流。"""
    mcmf = MinCostMaxFlow(3)
    mcmf.add_edge(0, 1, 10, 1)  # 容量 10，费用 1
    mcmf.add_edge(1, 2, 10, 2)  # 容量 10，费用 2
    
    flow, cost = mcmf.max_flow(0, 2, 10)
    assert flow == 10, f"Expected flow 10, got {flow}"
    assert cost == 30, f"Expected cost 30, got {cost}"  # 10 * (1 + 2)
    print("✓ test_simple_mcmf passed")


def test_multiple_paths():
    """测试多条路径的最小费用。"""
    mcmf = MinCostMaxFlow(4)
    
    # 路径 1: 0 -> 1 -> 3，费用 = 1 + 1 = 2
    mcmf.add_edge(0, 1, 5, 1)
    mcmf.add_edge(1, 3, 5, 1)
    
    # 路径 2: 0 -> 2 -> 3，费用 = 2 + 2 = 4
    mcmf.add_edge(0, 2, 5, 2)
    mcmf.add_edge(2, 3, 5, 2)
    
    flow, cost = mcmf.max_flow(0, 3, 10)
    # 应该先用路径1（费用2/单位）送5单位，再用路径2（费用4/单位）送5单位
    # 总费用 = 5*2 + 5*4 = 30
    assert flow == 10, f"Expected flow 10, got {flow}"
    assert cost == 30, f"Expected cost 30, got {cost}"
    print("✓ test_multiple_paths passed")


def test_capacity_limit():
    """测试容量限制。"""
    mcmf = MinCostMaxFlow(3)
    mcmf.add_edge(0, 1, 5, 1)
    mcmf.add_edge(1, 2, 10, 1)
    
    flow, cost = mcmf.max_flow(0, 2, 100)
    # 容量瓶颈是 0->1，只能流 5 单位
    assert flow == 5, f"Expected flow 5, got {flow}"
    assert cost == 10, f"Expected cost 10, got {cost}"
    print("✓ test_capacity_limit passed")


if __name__ == "__main__":
    test_simple_mcmf()
    test_multiple_paths()
    test_capacity_limit()
    print("\n所有 MCMF 测试通过! ✓")
