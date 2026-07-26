"""
扩展中国剩余定理（Extended Chinese Remainder Theorem）

求解同余方程组，模数可以不互质。

应用：
- 求解任意模数的同余方程组
- 模数不互质时的线性同余求解

复杂度：O(n log m)，其中 n 是方程个数，m 是模数大小
"""

from typing import List, Tuple
from math import gcd


class ExtendedCRT:
    """扩展中国剩余定理。"""
    
    @staticmethod
    def exgcd(a: int, b: int) -> Tuple[int, int, int]:
        """
        扩展欧几里得算法。
        
        求 x, y 使得 ax + by = gcd(a, b)
        
        Args:
            a, b: 输入数
            
        Returns:
            (x, y, gcd(a, b))
        """
        if b == 0:
            return 1, 0, a
        x, y, g = ExtendedCRT.exgcd(b, a % b)
        return y, x - (a // b) * y, g
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """求最小公倍数。"""
        return a * b // gcd(a, b)
    
    @staticmethod
    def crt(moduli: List[int], residues: List[int]) -> int:
        """
        中国剩余定理（模数两两互质）。
        
        求解同余方程组：
            x ≡ residues[i] (mod moduli[i])
        
        Args:
            moduli: 模数列表（必须两两互质）
            residues: 余数列表
            
        Returns:
            解 x（在 [0, 乘积) 内）
        """
        M = 1
        for m in moduli:
            M *= m
        
        res = 0
        for m, r in zip(moduli, residues):
            Mi = M // m
            x, _, _ = ExtendedCRT.exgcd(Mi, m)
            res += r * Mi * x
            res %= M
        
        return res
    
    @staticmethod
    def excrt(moduli: List[int], residues: List[int]) -> Tuple[int, int]:
        """
        扩展中国剩余定理（模数可以不互质）。
        
        求解同余方程组：
            x ≡ residues[i] (mod moduli[i])
        
        可能无解，此时返回 (-1, -1)。
        
        Args:
            moduli: 模数列表
            residues: 余数列表
            
        Returns:
            (解, 模数乘积) 或 (-1, -1) 如果无解
        """
        res, M = 0, 1
        
        for m, r in zip(moduli, residues):
            # 需要解：x ≡ res (mod M), x ≡ r (mod m)
            # 即：M*t + res ≡ r (mod m)
            # 即：M*t ≡ (r - res) (mod m)
            
            rhs = (r - res) % m
            g = gcd(M, m)
            
            # 检查无解条件
            if rhs % g != 0:
                return -1, -1
            
            # 使用扩展欧几里得算法求解
            x, y, _ = ExtendedCRT.exgcd(M, m)
            
            # 合并两个同余方程
            res += x * (rhs // g) % (m // g) * M
            M = ExtendedCRT.lcm(M, m)
            res %= M
        
        return res, M
    
    @staticmethod
    def excrt_weighted(weights: List[int], moduli: List[int], residues: List[int]) -> Tuple[int, int]:
        """
        带权重的扩展中国剩余定理。
        
        求解同余方程组：
            weights[i] * x ≡ residues[i] (mod moduli[i])
        
        Args:
            weights: 系数列表
            moduli: 模数列表
            residues: 余数列表
            
        Returns:
            (解, 模数) 或 (-1, -1) 如果无解
        """
        res, M = 0, 1
        
        for w, m, r in zip(weights, moduli, residues):
            # 需要解：w*x ≡ r (mod m)
            # 在已有约束 x ≡ res (mod M) 下
            
            rhs = (r - w * res) % m
            x, _, g = ExtendedCRT.exgcd((w * M) % m, m)
            
            if rhs % g != 0:
                return -1, -1
            
            res += x * (rhs // g) % (m // g) * M
            M = ExtendedCRT.lcm(M, m // gcd(m, w))
            res %= M
        
        return res, M


# 别名
CRT = ExtendedCRT


def test_basic_crt():
    """测试基本 CRT：x ≡ 2 (mod 3), x ≡ 3 (mod 5)"""
    # x = 8
    result = CRT.crt([3, 5], [2, 3])
    assert result == 8, f"Expected 8, got {result}"
    print("✓ test_basic_crt passed")


def test_basic_excrt():
    """测试 EXCRT：x ≡ 1 (mod 2), x ≡ 2 (mod 3)"""
    # x = 5 (mod 6)
    result, M = CRT.excrt([2, 3], [1, 2])
    assert result == 5 and M == 6, f"Expected (5, 6), got ({result}, {M})"
    print("✓ test_basic_excrt passed")


def test_excrt_non_coprime():
    """测试非互质模数：x ≡ 1 (mod 6), x ≡ 7 (mod 9)"""
    # x = 7 (mod 18)
    result, M = CRT.excrt([6, 9], [1, 7])
    assert result == 7 and M == 18, f"Expected (7, 18), got ({result}, {M})"
    print("✓ test_excrt_non_coprime passed")


def test_excrt_no_solution():
    """测试无解情况：x ≡ 1 (mod 4), x ≡ 2 (mod 4)"""
    result, M = CRT.excrt([4, 4], [1, 2])
    assert result == -1 and M == -1, f"Expected (-1, -1), got ({result}, {M})"
    print("✓ test_excrt_no_solution passed")


def test_weighted_excrt():
    """测试带权：2x ≡ 3 (mod 5)"""
    # 2x ≡ 3 (mod 5) => x ≡ 4 (mod 5)
    result, M = CRT.excrt_weighted([2], [5], [3])
    assert result == 4 and M == 5, f"Expected (4, 5), got ({result}, {M})"
    print("✓ test_weighted_excrt passed")


if __name__ == "__main__":
    test_basic_crt()
    test_basic_excrt()
    test_excrt_non_coprime()
    test_excrt_no_solution()
    test_weighted_excrt()
    print("\n所有 EXCRT 测试通过！✓")
