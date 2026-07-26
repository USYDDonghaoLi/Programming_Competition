"""
虚拟树（Auxiliary Tree / Virtual Tree）

从原树和一个关键节点集合构建一棵虚拟树，只包含关键节点及其所有 LCA。

原树保留了距离和 LCA 关系，虚拟树大小更小，用于处理子树相关的问题。

应用：
- 快速处理树上的查询
- 子树聚合问题
- 路径相关问题的优化

复杂度：
- 构建虚拟树：O(k log n)，其中 k 是关键节点数量
- LCA 查询：O(log n)
"""

from typing import List, Tuple


class AuxiliaryTree:
    """
    虚拟树。
    
    使用 ST 表进行 RMQ（Range Minimum Query）来支持 O(log n) 的 LCA 查询。
    """
    
    def __init__(self, n: int, edges: List[List[int]], root: int = 0):
        """
        初始化虚拟树。
        
        Args:
            n: 树的节点数
            edges: 邻接表（edges[u] = [v1, v2, ...] 表示 u 连接到 v1, v2 等）
            root: 树的根节点
        """
        self.n = n
        self.edges = edges
        self.root = root
        
        # 欧拉游走相关
        self.euler = []  # 欧拉序列
        self.first = [-1] * n  # 每个节点第一次出现的欧拉序位置
        self.depth = [-1] * n  # 节点深度
        
        # 预计算 log
        self.log = [0] * (2 * n)
        for i in range(2, 2 * n):
            self.log[i] = self.log[i >> 1] + 1
        
        # ST 表（用于 RMQ）
        self.st = []
        
        # 虚拟树邻接表
        self.virtual_edges = [[] for _ in range(n)]
        
        # 构建数据结构
        self._dfs(root)
        self._build_sparse_table()
    
    def _dfs(self, node: int) -> None:
        """
        DFS 建立欧拉序列。
        
        Args:
            node: 当前节点
        """
        stack = [node]
        self.depth[node] = 0
        pos = 0
        
        while stack:
            v = stack.pop()
            
            if v >= 0:
                # 第一次访问
                self.euler.append(v)
                self.first[v] = pos
                pos += 1
                
                # 将子节点压入栈（逆序保证正确遍历）
                for u in self.edges[v][::-1]:
                    if self.depth[u] == -1:
                        self.depth[u] = self.depth[v] + 1
                        stack.append(~v)  # 标记"返回"
                        stack.append(u)
            else:
                # 返回时，添加到欧拉序列
                self.euler.append(~v)
                pos += 1
    
    def _build_sparse_table(self) -> None:
        """
        构建 ST 表用于 RMQ。
        """
        euler_len = len(self.euler)
        self.st.append(self.euler)
        
        k = 1
        while 2 * k <= euler_len:
            prev = self.st[-1]
            nxt = []
            
            for j in range(euler_len - 2 * k + 1):
                v = prev[j]
                u = prev[j + k]
                
                # 选择深度更小的（即更靠近根）
                if isinstance(v, int) and isinstance(u, int):
                    nxt.append(v if self.depth[v] <= self.depth[u] else u)
                else:
                    # 处理标记值（~v 形式）
                    nxt.append(v if self.depth.get(v, float('inf')) <= self.depth.get(u, float('inf')) else u)
            
            self.st.append(nxt)
            k *= 2
    
    def lca(self, u: int, v: int) -> int:
        """
        查询 u 和 v 的最低公共祖先。
        
        Args:
            u, v: 两个节点
            
        Returns:
            LCA 节点编号
        """
        x = self.first[u]
        y = self.first[v]
        
        if x > y:
            x, y = y, x
        
        span = y - x + 1
        k = self.log[span]
        
        v1 = self.st[k][x]
        v2 = self.st[k][y - (1 << k) + 1]
        
        # 处理可能的标记值
        if isinstance(v1, int) and isinstance(v2, int):
            return v1 if self.depth[v1] <= self.depth[v2] else v2
        else:
            return u if self.depth[u] <= self.depth[v] else v
    
    def build_virtual_tree(self, nodes: List[int]) -> int:
        """
        从给定节点集合构建虚拟树。
        
        Args:
            nodes: 关键节点列表
            
        Returns:
            虚拟树的根节点
        """
        if not nodes:
            return -1
        
        k = len(nodes)
        
        # 按欧拉序排序
        nodes.sort(key=lambda x: self.first[x])
        
        # 清空虚拟树邻接表
        for i in range(self.n):
            self.virtual_edges[i] = []
        
        # 使用栈维护虚拟树
        stack = [nodes[0]]
        
        for i in range(k - 1):
            u = nodes[i]
            v = nodes[i + 1]
            w = self.lca(u, v)
            
            if w != u:
                # 弹出栈中所有深度大于 w 的节点
                last = stack.pop()
                
                while stack and self.depth[w] < self.depth[stack[-1]]:
                    self.virtual_edges[stack[-1]].append(last)
                    last = stack.pop()
                
                # 如果栈不为空且栈顶不是 w，添加 w
                if stack and stack[-1] != w:
                    self.virtual_edges[w].append(last)
                    stack.append(w)
                elif not stack:
                    stack.append(w)
                    self.virtual_edges[w].append(last)
                else:
                    # 栈顶就是 w
                    self.virtual_edges[w].append(last)
            
            stack.append(v)
        
        # 连接栈中剩余节点
        for i in range(len(stack) - 1):
            self.virtual_edges[stack[i]].append(stack[i + 1])
        
        return stack[0]


def test_basic_tree():
    """测试基本树的 LCA"""
    # 树：0 - 1 - 3
    #      \
    #       2
    edges = [
        [1, 2],
        [0, 3],
        [0],
        [1]
    ]
    
    tree = AuxiliaryTree(4, edges, root=0)
    
    # LCA(3, 2) = 0
    assert tree.lca(3, 2) == 0, "LCA(3, 2) should be 0"
    
    # LCA(1, 2) = 0
    assert tree.lca(1, 2) == 0, "LCA(1, 2) should be 0"
    
    # LCA(3, 1) = 1
    assert tree.lca(3, 1) == 1, "LCA(3, 1) should be 1"
    
    print("✓ test_basic_tree passed")


def test_virtual_tree():
    """测试虚拟树构建"""
    # 树：
    #       0
    #      / \
    #     1   2
    #    / \
    #   3   4
    edges = [
        [1, 2],
        [0, 3, 4],
        [0],
        [1],
        [1]
    ]
    
    tree = AuxiliaryTree(5, edges, root=0)
    
    # 虚拟树包含节点 [3, 4]，应该生成根为 1（3 和 4 的 LCA）
    root = tree.build_virtual_tree([3, 4])
    assert root == 1, f"Virtual tree root should be 1, got {root}"
    
    print("✓ test_virtual_tree passed")


if __name__ == "__main__":
    test_basic_tree()
    test_virtual_tree()
    print("\n所有虚拟树测试通过！✓")
