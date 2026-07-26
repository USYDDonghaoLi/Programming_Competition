"""
Tarjan 算法 - 强连通分量（Strongly Connected Component, SCC）。
强连通分量是指有向图中任意两个顶点可以相互到达的最大子图。
时间复杂度：O(V + E)
空间复杂度：O(V + E)
"""

from collections import defaultdict
from types import GeneratorType


def bootstrap(func, stack=[]):
    """
    Bootstrap 装饰器 - 将递归生成器转换为迭代栈执行。
    
    用途：避免 Python 的递归深度限制（默认 ~1000）。
    使用方法：
    1. 将递归函数改写为生成器函数，使用 yield 替代 return
    2. 用 @bootstrap 装饰该函数
    3. 递归调用时 yield 该调用结果
    
    Example:
        @bootstrap
        def dfs(node):
            # ... 处理代码 ...
            yield dfs(next_node)  # 递归调用前加 yield
            # ... 处理代码 ...
            yield None  # 函数末尾需要 yield None
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


class TarjanSCC:
    """
    Tarjan 算法求解有向图的强连通分量。
    
    原理：
    - dfn[v]: v 的发现时间
    - low[v]: v 及其子树中能到达的最小发现时间
    - 当 dfn[v] == low[v] 时，v 是某个 SCC 的根
    
    应用场景：
    - 求解有向图的强连通分量
    - 构造 SCC 的元图（DAG）
    - 分析系统的强连接性
    """
    
    def __init__(self, num_vertices: int):
        """
        初始化图。
        Args:
            num_vertices: 顶点数量（1 到 num_vertices）
        """
        self.adj = defaultdict(list)
        self.num_vertices = num_vertices
        self.dfn = [0] * (num_vertices + 1)  # 发现时间
        self.low = [0] * (num_vertices + 1)  # 最小发现时间
        self.dfn_count = 0  # DFN 计数器
        self.stack = [0] * (num_vertices + 1)  # 栈
        self.in_stack = [0] * (num_vertices + 1)  # 是否在栈中
        self.stack_pointer = 0  # 栈指针
        self.scc_id = [0] * (num_vertices + 1)  # 每个点的 SCC 编号
        self.scc_count = 0  # SCC 数量
        self.scc_size = [0] * (num_vertices + 1)  # 每个 SCC 的大小
        self.sccs = []  # 所有 SCC（点的集合）
    
    def add_edge(self, u: int, v: int) -> None:
        """
        添加有向边。
        Args:
            u, v: 边的起点和终点
        """
        self.adj[u].append(v)
    
    @bootstrap
    def _dfs(self, node: int):
        """
        DFS 遍历，寻找 SCC（使用 yield 改写为生成器，配合 bootstrap 装饰器）。
        Args:
            node: 当前顶点
        """
        self.dfn_count += 1
        self.stack_pointer += 1
        
        self.low[node] = self.dfn[node] = self.dfn_count
        self.stack[self.stack_pointer] = node
        self.in_stack[node] = 1
        
        # 遍历所有后继节点
        for neighbor in self.adj[node]:
            if not self.dfn[neighbor]:
                # 未访问，递归处理
                yield self._dfs(neighbor)
                self.low[node] = min(self.low[node], self.low[neighbor])
            elif self.in_stack[neighbor]:
                # 回边，更新 low 值
                self.low[node] = min(self.low[node], self.dfn[neighbor])
        
        # 如果 node 是 SCC 的根，弹出 SCC 中的所有点
        if self.dfn[node] == self.low[node]:
            scc_nodes = set()
            self.scc_count += 1
            
            while self.stack[self.stack_pointer] != node:
                v = self.stack[self.stack_pointer]
                self.scc_id[v] = self.scc_count
                scc_nodes.add(v)
                self.scc_size[self.scc_count] += 1
                self.in_stack[v] = 0
                self.stack_pointer -= 1
            
            v = self.stack[self.stack_pointer]
            self.scc_id[v] = self.scc_count
            scc_nodes.add(v)
            self.scc_size[self.scc_count] += 1
            self.in_stack[v] = 0
            self.stack_pointer -= 1
            self.sccs.append(scc_nodes)
        
        yield None
    
    def find_scc(self):
        """
        求解所有强连通分量。
        Returns:
            tuple: (SCC 数量, SCC 列表，点到 SCC 的映射)
        """
        for node in range(1, self.num_vertices + 1):
            if not self.dfn[node]:
                self._dfs(node)
        
        return self.scc_count, self.sccs, self.scc_id