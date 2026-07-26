"""
匈牙利算法（Hungarian Algorithm）

求二分图的最大匹配和最小点覆盖。

原理：使用增广路径的思想，每次为未匹配的点寻找增广路径，扩展匹配。

应用：
- 二分图最大匹配
- 二分图最小点覆盖（König定理）
- 指派问题（赋权版本）

复杂度：O(VE) 在标准实现中，优化版本可达 O(V²E)
"""

from typing import List, Tuple


class BipartiteMatching:
    """
    二分图最大匹配。
    
    使用增广路径法（匈牙利算法）找最大匹配。
    """
    
    def __init__(self, m: int, n: int):
        """
        初始化二分图。
        
        Args:
            m: 左侧节点数（1-indexed）
            n: 右侧节点数（1-indexed）
        """
        self.m = m
        self.n = n
        self.graph = [[] for _ in range(m + 1)]  # 邻接表
        self.match = [0] * (n + 1)  # match[j] = 右侧点 j 匹配的左侧点
        self.visited = [False] * (n + 1)
    
    def add_edge(self, u: int, v: int) -> None:
        """
        添加一条边从左侧 u 到右侧 v。
        
        Args:
            u: 左侧节点（1-indexed）
            v: 右侧节点（1-indexed）
        """
        self.graph[u].append(v)
    
    def _dfs(self, u: int) -> bool:
        """
        DFS 查找增广路径。
        
        Args:
            u: 左侧当前节点
            
        Returns:
            是否找到增广路径
        """
        for v in self.graph[u]:
            if not self.visited[v]:
                self.visited[v] = True
                
                # 如果 v 未被匹配或能为 match[v] 找到新的匹配
                if self.match[v] == 0 or self._dfs(self.match[v]):
                    self.match[v] = u
                    return True
        
        return False
    
    def max_matching(self) -> int:
        """
        求最大匹配数。
        
        Returns:
            最大匹配的大小
        """
        result = 0
        
        for u in range(1, self.m + 1):
            # 每次重置访问标记
            self.visited = [False] * (self.n + 1)
            
            if self._dfs(u):
                result += 1
        
        return result
    
    def get_matching(self) -> List[Tuple[int, int]]:
        """
        获取匹配结果。
        
        Returns:
            匹配的边列表 [(u, v), ...]
        """
        edges = []
        for v in range(1, self.n + 1):
            if self.match[v] != 0:
                edges.append((self.match[v], v))
        return edges
    
    def min_vertex_cover(self) -> int:
        """
        求最小点覆盖（König定理）。
        
        最小点覆盖数 = 最大匹配数
        
        Returns:
            最小点覆盖的大小
        """
        return self.max_matching()


def test_simple_matching():
    """测试简单匹配"""
    # 左侧 1, 2, 3；右侧 1, 2, 3
    # 边：1-1, 1-2, 2-2, 3-3
    bm = BipartiteMatching(3, 3)
    bm.add_edge(1, 1)
    bm.add_edge(1, 2)
    bm.add_edge(2, 2)
    bm.add_edge(3, 3)
    
    result = bm.max_matching()
    assert result == 3, f"Expected 3, got {result}"
    print("✓ test_simple_matching passed")


def test_partial_matching():
    """测试部分匹配"""
    # 左侧 1, 2, 3；右侧 1, 2
    # 边：1-1, 2-2, 3-1
    bm = BipartiteMatching(3, 2)
    bm.add_edge(1, 1)
    bm.add_edge(2, 2)
    bm.add_edge(3, 1)
    
    result = bm.max_matching()
    assert result == 2, f"Expected 2, got {result}"
    print("✓ test_partial_matching passed")


def test_get_edges():
    """测试获取匹配的边"""
    bm = BipartiteMatching(2, 2)
    bm.add_edge(1, 1)
    bm.add_edge(2, 2)
    
    result = bm.max_matching()
    edges = bm.get_matching()
    
    assert result == 2, f"Expected 2 matching, got {result}"
    assert len(edges) == 2, f"Expected 2 edges, got {len(edges)}"
    print("✓ test_get_edges passed")


if __name__ == "__main__":
    test_simple_matching()
    test_partial_matching()
    test_get_edges()
    print("\n所有匹配测试通过！✓")
