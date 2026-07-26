"""
Van Emde Boas 树（VEB Tree）

一种数据结构，用于高效的集合操作和范围查询。

支持的操作：
- insert: 插入元素
- delete: 删除元素
- member: 查询元素是否存在
- minimum/maximum: 查询最小/最大元素
- successor/predecessor: 查询后继/前驱元素

时间复杂度：所有操作均为 O(log log U)，其中 U 是值域大小

应用：
- 整数集合的高效管理
- 范围查询和排序
- 与哈希表相比，在最坏情况下提供更好的性能保证
"""

from typing import List, Optional


class VEBTree:
    """
    Van Emde Boas 树。
    
    将递归分解的思想应用于集合操作。
    """
    
    __slots__ = {'summary', 'MIN', 'MAX', 'size', 'u', 'divisor', 'cluster'}
    
    def __init__(self) -> None:
        """初始化空的 VEB 树。"""
        self.summary = None
        self.MIN = -1
        self.MAX = -1
    
    def build(self, size: int) -> None:
        """
        构建 VEB 树。
        
        Args:
            size: 树的大小为 2^size
        """
        self.size = size
        
        if self.size <= 1:
            self.u = 2
            self.divisor = 1
            return
        
        self.u = 1 << size
        self.divisor = 1 << (size >> 1)
        
        # 递归构建聚类
        cluster_size = (size >> 1) + (size & 1)
        self.cluster = [VEBTree() for _ in range(1 << cluster_size)]
        self.summary = VEBTree()
        self.summary.build(cluster_size)
        
        for i in range(1 << cluster_size):
            self.cluster[i].build(size >> 1)
    
    def _high(self, x: int) -> int:
        """获取高位。"""
        return x // self.divisor
    
    def _low(self, x: int) -> int:
        """获取低位。"""
        return x % self.divisor
    
    def _index(self, x: int, y: int) -> int:
        """由高位和低位构造值。"""
        return x * self.divisor + y
    
    def minimum(self) -> int:
        """获取最小元素（-1 如果为空）。"""
        return self.MIN
    
    def maximum(self) -> int:
        """获取最大元素（-1 如果为空）。"""
        return self.MAX
    
    def member(self, x: int) -> bool:
        """查询元素是否在树中。"""
        if x == self.MIN or x == self.MAX:
            return True
        if self.u == 2:
            return False
        return self.cluster[self._high(x)].member(self._low(x))
    
    def successor(self, x: int) -> int:
        """查询 x 的后继（-1 如果不存在）。"""
        if self.u == 2:
            return 1 if x == 0 and self.MAX == 1 else -1
        
        if self.MIN != -1 and x < self.MIN:
            return self.MIN
        
        max_low = self.cluster[self._high(x)].maximum()
        if max_low != -1 and self._low(x) < max_low:
            offset = self.cluster[self._high(x)].successor(self._low(x))
            return self._index(self._high(x), offset)
        
        succ_cluster = self.summary.successor(self._high(x))
        if succ_cluster == -1:
            return -1
        
        offset = self.cluster[succ_cluster].minimum()
        return self._index(succ_cluster, offset)
    
    def predecessor(self, x: int) -> int:
        """查询 x 的前驱（-1 如果不存在）。"""
        if self.u == 2:
            return 0 if x == 1 and self.MIN == 0 else -1
        
        if self.MAX != -1 and x > self.MAX:
            return self.MAX
        
        min_low = self.cluster[self._high(x)].minimum()
        if min_low != -1 and self._low(x) > min_low:
            offset = self.cluster[self._high(x)].predecessor(self._low(x))
            return self._index(self._high(x), offset)
        
        pred_cluster = self.summary.predecessor(self._high(x))
        if pred_cluster == -1:
            return self.MIN if self.MIN != -1 and x > self.MIN else -1
        
        offset = self.cluster[pred_cluster].maximum()
        return self._index(pred_cluster, offset)
    
    def insert(self, x: int) -> None:
        """插入元素。"""
        if self.MIN == -1:
            self.MIN = self.MAX = x
            return
        
        if x < self.MIN:
            self.MIN, x = x, self.MIN
        
        if self.u > 2:
            if self.cluster[self._high(x)].minimum() == -1:
                self.summary.insert(self._high(x))
                self.cluster[self._high(x)].MIN = self._low(x)
                self.cluster[self._high(x)].MAX = self._low(x)
            else:
                self.cluster[self._high(x)].insert(self._low(x))
        
        if x > self.MAX:
            self.MAX = x
    
    def delete(self, x: int) -> None:
        """删除元素。"""
        if self.MIN == self.MAX:
            self.MIN = self.MAX = -1
            return
        
        if self.u == 2:
            if x:
                self.MAX = self.MIN = 0
            else:
                self.MAX = self.MIN = 1
            return
        
        if self.MIN == x:
            first_cluster = self.summary.minimum()
            if first_cluster != -1:
                x = self._index(first_cluster, self.cluster[first_cluster].minimum())
                self.MIN = x
        
        self.cluster[self._high(x)].delete(self._low(x))
        if self.cluster[self._high(x)].minimum() == -1:
            self.summary.delete(self._high(x))
            if x == self.MAX:
                summary_max = self.summary.maximum()
                if summary_max == -1:
                    self.MAX = self.MIN
                else:
                    self.MAX = self._index(summary_max, self.cluster[summary_max].maximum())
        elif x == self.MAX:
            self.MAX = self._index(self._high(x), self.cluster[self._high(x)].maximum())


def test_basic_operations():
    """测试基本操作"""
    veb = VEBTree()
    veb.build(4)  # 范围 0-15
    
    veb.insert(3)
    veb.insert(7)
    veb.insert(12)
    
    assert veb.member(3), "3 should be in tree"
    assert veb.member(7), "7 should be in tree"
    assert not veb.member(5), "5 should not be in tree"
    assert veb.minimum() == 3, "Minimum should be 3"
    assert veb.maximum() == 12, "Maximum should be 12"
    
    print("✓ test_basic_operations passed")


def test_successor_predecessor():
    """测试后继和前驱"""
    veb = VEBTree()
    veb.build(4)
    
    veb.insert(1)
    veb.insert(5)
    veb.insert(10)
    
    assert veb.successor(1) == 5, "Successor of 1 should be 5"
    assert veb.successor(5) == 10, "Successor of 5 should be 10"
    assert veb.predecessor(10) == 5, "Predecessor of 10 should be 5"
    assert veb.predecessor(5) == 1, "Predecessor of 5 should be 1"
    
    print("✓ test_successor_predecessor passed")


if __name__ == "__main__":
    test_basic_operations()
    test_successor_predecessor()
    print("\n所有 VEB 树测试通过！✓")
