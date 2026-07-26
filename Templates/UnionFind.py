from collections import defaultdict


class UnionFind:
    """
    并查集（Union-Find）数据结构。
    支持快速的 find 和 union 操作，使用路径压缩和按大小的启发式合并。
    时间复杂度：近乎 O(1)（带路径压缩）
    """
    
    def __init__(self, n: int):
        """
        初始化并查集。
        Args:
            n: 元素个数
        """
        self.parent = [x for x in range(n)]
        self.size = [1 for _ in range(n)]
        self.n = n
        self.component_count = n
    
    def find(self, x: int) -> int:
        """
        查找元素 x 所在的集合代表（根节点）。
        使用迭代路径压缩优化，避免递归深度问题。
        时间复杂度：O(α(n))，其中 α 是反阿克曼函数
        Args:
            x: 元素
        Returns:
            x 所在集合的根节点
        """
        # 第一步：找到根节点
        root = self.parent[x]
        x_copy = root
        while root != self.parent[root]:
            root = self.parent[root]
        
        # 第二步：路径压缩，将 x_copy 到根的所有节点直接指向根
        while x_copy != root:
            self.parent[x_copy], x_copy = root, self.parent[x_copy]
        
        return root
    
    def union(self, x: int, y: int) -> bool:
        """
        合并包含 x 和 y 的两个集合。
        使用按大小的启发式合并（小树并入大树）。
        Args:
            x: 第一个元素
            y: 第二个元素
        Returns:
            True 表示成功合并（两个元素不在同一集合），False 表示它们已在同一集合
        """
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        
        # 将较小的树并入较大的树
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        self.component_count -= 1
        return True

    def is_connected(self, x: int, y: int) -> bool:
        """
        检查元素 x 和 y 是否在同一集合中。
        Args:
            x: 第一个元素
            y: 第二个元素
        Returns:
            True 表示连通，False 表示不连通
        """
        return self.find(x) == self.find(y)

    def get_component_size(self, x: int) -> int:
        """
        获取包含元素 x 的连通分量大小。
        Args:
            x: 元素
        Returns:
            连通分量中的元素个数
        """
        return self.size[self.find(x)]

    def get_members(self, x: int) -> list:
        """
        获取与元素 x 在同一集合中的所有元素。
        Args:
            x: 元素
        Returns:
            所有属于同一集合的元素列表
        """
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]
    
    def get_roots(self) -> list:
        """
        获取所有集合的根节点。
        Returns:
            根节点列表
        """
        return [i for i, x in enumerate(self.parent) if self.find(i) == i]
    
    def get_component_count(self) -> int:
        """
        获取当前的连通分量个数。
        Returns:
            连通分量个数
        """
        return self.component_count
    
    def get_all_components(self) -> dict:
        """
        获取所有连通分量及其成员。
        Returns:
            字典，key 为根节点，value 为该分量中的所有元素列表
        """
        components = defaultdict(list)
        for element in range(self.n):
            root = self.find(element)
            components[root].append(element)
        return dict(components)