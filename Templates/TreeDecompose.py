from collections import defaultdict
from types import GeneratorType


def bootstrap(f, stack=[]):
    """
    装饰器：将递归生成器转换为迭代式执行，避免超过 Python 递归深度限制（~1000）。
    
    使用方式：
    1. 在函数定义前加 @bootstrap
    2. 函数使用 yield 和 yield None 来控制递归流程
    3. 递归调用时使用 yield self.recursive_call(args)
    4. 函数末尾必须有 yield None
    
    原理：通过栈管理递归状态，让所有递归调用变成迭代过程。
    """
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to
    return wrappedfunc


class TreeDecompose:
    """
    树链剖分（Heavy-Light Decomposition）
    
    将树分解为若干条"重链"，使得树的任意两点间的路径可以分解为 O(log n) 条重链的并集。
    
    原理：
    - 将树的每个节点标记为其父亲的"重儿子"（子树最大的儿子）或"轻儿子"
    - 由重儿子形成的路径称为"重链"，任意节点对的路径至多跨越 O(log n) 条重链
    - 分配 DFS 序，使每条重链的节点 DFS 序连续
    
    时间复杂度：
    - 预处理：O(n)
    - 任意两点的路径分解：O(log n)
    - 结合线段树等数据结构可实现 O(log^2 n) 的路径查询/更新
    
    属性：
    - parent[i]：节点 i 的父亲
    - depth[i]：节点 i 的深度（根的深度为 0）
    - size[i]：以节点 i 为根的子树大小
    - heavy_child[i]：节点 i 的重儿子（子树最大的儿子），无则为 -1
    - chain_top[i]：节点 i 所在重链的顶端节点
    - dfs_id[i]：节点 i 的 DFS 序（用于线段树）
    - id_to_node[id]：DFS 序对应的节点
    """
    
    def __init__(self, n: int):
        """
        初始化树链剖分。
        
        Args:
            n: 树的节点数
        """
        self.n = n
        self._dfs_counter = 0
        self.adj = defaultdict(list)
        
        # 树的结构信息
        self.parent = [0] * (n + 1)
        self.depth = [0] * (n + 1)
        self.size = [0] * (n + 1)
        self.heavy_child = [0] * (n + 1)
        
        # 重链信息
        self.chain_top = [0] * (n + 1)
        self.dfs_id = [0] * (n + 1)
        self.id_to_node = [0] * (n + 1)
    
    def add_edge(self, u: int, v: int) -> None:
        """
        添加无向边。
        
        Args:
            u, v: 边连接的两个节点
        """
        self.adj[u].append(v)
        self.adj[v].append(u)
    
    @bootstrap
    def _dfs1(self, node: int) -> None:
        """
        第一阶段 DFS：计算每个节点的父亲、深度、子树大小和重儿子。
        
        使用 @bootstrap 装饰器避免递归深度限制。
        """
        self.heavy_child[node] = -1
        self.size[node] = 1
        
        for neighbor in self.adj[node]:
            if not self.depth[neighbor]:  # 未访问过
                self.depth[neighbor] = self.depth[node] + 1
                self.parent[neighbor] = node
                yield self._dfs1(neighbor)
                
                self.size[node] += self.size[neighbor]
                
                # 选择最大子树作为重儿子
                if self.heavy_child[node] == -1 or \
                   self.size[neighbor] > self.size[self.heavy_child[node]]:
                    self.heavy_child[node] = neighbor
        
        yield None
    
    @bootstrap
    def _dfs2(self, node: int, chain_head: int) -> None:
        """
        第二阶段 DFS：分配 DFS 序和重链顶端信息。
        
        优先遍历重儿子，保证重链的节点 DFS 序连续。
        使用 @bootstrap 装饰器避免递归深度限制。
        
        Args:
            node: 当前节点
            chain_head: 当前重链的顶端节点
        """
        self.chain_top[node] = chain_head
        self._dfs_counter += 1
        self.dfs_id[node] = self._dfs_counter
        self.id_to_node[self._dfs_counter] = node
        
        # 没有重儿子，停止
        if self.heavy_child[node] == -1:
            yield None
            return
        
        # 优先遍历重儿子，保持同一重链连续
        yield self._dfs2(self.heavy_child[node], chain_head)
        
        # 然后遍历轻儿子，每个轻儿子开启新的重链
        for neighbor in self.adj[node]:
            if neighbor != self.heavy_child[node] and neighbor != self.parent[node]:
                yield self._dfs2(neighbor, neighbor)
        
        yield None
    
    def build(self, root: int = 1) -> None:
        """
        对树进行链剖分。必须先调用 add_edge 添加所有边，再调用此函数。
        
        Args:
            root: 树的根节点，默认为 1
        """
        self.depth[root] = 0
        self._dfs1(root)
        self._dfs2(root, root)
    
    def lca(self, u: int, v: int) -> int:
        """
        求最近公共祖先（LCA）。
        
        通过跳跃重链，逐步向根靠近，直到两个节点在同一条重链上。
        时间复杂度：O(log n)
        
        Args:
            u, v: 两个节点
            
        Returns:
            u 和 v 的最近公共祖先
        """
        # 让深度较深的节点不断跳跃到链顶
        while self.chain_top[u] != self.chain_top[v]:
            if self.depth[self.chain_top[u]] > self.depth[self.chain_top[v]]:
                u = self.parent[self.chain_top[u]]
            else:
                v = self.parent[self.chain_top[v]]
        
        # 同一条链上，深度浅的就是 LCA
        return u if self.depth[u] < self.depth[v] else v
    
    def distance(self, u: int, v: int) -> int:
        """
        计算两个节点间的距离（边数）。
        
        Time complexity: O(log n)
        
        Args:
            u, v: 两个节点
            
        Returns:
            u 和 v 之间的最短路径长度
        """
        ancestor = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[ancestor]
    
    def decompose_path(self, u: int, v: int) -> list:
        """
        分解路径为若干条重链（每条重链用 DFS 序区间表示）。
        
        可用于结合线段树对路径进行范围查询/更新。
        时间复杂度：O(log n)
        
        Args:
            u, v: 两个节点
            
        Returns:
            路径分解后的重链区间列表，格式：[(top, bottom), ...]
            其中 top 和 bottom 是路径上某条重链的两端的 DFS 序
        """
        chains = []
        
        while self.chain_top[u] != self.chain_top[v]:
            if self.depth[self.chain_top[u]] > self.depth[self.chain_top[v]]:
                chain_top_node = self.chain_top[u]
                chains.append((self.dfs_id[chain_top_node], self.dfs_id[u]))
                u = self.parent[chain_top_node]
            else:
                chain_top_node = self.chain_top[v]
                chains.append((self.dfs_id[chain_top_node], self.dfs_id[v]))
                v = self.parent[chain_top_node]
        
        # 最后的重链片段
        chains.append((min(self.dfs_id[u], self.dfs_id[v]), 
                      max(self.dfs_id[u], self.dfs_id[v])))
        
        return chains