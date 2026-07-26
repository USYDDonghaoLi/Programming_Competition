"""
树链剖分（Heavy-Light Decomposition, HLD）。
将树分解为若干条链，支持快速查询 LCA、路径、子树等信息。
时间复杂度：预处理 O(n)，单次查询 O(log^2 n) - O(log n)（取决于实现）
空间复杂度：O(n)
"""

from types import GeneratorType


def bootstrap(func, stack=[]):
    """
    Bootstrap 装饰器 - 将递归生成器转换为迭代栈执行。
    用于树链剖分中的 DFS，避免递归深度限制。
    
    使用方法：@bootstrap 装饰 DFS 函数，使用 yield 替代 return
    """
    def wrapper(*args, **kwargs):
        if stack:
            return func(*args, **kwargs)
        else:
            to = func(*args, **kwargs)
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
    return wrapper


class HLD:
    """
    树链剖分（Heavy-Light Decomposition）。
    
    核心思想：
    - 对每个节点定义"重儿子"为子树最大的子节点
    - 将节点沿着重儿子连成若干条"重链"
    - 使用 DFN 时间戳将链转换为数组区间
    - 可以在 O(log^2 n) 时间内回答路径查询
    
    支持操作：
    - LCA（最低公共祖先）
    - 路径距离
    - 路径信息查询（需配合线段树等数据结构）
    - 子树路径分解
    
    注意：节点编号从 0 开始，或从 1 开始（需保证不超过 n）
    """
    
    def __init__(self, num_nodes: int):
        """
        初始化树链剖分。
        Args:
            num_nodes: 树的节点数
        """
        self.num_nodes = num_nodes
        
        # 基础图结构
        self.adj = [[] for _ in range(num_nodes)]
        
        # DFS 信息
        self.depth = [0] * num_nodes  # 节点深度
        self.parent = [-1] * num_nodes  # 父节点
        self.subtree_size = [0] * num_nodes  # 子树大小
        self.heavy_child = [-1] * num_nodes  # 重儿子
        
        # 链分解信息
        self.dfs_num = [0] * num_nodes  # DFS 时间戳
        self.dfs_num_to_node = {}  # 时间戳反向映射
        self.chain_top = [-1] * num_nodes  # 所在链的顶部
        self.dfs_time = 0
    
    def add_edge(self, u: int, v: int) -> None:
        """
        添加树边。
        Args:
            u, v: 边的两个端点
        """
        self.adj[u].append(v)
        self.adj[v].append(u)
    
    @bootstrap
    def _dfs_first(self, u: int) -> None:
        """
        第一次 DFS：计算深度、父节点、子树大小和重儿子。
        使用 yield 改写为生成器，配合 bootstrap 装饰器避免递归深度限制。
        Args:
            u: 当前节点
        """
        self.subtree_size[u] = 1
        
        for v in self.adj[u]:
            if v != self.parent[u]:
                self.parent[v] = u
                self.depth[v] = self.depth[u] + 1
                yield self._dfs_first(v)
                self.subtree_size[u] += self.subtree_size[v]
                
                # 选择子树最大的子节点为重儿子
                if self.heavy_child[u] == -1 or self.subtree_size[v] > self.subtree_size[self.heavy_child[u]]:
                    self.heavy_child[u] = v
        
        yield None
    
    @bootstrap
    def _dfs_second(self, u: int) -> None:
        """
        第二次 DFS：分解成链并计算 DFS 时间戳。
        使用 yield 改写为生成器，配合 bootstrap 装饰器避免递归深度限制。
        Args:
            u: 当前节点
        """
        self.dfs_time += 1
        self.dfs_num[u] = self.dfs_time
        self.dfs_num_to_node[self.dfs_time] = u
        
        # 先遍历重儿子（保持在同一条链上）
        if self.heavy_child[u] != -1:
            self.chain_top[self.heavy_child[u]] = self.chain_top[u]
            yield self._dfs_second(self.heavy_child[u])
        
        # 再遍历所有轻儿子（每个开始新的链）
        for v in self.adj[u]:
            if v != self.parent[u] and v != self.heavy_child[u]:
                self.chain_top[v] = v
                yield self._dfs_second(v)
        
        yield None
    
    def build(self, root: int) -> None:
        """
        构造树链剖分。
        必须在所有 add_edge 之后调用。
        Args:
            root: 树的根节点
        """
        self.depth[root] = 0
        self.chain_top[root] = root
        
        # 第一次 DFS：计算各项信息
        self._dfs_first(root)
        
        # 第二次 DFS：分解成链
        self.dfs_time = 0
        self._dfs_second(root)
    
    def lca(self, u: int, v: int) -> int:
        """
        求最低公共祖先（Lowest Common Ancestor）。
        Args:
            u, v: 两个节点
        Returns:
            u 和 v 的最低公共祖先
        """
        # 将两个节点提升到同一条链
        while self.chain_top[u] != self.chain_top[v]:
            if self.depth[self.chain_top[u]] < self.depth[self.chain_top[v]]:
                u, v = v, u
            u = self.parent[self.chain_top[u]]
        
        # 同一条链上，深度较小的是 LCA
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        return u
    
    def distance(self, u: int, v: int) -> int:
        """
        求两点间的距离（边数）。
        Args:
            u, v: 两个节点
        Returns:
            u 到 v 的距离
        """
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]
    
    def get_path(self, u: int, v: int):
        """
        获取 u 到 v 的路径（分解为链上的区间）。
        返回多个 (start_dfs_num, end_dfs_num) 对，表示链上的连续区间。
        Args:
            u, v: 两个节点
        Returns:
            list: [(start, end), ...] 的路径分解
        """
        path_u = []
        path_v = []
        
        # 分别沿着 u 和 v 向上爬升，直到到达同一条链
        while self.chain_top[u] != self.chain_top[v]:
            if self.depth[self.chain_top[u]] > self.depth[self.chain_top[v]]:
                path_u.append((self.dfs_num[u], self.dfs_num[self.chain_top[u]]))
                u = self.parent[self.chain_top[u]]
            else:
                path_v.append((self.dfs_num[self.chain_top[v]], self.dfs_num[v]))
                v = self.parent[self.chain_top[v]]
        
        # 同一条链上的路径
        path_u.append((self.dfs_num[u], self.dfs_num[v]))
        
        # 合并路径（v 的路径反向拼接）
        path_u.extend(reversed(path_v))
        return path_u

        return v1