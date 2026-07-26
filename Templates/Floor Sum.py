"""
地板函数求和（Floor Sum）

快速计算 sum_{i=0}^{n-1} floor((a*i + b) / m)，时间复杂度 O(log m)。

应用：多项式乘法、大整数乘法、卷积计算。

复杂度：O(log(m))
"""

from typing import Tuple


def floor_sum(a: int, b: int, m: int, n: int) -> int:
    """
    计算 sum_{i=0}^{n-1} floor((a*i + b) / m)。
    
    Args:
        a: 系数 a
        b: 常数项 b
        m: 模数 m
        n: 项数 n（从 i=0 到 i=n-1）
        
    Returns:
        求和结果
    """
    ret = 0
    
    while True:
        # 处理 a >= m
        if a >= m:
            ret += (n - 1) * n * (a // m) // 2
            a %= m
        
        # 处理 b >= m
        if b >= m:
            ret += n * (b // m)
            b %= m
        
        # 递推计算
        y = (a * n + b) // m
        
        # 终止条件
        if y == 0:
            return ret
        
        # 避免除以零
        if a == 0:
            return ret
        
        # 关键递推
        x = b - y * m
        ret += (n + x // a) * y
        
        # 更新参数进行下一次迭代
        a, b, m, n = m, x % a, a, y


def test_simple():
    """测试：floor_sum(1, 0, 1, 3)"""
    result = floor_sum(1, 0, 1, 3)
    assert result == 3, f"Expected 3, got {result}"
    print("✓ test_simple passed")


def test_case_2():
    """测试：floor_sum(2, 3, 4, 5)"""
    result = floor_sum(2, 3, 4, 5)
    expected = sum((2*i + 3) // 4 for i in range(5))
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ test_case_2 passed")


def test_case_3():
    """测试：floor_sum(100, 50, 7, 10)"""
    result = floor_sum(100, 50, 7, 10)
    expected = sum((100*i + 50) // 7 for i in range(10))
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ test_case_3 passed")


if __name__ == "__main__":
    print("Running Floor Sum tests...")
    test_simple()
    test_case_2()
    test_case_3()
    print("\n所有 Floor Sum 测试通过！✓")
