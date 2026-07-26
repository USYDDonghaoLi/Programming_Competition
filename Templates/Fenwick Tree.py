class FenwickTree:
    """
    树状数组（Fenwick Tree / Binary Indexed Tree）。
    支持单点修改和前缀和查询，都在 O(log n) 时间内完成。
    """
    
    def __init__(self, n: int):
        """
        初始化树状数组。
        Args:
            n: 数组大小
        """
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed
    
    def _lowbit(self, x: int) -> int:
        """
        获取 x 的最低有效位（2 的幂）。
        Args:
            x: 正整数
        Returns:
            x 的最低有效位的值
        """
        return x & (-x)

    def build(self, arr: list) -> None:
        """
        用数组初始化树状数组。
        Args:
            arr: 输入数组（0-indexed），长度为 n
        """
        for i in range(len(arr)):
            self.update(i + 1, arr[i])

    def update(self, pos: int, delta: int) -> None:
        """
        将位置 pos（1-indexed）的值增加 delta。
        Args:
            pos: 位置（1-indexed）
            delta: 增量
        """
        while pos <= self.n:
            self.tree[pos] += delta
            pos += self._lowbit(pos)

    def query(self, pos: int) -> int:
        """
        查询前 pos 个元素的和（1-indexed）。
        Args:
            pos: 位置（1-indexed），查询 [1, pos] 的和
        Returns:
            前 pos 个元素的和
        """
        result = 0
        while pos > 0:
            result += self.tree[pos]
            pos -= self._lowbit(pos)
        return result

    def range_query(self, left: int, right: int) -> int:
        """
        查询区间 [left, right] 的和（1-indexed）。
        Args:
            left: 左端点（1-indexed）
            right: 右端点（1-indexed）
        Returns:
            区间和
        """
        return self.query(right) - self.query(left - 1)

    def lower_bound(self, target: int) -> int:
        """
        在树状数组中进行二分查找，找最小的 pos 使得 query(pos) >= target。
        前提：所有元素非负且累积和单调递增。
        Args:
            target: 目标值
        Returns:
            满足条件的最小位置（1-indexed），若不存在返回 n+1
        """
        pos, cum_sum = 0, 0
        for i in range(self.n.bit_length() - 1, -1, -1):
            next_pos = pos + (1 << i)
            if next_pos <= self.n and cum_sum + self.tree[next_pos] < target:
                cum_sum += self.tree[next_pos]
                pos = next_pos
        return pos + 1
    
    def upper_bound(self, target: int) -> int:
        """
        在树状数组中进行二分查找，找最小的 pos 使得 query(pos) > target。
        前提：所有元素非负且累积和单调递增。
        Args:
            target: 目标值
        Returns:
            满足条件的最小位置（1-indexed），若不存在返回 n+1
        """
        pos, cum_sum = 0, 0
        for i in range(self.n.bit_length() - 1, -1, -1):
            next_pos = pos + (1 << i)
            if next_pos <= self.n and cum_sum + self.tree[next_pos] <= target:
                cum_sum += self.tree[next_pos]
                pos = next_pos
        return pos + 1

def test_fenwick_tree():
    """测试树状数组"""
    # 基本测试
    ft = FenwickTree(5)
    ft.build([1, 2, 3, 4, 5])
    assert ft.query(3) == 6, "query(3) should be 1+2+3=6"
    print("✓ test_build_query passed")
    
    # 更新测试
    ft.update(2, 5)  # arr[2] += 5，即变成 2+5=7
    assert ft.query(3) == 11, "After update, query(3) should be 1+7+3=11"
    print("✓ test_update passed")
    
    # 区间查询
    ft2 = FenwickTree(5)
    ft2.build([1, 2, 3, 4, 5])
    assert ft2.range_query(2, 4) == 9, "range_query(2,4) should be 2+3+4=9"
    print("✓ test_range_query passed")


if __name__ == "__main__":
    test_fenwick_tree()
    print("\n所有 Fenwick Tree 测试通过！✓")
