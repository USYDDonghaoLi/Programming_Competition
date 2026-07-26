"""
稀疏表（Sparse Table）。

用于解决静态数组的区间查询问题（Range Query）。
支持任何满足以下条件的二元操作：
- 满足结合律：(a op b) op c = a op (b op c)
- 满足幂等性：a op a = a（如最大值、最小值、按位与、按位或等）

不支持区间修改。如果需要动态维护，使用线段树或其他数据结构。

时间复杂度：
- 预处理：O(n log n)
- 单次查询：O(1)
- 空间：O(n log n)

应用：
- 区间最大值/最小值查询
- 区间最大公约数（GCD）查询
- 区间按位与/或查询
- 任何幂等性二元运算的范围查询
"""


class SparseTable:
    """
    稀疏表数据结构。
    
    原理：
    1. 预计算 info[i][j] = 从位置 i 开始、长度为 2^j 的区间的查询结果
    2. 任意区间 [l, r] 可以分解为两个 2^k 长度的区间的结合
    3. 由于操作幂等，重叠部分不影响结果
    
    属性：
    - info[i][j]：从位置 i 开始、长度为 2^j 的区间查询结果
    - log2[x]：log2(x) 的整数部分
    """
    
    def __init__(self, values: list, operation, identity):
        """
        初始化稀疏表。
        
        Args:
            values: 原数组
            operation: 二元操作函数（必须满足结合律和幂等性）
            identity: 恒等元素（通常不会用到，但为兼容性保留）
            
        示例:
            >>> st = SparseTable([1, 3, 2, 7, 5], min, float('inf'))
            >>> st.query(0, 3)  # [1, 3, 2, 7] 的最小值 = 1
            1
        """
        self.n = len(values)
        self.operation = operation
        self.identity = identity
        self.values = values
        
        # 预计算 log2 表
        self.log2 = [0] * (self.n + 1)
        self.log2[1] = 0
        for i in range(2, self.n + 1):
            self.log2[i] = self.log2[i >> 1] + 1
        
        # 最大的 k 使得 2^k <= n
        self.max_power = self.log2[self.n]
        
        # 初始化稀疏表
        # info[i][j] = [i, i+2^j) 区间的查询结果
        self.info = [[self.identity] * (self.max_power + 1) for _ in range(self.n)]
        
        # 初始化长度为 2^0 = 1 的区间
        for i in range(self.n):
            self.info[i][0] = self.values[i]
        
        # 逐步建造更长的区间
        # info[i][j] = op(info[i][j-1], info[i+2^(j-1)][j-1])
        for j in range(1, self.max_power + 1):
            for i in range(self.n):
                right_start = i + (1 << (j - 1))
                if right_start < self.n:
                    self.info[i][j] = self.operation(
                        self.info[i][j - 1],
                        self.info[right_start][j - 1]
                    )
    
    def query(self, left: int, right: int):
        """
        查询 [left, right] 区间的操作结果。
        
        使用两个重叠的幂次区间来覆盖整个区间。
        由于操作满足幂等性，重叠部分不影响结果。
        
        时间复杂度：O(1)
        
        Args:
            left: 左端点（包含）
            right: 右端点（包含）
            
        Returns:
            区间 [left, right] 的查询结果
            
        示例:
            >>> st = SparseTable([1, 3, 2, 7, 5], min, float('inf'))
            >>> st.query(0, 3)  # [1, 3, 2, 7] 的最小值
            1
            >>> st.query(2, 4)  # [2, 7, 5] 的最小值
            2
        """
        # 计算覆盖 [left, right] 的最大 2^k
        length = right - left + 1
        k = self.log2[length]
        
        # 左边界对应的区间：[left, left + 2^k)
        # 右边界对应的区间：[right - 2^k + 1, right + 1)
        # 两个区间可能有重叠，但由于幂等性，结果正确
        left_result = self.info[left][k]
        right_start = right - (1 << k) + 1
        right_result = self.info[right_start][k]
        
        return self.operation(left_result, right_result)
    
    def range_min(self, left: int, right: int) -> int:
        """
        查询 [left, right] 的最小值。
        
        便捷方法。
        
        Args:
            left: 左端点（包含）
            right: 右端点（包含）
            
        Returns:
            区间最小值
        """
        return self.query(left, right)
    
    def range_max(self, left: int, right: int) -> int:
        """
        查询 [left, right] 的最大值。
        
        便捷方法。
        
        Args:
            left: 左端点（包含）
            right: 右端点（包含）
            
        Returns:
            区间最大值
        """
        return self.query(left, right)
    
    def range_gcd(self, left: int, right: int) -> int:
        """
        查询 [left, right] 的最大公约数。
        
        便捷方法。
        
        Args:
            left: 左端点（包含）
            right: 右端点（包含）
            
        Returns:
            区间 GCD
        """
        return self.query(left, right)
